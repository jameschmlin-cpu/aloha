# Genesis Software Assets Catalog (v1.0.0)

This registry records the specifications and execution signatures for all self-purchased creative AI software modules.

---

## 🎨 1. Artistly.ai
- **Category**: Image Generation & Art Synthesis
- **Brick Identifier**: `EXT_Artistly_Image_Gen`
- **Primary Function**: `run(prompt, aspect_ratio="16:9", style="cinematic") -> image_url`
- **Input Parameters**:
  - `prompt` (str): Text prompt detailing image content.
  - `aspect_ratio` (str): Dimension layout, e.g. "16:9", "1:1", "9:16".
  - `style` (str): Target rendering style, e.g. "cinematic", "anime", "watercolor".
- **Return Type**:
  - `image_url` (str): Hosted URL link to the synthesized PNG asset.

---

## 🎬 2. VidSpace AI
- **Category**: Video Render & Composition
- **Brick Identifier**: `EXT_VidSpace_Video_Gen`
- **Primary Function**: `run(image_url, motion_factor=5, duration=4) -> video_url`
- **Input Parameters**:
  - `image_url` (str): Base image URL source for image-to-video synthesis.
  - `motion_factor` (int): Animation speed scale, range 1-10.
  - `duration` (int): Target length in seconds, default 4.
- **Return Type**:
  - `video_url` (str): URL to the rendered MP4 video.

---

## 🎵 3. Kleva AI
- **Category**: Audio, SFX & Music Synthesis
- **Brick Identifier**: `EXT_Kleva_Audio_Gen`
- **Primary Function**: `run(description, duration=30, track_type="music") -> audio_url`
- **Input Parameters**:
  - `description` (str): Audio/music details (e.g. "high energy cyberpunk beat").
  - `duration` (int): Length of generated track in seconds.
  - `track_type` (str): E.g., "music", "sfx", "voiceover".
- **Return Type**:
  - `audio_url` (str): URL of the generated MP3 file.
