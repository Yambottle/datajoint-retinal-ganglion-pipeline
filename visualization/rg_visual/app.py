# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import os
import sys
import argparse
import configparser

import datajoint as dj
from rg_pipeline.run import set_config
from rg_pipeline import compute_utils as cpt_uils
from rg_visual import plot_utils

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://codepen.io/chriddyp/pen/brPBPO.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def get_session_options()->list:
    """
    Get session options for the session dropdown list
    """
    from rg_pipeline.ingest.experiment import Session, Subject, Stimulation, SpikeGroup, Spike
    session = Session()
    subject = Subject()
    query = session * subject
    sessions = query.fetch(as_dict=True)
    session_options = []
    for session in sessions:
        session_options.append({
            'label':'Subject: {} | Sample Number: {} | Session Date: {}'.format(
                session['subject_name'], 
                session['sample_number'], 
                session['session_date']
            ), 
            'value':session['session_id']
        })
    return session_options

app.layout = html.Div(children=["Loading"])
def get_layout():
    session_options = get_session_options()
    layout = html.Div(children=[
        html.H1(children='Retinal Ganglion Cell Experiment Visualization - Drew Yang'),
        dcc.Dropdown(
            id='session-dropdown',
            options=session_options,
            placeholder='Select a session'
        ),
        dcc.Dropdown(
            id='stimulation-dropdown',
            options=[],
            placeholder='Select a stimulation'
        ),
        dcc.Dropdown(
            id='spike-group-dropdown',
            options=[],
            placeholder='Select a spike group'
        ),
        dcc.Dropdown(
            id='spike-dropdown',
            options=[],
            placeholder='Select a spike'
        ),
        dcc.Input(id='delay-input', type='number', min=1, placeholder='Number of frames that are previously from the selected spike', style={'width':'500px'}),
        html.P(id='warning', children='', style={'color':'orange'}),
        html.P(id='error', children='', style={'color':'red'}),
        dcc.Graph(
            id='spike-time-graph',
            figure=go.Figure()
        ),
        dcc.Graph(
            id='sta-graph',
            figure=go.Figure()
        )
    ])
    return layout



@app.callback(
    [
        Output("stimulation-dropdown", "options"),
        Output("stimulation-dropdown", "value")
    ],
    [
        Input("session-dropdown", "value")
    ],
)
def update_stimulation_options(session_value):
    from rg_pipeline.ingest.experiment import Session, Subject, Stimulation, SpikeGroup, Spike
    if session_value:
        stimulation_options = []
        stimulation = Stimulation()
        session = Session()
        query =  stimulation * session & 'session_id = "{}"'.format(session_value)
        stimulations = query.fetch('stimulation_id', 'fps', 'pixel_size', 'stim_height', 'stim_width', 'stimulus_onset', 'x_block_size', 'y_block_size', as_dict=True)
        for stimulation in stimulations:
            stimulation_options.append({
                'label':'FPS: {} | Pixel Size/px: {} | Onset/s: {} | Stimulus Size/blocks {}w * {}h | Block Size/px: {}w * {}h'.format(
                    stimulation['fps'],
                    stimulation['pixel_size'],
                    stimulation['stimulus_onset'],
                    stimulation['stim_width'],stimulation['stim_height'],
                    stimulation['x_block_size'],stimulation['y_block_size']
                ),
                'value':stimulation['stimulation_id'],
            })

        return stimulation_options, ''
    return [], ''

@app.callback(
    [
        Output("spike-group-dropdown", "options"),
        Output("spike-group-dropdown", "value")
    ],
    [
        Input("stimulation-dropdown", "value")
    ],
)
def update_spike_group_options(stimulation_value):
    from rg_pipeline.ingest.experiment import Session, Subject, Stimulation, SpikeGroup, Spike
    if stimulation_value:
        spike_group_options = []
        spike_group = SpikeGroup()
        stimulation = Stimulation()
        query =  spike_group * stimulation & 'stimulation_id = "{}"'.format(stimulation_value)
        spike_groups = query.fetch(as_dict=True)
        for group in spike_groups:
            spike_group_options.append({
                'label':'Spike Group ID: {}'.format(
                    group['spike_group_id']
                ),
                'value':group['spike_group_id'],
            })

        return spike_group_options, ''
    return [], ''

@app.callback(
    [
        Output("spike-dropdown", "options"),
        Output("spike-dropdown", "value")
    ],
    [
        Input("spike-group-dropdown", "value")
    ],
)
def update_spike_options(spike_group_value):
    from rg_pipeline.ingest.experiment import Session, Subject, Stimulation, SpikeGroup, Spike
    if spike_group_value:
        spike_options = []
        spike = Spike()
        spike_group = SpikeGroup()
        query =  spike * spike_group & 'spike_group_id = "{}"'.format(spike_group_value)
        spikes = query.fetch('spike_id', 'spike_time', 'spike_movie_time', as_dict=True)
        for spike in spikes:
            spike_options.append({
                'label':'Spike Time: {} | Spike Movie Time: {}'.format(
                    spike['spike_time'],
                    spike['spike_movie_time']
                ),
                'value':spike['spike_id'],
            })

        return spike_options, ''
    return [], ''

@app.callback(
    [
        Output("spike-time-graph", "figure"),
        Output("sta-graph", "figure"),
        Output("error", "children"),
        Output("warning", "children")
    ],
    [
        Input("spike-dropdown", "value"),
        Input("delay-input", "value")
    ],
    [
        State("spike-group-dropdown", "value"),
        State("stimulation-dropdown", "value"),
        State("session-dropdown", "value"),
        State("delay-input", "value")
    ]
)
def update_spike_time(spike_value, delay_value, spike_group_value, stimulation_value, session_value, n_delays):
    from rg_pipeline.ingest.experiment import Session, Subject, Stimulation, SpikeGroup, Spike
    # from rg_visual import plot_utils
    if spike_value:
        stimulation = Stimulation()
        stimulation_query = stimulation & 'stimulation_id = "{}"'.format(stimulation_value)
        selected_stimulation = stimulation_query.fetch(as_dict=True)[0]
        spike = Spike()
        spike_query = spike & 'spike_id = "{}"'.format(spike_value)
        selected_spike = spike_query.fetch(as_dict=True)[0]

        warning_msg = ""
        error_msg = ""

        n_frames = cpt_uils.get_frame_idx(selected_spike['spike_movie_time'], selected_stimulation['fps'])
        movie = np.frombuffer(selected_stimulation['movie'])
        movie = eval("movie.reshape{}".format(selected_stimulation['movie_shape']))
        frame_2d = cpt_uils.get_frame_2darray(selected_stimulation, movie, n_frames) 
        if frame_2d is not None:
            frame_fig = plot_utils.plot_frame(n_frames, frame_2d)
        else:
            error_msg = "Error: Frame is not available, maybe spike shows after the movie ends."
            return go.Figure(), go.Figure(), error_msg, warning_msg
        
        if n_delays is not None:
            if n_delays<2:
                warning_msg = "Warning: Quickly input multiple digits from the keyboard needs to be tuned. Correct it by clicking increase/decrease after inputting or input slowly"

            sta = cpt_uils.get_sta(selected_stimulation, movie, selected_spike['spike_movie_time'], n_delays)
            if sta is not None:
                sta_fig = plot_utils.plot_sta(n_frames, n_delays, sta)
            else:
                sta_fig = go.Figure()
                error_msg = "Error: STA plot is not available since Spike Movie Time is less than 0 or not enough frames to calculate."
        else:
            sta_fig = go.Figure()
            error_msg = "Error: STA plot is require to set a number of frames that are previously from the selected spike."

        return frame_fig, sta_fig, error_msg, warning_msg
    return go.Figure(), go.Figure(), "", ""

def main(args):
    if args.config and os.path.exists(args.config):
        config = configparser.ConfigParser()
        config.read(args.config)
        set_config(config['DEFAULT']['database'], config['DEFAULT']['user'], config['DEFAULT']['pwd'])
    else:
        raise FileNotFoundError("Datajoint database config file not found.")
    app.layout = get_layout
    app.run_server(debug=True, host='0.0.0.0')

def parse_args_for_main(app_home=os.path.realpath(__file__+'/../..')):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', default=None, help='DataJoint database config file path')
    args = parser.parse_args()
    main(args)

if __name__ == '__main__':
    parse_args_for_main(app_home=os.path.realpath(__file__+'/../..'))