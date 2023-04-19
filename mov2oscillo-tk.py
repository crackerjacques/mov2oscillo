import sys
import os
import numpy as np
from PIL import Image
import argparse
import soundfile as sf
import tkinter as tk
from tkinter import filedialog, messagebox


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


def on_browse_input_folder():
    folder = filedialog.askdirectory()
    input_folder_var.set(folder)


def on_browse_output_file():
    file = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
    output_file_var.set(file)


def on_render():
    input_folder = input_folder_var.get()
    output_file = output_file_var.get()
    frequency_multiplier = float(frequency_var.get())
    interval = int(interval_var.get())
    frame_rate = int(frame_rate_var.get())
    sample_rate = int(sample_rate_var.get())
    rotation_angle = float(angle_var.get())
    image_files = find_image_files(input_folder)
    duration_ms = 1000 // frame_rate

    full_audio = []

    for image_file in image_files:
        xy_data = bitmap_to_xy(image_file, rotation_angle)
        audio_segment = xy_to_audio(xy_data, sample_rate=sample_rate, duration_ms=duration_ms, frequency_multiplier=frequency_multiplier, interval=interval)
        if audio_segment is not None:
            full_audio.append(audio_segment)

    full_audio = np.vstack(full_audio)
    sf.write(output_file, full_audio, sample_rate, subtype='PCM_24')

    messagebox.showinfo()

# Create the GUI
root = tk.Tk()
root.title("Movie to Oscilloscope Converter")

input_folder_var = tk.StringVar()
output_file_var = tk.StringVar()
frequency_var = tk.StringVar(value="1")
interval_var = tk.StringVar(value="1")
frame_rate_var = tk.StringVar(value="30")
sample_rate_var = tk.StringVar(value="44100")
angle_var = tk.StringVar(value="0")

tk.Label(root, text="Input folder:").grid(row=0, column=0, sticky="e")
tk.Entry(root, textvariable=input_folder_var).grid(row=0, column=1)
tk.Button(root, text="Browse", command=on_browse_input_folder).grid(row=0, column=2)

tk.Label(root, text="Output file:").grid(row=1, column=0, sticky="e")
tk.Entry(root, textvariable=output_file_var).grid(row=1, column=1)
tk.Button(root, text="Browse", command=on_browse_output_file).grid(row=1, column=2)

tk.Label(root, text="Frequency multiplier:").grid(row=2, column=0, sticky="e")
tk.Entry(root, textvariable=frequency_var).grid(row=2, column=1)

tk.Label(root, text="Sample interval:").grid(row=3, column=0, sticky="e")
tk.Entry(root, textvariable=interval_var).grid(row=3, column=1)

tk.Label(root, text="Frame rate:").grid(row=4, column=0, sticky="e")
tk.Entry(root, textvariable=frame_rate_var).grid(row=4, column=1)

tk.Label(root, text="Sample rate:").grid(row=5, column=0, sticky="e")
tk.Entry(root, textvariable=sample_rate_var).grid(row=5, column=1)

tk.Label(root, text="Rotation angle:").grid(row=6, column=0, sticky="e")
tk.Entry(root, textvariable=angle_var).grid(row=6, column=1)

tk.Button(root, text="Render", command=on_render).grid(row=7, columnspan=3)

root.mainloop()


