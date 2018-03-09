#!/usr/bin/env python
#   Program:
#       To repackage and generate the equirectangular video from tiled videos.
#   Author:
#       Wen-Chih, MosQuito, Lo
#   Date:
#       2017.3.2

import os 
import sys 
import math 
import subprocess

bitrate_path = "./bitrate/"
qp_path = "./qp/"
auto_path = "/auto/"
output_path = "./output/"
tmp_path = "./tmp/"

def mixed_tiles_quality(no_of_tiles, seg_length, seg_id, 
        low=[], medium=[], high=[]):
    video_list = []
    video_list.append("dash_tiled_set1_init.mp4")

    # Sort the tracks into tiled videos list
    for i in range(1, no_of_tiles+2, 1):
        if i == 1:
            # track1 is needed
            video_list.append("video_tiled_" + "low_" + "dash_" 
                    + "track" + str(i) + "_" + str(seg_id) + ".m4s")
        elif i in low:
            video_list.append("video_tiled_" + "low_" + "dash_" 
                    + "track" + str(i) + "_" + str(seg_id) + ".m4s")
        elif i in medium:
            video_list.append("video_tiled_" + "medium_" + "dash_" 
                    + "track" + str(i) + "_" + str(seg_id) + ".m4s")
        elif i in high:
            video_list.append("video_tiled_" + "high_" + "dash_" 
                    + "track" + str(i) + "_" + str(seg_id) + ".m4s")
        else:
            video_list.append("video_tiled_" + "low_" + "dash_" 
                    + "track" + str(i) + "_" + str(seg_id) + ".m4s")

    make_sure_path_exists(tmp_path)
    make_sure_path_exists(output_path)
    clean_exsited_files(tmp_path, output_path, seg_id)

    # Concatenate init track and each tiled tracks
    for i in range(0, len(video_list), 1):
        subprocess.call('cat %s >> temp_%s.mp4' % 
                ( (bitrate_path + str(seg_length) + "s" + auto_path 
                    + video_list[i]), seg_id), shell=True)

    # Extract the raw hevc bitstream
    subprocess.call('MP4Box -raw 1 temp_%s.mp4' % seg_id, shell=True)

    # Repackage and generate new ERP video
    subprocess.call('MP4Box -add temp_%s_track1.hvc:fps=25 -new output_%s.mp4' % 
            (seg_id, seg_id), shell=True)

    # Move all the files into folders
    subprocess.call('mv temp_%s.mp4 %s' % (seg_id, tmp_path), shell=True)
    subprocess.call('mv temp_%s_track1.hvc %s' % (seg_id, tmp_path), shell=True)
    subprocess.call('mv output_%s.mp4 %s' % (seg_id, output_path), shell=True)


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError:
        print("Folder %s already exsits." % path)
        pass


def clean_exsited_files(tmp_path, output_path, seg_id):
    # Remove files at first
    try:
        rm_temp_mp4 = tmp_path + "temp_" + str(seg_id) + ".mp4" 
        os.remove(rm_temp_mp4)
    except OSError:
        print("File %s do not exsit." % rm_temp_mp4)
        pass

    try:
        rm_temp_hvc = tmp_path + "temp_" + str(seg_id) + "_track1.hvc"
        os.remove(rm_temp_hvc)
    except OSError:
        print("File %s do not exsit." % rm_temp_hvc)
        pass 

    try:
        rm_output = output_path + "output_" + str(seg_id) + ".mp4"
        os.remove(rm_output)
    except OSError:
        print("File %s do not exsit." % rm_output)
        pass


# Testing
#mixed_tiles_quality(9, 10, 1, [2, 3, 4], [5, 6, 7], [8., 9, 10])
