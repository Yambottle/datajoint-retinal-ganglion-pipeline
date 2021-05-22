import datajoint as dj
import numpy as np
import pandas as pd
import pickle
import os
import traceback

from ingest.experiment import Session, Stimulation

class Loader():
    def __init__(self, metadata:str):
        self.metadata = metadata

    def load(self):
        for datasource in self.metadata:
            source_type, sub_type = datasource['type'].split("/")
            # call self.load_sourcetype_subtype(datasource) dynamically depending on metadata.json
            try:
                eval("self.load_{}_{}({})".format(source_type, sub_type, datasource))
            except FileNotFoundError:
                traceback.print_exc()
    
    def load_file_pickle(self, datasource:dict):
        if os.path.exists(datasource['path']):
            with open(datasource['path'], 'rb') as datafile:
                data = pickle.load(datafile)
            print(data[0].keys())
        else:
            raise FileNotFoundError

    # TODO - since these data sources are not required in this specific task, ignore implementation for now
    def load_file_csv(self, datasource:dict):
        pass

    def load_file_parquet(self, datasource:dict):
        pass

    def load_file_json(self, datasource:dict):
        pass

    def load_database_mysql(self, datasource:dict):
        pass

    def load_database_mssql(self, datasource:dict):
        pass

    def load_database_mongodb(self, datasource:dict):
        pass

    def load_request_json(self, datasource:dict):
        pass