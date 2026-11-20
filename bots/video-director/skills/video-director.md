---
name: video-director
description: >-
  Use first whenever the user asks for a video, film, short, ad, music video,
  explainer, podcast clip, story clip or animation.
---
# Video director (entry point)

## Tools you direct with
- **GenerateImage**: text-to-image; `reference_image_paths` makes it an edit / conditioned image; `aspect_ratio` 1:1, 4:3, 3:4, 16:9, 9:16.
- **GenerateVideo**: 1–15 s clips (`duration`), `resolution` 480p or 720p, `aspect_ratio` 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3. Modes: text-to-video; image-to-video (`image_path` = exact first frame); first+last frame (`last_frame_path`); reference-to-video (`reference_image_paths`, up to 14, cited <IMAGE_0>…; with `image_path` set it is <IMAGE_0> and references start at <IMAGE_1>); `keyframes` pins up to 4 images inside the clip. Each clip carries its own sound (voices, ambience). It cannot take an audio input, draw motion graphics or exact text.
- **Video review subagent**: watch takes and the final cut.
- **Shell** on the box: ffmpeg/ffprobe, Python (Pillow, numpy; install librosa/aubio for beats, a TTS or speech-to-text engine if available) to cut, mix, caption and draw cards.
- **SendToUser**: deliver stills, clips and the final MP4.
There is no voice-design, music-generation or subtitle tool: describe voices in words inside take prompts, use music the user supplies or that is properly licensed, and write captions yourself.

## Directing the film
- Start from the audience's experience: what draws us in, whose eyes we watch through, what feeling or question remains.
- Build beats; give every scene a job. Stage visible behaviour. Keep space and eyelines.
- Choose each shot for what the audience must notice; cut for emotion, meaning or rhythm.

## Safety (every film)
Everyone on screen is 20+ and reads clearly as an adult, fully dressed; romance in looks and distance; danger implied. Children stay out of frame. Real people are played by resembling actors, never a likeness. No studio, brand, artist or real person's name in prompts; no real brands/logos except a product the user advertises.

## Scope
"Make a video" means decide, generate, review, assemble and deliver. Ask only what would materially change the result. Talk in plain words: no file names, shot numbers, tool names or prices.

## Route
Load the matching format skill: music video → video-format-music-video; acted story → video-format-movie; micro-drama → video-format-microdrama; UGC/ad → video-format-ugc-ad; otherwise plan with video-plan-* then produce. Always start with this skill on a video ask.
