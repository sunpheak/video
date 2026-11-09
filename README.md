# វីដេអូក្តារខៀនស៖ ការរៀបចំផែនការលំហូរការងារ

Whiteboard-style tutorial video (Khmer, with Khmer narration) on how to plan a workflow in 6 steps.

- Video: [`output/workflow_planning_whiteboard_km.mp4`](output/workflow_planning_whiteboard_km.mp4) (1920×1080, 30 fps, ~2 min)
- Subtitles: [`output/workflow_planning_km.srt`](output/workflow_planning_km.srt)

## Scenes
1. ចំណងជើង — ការរៀបចំផែនការលំហូរការងារ
2. ហេតុអ្វីត្រូវការផែនការ?
3. ជំហានទី១ — កំណត់គោលដៅ
4. ជំហានទី២ — រាយបញ្ជីកិច្ចការ
5. ជំហានទី៣ — រៀបលំដាប់កិច្ចការ
6. ជំហានទី៤ — ចាត់តាំងអ្នកទទួលខុសត្រូវ
7. ជំហានទី៥ — កំណត់ពេលវេលា
8. ជំហានទី៦ — តាមដាន និងកែលម្អ
9. សរុប — វដ្តលំហូរការងារ
10. អរគុណ

## Rebuild
Requires Python 3 with Pillow (built with raqm), numpy, gTTS (needs network for Google TTS) and ffmpeg.

```bash
pip install pillow numpy gtts
python3 src/build.py            # renders output/*.mp4 and *.srt
python3 src/build.py --preview  # one still per scene in build/preview/
```

Edit the storyboard (text, narration, drawings) in `src/scenes.py`; the drawing engine is `src/whiteboard.py`.
Fonts: Kantumruy Pro and Koulen (SIL Open Font License), in `assets/fonts/`.
