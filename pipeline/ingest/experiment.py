import datajoint as dj

schema = dj.schema(dj.config['schema'], locals())

@schema
class Stimulation(dj.Manual):
    definition = """
    # represent a stimulation during a experimental session
    stimulation_id: int # unique stimulation id
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
    spikes: longblob # a list of spike times for recorded retinal neurons.
    """

@schema
class Session(dj.Manual):
    definition = """
    # represent a single experimental session with a sample of mouse retina
    sample_number: int # unique sample id
    ->Stimulation
    ---
    subject_name: varchar(50) # experimental subject's name
    session_date: date # experiment date
    """