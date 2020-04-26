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
    args = parser.parse_args()
    if args.subcommand == "setup":
        config = {
            "remote": args.remote,
            "password": args.password
        }
        with open("config.json", "w") as file:
            json.dump(config, file)
    elif args.subcommand == "sync": 
        if not os.path.isdir(args.folder): 
            logger.error(f"\"{args.folder}\" is an invalid folder path.")
            return
        core = Core(args.folder)
        core.ping()
        core.sync()
        logger.info("Successfully synced distributions.")

if __name__ == "__main__":
    main()
