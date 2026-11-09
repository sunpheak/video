"""Storyboard: Khmer whiteboard tutorial on planning a workflow."""
import math

import numpy as np

from whiteboard import (BLUE, GRAY, GREEN, INK, ORANGE, PURPLE, RED, TEAL, Dot, Fill, Pause, Scene,
                        Stroke, Text, arrow, arrowhead, ellipse, line, polyline, rrect)

KH_DIGITS = "០១២៣៤៥៦៧៨៩"


def kh(n):
    return "".join(KH_DIGITS[int(c)] for c in str(n))


def star(cx, cy, r, color):
    return Stroke([line((cx - r, cy), (cx + r, cy), 0.5), line((cx, cy - r), (cx, cy + r), 0.5)], color, 5)


# ------------------------------------------------------------ 0. title
def scene_title():
    t1 = Text(960, 250, "ការរៀបចំផែនការ", 118, INK, title=True)
    t2 = Text(960, 430, "លំហូរការងារ", 150, BLUE, title=True)
    x0, x1 = t2.bbox[0], t2.bbox[2]
    wave = np.array([(x, 560 + 9 * math.sin((x - x0) / 38)) for x in np.linspace(x0, x1, 120)])
    els = [t1, t2, Stroke(wave, ORANGE, 8), Pause(0.2)]
    labels = ["គំនិត", "ផែនការ", "សម្រេច"]
    cols = [ORANGE, BLUE, GREEN]
    for i, (lab, c) in enumerate(zip(labels, cols)):
        x = 520 + i * 330
        els += [Fill(x, 640, 220, 110, c, 55), Stroke(rrect(x, 640, 220, 110, 22), c, 6),
                Text(x + 110, 695, lab, 46, INK)]
        if i < 2:
            els.append(Stroke(arrow((x + 235, 695), (x + 315, 695), 1.0, 20), INK, 6))
    # light bulb
    bx, by = 1640, 250
    els += [Stroke(ellipse(bx, by, 62, 66, start=125, sweep=290), ORANGE, 6),
            Stroke([line((bx - 30, by + 58), (bx - 26, by + 100)), line((bx + 30, by + 58), (bx + 26, by + 100))], ORANGE, 6),
            Stroke([line((bx - 28, by + 112), (bx + 28, by + 112)), line((bx - 22, by + 128), (bx + 22, by + 128))], INK, 6),
            Stroke([line((bx + 95 * math.cos(a), by + 95 * math.sin(a)), (bx + 125 * math.cos(a), by + 125 * math.sin(a)), 0.3)
                    for a in np.radians([-160, -125, -90, -55, -20])], ORANGE, 5)]
    els += [star(280, 300, 22, BLUE), star(1700, 820, 18, GREEN),
            Text(960, 900, "មគ្គុទ្ទេសក៍ ៦ ជំហានងាយៗ", 56, GRAY)]
    return Scene("title", "សួស្តី! ថ្ងៃនេះ យើងនឹងរៀនពីរបៀបរៀបចំផែនការលំហូរការងារ ក្នុងប្រាំមួយជំហានងាយៗ។", els)


# ------------------------------------------------------------ 1. why
def scene_why():
    head = Text(960, 120, "ហេតុអ្វីត្រូវការផែនការ?", 84, INK, title=True)
    els = [head, Stroke(line((head.bbox[0], 190), (head.bbox[2], 190), 1.5), RED, 7)]
    # messy scribble
    t = np.linspace(0, 7 * math.pi, 420)
    cx, cy = 480, 440
    pts = np.stack([cx + 150 * np.sin(1.31 * t + 0.4) * np.cos(0.53 * t) + 25 * np.sin(4.1 * t),
                    cy + 120 * np.sin(1.73 * t) * np.cos(0.31 * t + 1) + 20 * np.cos(3.7 * t)], 1)
    els += [Stroke(pts, RED, 5, dur=2.0), Text(480, 650, "គ្មានផែនការ", 52, RED),
            Stroke(arrow((790, 440), (1110, 440), 2.0, 30), GRAY, 7)]
    # clean path
    xs = np.linspace(1220, 1680, 80)
    clean = np.stack([xs, 470 - 90 * np.sin((xs - 1220) / 460 * math.pi / 2)], 1)
    els += [Dot(1220, 470, 14, GREEN), Stroke([clean, arrowhead(clean[-1], clean[-5], 30)], GREEN, 7),
            star(1740, 300, 22, ORANGE), Text(1450, 650, "មានផែនការ", 52, GREEN), Pause(0.3)]
    for i, (lab, c) in enumerate([("ច្បាស់លាស់", BLUE), ("សន្សំពេលវេលា", ORANGE), ("ក្រុមការងារល្អ", GREEN)]):
        x = 200 + i * 560
        els += [Fill(x, 790, 440, 120, c, 50), Stroke(rrect(x, 790, 440, 120, 26), c, 6),
                Text(x + 220, 850, lab, 50, INK)]
    return Scene("why", "ហេតុអ្វីបានជាយើងត្រូវការផែនការលំហូរការងារ? បើគ្មានផែនការ ការងារនឹងច្របូកច្របល់។ "
                        "ផែនការល្អ ជួយឱ្យការងារច្បាស់លាស់ សន្សំពេលវេលា និងជួយឱ្យក្រុមធ្វើការជាមួយគ្នាបានល្អ។", els)


# ------------------------------------------------------------ steps
def step_frame(n, title, color):
    els = [Fill(80, 58, 124, 124, color, 45, r=62, dur=0.2), Stroke(ellipse(142, 120, 64), color, 7),
           Text(142, 124, kh(n), 78, color, title=True, dur=0.3)]
    t = Text(240, 120, title, 84, INK, title=True, anchor="lm", max_w=1500)
    els += [t, Stroke(line((240, 196), (t.bbox[2], 196), 1.5), color, 7)]
    return els


def bullets(items, color, x=1060, y0=430, gap=150):
    els = []
    for i, s in enumerate(items):
        y = y0 + i * gap
        els += [Pause(0.25), Stroke(polyline([(x - 22, y + 2), (x - 6, y + 20), (x + 24, y - 22)], 0.5), color, 7),
                Text(x + 55, y, s, 50, INK, anchor="lm", max_w=760)]
    return els


def progress(n, color):
    els = []
    for i in range(6):
        x = 760 + i * 80
        if i + 1 < n:
            els.append(Dot(x, 1010, 13, GRAY, dur=0.08))
        elif i + 1 == n:
            els.append(Dot(x, 1010, 17, color, dur=0.12))
        else:
            els.append(Stroke(ellipse(x, 1010, 13), GRAY, 3, dur=0.08))
    return els


def icon_target(c):
    cx, cy = 500, 600
    els = [Stroke(ellipse(cx, cy, r), c, 8) for r in (230, 155, 80)]
    els += [Dot(cx, cy, 32, c), Pause(0.2)]
    tail, tip = np.array([800, 320.0]), np.array([cx + 14, cy - 14])
    els += [Stroke(arrow(tail, tip, 1.0, 34), INK, 8),
            Stroke([line(tail, tail + (-6, -48), 0.3), line(tail, tail + (48, 6), 0.3),
                    line(tail + (22, -18), tail + (16, -66), 0.3), line(tail + (22, -18), tail + (70, -12), 0.3)], INK, 6)]
    return els


def icon_checklist(c):
    els = [Stroke(rrect(290, 300, 440, 580, 26), INK, 7), Fill(420, 272, 180, 62, GRAY, 90, 14),
           Stroke(rrect(420, 272, 180, 62, 14), INK, 6)]
    rows = [420 + i * 115 for i in range(4)]
    for y in rows:
        els += [Stroke(rrect(345, y - 30, 60, 60, 10, 1.0), INK, 5), Stroke(line((440, y), (670, y), 1.0), GRAY, 7)]
    for y in rows[:3]:
        els.append(Stroke(polyline([(355, y - 2), (375, y + 22), (420, y - 42)], 0.4), c, 8))
    return els


def icon_sequence(c):
    boxes = {"ក": (170, 380), "ខ": (430, 380), "គ": (690, 380), "ឃ": (430, 680)}
    els = []
    for k, (x, y) in boxes.items():
        els += [Fill(x, y, 160, 120, c, 45), Stroke(rrect(x, y, 160, 120, 20), c, 6), Text(x + 80, y + 64, k, 66, INK, title=True)]
    els += [Stroke(arrow((338, 440), (422, 440), 0.5, 20), INK, 6), Stroke(arrow((598, 440), (682, 440), 0.5, 20), INK, 6),
            Stroke(arrow((510, 508), (510, 672), 0.5, 20), INK, 6), Stroke(arrow((598, 720), (760, 512), 1.0, 20), RED, 6),
            Text(250, 340, "មុន", 40, GRAY), Text(770, 340, "ក្រោយ", 40, GRAY)]
    return els


def icon_people(c):
    els = []
    for i, (x, tag, col) in enumerate([(260, "កិច្ចការ ក", BLUE), (500, "កិច្ចការ ខ", ORANGE), (740, "កិច្ចការ គ", GREEN)]):
        els += [Fill(x - 100, 310, 200, 90, col, 50), Stroke(rrect(x - 100, 310, 200, 90, 16), col, 6),
                Text(x, 357, tag, 36, INK), Stroke(arrow((x, 412), (x, 488), 0.3, 18), INK, 5),
                Stroke(ellipse(x, 550, 45), INK, 6),
                Stroke([line((x, 597), (x, 730), 0.8), line((x, 630), (x - 60, 690), 0.6), line((x, 630), (x + 60, 690), 0.6),
                        line((x, 730), (x - 45, 830), 0.6), line((x, 730), (x + 45, 830), 0.6)], INK, 6),
                Dot(x - 15, 545, 5, INK, 0.05), Dot(x + 15, 545, 5, INK, 0.05),
                Stroke(ellipse(x, 560, 20, 14, start=20, sweep=140, amp=0.0), INK, 4, dur=0.12)]
    return els


def icon_timeline(c):
    els = [Stroke(arrow((180, 840), (880, 840), 1.0, 24), INK, 7)]
    els += [Stroke([line((x, 828), (x, 852), 0.2) for x in range(240, 860, 110)], INK, 5, dur=0.4)]
    for i, (x0, x1, col) in enumerate([(220, 480, BLUE), (420, 680, ORANGE), (620, 820, GREEN)]):
        y = 430 + i * 120
        els += [Fill(x0, y, x1 - x0, 76, col, 90, 16), Stroke(rrect(x0, y, x1 - x0, 76, 16, 1.0), col, 5)]
    els += [Stroke(line((860, 820), (860, 330), 0.8), INK, 6),
            Fill(862, 330, 110, 70, RED, 140, 6, dur=0.3), Stroke(polyline([(860, 330), (975, 365), (860, 400)], 0.6), RED, 6),
            Stroke(ellipse(250, 330, 60), INK, 6), Stroke(polyline([(250, 295), (250, 330), (278, 348)], 0.3), RED, 6)]
    return els


def icon_cycle(c):
    cx, cy, R = 520, 600, 240
    labels = [("ផែនការ", BLUE), ("អនុវត្ត", ORANGE), ("ពិនិត្យ", GREEN), ("កែលម្អ", PURPLE)]
    els = []
    for i, (lab, col) in enumerate(labels):
        a0 = -90 + i * 90 + 22
        arc = ellipse(cx, cy, R, R, start=a0, sweep=46, amp=0.004)
        mid = math.radians(-90 + i * 90)
        lx, ly = cx + R * math.cos(mid), cy + R * math.sin(mid)
        els += [Fill(lx - 95, ly - 42, 190, 84, col, 60, 40), Text(lx, ly, lab, 42, INK)]
        els.append(Stroke([arc, arrowhead(arc[-1], arc[-4], 28)], col, 8))
    els += [Stroke([ellipse(cx, cy, 60, 60, start=-60, sweep=280, amp=0.0)], INK, 6),
            Stroke(arrowhead(ellipse(cx, cy, 60, 60, start=-60, sweep=280, amp=0.0)[-1],
                             ellipse(cx, cy, 60, 60, start=-60, sweep=280, amp=0.0)[-4], 20), INK, 6)]
    return els


STEPS = [
    (1, "កំណត់គោលដៅ", RED, icon_target, ["តើយើងចង់សម្រេចអ្វី?", "គោលដៅច្បាស់លាស់", "អាចវាស់វែងបាន"],
     "ជំហានទីមួយ៖ កំណត់គោលដៅ។ សួរខ្លួនឯងថា តើយើងចង់សម្រេចអ្វី? គោលដៅត្រូវតែច្បាស់លាស់ និងអាចវាស់វែងបាន។"),
    (2, "រាយបញ្ជីកិច្ចការ", GREEN, icon_checklist, ["សរសេរកិច្ចការទាំងអស់", "បំបែកកិច្ចការធំៗ", "ជាកិច្ចការតូចៗ"],
     "ជំហានទីពីរ៖ រាយបញ្ជីកិច្ចការទាំងអស់។ សរសេរគ្រប់កិច្ចការដែលត្រូវធ្វើ ដើម្បីសម្រេចគោលដៅ "
     "ហើយបំបែកកិច្ចការធំៗ ទៅជាកិច្ចការតូចៗ។"),
    (3, "រៀបលំដាប់កិច្ចការ", BLUE, icon_sequence, ["អ្វីធ្វើមុន អ្វីធ្វើក្រោយ", "កិច្ចការណាពឹងផ្អែកគ្នា"],
     "ជំហានទីបី៖ រៀបលំដាប់កិច្ចការ។ កំណត់ថាកិច្ចការណាត្រូវធ្វើមុន កិច្ចការណាធ្វើក្រោយ "
     "ហើយកិច្ចការណាពឹងផ្អែកលើកិច្ចការផ្សេងទៀត។"),
    (4, "ចាត់តាំងអ្នកទទួលខុសត្រូវ", ORANGE, icon_people, ["កិច្ចការនីមួយៗ មានម្ចាស់", "ជៀសវាងការភាន់ច្រឡំ"],
     "ជំហានទីបួន៖ ចាត់តាំងអ្នកទទួលខុសត្រូវ។ កិច្ចការនីមួយៗ ត្រូវមានម្ចាស់ច្បាស់លាស់ ដើម្បីកុំឱ្យមានការភាន់ច្រឡំ។"),
    (5, "កំណត់ពេលវេលា", TEAL, icon_timeline, ["ដាក់ថ្ងៃផុតកំណត់", "ទុកពេលបន្ថែមខ្លះ"],
     "ជំហានទីប្រាំ៖ កំណត់ពេលវេលា។ ដាក់ថ្ងៃផុតកំណត់ សម្រាប់កិច្ចការនីមួយៗ "
     "ហើយទុកពេលបន្ថែមខ្លះ សម្រាប់បញ្ហាដែលមិនបានរំពឹងទុក។"),
    (6, "តាមដាន និងកែលម្អ", PURPLE, icon_cycle, ["ពិនិត្យវឌ្ឍនភាពជាប្រចាំ", "ដោះស្រាយចំណុចស្ទះ", "កែសម្រួលផែនការ"],
     "ជំហានទីប្រាំមួយ៖ តាមដាន និងកែលម្អ។ ពិនិត្យវឌ្ឍនភាពជាប្រចាំ ស្វែងរកចំណុចដែលស្ទះ "
     "ហើយកែសម្រួលផែនការឱ្យកាន់តែប្រសើរ។"),
]


def scene_step(n, title, color, icon, items, narration):
    els = step_frame(n, title, color) + [Pause(0.2)] + icon(color) + bullets(items, color) + progress(n, color)
    return Scene(f"step{n}", narration, els)


# ------------------------------------------------------------ summary
def scene_summary():
    cx, cy, rx, ry = 960, 555, 640, 340
    bw, bh = 410, 108
    centers = []
    for i in range(6):
        a = math.radians(-90 + i * 60)
        centers.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    els = [Text(cx, cy - 20, "វដ្តលំហូរការងារ", 76, INK, title=True), Text(cx, cy + 70, "ធ្វើម្តងទៀត ហើយកែលម្អជានិច្ច", 40, GRAY)]
    for i, (n, title, color, *_r) in enumerate(STEPS):
        x, y = centers[i]
        els += [Fill(x - bw / 2, y - bh / 2, bw, bh, color, 55), Stroke(rrect(x - bw / 2, y - bh / 2, bw, bh, 22), color, 6),
                Text(x, y + 2, f"{kh(n)}. {title}", 42, INK, max_w=bw - 30)]
        nx, ny = centers[(i + 1) % 6]

        def edge(px, py, qx, qy):  # point on box (px,py) boundary toward q
            dx, dy = qx - px, qy - py
            s = min((bw / 2 + 16) / (abs(dx) + 1e-9), (bh / 2 + 16) / (abs(dy) + 1e-9))
            return px + dx * s, py + dy * s

        a, b = edge(x, y, nx, ny), edge(nx, ny, x, y)
        els.append(Stroke(arrow(a, b, 1.5, 24), INK, 6))
    return Scene("summary", "សរុបមក៖ កំណត់គោលដៅ រាយបញ្ជីកិច្ចការ រៀបលំដាប់ ចាត់តាំងអ្នកទទួលខុសត្រូវ "
                            "កំណត់ពេលវេលា ហើយតាមដាន និងកែលម្អ។ នេះគឺជាវដ្ត ដែលយើងធ្វើម្តងហើយម្តងទៀត។", els)


# ------------------------------------------------------------ outro
def scene_outro():
    els = [Text(960, 260, "អរគុណសម្រាប់ការទស្សនា!", 110, BLUE, title=True), Pause(0.2),
           Fill(830, 460, 260, 260, ORANGE, 60, 130), Stroke(ellipse(960, 590, 135), ORANGE, 8),
           Dot(910, 550, 14, INK), Dot(1010, 550, 14, INK),
           Stroke(ellipse(960, 600, 70, 60, start=20, sweep=140, amp=0.0), INK, 8),
           star(640, 520, 26, GREEN), star(1290, 660, 22, RED), star(1330, 470, 16, BLUE),
           Text(960, 880, "ចាប់ផ្តើមរៀបចំផែនការរបស់អ្នក ថ្ងៃនេះ!", 58, INK)]
    return Scene("outro", "អរគុណសម្រាប់ការទស្សនា! សាកល្បងរៀបចំផែនការលំហូរការងារ ក្នុងការងាររបស់អ្នក ចាប់ពីថ្ងៃនេះ។", els)


def all_scenes():
    return [scene_title(), scene_why()] + [scene_step(*s) for s in STEPS] + [scene_summary(), scene_outro()]
