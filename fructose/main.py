import logging
import argparse
import json
import os

from fructose.core import Core

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(): 
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="subcommand", dest="subcommand", required=True)
    sync_parser = subparsers.add_parser("sync", help="sync distributions with remote server")
    sync_parser.add_argument("folder", type=str, help="path to folder of distributions")
    setup_parser = subparsers.add_parser("setup", help="setup remote path and password")
    setup_parser.add_argument("remote", type=str, help="url path of the server")
    setup_parser.add_argument("password", type=str, help="password for backend access")
    subparsers.add_parser("reset", help="remove current configurations")
    args = parser.parse_args()
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    if args.subcommand == "setup":
        config = {
            "remote": args.remote,
            "password": args.password
        }
        with open(config_path, "w") as file:
            json.dump(config, file)
    elif args.subcommand == "sync": 
        if not os.path.isdir(args.folder): 
            logger.error(f"\"{args.folder}\" is an invalid folder path.")
            return
        core = Core(args.folder)
        core.ping()
        core.sync()
        logger.info("Successfully synced distributions.")
    elif args.subcommand == "reset":
        if os.path.isfile(config_path):
            os.unlink(config_path)

if __name__ == "__main__":
    main()
