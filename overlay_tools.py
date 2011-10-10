#!/usr/bin/env python

import subprocess as sp
import sys
import os
import re
import glob
import tempfile
import optparse

FFMPEG_CMD = "/usr/bin/ffmpeg"
FFPROBE_CMD = "/usr/bin/ffprobe"
CONVERT_CMD = "/usr/bin/convert"
MENCODER_CMD = "/usr/bin/mencoder"

OVERLAY_CENTER = "(W-w)/2:(H-h)/2"
OVERLAY_BOTTOM_LEFT = "0:H-h"
OVERLAY_BOTTOM_RIGHT = "W-h:H-h"
OVERLAY_TOP_LEFT = "0:0" 
OVERLAY_TOP_RIGHT = "W-h:0"

def create_video(image, video, length, framerate=5, params=''):
    "Create video from animated gif"

    if not os.path.isabs(image):
        image = os.path.abspath(image)
    if not os.path.isabs(video):
        video = os.path.abspath(video)

    # create temprorary directory
    tmpdir = tempfile.mkdtemp()
    cwd = os.getcwd()
    os.chdir(tmpdir)
    
    # extract images from animated gif
    path, ext = os.path.splitext(image)
    cmd = "%s %s %%03d%s" % (CONVERT_CMD, image, ext)
    
    p = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    (stdoutdata, stderrdata) = p.communicate()
    if p.returncode:
        raise Exception("Return code is not null")
    
    frames = glob.glob("*%s" % ext)

    # create video from image
    cmd = "%s -y -r %d -f image2 -i '%%03d%s' %s video.avi" % (FFMPEG_CMD, framerate, ext, params)
    p = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    (stdoutdata, stderrdata) = p.communicate()
    if p.returncode:
        raise Exception("Return code is not null")

    length_video = len(frames) / framerate
    
    # create video
    files = ''
    for i in xrange(0, length / length_video):
        files = files + " video.avi"

    cmd = "%s -forceidx -oac copy -ovc copy -o %s %s" % (MENCODER_CMD, video, files)
    p = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    (stdoutdata, stderrdata) = p.communicate()
    if p.returncode:
        raise Exception("Return code is not null")

    # delete temprorary data    
    os.chdir(cwd)
    for root, dirs, files in os.walk(tmpdir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(tmpdir)
     
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
    create_video(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    print argv

if __name__ == "__main__":
    sys.exit(main(sys.argv))
