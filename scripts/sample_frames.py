
from pathlib import Path
import cv2

# Dataset folders
VIDEOS_DIR = Path("/content/EchoNet/Videos")
OUTPUT_DIR = Path("/content/EchoNet/SampledFrames")

# Number of frames to extract from each video
NUM_SAMPLES = 5

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Find every AVI video
video_files = sorted(VIDEOS_DIR.glob("*.avi"))

print(f"Found {len(video_files)} AVI video(s).")


for video_path in video_files:

    print(f"\nProcessing: {video_path.name}")

    # Open video
    video = cv2.VideoCapture(str(video_path))

    if not video.isOpened():
        print(f"ERROR: Could not open {video_path.name}")
        continue

    # Get video metadata
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"  Frames: {total_frames}")
    print(f"  FPS: {fps}")
    print(f"  Resolution: {width} x {height}")

    if total_frames <= 0:
        print("  ERROR: No readable frames.")
        video.release()
        continue

    # Don't request more samples than frames available
    sample_count = min(NUM_SAMPLES, total_frames)

    # Select evenly spaced frame numbers
    if sample_count == 1:
        frame_numbers = [0]
    else:
        frame_numbers = [
            round(i * (total_frames - 1) / (sample_count - 1))
            for i in range(sample_count)
        ]

    print(f"  Sampling frames: {frame_numbers}")

    # Separate output directory for each video
    video_output_dir = OUTPUT_DIR / video_path.stem
    video_output_dir.mkdir(parents=True, exist_ok=True)

    # Extract selected frames
    for frame_number in frame_numbers:

        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        success, frame = video.read()

        if not success:
            print(f"  ERROR reading frame {frame_number}")
            continue

        output_path = (
            video_output_dir /
            f"frame_{frame_number:04d}.png"
        )

        success = cv2.imwrite(str(output_path), frame)

        if success:
            print(f"  Saved: {output_path.name}")
        else:
            print(f"  ERROR saving frame {frame_number}")

    video.release()


print("\nFrame sampling complete.")
