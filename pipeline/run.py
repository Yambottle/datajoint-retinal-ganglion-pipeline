import argparse
import configparser
import datajoint as dj
import json
import logging
import traceback

# TODO - logger not working right now
logger = logging.getLogger(__name__)

def test():
    from ingest.experiment import Session, Subject, Stimulation, SpikeGroup, Spike

    print(Subject.describe())
    print(Subject.fetch())
    print(Session.describe())
    print(Session.fetch())
    print(Stimulation.describe())
    print(Stimulation.fetch('stimulation_id'))
    print(Spike.describe())
    print(Spike.fetch('spike_id', 'spike_time', 'spike_movie_time', 'spike_group_id'))

def load(datasource_manifest_path:str):
    """
    Load data

    :param datasource_manifest_path: a JSON file that specify datasource with "type/subtype" and detailed access.
    Prevent confusing terms such as metadata: https://docs.datajoint.io/python/concepts/02-Terminology.html#metadata
    """
    # in-function import after set_config() can set schema dynamically
    import load_utils
    with open(datasource_manifest_path, 'rb') as datasource_json:
        datasources = json.load(datasource_json)
    try:
        for datasource in datasources:
            if datasource['type'] == "file/pickle":
                load_utils.load_file_pickle(datasource)
            # elif datasource['type'] == "file/csv":
            #     load_utils.load_file_csv(datasource)
            # .... extensible for other data source types
    except FileNotFoundError:
        traceback.print_exc()

def build(is_clean:bool):
    """
    Build pipeline, create tables

    :param is_clean: Drop tables or not
    """
    # in-function import after set_config() can set schema dynamically
    from ingest.experiment import Session, Subject, Stimulation, SpikeGroup, Spike
    stimulation = Stimulation()
    stimulation.describe()
    spikegroup = SpikeGroup()
    spikegroup.describe()
    spike = Spike()
    spike.describe()
    subject = Subject()
    subject.describe()
    session = Session()
    session.describe()
    # clean up tables
    if is_clean:
        # TODO - Automation: clean up without cmd manually input yes
        stimulation.drop()
        subject.drop()
        # dropping referenced table will also remove the upper level table, so commented session.drop()
        # session.drop()

def set_config(database:str, user:str, pwd:str):
    """
    Set DataJoint dj.config
    """
    dj.config['database.host'] = database
    dj.config['database.user'] =  user
    dj.config['database.password'] = pwd
    # use dj.config to pass schema name dynamically
    dj.config['schema'] = "{}_retinal".format(user)
    # dj.config['fetch_format'] = 'frame'
    print(dj.config)

def main(args):
    if args.config:
        config = configparser.ConfigParser()
        config.read(args.config)
        set_config(config['DEFAULT']['database'], config['DEFAULT']['user'], config['DEFAULT']['pwd'])
    else:
        set_config(args.database, args.user, args.pwd)
    
    if args.build:
        build(is_clean=args.clean)

    if args.load:
        load(args.load)

    if args.test:
        test()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', default=None, help='DataJoint database config file path')
    parser.add_argument('-db', '--database', default=None, help='DataJoint database host')
    parser.add_argument('-u', '--user', default=None, help='DataJoint database user')
    parser.add_argument('-p', '--pwd', default=None, help='DataJoint database password')
    parser.add_argument('-b', '--build', default=False, action='store_true', help='Build tables')
    parser.add_argument('-cln', '--clean', default=False, action='store_true', help='Drop tables')
    # TODO - any industrial/academic pre-defined common data model schema standard available? 
    # TODO - maybe extend loader's feature to accept universal types from multiple data sources later 
    # such as pickle, csv, JSON file on db or through HTTP request?
    # like an universal loader or importer concept for dj.Imported/dj.Manual
    # TODO - maybe add a loading real-time streaming data feature?
    parser.add_argument('-l', '--load', help='JSON file path: specifies multiple data sources i.e. data_source_manifest.json') 
    parser.add_argument('-t', '--test', default=False, action='store_true', help='Whether or not to run test')
    args = parser.parse_args()
    main(args)