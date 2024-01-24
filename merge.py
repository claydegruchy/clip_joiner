import pygame
from moviepy.editor import *
import argparse
import random


parser = argparse.ArgumentParser(
    description='Concatenate videos with FFMPEG, add "xfade" between segments.')
parser.add_argument('-m', '--main', required=True, description="Main video file or directory of video files. If directory, will operate on every file in that directory" )
# mandatory
parser.add_argument('-i', '--insert', required=True, description="Video file or directory of video files to insert at random into a main file. If directory, will pick a random file from that directory")
parser.add_argument('-o', '--out_dir', default="done_clips/")

args = parser.parse_args()


def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f


# if args.insert is a directory, pick a random file from that directory
# if args.insert is a file, use that file
if os.path.isdir(args.insert):
    args.insert = os.path.join(args.insert, random.choice(
        [f for f in os.listdir(args.insert) if not f.startswith('.')]))

if os.path.isdir(args.main):
    # generate a list of all files (with full dir) in the directory that are not hidden
    args.list = [os.path.join(args.main, f)
                 for f in listdir_nohidden(args.main)]


print("###", "main file", args)
# exit()


def cut_video(video, start, end):
    return [video.subclip(start, end), video.subclip(end)]


def main_process(args, custom_padding=1, insert_length=5):
    print("###", "starting")
    print("###\t", "main file", args.main)
    print("###\t", "insert file", args.insert)

    insert = VideoFileClip(args.insert)
    # get fps
    if insert.audio:
        insert.audio.set_fps(25)
    random_insert_position = random.randint(
        1, int(insert.duration-insert_length)-1)
    insert = insert.subclip(random_insert_position,
                            random_insert_position+insert_length)

    clip = VideoFileClip(args.main)
    if clip.audio:
        clip.audio.set_fps(25)

    l = int(clip.duration)
    print("###\t", "main file length", l)
    random_clip_cut_time = random.randint(l//4, (l//4)*3-1)
    # random_clip_cut_time = 2  # testing

    [part1, part2] = cut_video(clip, 0, random_clip_cut_time)

    if insert.h > part1.h:
        insert = insert.resize(height=part1.h)

    if insert.w > part1.w:
        insert = insert.resize(width=part1.w)

    combined = concatenate_videoclips(
        [
            part1,
            insert.crossfadein(custom_padding),
            part2.crossfadein(custom_padding)
        ],
        padding=-custom_padding,
        method="compose"
    )
    if combined.audio:
        combined.audio.fps = 25

    return combined, insert, clip


if __name__ == "__main__":
    if not hasattr(args, 'list'):
        args.list = [args.main]

    for main in args.list:
        print("###\t", "starting clip\t", main)
        args.main = main
        if os.path.isfile(args.out_dir+os.path.basename(args.main)):
            print("###\t", "skipping\t", main)
            continue
        combined, insert, clip = main_process(args)
        # combined.preview()
        lowest_fps = min([insert.fps, clip.fps])
        # get base filename of main file
        base_filename = os.path.basename(args.main)
        combined.write_videofile(
            args.out_dir+'last_file.mp4', fps=lowest_fps, verbose=False)
        combined.write_videofile(
            args.out_dir+base_filename, fps=lowest_fps, verbose=False)

        print("###", "done")
    print("###", "all done")
