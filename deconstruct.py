import os
import sys
import argparse
import subprocess

def extract_frames(input_video, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    file_name = os.path.splitext(os.path.basename(input_video))[0]

    ffmpeg_command = f"ffmpeg -i {input_video} {os.path.join(output_directory, file_name)}_%04d.png"
    subprocess.call(ffmpeg_command, shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract all frames from a video file")
    parser.add_argument("-i", "--inputvideo", required=True, help="Input video file")
    parser.add_argument("-d", "--directory", required=True, help="Output directory for extracted frames")

    args = parser.parse_args()

    input_video = args.inputvideo
    output_directory = args.directory

    extract_frames(input_video, output_directory)
    print("DONE!")
