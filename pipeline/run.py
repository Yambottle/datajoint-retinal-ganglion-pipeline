import argparse
import configparser
import datajoint as dj
import json

def load(metadata_path:str):
    from loader import Loader
    with open(metadata_path, 'rb') as meta_json:
        metadata = json.load(meta_json)
    loader = Loader(metadata)
    loader.load()

def build(is_clean:bool):
    # in-function import after set_config() can set schema dynamically
    from ingest.experiment import Session, Stimulation
    stimulation = Stimulation()
    stimulation.describe()
    session = Session()
    session.describe()
    # clean up tables
    if is_clean:
        # TODO - Automation: clean up without cmd manually input yes
        # dropping referenced table will also remove the upper level table, so commented session.drop()
        stimulation.drop()
        # session.drop()

def set_config(database:str, user:str, pwd:str):
    dj.config['database.host'] = database
    dj.config['database.user'] =  user
    dj.config['database.password'] = pwd
    # use dj.config to pass schema name dynamically
    dj.config['schema'] = "{}_retinal".format(user)

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', default=None, help='DataJoint database config file path')
    parser.add_argument('-db', '--database', default=None, help='DataJoint database host')
    parser.add_argument('-u', '--user', default=None, help='DataJoint database user')
    parser.add_argument('-p', '--pwd', default=None, help='DataJoint database password')
    parser.add_argument('-b', '--build', default=False, action='store_true', help='Build tables')
    parser.add_argument('-cln', '--clean', default=False, action='store_true', help='Drop tables')
    # TODO - maybe extend load feature to accept universal types from multiple data sources later 
    # such as pickle, csv, JSON file on db or through HTTP request?
    parser.add_argument('-l', '--load', help='JSON file path: Metadata of data source i.e. metadata.json')
    # TODO - maybe add a stream loading feature? 
    args = parser.parse_args()
    main(args)