#!/usr/bin/env python

import subprocess
import sys
import os
import optparse

FFMPEG_CMD = "/usr/bin/ffmpeg"
CONVER_CMD = "/usr/bin/convert"
MENCODER_CMD = "/usr/bin/mencoder"

OVERLAY_CENTER = "W/2-w/2:H/2-h2"
OVERLAY_TOP_LEFT = "0:H-h"
OVERLAY_TOP_RIGHT = "W-h:H-h"
OVERLAY_BOTTOM_LEFT = "0:0" 
OVERLAY_BOTTOM_RIGHT = "W-h:0"

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
    pass

def overlay_video(filename, overlay, params=None):
    "Overlay video or image"
    pass

def main(argv):
    print argv

if __name__ == "__main__":
    sys.exit(main(sys.argv))
