import av


def extract_frames_from_video(video_path: str, frame_count) -> bytes:
    """Return every N frame from video.

    Args:
        video_path: Input video path.
        frame_count: Number indicating which each frame to take from video.

    Returns:
        Image in bytes.
    """
    container = av.open(video_path)
    stream = container.streams.video[0]

    for frame in container.decode(stream):
        if frame.index % frame_count == 0:
            yield frame.to_image()
