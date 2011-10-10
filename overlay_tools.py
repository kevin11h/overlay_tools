#!/usr/bin/env python

import subprocess as sp
import sys
import os
import optparse

FFMPEG_CMD = "/usr/bin/ffmpeg"
FFPROBE_CMD = "/usr/bin/ffprobe"
CONVER_CMD = "/usr/bin/convert"
MENCODER_CMD = "/usr/bin/mencoder"

OVERLAY_CENTER = "(W-w)/2:(H-h)/2"
OVERLAY_BOTTOM_LEFT = "0:H-h"
OVERLAY_BOTTOM_RIGHT = "W-h:H-h"
OVERLAY_TOP_LEFT = "0:0" 
OVERLAY_TOP_RIGHT = "W-h:0"

def create_video(image, video, length, framerate, params=None):
    "Create video from animated gif"
    pass

def video_params(video):
    "Get video length, height and width"
    length = 0
    height = 0
    width = 0
    return (length, height, width)

def convert_video(video, extension="mp4", params=''):
    "Convert video"

    if not os.path.exists(video):
        raise Exception("No such file %s" % video)

    path = "%s.%s" % (os.path.splitext(video)[0], extension)
    cmd =  "%s -y -i %s %s %s" % (FFMPEG_CMD, video, params, path)

    p = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    (stdoutdata, stderrdata) = p.communicate()
    if p.returncode:
        raise Exception("Return code is not null")

    return path

def overlay_video(video, overlay, new_video, overlay_params=OVERLAY_CENTER, video_params=''):
    "Overlay video or image"

    if not os.path.exists(video):
        raise Exception("No such file %s" % video)
    if not os.path.exists(overlay):
        raise Exception("No such file %s" % overlay)

    cmd_fmt = "%s -y -i %s -vf \"movie=%s [logo]; [in][logo] overlay=%s [out]\" %s %s"
    cmd = cmd_fmt % (FFMPEG_CMD, video, overlay, overlay_params, video_params, new_video)
    
    p = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    (stdoutdata, stderrdata) = p.communicate()
    if p.returncode:
        raise Exception("Return code is not null")

def main(argv):
    print argv

if __name__ == "__main__":
    sys.exit(main(sys.argv))
