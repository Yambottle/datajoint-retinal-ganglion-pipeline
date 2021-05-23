import os
import pickle
import numpy as np

from ingest.experiment import Session, Stimulation

def load_file_pickle(datasource:dict):
    """
    Implementation of load() specifically for pickle files

    :param datasource: a dictionary including pickle file path
    """
    if os.path.exists(datasource['path']):
        with open(datasource['path'], 'rb') as datafile:
            data = pickle.load(datafile)
        # TODO - insert pandas dataframe not included in the documentation https://docs.datajoint.io/python/manipulation/1-Insert.html#insert
        sessions = []
        stimulations = []
        # TODO - max stimulation id
        stimulation_idx = 0
        for session in data:
            for idx in range(len(session['stimulations'])):
                sessions.append([ \
                    session['sample_number'], \
                    stimulation_idx, \
                    session['subject_name'], \
                    session['session_date'] \
                ])
                stimulation = session['stimulations'][idx]
                stimulation_spikes = np.array(stimulation['spikes'], dtype=object)
                # print(type(stimulation['movie'].tobytes()), type(stimulation_spikes.tobytes()))
                stimulations.append([ \
                    stimulation_idx, \
                    stimulation['fps'], \
                    stimulation['movie'].tobytes(), \
                    stimulation['n_frames'], \
                    stimulation['pixel_size'], \
                    stimulation['stim_height'], \
                    stimulation['stim_width'], \
                    stimulation['stimulus_onset'], \
                    stimulation['x_block_size'], \
                    stimulation['y_block_size'], \
                    stimulation_spikes.tobytes() \
                ])
                stimulation_idx += 1

        print("Loading Stimulations...")
        Stimulation.insert(stimulations)
        # print(Stimulation.fetch('fps'))
        print("Loading Sessions...")
        Session.insert(sessions)
        # print(Session.fetch())

    else:
        raise FileNotFoundError

# TODO - since these data sources are not required in this specific task, ignore implementation for now
# def load_file_csv(datasource:dict):
#     pass

# def load_file_parquet(datasource:dict):
#     pass

# def load_file_json(datasource:dict):
#     pass

# def load_database_mysql(datasource:dict):
#     pass

# def load_database_mssql(datasource:dict):
#     pass

# def load_database_mongodb(datasource:dict):
#     pass

# def load_request_json(datasource:dict):
#     pass