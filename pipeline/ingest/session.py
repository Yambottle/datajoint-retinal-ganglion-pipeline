import datajoint as dj

schema = dj.schema(dj.config['schema'], locals())

@schema
class Session(dj.Manual):
    definition = """
    # represent a single experimental session with a sample of mouse retina
    sample_number: int # unique sample id
    ---
    subject_name: varchar(50) # experimental subject's name
    session_date: date # experiment date
    stimulation_id: int # reference id of a stimulation
    """