import os
import argparse

from scripts.main import create_object

def main(args):
    print("Creating 3d Model in path:  '", args.output, "'")
    try:    
        total_time = create_object(args.input, args.output, args.fps, args.preset)
        print(f"Successfully Created 3d Model in {total_time} seconds")
    except:
        print("Error Creating 3d Model")
    

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str, required=False, default="data/example_video.mp4", 
                        help='Path to input video file')
    parser.add_argument('--output', '-o', type=str, required=False, default="data/example_video_out", 
                        help='Path to output')
    parser.add_argument('--preset', '-p', type=str, required=False, default="NORMAL", 
                        help='Quality Preset 1] NORMAL 2] HIGH 3] ULTRA')
    parser.add_argument('--fps', '-f', type=int, required=False, default="15", 
                        help='Number of frames to be extracted from the video per second')
    args = parser.parse_args()
    
    main(args)