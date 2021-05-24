import numpy as np
import pandas as pd
import math

# Take the total of 5 frames before the spike detected to calculate STA 
STA_DELAY = 5

def get_sta(stimulation:dict, movie:np.ndarray, spike_movie_time:float, n_delays:int=STA_DELAY)->np.ndarray:
    """
    Get STA from 'STA_DELAY' numbers of frames

    :param stimulation: will use 'movie', 'fps'
    :param movie: stimulation['movie'] or from DB longblob -> 2d array
    :param spike_movie_time: spike_time - stimulus onset
    """

    ## Filter
    hor_blocks, ver_blocks, total_frames = movie.shape
    # records before movie starts
    if spike_movie_time < 0:
        return None
    frame_idx = get_frame_idx(spike_movie_time, stimulation['fps'])
    # records after movie stops or records don't have enough delays to calculate STA
    if frame_idx >= total_frames or frame_idx<n_delays-1:
        return None
    
    # STA Calculation
    delay_frames = []
    for n in range(n_delays):
        delay_frames.append(get_frame_2darray(stimulation, movie, frame_idx-n))
    delay_frames = np.array(delay_frames)
    sta = np.average(delay_frames, axis=0)
    
    return sta

def get_frame_idx(spike_movie_time:float, fps:float):
    """ Get the frame index by time """
    return math.ceil(spike_movie_time*fps)

def get_frame_2darray(stimulation:dict, movie:np.ndarray, n_frames:int)->np.ndarray:
    """
    Get a 2d array of a movie frame

    :param stimulation: stimulation dictionary
    :param movie: stimulation movie 3d array (horizontal_blocks, vertical_blocks, frames)
    :param n_frames: the number of a frame in the movie
    """
    ## Filter
    hor_blocks, ver_blocks, total_frames = movie.shape
    # records after movie stops or records don't have enough delays to calculate STA
    if n_frames >= total_frames:
        return None
    screen_at_this_frame = np.zeros((stimulation['stim_width'], stimulation['stim_height']))
    for block_x in range(int(stimulation['stim_width']/stimulation['x_block_size'])):
        for block_y in range(int(stimulation['stim_height']/stimulation['y_block_size'])):
            is_block_active = True if movie[block_x][block_y][n_frames] > 0 else False
            # print(block_x, block_y, n_frames, is_block_active)
            screen_x_from = block_x*stimulation['x_block_size']
            screen_x_to = (block_x+1)*stimulation['x_block_size']
            screen_y_from = block_y*stimulation['y_block_size']
            screen_y_to = (block_y+1)*stimulation['y_block_size']
            # print("x {}~{} y {}~{}".format(screen_x_from, screen_x_to, screen_y_from, screen_y_to))
            if is_block_active:
                screen_at_this_frame[screen_x_from:screen_x_to, screen_y_from:screen_y_to] = 100
    return screen_at_this_frame.T