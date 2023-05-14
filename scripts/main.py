import os
from time import time
from scripts.utils import video2frames, mkdir
from scripts.objectmesh_run import objectmesh

def create_object(path_to_video, output_path, fps, preset):
    start_time = time()
    dir_path = os.path.join(*os.path.split(path_to_video)[:-1])
    mkdir(output_path)
    
    frames_path = output_path + os.sep + "frames"
    mkdir(frames_path)
    vheight, vwidth = video2frames(path_to_video, fps, frames_path)
    focal = str(int(max(vheight,vwidth) * 1.2))
    
    try:
        success = objectmesh(dir_path, frames_path, focal, preset)
    except:
        raise
    
    end_time = time()
    
    return end_time-start_time