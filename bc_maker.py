# a python script that uses moviepy to join 3 videos together side by side
from moviepy.editor import *
import os

outdir = "done_clips/"
indir = "main_clips/bc/"


def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f


def get_filename(path):
    return os.path.basename(path)


def join_videos(videoArr):
    print("###", "joining videos")
    final_clip = clips_array(videoArr)
    final_clip.write_videofile(outdir + "final.mp4", codec="libx264", fps=24)
    # final_clip = concatenate_videoclips([clip1,clip2,clip3])
    # final_clip.write_videofile("my_concatenation.mp4")


clips = "main_clips/bc/r-7.webm main_clips/bc/l-2.webm main_clips/bc/c-7.mp4"


left = None
center = None
right = None

clips = [VideoFileClip(c) for c in clips.split(" ")]
print("###", [get_filename(c.filename) for c in clips])
for filename in [get_filename(c.filename) for c in clips]:
    if filename.startswith("l-"):
        left = clips.pop(0)
    elif filename.startswith("c-"):
        center = clips.pop(0)
    elif filename.startswith("r-"):
        right = clips.pop(0)
    elif filename.startswith("s-"):
        if not left:
            left = clips.pop(0)
            continue
        if not right:
            right = clips.pop(0)
            continue

videos = [left, center, right]
print("##", "length check 1")
for idx, file in enumerate(videos):
    print("###", get_filename(file.filename), "duration", file.duration)

shortest_drop = min([float(get_filename(c.filename).split(
    "-")[1].split(".")[0]) for c in videos])

for idx, file in enumerate(videos):
    print("\n##", "file", idx, file, get_filename(videos[idx].filename))
    length = float(videos[idx].duration)
    drop = float(get_filename(
        videos[idx].filename).split("-")[1].split(".")[0])
    # print("###", "length", videos[idx].duration, "drop@", drop)
    if drop > shortest_drop:
        diff = drop - shortest_drop
        # trim the start down by the difference
        videos[idx] = videos[idx].subclip(diff, videos[idx].duration)
        print("###",
              "diff", diff,
              "prevlength", length,
              "newlength", videos[idx].duration,
              "expected_duration", length-diff)
    else:
        print("###", "no need to trim")


shortest = min(videos, key=lambda x: x.duration).duration
print("###", "shortest", shortest)
for idx, file in enumerate(videos):
    videos[idx] = videos[idx].subclip(0, shortest)

print("##", "length check 2")
for idx, file in enumerate(videos):
    print("###", get_filename(file.filename), "duration", file.duration)

lowest_fps = min([v.fps for v in videos])

# join_videos(videos)
final_clip = clips_array([videos])

print("###", final_clip.duration, lowest_fps)


final_clip.write_videofile(outdir + "final.webm", codec="libvpx",
                           audio_codec='libvorbis',
                           fps=lowest_fps)
print("###", "main file", "start")
