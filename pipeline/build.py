import argparse
import configparser
import datajoint as dj

def build():
    dj.conn()

def set_config(database:str, user:str, pwd:str):
    dj.config['database.host'] = database
    dj.config['database.user'] =  user
    dj.config['database.password'] = pwd

def main(args):
    if args.config:
        config = configparser.ConfigParser()
        config.read(args.config)
        set_config(config['DEFAULT']['database'], config['DEFAULT']['user'], config['DEFAULT']['pwd'])
    else:
        set_config(args.database, args.user, args.pwd)
    
    build()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', default=None, help='DataJoint database config file path')
    parser.add_argument('-db', '--database', default=None, help='DataJoint database host')
    parser.add_argument('-u', '--user', default=None, help='DataJoint database user')
    parser.add_argument('-p', '--pwd', default=None, help='DataJoint database password')
    args = parser.parse_args()
    main(args)