---
name: video-project-folder
description: >-
  Use when setting up or resuming a video project and when assembling and
  delivering the cut.
---
# The project folder, the cut and the finish

Layout under `/workspace/films/<slug>/`: project.json, script.md, NOTES.md, characters/, places/, props/, shots/, audio/, uploads/, edit.json, published/, .preview/.

Persistence: copy every generated image/clip and published cut to the agent store as soon as it exists. Log every generation to prompts.json with cost.

NOTES.md (<8 KB): What this film is; Decisions; Feedback; State; Remix guide.

Assemble with ffmpeg from edit.json to published/vN.mp4. Straight cuts unless asked. Music ducked under dialogue. Captions in safe area.
