"""Build the Khmer whiteboard video.

    python3 src/build.py            # full video
    python3 src/build.py --preview  # one PNG per scene (last frame) into build/preview
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from whiteboard import FPS, H, ROOT, W, board_texture  # noqa: E402
from scenes import all_scenes  # noqa: E402

BUILD = ROOT / "build"
OUT = ROOT / "output"
TEMPO = 1.12  # Google TTS Khmer is a bit slow; speed it up slightly
LEAD = 0.35


def sh(*cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         check=True, capture_output=True, text=True).stdout
    return float(out)


def tts(scene):
    mp3 = BUILD / "audio" / f"{scene.name}.mp3"
    txt = mp3.with_suffix(".txt")
    if not (mp3.exists() and txt.exists() and txt.read_text() == scene.narration):
        from gtts import gTTS
        mp3.parent.mkdir(parents=True, exist_ok=True)
        gTTS(scene.narration, lang="km").save(str(mp3))
        txt.write_text(scene.narration)
    wav = mp3.with_suffix(".wav")
    sh("ffmpeg", "-y", "-i", str(mp3), "-af", f"atempo={TEMPO},silenceremove=start_periods=1:start_threshold=-50dB",
       "-ar", "44100", "-ac", "1", str(wav))
    return wav


def srt_time(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


def main():
    preview = "--preview" in sys.argv
    scenes = all_scenes()
    BUILD.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)

    lengths, wavs = [], []
    for sc in scenes:
        wav = tts(sc)
        speech = duration(wav)
        L = sc.schedule(speech + LEAD + 0.9, lead=LEAD)
        lengths.append(L)
        padded = BUILD / "audio" / f"{sc.name}_pad.wav"
        ms = int(LEAD * 1000)
        sh("ffmpeg", "-y", "-i", str(wav), "-af", f"adelay={ms},apad=whole_dur={L:.3f}", "-t", f"{L:.3f}", str(padded))
        wavs.append(padded)
        print(f"{sc.name:8s} speech {speech:5.1f}s  scene {L:5.1f}s", flush=True)

    tex = board_texture()
    if preview:
        from PIL import Image
        pdir = BUILD / "preview"
        pdir.mkdir(exist_ok=True)
        for sc, L in zip(scenes, lengths):
            keep, seen = int((L - 0.5) * FPS), []
            sc.render(L, lambda b: seen.append(b if len(seen) == keep else None), tex)
            Image.frombytes("RGB", (W, H), seen[keep]).save(pdir / f"{sc.name}.png")
            print("preview", sc.name, flush=True)
        return

    lst = BUILD / "audio" / "list.txt"
    lst.write_text("".join(f"file '{w}'\n" for w in wavs))
    audio = BUILD / "narration.wav"
    sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(audio))

    # subtitles
    t, srt = 0.0, []
    for i, (sc, L) in enumerate(zip(scenes, lengths), 1):
        srt.append(f"{i}\n{srt_time(t + LEAD)} --> {srt_time(t + L - 0.3)}\n{sc.narration}\n")
        t += L
    (OUT / "workflow_planning_km.srt").write_text("\n".join(srt), encoding="utf-8")

    out = OUT / "workflow_planning_whiteboard_km.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-i", str(audio), "-c:v", "libx264", "-preset", "medium",
                           "-crf", "22", "-tune", "animation", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
                           "-shortest", "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
    for sc, L in zip(scenes, lengths):
        sc.render(L, ff.stdin.write, tex)
        print("rendered", sc.name, flush=True)
    ff.stdin.close()
    ff.wait()
    print("wrote", out, f"{sum(lengths):.1f}s")


if __name__ == "__main__":
    main()
