

# a python script that uses moviepy to join 3 videos together side by side
from moviepy.editor import *
import os

outdir = "done_clips/bc/"
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


# clips = "main_clips/bc/c-7.mp4"


# linedClips = """main_clips/bc/r-7-ecbjricnrjveijhkdkkinfcbnbtfudh.webm
# main_clips/bc/l-2-ebcfnbgftvricljhnegukdjlrkirbfnn.webm
# main_clips/bc/c-7-dancinggirl.mp4"""

linedClips = """main_clips/bc/c-1-8657187155864411810-jNnpIkZU.mp4
main_clips/bc/s-4-1695305048419498.webm
main_clips/bc/s-1-4 ch1.webm"""




left = None
center = None
right = None

# clips = [VideoFileClip(c) for c in clips.split(" ")]
clips = [VideoFileClip(c) for c in linedClips.split("\n")]
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
    elif filename.startswith("a-"):
        if not left:
            left = clips.pop(0)
            continue
        if not center:
            center = clips.pop(0)
            continue
        if not right:
            right = clips.pop(0)
            continue

videos = [left, center, right]
videos = [v for v in videos if v is not None]
print("##", "length check 1")
for idx, file in enumerate(videos):
    print("###", get_filename(file.filename), "duration", file.duration)

try:
    shortest_drop = min([float(get_filename(v.filename).split("-")[1].split(".")[0])
                        for v in videos if get_filename(v.filename).split("-")[1].split(".")[0] != "n"])
except:
    shortest_drop = 999
    for idx, file in enumerate(videos):
        if file.duration < shortest_drop:
            shortest_drop = file.duration

for idx, file in enumerate(videos):
    print("\n##", "file", idx, file, get_filename(videos[idx].filename))
    length = float(videos[idx].duration)
    val = get_filename(videos[idx].filename).split("-")[1].split(".")[0]
    print(val)
    if val == "n":
        drop = videos[idx].duration
    else:
        drop = float(val)
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

# find the video with the shorted x
# for idx, file in enumerate(videos):
biggest_x = max(videos, key=lambda x: x.h).h
biggest_y = max(videos, key=lambda x: x.w).w
smallest_x = min(videos, key=lambda x: x.h).h
smallest_y = min(videos, key=lambda x: x.w).w


print("###", "smallest_x", smallest_x)

for idx, file in enumerate(videos):
    print("###", get_filename(file.filename), "size", file.size)
    if file.h > smallest_x:
        videos[idx] = videos[idx].resize(height=smallest_x)


shortest = min(videos, key=lambda x: x.duration).duration
# shortest = 3
print("###", "shortest", shortest)
for idx, file in enumerate(videos):
    videos[idx] = videos[idx].subclip(0, shortest)

print("##", "length check 2")
for idx, file in enumerate(videos):
    print("###", get_filename(file.filename), "duration", file.duration)

lowest_fps = min([v.fps for v in videos])

# join_videos(videos)
final_clip = clips_array([videos])


def addText(text, clip):
    txt_clip = TextClip(text, fontsize=30, color='gray', transparent=True)

    # setting position of text in the center and duration will be 10 seconds
    txt_clip = txt_clip.set_position(
        (0.3, 0.2), relative=True)
    txt_clip = txt_clip.set_duration(clip.duration).set_fps(clip.fps)
    txt_clip.set_ismask(True)
    # Overlay the text clip on the first video clip
    video = CompositeVideoClip([clip, txt_clip])
    # return concatenate_videoclips([text_clip, clip])
    return video


def calculate_bitrate(max_filesize_kb, duration_seconds, framerate):
    # Convert max filesize from KB to bits
    max_filesize_bits = max_filesize_kb * 8 * 1024
    
    # Calculate maximum number of bits available for video data
    max_video_bits = max_filesize_bits - (framerate * duration_seconds * 1000)
    
    # Calculate bitrate in kbps
    bitrate_kbps = max_video_bits / duration_seconds / 1000
    
    # Adjust bitrate if it exceeds the maximum file size
    if bitrate_kbps * duration_seconds * 1000 > max_video_bits:
        bitrate_kbps = max_video_bits / (duration_seconds * 1000)
    
    return bitrate_kbps


print("###", final_clip.duration, lowest_fps)

final_clip = addText("rip /bcg/", final_clip)

# scale down to a max of 2048x2048px
if final_clip.h > 2048:
    final_clip = final_clip.resize(height=2048)
if final_clip.w > 2048:
    final_clip = final_clip.resize(width=2048)

name = [get_filename(v.filename).split(".")[0] for v in videos]
name = [n.split("-")[-1][:4] for n in name]
name = "-".join(name)+".webm"
print(name)

# calculate bitrate


# Example usage
filesize_kb = float(3500)  # give ourselves a gap
bitrate = str(calculate_bitrate(filesize_kb, final_clip.duration,lowest_fps))+"k"
print("Bitrate: {} kbps".format(bitrate))


# exit()
final_clip.write_videofile(outdir + name, codec="libvpx",
                           audio_codec='libvorbis',
                           fps=lowest_fps,                     threads='12', bitrate=bitrate,
                           )

# final_clip.write_videofile(outdir + "final.mp4",
#                            fps=lowest_fps)
print("###", "main file", "start")
