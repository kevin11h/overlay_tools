#!/usr/bin/env python

import subprocess as sp
import sys
import os
import optparse

FFMPEG_CMD = "/usr/bin/ffmpeg"
CONVER_CMD = "/usr/bin/convert"
MENCODER_CMD = "/usr/bin/mencoder"

OVERLAY_CENTER = "(W-w)/2:(H-h)/2"
OVERLAY_BOTTOM_LEFT = "0:H-h"
OVERLAY_BOTTOM_RIGHT = "W-h:H-h"
OVERLAY_TOP_LEFT = "0:0" 
OVERLAY_TOP_RIGHT = "W-h:0"

def create_video(filename, image, params=None):
    "Create video from animated gif"
    pass

def video_params(filename):
    "Get video length, height and width"
    length = 0
    height = 0
    width = 0
    return (length, height, width)

def convert_video(filename, extension="mp4", params=None):
    "Convert video"

    if not os.path.exists(filename):
        raise Exception("No such file %s" % filename)

    path = "%s.%s" % (os.path.splitext(filename)[0], extension)
    if params:
        cmd = "%s -y -i %s %s %s" % (FFMPEG_CMD, filename, params, path)
    else:
        cmd = "%s -y -i %s %s" % (FFMPEG_CMD, filename, path)

    p = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    (stdoutdata, stderrdata) = p.communicate()
    if p.returncode:
        raise Exception("Return code is not null")

    return path

def overlay_video(filename, overlay, params=None):
    "Overlay video or image"
    pass

def main(argv):
    convert_video(sys.argv[1])
    print argv

if __name__ == "__main__":
    sys.exit(main(sys.argv))
