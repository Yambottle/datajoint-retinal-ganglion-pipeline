import datajoint as dj

schema = dj.schema(dj.config['schema'], locals())

class Session(dj.Manual):
    pass