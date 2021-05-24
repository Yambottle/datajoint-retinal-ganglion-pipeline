import numpy as np
import plotly.graph_objects as go

def plot_frame(n_frames:int, frame:np.ndarray):
    """
    Plot a frame

    :param n_frames: the number of a frame
    :param frame: a 2d array of a frame
    """
    height, width = frame.shape
    fig = go.Figure(data=go.Heatmap(
                    z=frame,
                    colorscale='greys'))
    fig.update_layout(title='Movie at #{} frame'.format(n_frames),
                        xaxis_title='stimulus_width {}'.format(width),
                        yaxis_title='stimulus_height {}'.format(height),
                        hovermode=False)
    fig.update_traces(showscale=False)
    
    return fig

def plot_sta(n_frames:int, n_frames_of_delay:int, sta:np.ndarray):
    """
    Plot a STA of several delays of a frame

    :param n_frames: the number of a frame
    :param n_delays: how many delays of a frame i.e. n_delays=5 from frame 49 -> 49, 48, 47, 46, 45 
    :param frame: a 2d array of a frame
    """
    height, width = sta.shape
    fig = go.Figure(data=go.Heatmap(
                    z=sta,
                    colorscale='greys'))
    fig.update_layout(title='STA at #{} frame with {} previous frames'.format(n_frames, n_frames_of_delay),
                        xaxis_title='stimulus_width {}'.format(width),
                        yaxis_title='stimulus_height {}'.format(height),
                        hovermode=False)
    fig.update_traces(showscale=False)
    
    return fig