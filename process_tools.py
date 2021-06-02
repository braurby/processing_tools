#!/usr/bin/env python3

import argparse
import sys
import os
from processing_tools import process_image
from processing_tools import process_video
from pathlib import Path


IMG_FORMATS = ['.jpeg', '.jpg', '.png', '.gif']
VID_FORMATS = ['.mov', '.mp4', '.avi']
OUTPUT_FOLDER = 'output'

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('location', help='Locations of files or folder with multiple files.')
    parser.add_argument('-o', '--output', help='Output folder location. '
                                               'If empty - output folder will be created in the 1st location parent.')
    parser.add_argument('-c', '--caption', help='Provide text caption for each file separated with |')

    # Check if arguments are empty
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit()

    locs = args.location.split()

    print(f'LOCATIONS: {locs}')

    # Check if caption is defined
    captions = [i.strip() for i in args.caption.split('|')] if args.caption else ''

    if captions:
        print(f'CAPTIONS: {captions}')

        # Check if locations and captions are the same length
        if len(locs) is not len(captions):
            print('\nFound locations:')
            for loc in locs:
                print(f'\t{loc}')
            print('\nFound captions:')
            for cap in captions:
                print(f'\t{cap}')
            raise Exception('\tNumber of captions should be the same as number of items.')

    if Path(locs[0]).is_file():
        # Define output folder
        output = args.output if args.output else Path(locs[0]).parents[1] / OUTPUT_FOLDER
        # Create output folder if not exists
        os.makedirs(output, exist_ok=True)

        # Process single files provided
        if Path(locs[0]).suffix in IMG_FORMATS:
            # It's images, use process_image script
            process_image.merge_images(locs, output, captions)
        elif Path(locs[0]).suffix in VID_FORMATS:
            # It's video, use process_video script
            process_video.merge_videos(locs, output, captions)
        else:
            print('Unknown file format.')
    else:
        # Define output folder
        output = Path(args.output) if args.output else Path(locs[0]).parent / OUTPUT_FOLDER
        # Create output folder if not exists
        os.makedirs(output, exist_ok=True)

        # Process multiple files in folder
        for item in Path(locs[0]).iterdir():
            img_locs = []
            vid_locs = []

            if item.is_file() and item.suffix.lower() in IMG_FORMATS:
                for location in locs:
                    img_locs.append(Path(location) / Path(item.name))

            elif item.is_file() and item.suffix in VID_FORMATS:
                for location in locs:
                    vid_locs.append(Path(location) / Path(item.name))

            if img_locs:
                process_image.merge_images(img_locs, output, captions)
            elif vid_locs:
                process_video.merge_videos(vid_locs, output, captions)
