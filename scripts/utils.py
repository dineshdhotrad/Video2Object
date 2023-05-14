import cv2
import os
import sys
import subprocess

def mkdir(dirname):
    """Create the folder if not presents"""
    if not os.path.exists(dirname):
        os.mkdir(dirname)

def video2frames(path_to_video, fps, out_dir, downsample = False):

    """ Set Output Video Resolution """
    OUT_WIDTH = 640
    OUT_HEIGHT = 480

    """ Read the video from specified path"""
    cam = cv2.VideoCapture(path_to_video)
    width, height  = cam.get(3), cam.get(4)
    mkdir(out_dir)
    currentframe = 0
    while(True):
        """ Reading from frame"""
        ret,frame = cam.read()
        if ret:
            if currentframe % int(fps) == 0:
                """ If video is still left continue creating images"""
                name = os.path.join(out_dir, str(currentframe)) + '.jpg'
                """ Writing the extracted images"""
                if downsample:
                    frame = cv2.resize(frame, (OUT_WIDTH, OUT_HEIGHT))
                cv2.imwrite(name, frame)
            """ Increasing counter so that it willshow how many frames are created """
            currentframe += 1
        else:
            break
    """ Release all space and windows once done """
    cam.release()
    return(int(height),int(width))

def whereis(afile):
    """
        return directory in which afile is, None if not found. Look in PATH
    """
    if sys.platform.startswith('win'):
        cmd = "where"
    else:
        cmd = "which"
    try:
        ret = subprocess.run([cmd, afile], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)
        return os.path.split(ret.stdout.decode())[0]
    except subprocess.CalledProcessError:
        return None