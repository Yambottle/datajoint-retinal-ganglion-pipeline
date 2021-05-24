import datajoint as dj

schema = dj.schema(dj.config['schema'], locals())

@schema
class Stimulation(dj.Manual):
    definition = """
    # represent a stimulation during a experiment session
    stimulation_id: int auto_increment # unique stimulation id
    ---
    fps: float # movie frequency: frame per second
    movie: longblob # movie numpy array: The array is shaped as (horizontal blocks, vertical blocks, frames).
    n_frames: int # the number of frames in the movie
    pixel_size: float # pixel size on the retina in um/pixel
    stim_height: int # the height of the stimulus (movie) in pixels
    stim_width: int # the width of the stimulus (movie) in pixels
    stimulus_onset: float # onset of the stimulus from the beginning of the recording session in seconds
    x_block_size: int # size of x (horizontal) blocks in pixels
    y_block_size: int # size of y (vertical) blocks in pixels
    """

@schema
class SpikeGroup(dj.Manual):
    # TODO - maybe call it SpikeGroup of a retinal neuron?
    definition = """
    # represent a group of spike records from a stimulation
    spike_group_id: int auto_increment # unique spike group id
    ---
    ->Stimulation
    """

@schema
class Spike(dj.Manual):
    definition = """
    # represent a spike records from a spike group
    spike_id: int auto_increment # unique spike group id
    ---
    spike_time: float # spike time recorded from the beginning of the session
    spike_movie_time: float # spike time excludes stimulus onset, recorded from the beginning of the movie
    ->SpikeGroup
    """

@schema
class Subject(dj.Manual):
    definition = """
    # represent a subject that will be used in an experiment
    subject_id: int auto_increment # unique subject id
    ---
    subject_name: varchar(50) # experimental subject's name
    """

@schema
class Session(dj.Manual):
    definition = """
    # represent a single experimental session with a sample of mouse retina
    session_id: int auto_increment # unique sample id
    ---
    sample_number: int # sample number
    session_date: date # experiment date
    ->Subject
    ->[nullable] Stimulation
    """
    # subject_name: varchar(50) # experimental subject's name