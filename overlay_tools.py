#!/usr/bin/env python

import subprocess as sp
import sys
import os

FFMPEG_CMD = "/usr/bin/ffmpeg"
FFPROBE_CMD = "/usr/bin/ffprobe"
CONVERT_CMD = "/usr/bin/convert"
IDENTIFY_CMD = "/usr/bin/identify"
MENCODER_CMD = "/usr/bin/mencoder"

OVERLAY_CENTER = "(W-w)/2:(H-h)/2"
OVERLAY_BOTTOM_LEFT = "0:H-h"
OVERLAY_BOTTOM_RIGHT = "W-w:H-h"
OVERLAY_TOP_LEFT = "0:0"
OVERLAY_TOP_RIGHT = "W-w:0"

def create_video(image, video, length, framerate=5, params=''):
    '''Create video from animated gif.

    Arguments:
    image -- The input image file.
    video -- The output video file.
    length -- The length of video in seconds.
    framerate -- The framerate of the video (default is 5).
    params -- Additional ffmpeg video parameters.

    Returns:
    None.

    Create video file from animated image with the framerate.

    '''

    import glob
    import tempfile

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
    files = 'video.avi'
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

def get_image_params(image):
    '''Get image number of frames, width and height.

    Arguments:
    image -- The input image file.

    Returns:
    Tuaple (number of frames, width, height)

    '''
    import re

    num_frames = 0
    width = 0
    height = 0

    cmd = "%s %s" % (IDENTIFY_CMD, image)

    p = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    (stdoutdata, stderrdata) = p.communicate()

    if p.returncode:
        raise Exception("Return code is not null")

    lines = stdoutdata.splitlines()
    if lines:

        num_frames = len(lines)
        width_height_regexp = re.compile(".*\s(?P<width>\d+)x(?P<height>\d+)\s.*")
        match = width_height_regexp.match(lines[0])

        if match:
            width = int(match.groupdict()["width"])
            height = int(match.groupdict()["height"])

    return (num_frames, width, height)

def get_video_params(video):
    '''Get video length, width and height.

    Arguments:
    video -- The input video file.

    Returns:
    Tuaple (length, width, height)

    '''

    import re

    length = 0
    height = 0
    width = 0

    cmd = "%s %s" % (FFPROBE_CMD, video)

    p = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    (stdoutdata, stderrdata) = p.communicate()

    if p.returncode:
        raise Exception("Return code is not null")

    duration_regexp = re.compile(".*Duration:\s(?P<hours>[0-9.]+):(?P<minutes>[0-9.]+):(?P<seconds>[0-9.]+),.*")
    width_height_regexp = re.compile(".*Stream.*,\s(?P<width>\d+)x(?P<height>\d+).*")

    for line in stderrdata.splitlines():

        match = duration_regexp.match(line)
        if not length and match:
            seconds = int(round(float(match.groupdict()["seconds"])))
            minutes = int(round(float(match.groupdict()["minutes"])))
            hours = int(round(float(match.groupdict()["hours"])))
            length = seconds + 60 * minutes + 3600 * hours

        match = width_height_regexp.match(line)
        if not height and not width and match:
            width = int(match.groupdict()["width"])
            height = int(match.groupdict()["height"])

    return (length, width, height)

def convert_video(video, extension="mp4", params=''):
    '''Convert video.

    Arguments:
    video -- The input video file.
    extension -- The output video extension.
    video_params -- Additional ffmpeg video parameters.

    Returns:
    None.

    Convert input video file into video file with the new extension.

    '''

    if not os.path.exists(video):
        raise Exception("No such file %s" % video)

    path = "%s.%s" % (os.path.splitext(video)[0], extension)
    cmd =  "%s -y -i %s %s %s" % (FFMPEG_CMD, video, params, path)

    p = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    (stdoutdata, stderrdata) = p.communicate()

    if p.returncode:
        raise Exception("Return code is not null")

    return path

def create_overlay_video(video, overlay, new_video, audio=None, overlay_params=OVERLAY_CENTER,
    video_params="-strict experimental"):
    '''Create video overlay.
    
    Arguments:
    video -- The input video file.
    overlay -- The input video file for overlay. 
    new_video -- The new video file name.
    audio -- The soundtrack audio file.
    overlay_params -- Overlay position parameter. Possible values are OVERLAY_CENTER, 
                      OVERLAY_BOTTOM_LEFT, OVERLAY_BOTTOM_RIGHT, OVERLAY_TOP_LEFT and
                      OVERLAY_TOP_RIGHT.
    video_params -- Additional ffmpeg video parameters.

    Returns:
    None.

    Create overlay of video and store it into new video file. One may change a default soundtrack
    of input video with help new audio soundtrack file. Soundtrack file may be any of supported by 
    ffmpeg audio file, for example, a mp3 file.
  
    '''

    if not os.path.exists(video):
        raise IOError("No such file %s" % video)
    if not os.path.exists(overlay):
        raise IOError("No such file %s" % overlay)
    if not os.path.exists(audio):
        raise IOError("No such file %s" % audio)

    if audio:
        video_length, video_width, video_height = get_video_params(video)
        cmd_fmt = "%s -y -i %s -t %d -i %s -vf \"movie=%s [logo]; [in][logo] overlay=%s [out]\" %s %s"
        cmd = cmd_fmt % (FFMPEG_CMD, audio, video_length, video, overlay,
            overlay_params, video_params, new_video)
    else:
        cmd_fmt = "%s -y -i %s -vf \"movie=%s [logo]; [in][logo] overlay=%s [out]\" %s %s"
        cmd = cmd_fmt % (FFMPEG_CMD, video, overlay, overlay_params, video_params, new_video)

    p = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    (stdoutdata, stderrdata) = p.communicate()

    if p.returncode:
        raise Exception("Return code is not null")

def set_video_hue_and_saturation(video, new_video, hue=0, saturation=1, video_params="-strict experimental"):
    '''Set video hue and saturation.

    Arguments:
    video -- The input video file.
    new_video -- The new video file name.
    hue -- The hue of video (default is 0).
    saturation -- The saturation of video (default is 0).
    video_params -- Additional ffmpeg video parameters.

    Returns:
    None.

    Set hue and saturation for video and store it into new video file.

    '''

    cmd = "%s -y -i %s -vf 'mp=hue=%d:%d' %s %s" % (FFMPEG_CMD, video, hue, saturation, video_params, new_video)

    p = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    (stdoutdata, stderrdata) = p.communicate()

    if p.returncode:
        raise Exception("Return code is not null")

def set_video_brightness_and_contrast(video, new_video, brightness=0, contrast=0, video_params="-strict experimental"):
    '''Set video brightness and contrast.

    Arguments:
    video -- The input video file.
    new_video -- The new video file name.
    brightness -- The brightness of video (default is 0).
    contrast -- The contrast of video (default is 0).
    video_params -- Additional ffmpeg video parameters.

    Returns:
    None.

    Set brightness and contrast for video and store it into new video file.

    '''

    cmd = "%s -y -i %s -vf 'mp=eq=%d:%d' %s %s" % (FFMPEG_CMD, video, brightness, contrast, video_params, new_video)

    p = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    (stdoutdata, stderrdata) = p.communicate()

    if p.returncode:
        raise Exception("Return code is not null")

def overlay_video_worker(video, overlays, new_video, overlay_params=OVERLAY_CENTER, video_params=''):
    '''Complex overlay video.
    
    Arguments:

    Returns:

    '''
    pass

def regular_http_download(url, filename, size_constraint=0):
    '''Download file from url.

    Arguments:
    url -- The uniform resource locator.
    filename -- The name of file to store url content.
    size_constraint -- The size of url content constraint. 0 means no constraint.

    Returns:
    None.

    Download the url content and store it into file. If content size is greater then 
    size of content constraint the function raises exception.

    '''
    import urllib

    u = urllib.urlopen(url)
    content_length = u.info()['Content-Length']

    if not size_constraint or size_constraint > content_length:
        f = open(filename, 'wb') 
        f.write(u.read())
        f.close()
    else:
        raise Exception('File is too big for downloading due to size constraint!')

def main(argv):
    '''Main function.

    Arguments:
    argv -- The command line arguments.

    Returns:
    Return code.
 
    Do main work to parse command line arguments and to applay overlay.

    '''
    from optparse import OptionParser

    usage = "usage: %prog -i IMAGE [-f FRAMERATE] [-a AUDIO] [-o output_video] [--overlay-ceter | ...] <input_video>"
    parser = OptionParser(usage)

    parser.add_option("--overlay-center",
        action="store_true",
        dest="overlay_center",
        default=False,
        help="overlay at center of input video")

    parser.add_option("--overlay-bottom-left",
        action="store_true",
        dest="overlay_bottom_left",
        default=False,
        help="overlay at bottom left of input video")

    parser.add_option("--overlay-bottom-right",
        action="store_true",
        dest="overlay_bottom_right",
        default=False,
        help="overlay at bottom right of input video")

    parser.add_option("--overlay-top-left",
        action="store_true",
        dest="overlay_top_left",
        default=False,
        help="overlay at top left of input video")

    parser.add_option("--overlay-top-right",
        action="store_true",
        dest="overlay_top_right",
        default=False,
        help="overlay at top right of input video")

    parser.add_option("-i", "--image",
        action="store",
        type="string",
        dest="image",
        metavar="IMAGE",
        help="set overlay IMAGE")

    parser.add_option("-f", "--framerate",
        action="store",
        type="int",
        dest="framerate",
        metavar="FRAMERATE",
        help="set overlay animated FRAMERATE")

    parser.add_option("-o", "--output-video",
        action="store",
        type="string",
        dest="output_video",
        metavar="FILE",
        help="set output video filename")

    parser.add_option("-a", "--audio",
        action="store",
        type="string",
        dest="audio",
        metavar="FILE",
        help="set audio file as soundtrack")

    (options, args) = parser.parse_args()

    overlay_place = OVERLAY_CENTER
    if options.overlay_center:
        overlay_place = OVERLAY_CENTER
    elif options.overlay_bottom_left:
        overlay_place = OVERLAY_BOTTOM_LEFT
    elif options.overlay_bottom_right:
        overlay_place = OVERLAY_BOTTOM_RIGHT
    elif options.overlay_top_left:
        overlay_place = OVERLAY_TOP_LEFT
    elif options.overlay_top_right:
        overlay_place = OVERLAY_TOP_RIGHT

    if not options.image or not args:
        parser.print_help()
        return 1

    image = options.image
    if not os.path.isabs(image):
        image = os.path.abspath(image)

    video = args[0]
    if not os.path.isabs(video):
        video = os.path.abspath(video)

    if options.output_video:
        new_video = options.output_video
        if not os.path.isabs(new_video):
            new_video = os.path.abspath(new_video)
    else:
        path, ext = os.path.splitext(video)
        new_video = "%s_overlay.mp4" % (path)

    video_length, video_width, video_height = get_video_params(video)
    image_num_frames, image_width, image_height = get_image_params(image)

    if not image_num_frames:
        print >> sys.stderr, "Image is broken!"
        return 1

    if image_num_frames == 1:
        image_video = image
    else:
        image_path, image_ext = os.path.splitext(image)
        image_video = "%s.mp4" % (image_path)

        if options.framerate:
            create_video(image, image_video, video_length, options.framerate)
        else:
            create_video(image, image_video, video_length)

    if options.audio:
        audio = options.audio
        if not os.path.isabs(audio):
            audio = os.path.abspath(audio)
        create_overlay_video(video, image_video, new_video, audio, overlay_place)
    else:
        create_overlay_video(video, image_video, new_video, overlay_params=overlay_place)

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
