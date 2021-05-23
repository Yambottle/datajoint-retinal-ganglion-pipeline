import os
import pickle
import numpy as np

from ingest.experiment import Session, Subject, Stimulation

def load_file_pickle(datasource:dict):
    """
    Implementation of load() specifically for pickle files

    :param datasource: a dictionary including pickle file path
    """
    if os.path.exists(datasource['path']):
        with open(datasource['path'], 'rb') as datafile:
            data = pickle.load(datafile)
        sessions = []
        subject_names = Subject.fetch('subject_name')
        subjects = []
        stimulations = []
        stimulation_idx = len(Stimulation.fetch('stimulation_id'))+1
        for session in data:
            # Subject
            if session['subject_name'] not in subject_names:
                subjects.append([ 
                    None,
                    session['subject_name']
                ])
                subject_names = np.append(subject_names, session['subject_name'])
            
            # Session without Stimulations
            if len(session['stimulations'])==0:
                sessions.append([ 
                    None,
                    session['sample_number'], 
                    session['session_date'], 
                    np.where(subject_names==session['subject_name'])[0][0]+1,
                    None
                ])
            # Session with Stimulations
            else:
                for idx in range(len(session['stimulations'])):
                    sessions.append([ 
                        None,
                        session['sample_number'], 
                        session['session_date'], 
                        np.where(subject_names==session['subject_name'])[0][0]+1,
                        stimulation_idx, 
                    ])
                    stimulation = session['stimulations'][idx]
                    stimulation_spikes = np.array(stimulation['spikes'], dtype=object)
                    stimulations.append([ 
                        None,
                        stimulation['fps'], 
                        stimulation['movie'].tobytes(), 
                        stimulation['n_frames'], 
                        stimulation['pixel_size'], 
                        stimulation['stim_height'], 
                        stimulation['stim_width'], 
                        stimulation['stimulus_onset'], 
                        stimulation['x_block_size'], 
                        stimulation['y_block_size'], 
                        stimulation_spikes.tobytes()
                    ])
                    stimulation_idx += 1

        print("Loading Subject...")
        Subject.insert(subjects)
        print(Subject.fetch())
        print("Loading Stimulations...")
        Stimulation.insert(stimulations)
        print(Stimulation.fetch('stimulation_id', 'fps', 'n_frames', 'pixel_size', 'stimulus_onset'))
        print("Loading Sessions...")
        Session.insert(sessions)
        print(Session.fetch())

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