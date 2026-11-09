"""Tiny whiteboard-animation engine (Pillow + numpy).

Everything is drawn on a 2x super-sampled "board" that is updated
incrementally, then reduced to 1x for each output frame so lines stay
anti-aliased. A marker pen sprite follows the point being drawn.
"""
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, S, FPS = 1920, 1080, 2, 30
ROOT = Path(__file__).resolve().parent.parent
FONT_TITLE = str(ROOT / "assets/fonts/Koulen-Regular.ttf")
FONT_BODY = str(ROOT / "assets/fonts/KantumruyPro-Bold.ttf")

BG = (250, 250, 247)
INK = (36, 42, 52)
GRAY = (120, 126, 136)
BLUE = (33, 102, 182)
RED = (210, 60, 52)
GREEN = (40, 145, 85)
ORANGE = (232, 128, 24)
PURPLE = (124, 72, 168)
TEAL = (16, 140, 150)

rng = np.random.default_rng(7)
_font_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)
    return _font_cache[key]


# ---------------------------------------------------------------- geometry
def _smooth_noise(n, amp, k=3):
    t = np.linspace(0, 1, n)
    out = np.zeros(n)
    for i in range(1, k + 1):
        out += rng.normal() * amp / i * np.sin(np.pi * i * t * rng.uniform(0.8, 1.6) + rng.uniform(0, 6.28))
    return out


def line(a, b, amp=2.0):
    a, b = np.array(a, float), np.array(b, float)
    d = b - a
    L = math.hypot(*d) + 1e-9
    n = max(6, int(L / 8))
    t = np.linspace(0, 1, n)
    pts = a + d * t[:, None]
    nrm = np.array([-d[1], d[0]]) / L
    k = min(1.0, L / 250)
    off = (_smooth_noise(n, amp * 0.6) + rng.normal() * amp * 1.2) * k * np.sin(np.pi * t)
    return pts + nrm * off[:, None]


def _jitter(pts, amp):
    d = np.gradient(pts, axis=0)
    nrm = np.stack([-d[:, 1], d[:, 0]], 1)
    nrm /= np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-9
    return pts + nrm * _smooth_noise(len(pts), amp, 4)[:, None]


def rrect(x, y, w, h, r=18, amp=2.0):
    r = min(r, w / 2, h / 2)
    pts = []

    def arc(cx, cy, a0):
        for a in np.linspace(a0, a0 + 90, 7):
            pts.append((cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))))

    def seg(p, q):
        n = max(2, int(math.hypot(q[0] - p[0], q[1] - p[1]) / 10))
        for t in np.linspace(0, 1, n, endpoint=False)[1:]:
            pts.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))

    arc(x + r, y + r, 180)
    seg((x + r, y), (x + w - r, y))
    arc(x + w - r, y + r, 270)
    seg((x + w, y + r), (x + w, y + h - r))
    arc(x + w - r, y + h - r, 0)
    seg((x + w - r, y + h), (x + r, y + h))
    arc(x + r, y + h - r, 90)
    seg((x, y + h - r), (x, y + r))
    pts = np.array(pts)
    over = pts[:5] + np.array([1.5, -2.5])  # hand-drawn overshoot past the start
    pts = np.vstack([pts, over])
    return _jitter(pts, amp)


def ellipse(cx, cy, rx, ry=None, start=-100, sweep=375, amp=0.012):
    ry = rx if ry is None else ry
    n = max(24, int(abs(sweep) / 360 * 2 * math.pi * max(rx, ry) / 8))
    th = np.radians(np.linspace(start, start + sweep, n))
    f = 1 + _smooth_noise(n, amp, 3) + np.linspace(0, 0.025, n) * (abs(sweep) > 360)
    return np.stack([cx + rx * f * np.cos(th), cy + ry * f * np.sin(th)], 1)


def arrowhead(tip, frm, size=26, spread=28):
    tip, frm = np.array(tip, float), np.array(frm, float)
    d = tip - frm
    ang = math.atan2(d[1], d[0])
    p1 = tip - size * np.array([math.cos(ang + math.radians(spread)), math.sin(ang + math.radians(spread))])
    p2 = tip - size * np.array([math.cos(ang - math.radians(spread)), math.sin(ang - math.radians(spread))])
    return np.vstack([line(p1, tip, 0.5), line(tip, p2, 0.5)[1:]])


def arrow(a, b, amp=2.0, size=26):
    shaft = line(a, b, amp)
    return [shaft, arrowhead(shaft[-1], shaft[-4], size)]


def polyline(pts, amp=1.0):
    out = [np.array(pts[0], float)[None]]
    for p, q in zip(pts[:-1], pts[1:]):
        out.append(line(p, q, amp)[1:])
    return np.vstack(out)


# ---------------------------------------------------------------- elements
class Element:
    dur = 0.5
    color = INK

    def advance(self, board, p):  # draw up to progress p (0..1), incrementally
        pass

    def pen(self, p, t):  # pen-tip position at progress p (1x coords) or None
        return None


class Pause(Element):
    def __init__(self, dur=0.3):
        self.dur = dur


class Stroke(Element):
    def __init__(self, paths, color=INK, width=6, dur=None, speed=1000):
        if isinstance(paths, np.ndarray):
            paths = [paths]
        self.paths = [np.asarray(p, float) for p in paths]
        self.cums = []
        for p in self.paths:
            seg = np.hypot(*np.diff(p, axis=0).T)
            self.cums.append(np.concatenate([[0], np.cumsum(seg)]))
        self.total = sum(c[-1] for c in self.cums)
        self.color, self.width = color, width
        self.dur = dur if dur is not None else float(np.clip(self.total / speed, 0.2, 2.2))
        self.done = 0.0

    def _sub(self, path, cum, a, b):
        a, b = max(a, 0.0), min(b, cum[-1])
        if b <= a:
            return None
        xs = np.interp([a, b], cum, path[:, 0])
        ys = np.interp([a, b], cum, path[:, 1])
        mid = path[(cum > a) & (cum < b)]
        return np.vstack([[xs[0], ys[0]], mid, [xs[1], ys[1]]])

    def advance(self, board, p):
        target = self.total * p
        if target <= self.done:
            return
        d = ImageDraw.Draw(board)
        w = self.width * S
        off = 0.0
        for path, cum in zip(self.paths, self.cums):
            sub = self._sub(path, cum, self.done - off, target - off)
            if sub is not None:
                pts = [tuple(q) for q in sub * S]
                d.line(pts, fill=self.color, width=w, joint="curve")
                for q in (pts[0], pts[-1]):
                    d.ellipse([q[0] - w / 2, q[1] - w / 2, q[0] + w / 2, q[1] + w / 2], fill=self.color)
            off += cum[-1]
        self.done = target

    def pen(self, p, t):
        target, off = self.total * p, 0.0
        for path, cum in zip(self.paths, self.cums):
            if target <= off + cum[-1]:
                l = target - off
                return (np.interp(l, cum, path[:, 0]), np.interp(l, cum, path[:, 1]))
            off += cum[-1]
        return tuple(self.paths[-1][-1])


class Wipe(Element):
    """A pre-rendered RGBA layer revealed left-to-right (text, fills)."""

    def __init__(self, layer, ox, oy, color=INK, dur=None, speed=750):
        self.layer, self.ox, self.oy, self.color = layer, ox, oy, color
        self.w1 = layer.width / S
        self.dur = dur if dur is not None else float(np.clip(self.w1 / speed, 0.3, 2.4))
        self.col = 0

    def advance(self, board, p):
        c = int(round(self.layer.width * p))
        if c <= self.col:
            return
        crop = self.layer.crop((self.col, 0, c, self.layer.height))
        board.paste(crop, (self.ox + self.col, self.oy), crop)
        self.col = c

    def pen(self, p, t):
        x = (self.ox + self.layer.width * p) / S
        y = (self.oy + self.layer.height * 0.55) / S + math.sin(t * 28) * self.layer.height / S * 0.18
        return (x, y)


def Text(x, y, text, size=48, color=INK, title=False, anchor="mm", max_w=None, dur=None):
    f = font(FONT_TITLE if title else FONT_BODY, size * S)
    if max_w:
        while f.getbbox(text, anchor=anchor)[2] - f.getbbox(text, anchor=anchor)[0] > max_w * S and size > 16:
            size -= 2
            f = font(FONT_TITLE if title else FONT_BODY, size * S)
    pad = 8 * S
    l, t, r, b = f.getbbox(text, anchor=anchor)
    layer = Image.new("RGBA", (r - l + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((-l + pad, -t + pad), text, font=f, fill=color + (255,), anchor=anchor)
    e = Wipe(layer, int(x * S + l - pad), int(y * S + t - pad), color, dur)
    e.bbox = ((x * S + l) / S, (y * S + t) / S, (x * S + r) / S, (y * S + b) / S)
    return e


def Fill(x, y, w, h, color, alpha=70, r=18, dur=None):
    """Translucent marker-highlight filled rounded rect."""
    layer = Image.new("RGBA", (int(w * S), int(h * S)), (0, 0, 0, 0))
    ImageDraw.Draw(layer).rounded_rectangle([0, 0, w * S - 1, h * S - 1], radius=r * S, fill=color + (alpha,))
    return Wipe(layer, int(x * S), int(y * S), color, dur, speed=1400)


def Dot(cx, cy, r, color, dur=0.25):
    layer = Image.new("RGBA", (int(2 * r * S) + 2, int(2 * r * S) + 2), (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse([1, 1, 2 * r * S, 2 * r * S], fill=color + (255,))
    return Wipe(layer, int((cx - r) * S), int((cy - r) * S), color, dur)


# ---------------------------------------------------------------- pen sprite
_pen_cache = {}


def pen_sprite(color):
    if color in _pen_cache:
        return _pen_cache[color]
    k = 4
    size = 340
    img = Image.new("RGBA", (size * k, size * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    tip = np.array([30.0, size - 30.0])
    ang = math.radians(-55)  # pen body goes up-right
    u = np.array([math.cos(ang), math.sin(ang)])
    v = np.array([-u[1], u[0]])

    def quad(a, b, wa, wb, fill):
        P = [tip + u * a + v * wa, tip + u * b + v * wb, tip + u * b - v * wb, tip + u * a - v * wa]
        d.polygon([tuple(q * k) for q in P], fill=fill)

    quad(0, 14, 3, 6, color + (255,))  # felt tip
    quad(14, 40, 8, 17, (70, 74, 82, 255))  # cone
    quad(40, 230, 17, 17, (245, 245, 245, 255))  # body
    quad(40, 230, 17, 17, (0, 0, 0, 0))
    quad(42, 228, 16, 16, (238, 240, 243, 255))
    quad(150, 270, 19, 19, color + (255,))  # cap
    quad(160, 166, 19.5, 19.5, (255, 255, 255, 90))
    img = img.resize((size, size), Image.LANCZOS)
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    alpha = img.getchannel("A").point(lambda a: a * 0.22)
    shadow.putalpha(alpha)
    shadow = shadow.filter(ImageFilter.GaussianBlur(7))
    out = Image.new("RGBA", (size + 30, size + 30), (0, 0, 0, 0))
    out.alpha_composite(shadow, (22, 12))
    out.alpha_composite(img, (0, 0))
    _pen_cache[color] = (out, (30, size - 30))
    return _pen_cache[color]


def board_texture():
    """Subtle whiteboard sheen + vignette at 2x."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    v = 1 - 0.06 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    sheen = 0.012 * np.sin((xx + yy * 0.6) / 260.0)
    g = np.clip((v + sheen)[..., None] * np.array(BG, np.float32), 0, 255).astype(np.uint8)
    return Image.fromarray(g, "RGB").resize((W * S, H * S), Image.BILINEAR)


# ---------------------------------------------------------------- scene
class Scene:
    def __init__(self, name, narration, elements):
        self.name, self.narration, self.elements = name, narration, elements

    def schedule(self, length, lead=0.35, tail=0.9):
        """Fit drawing time to the narration length; returns final length."""
        total = sum(e.dur for e in self.elements)
        target = max(1.0, length - lead - tail)
        f = float(np.clip(target / total, 0.5, 1.7))
        t = lead
        for e in self.elements:
            e.dur *= f
            e.start = t
            t += e.dur
        return max(length, t + 0.6)

    def render(self, length, write, texture):
        board = texture.copy()
        n = int(round(length * FPS))
        last = None
        for i in range(n):
            t = i / FPS
            active = None
            for e in self.elements:
                if t >= e.start:
                    p = min(1.0, (t - e.start) / e.dur) if e.dur > 0 else 1.0
                    e.advance(board, p)
                    if p < 1.0 and not isinstance(e, Pause):
                        active = (e, p)
            frame = board.reduce(S)
            if active:
                e, p = active
                pos = e.pen(p, t)
                if pos is not None:
                    spr, (tx, ty) = pen_sprite(e.color)
                    frame.paste(spr, (int(pos[0] - tx), int(pos[1] - ty)), spr)
            fade = min(1.0, t / 0.3, (length - t) / 0.35)
            if fade < 1.0:
                frame = Image.blend(Image.new("RGB", frame.size, BG), frame, max(0.0, fade))
            data = frame.tobytes()
            write(data)
            last = data
        return last
