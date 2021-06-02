import ffmpeg
import sys
from pathlib import Path


def check_videos(videos):
    # Check if video file is valid
    for video in videos:
        try:
            probe = ffmpeg.probe(video)
        except ffmpeg.Error as e:
            print(e.stderr, file=sys.stderr)
            sys.exit(1)

        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        if video_stream is None:
            print('No video stream found', file=sys.stderr)
            sys.exit(1)


def merge_videos(locations, output, text=[]):
    videos = []
    text = ' | '.join(text)

    # Check if videos input is correct
    check_videos(locations)

    # Input videos
    for i in locations:
        videos.append(ffmpeg.input(i))

    output = Path(output) / Path(locations[0]).name

    if text:
        (
            ffmpeg
            .filter(videos, 'hstack', len(videos))  # hstack - horizontal, vstack - vertical
            .drawtext(
                fontfile='/Library/Fonts/Verdana.ttf',
                text=text,
                fontcolor='white',
                fontsize=32,
                box=1,
                boxcolor='black@0.5',
                boxborderw=10,
                x='(w-text_w)/2',
                y=40
            )
            .output(str(output))
            .run()
        )
    else:
        (
            ffmpeg
            .filter(videos, 'hstack', len(videos))
            .output(str(output))
            .run()
        )
    print(f'\tVideo {Path(locations[0]).name} saved to {output}.')
