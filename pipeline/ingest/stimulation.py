import datajoint as dj

schema = dj.schema(dj.config['schema'], locals())

@schema
class Stimulation(dj.Manual):
    description = """
    # represent a stimulation during a experimental session
    stimulation_id: int # unique stimulation id
    ---
    fps: float # movie frequency: frame per second
    movie: 

    """