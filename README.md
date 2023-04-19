# mov2oscillo
Convert movie file to Oscillo Scope vector animation.

# 1

download or clone this repo.
```
git clone https://github.com/crackerjacques/mov2oscillo.git

cd mov2oscillo
```

install requirements

___FFMPEG___

it need to deconstruct your movie files.
when you have some solution to similar, skip this process.

Windows
```
download and add path to your system path or symbolic link to your windows dir
https://ffmpeg.org/download.html
```

MacOS 
```
brew install ffmpeg
```
Linux
```
apt install ffmpeg
```

__Python__

```
pip install numpy pillow soundfile argparse
```

# 2

Deconstruct your movie.
```
python decnstruct -i [your_movie_file.mp4] -d [your_deconstructed_directory]
```
it makes movie file to per frame .pngs

Material files should be as black and white as possible, preferably drawn with black lines on a white background.
It is recommended to use OpenCV or video editing software to create them.

# 3

Type in your terminal or command prompt.

```
python mov2oscillo.py -i [your_deconstructed_directory] -o [your_wav.file.wav] 

```
options:

```
  -h, --help            show this help message and exit
  -i INPUTFOLDER, --inputfolder INPUTFOLDER
                        Input folder containing image sequence (JPEG, PNG, or
                        BMP)
  -o OUTPUTFILE, --outputfile OUTPUTFILE
                        Output audio file (WAV format)
  -f FREQUENCY, --frequency FREQUENCY
                        Frequency multiplier (default: 1, accepts decimal
                        values)
  -v INTERVAL, --interval INTERVAL
                        Sample interval (default: 1)
  -r FRAMERATE, --framerate FRAMERATE
                        Frame rate (default: 30)
  -s SAMPLERATE, --samplerate SAMPLERATE
                        Sample rate (default: 44100)
  -a ANGLE, --angle ANGLE
                        Rotation angle (default: 0)
  -j CORES, --cores CORES
                        Number of cores for multiprocessing (default: all
                        available)
```

Drag and drop the resulting Wav file into your DAW, insert the analyzer, and play it. 
recommended analyzer is FLUX:: Stereo Tool.(freeware)
https://www.flux.audio/project/stereo-tool-freeware/

# APPENDIX

■ ___mov2oscillo-tk.py___

tkinter easy GUI implementation.

■ ___mov2oscillo-mc.py___

multi-core implementation, 
faster rendering.

e.g.
```
python -i your_dir -o your_file.wav -r 30 -s 48000 -v 2 -j 8
```

■ ___mov2oscillo-cuda.py___

CUDA implementation
calclate by GPU

need to cudatoolkit and environments.
I thought having cupy and numba do the processing would accelerate the process, but they are ___slow as slugs___ and you don't need to use them.


# TIPS
There is a trade-off between image quality and drawing range, in the sampling frequency for audio may require some interval.
After running various experiments on my own, I think a resolution of 100-200px is preferable.
If you find that the video is played back slower or faster than the original, try changing the frame rate.

If you use the -f2 option to increase the frequency, the image quality will improve, but the drawing area will narrow.

The gif animation settings above are
```
python mov2oscillo-mp.py -i x100 -o badapple100-15-f2.wav -r 15 -s 352800 -a 45 -j 24 -f 2
```

Common VST plug-ins typically have a sampling frequency limit of 192kHz to 384kHz, and audio interfaces are typically 192kHz or 96kHz.
Further image quality improvement may require the use of an audio interface other than that used for production.


If I have free time in the future, I would like to implement various preparations, such as resizing the input image, thickening the lines with OpenCV, etc.
