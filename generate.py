import argparse
from pathlib import Path
from yt_dlp import YoutubeDL
from moviepy.editor import *
import os
from fpdf import FPDF

def generate():
    parser = argparse.ArgumentParser(
        "youtube-to-pdf", 
        description="Convert a youtube link to pdf by taking a screenshot every specified number of seconds (defaults to 11.25 (24 beats at 128 bpm) seconds)."
    )
    parser.add_argument("url", type=str)
    parser.add_argument('-b', '--bpm', type = float, default=None, help="bpm for 24 beats on the screen")
    parser.add_argument('-d', '--delay', type=float, default=11.25, help="Delay between screenshots")
    parser.add_argument('-n', '--name', type=str, default='output', help="output file path name")
    args = parser.parse_args()
    if args.bpm is not None:
        args.delay = 24.0 / args.bpm * 60.0

    options = {
        'outtmpl': f'{args.name}.webm',
    }

    with YoutubeDL(options) as ydl:
        ydl.download([args.url])

    i = 0
    with VideoFileClip(f'{args.name}.webm') as clip:
        while i * args.delay < clip.duration:
            clip.save_frame(f'{args.name}{i}.png', t = i * args.delay)
            i += 1 

        pdf = FPDF()
        for j in range(i):
            if j % 2 == 0:
                pdf.add_page()
            pdf.image(f'{args.name}{j}.png', None, None, 175)
        pdf.output(f'{args.name}.pdf', "F")

    for j in range(i):
        os.remove(f'{args.name}{j}.png')
    os.remove(f'{args.name}.webm')


if __name__ == "__main__":
    generate()