#!/usr/bin/env python

import subprocess
import sys
import os
import optparse

FFMPEG_CMD = "/usr/bin/ffmpeg"
CONVER_CMD = "/usr/bin/convert"
MENCODER_CMD = "/usr/bin/mencoder"

def create_video(filename, image):
    "Create video from animated gif"
    pass

def video_length(filename):
    "Get video lenght"
    pass

def convert_video(filename, container):
    "Convert video"
    pass

def overlay_video(filename, overlay):
    "Overlay video or image"
    pass

def main(argv):
    print argv

if __name__ == "__main__":
    sys.exit(main(sys.argv))
