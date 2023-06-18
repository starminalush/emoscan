import av
def extract_frames_from_video(video_path, n):
    container = av.open(video_path)
    stream = container.streams.video[0]

    for frame in container.decode(stream):
        if frame.index % n == 0:
            yield frame.to_image()