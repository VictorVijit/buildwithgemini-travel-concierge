import imageio.v3 as iio
from PIL import Image
import os

input_webm = "agent_demo.webm"
output_gif = "demo.gif"

print(f"Reading frames from {input_webm}...")
# Read frames using imageio
frames = iio.imread(input_webm, plugin="pyav") if hasattr(iio, "pyav") else iio.imread(input_webm)

print(f"Total frames read: {len(frames)}")

pil_frames = []
for i, frame in enumerate(frames):
    # Subsample frames to reduce size (e.g., every 2nd or 3rd frame)
    if i % 3 != 0:
        continue
    img = Image.fromarray(frame)
    # Resize to 800px width maintaining aspect ratio
    w, h = img.size
    new_w = 800
    new_h = int(h * (new_w / w))
    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    pil_frames.append(img)

print(f"Saving {len(pil_frames)} processed frames to {output_gif}...")
if pil_frames:
    pil_frames[0].save(
        output_gif,
        save_all=True,
        append_images=pil_frames[1:],
        optimize=True,
        duration=100,  # 10 fps
        loop=0
    )
    print(f"Saved {output_gif} successfully! Size: {os.path.getsize(output_gif)} bytes")
