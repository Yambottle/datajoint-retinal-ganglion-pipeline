import datajoint as dj
import numpy as np
import pandas as pd
import pickle
import os
import traceback

from rg_pipeline.ingest.experiment import Session, Stimulation

## This implementation is not able to accept user's customized loading process, since the data's format is not standardized 
# def load(datasource_manifest_path:str):
#     """
#     Load data

#     :param datasource_manifest_path: a JSON file that specify datasource with "type/subtype" and detailed access.
#     Prevent confusing terms such as metadata: https://docs.datajoint.io/python/concepts/02-Terminology.html#metadata
#     """
#     from loader import Loader
#     with open(datasource_manifest_path, 'rb') as datasource_json:
#         datasources = json.load(datasource_json)
#     loader = Loader(datasources)
#     loader.load()


# Batched inserts is better but be careful with buffer size: 
# https://docs.datajoint.io/python/manipulation/1-Insert.html#batched-inserts
class Loader():
    """
    Loader can work with dj pipeline to load different types of data from different data sources

    :param datasources: a list of datasources that parsed from the datasource manifest JSON file
    """

    def __init__(self, datasources:list):
        self.datasources = datasources

    def load(self):
        """
        Act like an abstract function will call a more specific function based on the datasource
        """
        for datasource in self.datasources:
            source_type, sub_type = datasource['type'].split("/")
            # call self.load_sourcetype_subtype(datasource) dynamically depending on data_source_manifest.json
            try:
                # TODO - Security: validating data_source_manifest.json prevents injection
                eval("self.load_{}_{}({})".format(source_type, sub_type, datasource))
            except FileNotFoundError:
                traceback.print_exc()
    
    def load_file_pickle(self, datasource:dict):
        """
        Implementation of load() specifically for pickle files

        :param datasource: a dictionary including pickle file path
        """
        if os.path.exists(datasource['path']):
            with open(datasource['path'], 'rb') as datafile:
                data = pickle.load(datafile)
            print(data[0].keys())
            # TODO - insert pandas dataframe not included in the documentation 
            # https://docs.datajoint.io/python/manipulation/1-Insert.html#insert

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