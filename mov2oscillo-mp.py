import sys
import os
import time
import numpy as np
from PIL import Image
import argparse
import soundfile as sf
import multiprocessing as mp

def plot_coordinates(xy_data):
    x_data = [x for x, y in xy_data]
    y_data = [y for x, y in xy_data]

    plt.scatter(x_data, y_data, s=1)
    plt.gca().invert_yaxis()
    plt.show()


def bitmap_to_xy(bitmap_image, rotation_angle):
    img = Image.open(bitmap_image).convert("L")
    img = img.rotate(rotation_angle)
    width, height = img.size
    coordinates = []

    for y in range(height):
        for x in range(width):
            if img.getpixel((x, y)) < 128:
                coordinates.append((x, y))
    return coordinates


def xy_to_audio(xy_data, sample_rate=44100, duration_ms=1000, frequency_multiplier=1, interval=1):
    if not xy_data:
        return None

    x_data = np.array([x for x, y in xy_data])
    y_data = np.array([y for x, y in xy_data])

    x_data_normalized = x_data / max(x_data)
    y_data_normalized = y_data / max(y_data)

    x_audio = (x_data_normalized * 2 - 1) * (2 ** 23 - 1)
    y_audio = (y_data_normalized * 2 - 1) * (2 ** 23 - 1)

    left_channel = x_audio.astype(np.int32)
    right_channel = y_audio.astype(np.int32)

    stereo_audio = np.column_stack((left_channel, right_channel))
    stereo_audio = np.repeat(stereo_audio, frequency_multiplier, axis=0)[::interval]
    stereo_audio = stereo_audio[:sample_rate * duration_ms // 1000]

    return stereo_audio


def find_image_files(image_folder, file_types=('bmp', 'jpg', 'png')):
    image_files = []
    for file in sorted(os.listdir(image_folder)):
        if file.lower().endswith(file_types):
            image_files.append(os.path.join(image_folder, file))
    return image_files


def process_image(args_and_image_file):
    rotation_angle, sample_rate, duration_ms, frequency_multiplier, interval, image_file = args_and_image_file
    xy_data = bitmap_to_xy(image_file, rotation_angle)
    audio_segment = xy_to_audio(xy_data, sample_rate=sample_rate, duration_ms=duration_ms, frequency_multiplier=frequency_multiplier, interval=interval)
    return audio_segment



if __name__ == "__main__":
    start_time = time.time()
    parser = argparse.ArgumentParser(description="Convert image sequence to Lissajous audio animation")
    parser.add_argument("-i", "--inputfolder", required=True, help="Input folder containing image sequence (JPEG, PNG, or BMP)")
    parser.add_argument("-o", "--outputfile", required=True, help="Output audio file (WAV format)")
    parser.add_argument("-f", "--frequency", type=float, default=1, help="Frequency multiplier (default: 1, accepts decimal values)")
    parser.add_argument("-v", "--interval", type=int, default=1, help="Sample interval (default: 1)")
    parser.add_argument("-r", "--framerate", type=int, default=30, help="Frame rate (default: 30)")
    parser.add_argument("-s", "--samplerate", type=int, default=44100, help="Sample rate (default: 44100)")
    parser.add_argument("-a", "--angle", type=float, default=0, help="Rotation angle (default: 0)")
    parser.add_argument("-j", "--cores", type=int, default=mp.cpu_count(), help="Number of cores for multiprocessing (default: all available)")

    args = parser.parse_args()

    input_folder = args.inputfolder
    output_file = args.outputfile
    frequency_multiplier = args.frequency
    interval = args.interval
    frame_rate = args.framerate
    sample_rate = args.samplerate
    rotation_angle = args.angle
    num_cores = args.cores
    image_files = find_image_files(input_folder)
    duration_ms = 1000 // frame_rate

    with mp.Pool(processes=num_cores) as pool:
            full_audio = pool.map(process_image, [(rotation_angle, sample_rate, duration_ms, frequency_multiplier, interval, image_file) for image_file in image_files])

    full_audio = [audio_segment for audio_segment in full_audio if audio_segment is not None]
    full_audio = np.vstack(full_audio)
    sf.write(output_file, full_audio, sample_rate, subtype='PCM_24')

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"DONE! Elapsed time: {elapsed_time:.2f} seconds")
