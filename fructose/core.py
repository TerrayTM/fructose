import requests
import json
import os
import logging

logger = logging.getLogger(__name__)

class Core:
    def __init__(self, folder):
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        if not os.path.isfile(config_path):
            logger.error("Missing config file. Please specify config using \"fructose setup\".")
            exit()
        try:
            with open(config_path) as file:
                config = json.load(file)
                self._url = config["remote"]
                self._password = config["password"]
        except Exception:
            logger.error("Bad config file. Please try \"fructose setup\".")
            exit()
        self._folder = folder
    
    def ping(self):
        try:
            response = requests.post(self._url, {
                "password": self._password,
                "action": "ping"
            })
            response = response.json()
            if not response["success"] == "true":
                raise Exception()
        except Exception:
            logger.error("Server is offline.")
            exit()

    def sync(self):
        is_top = True
        root_top = None
        for root, subdirectories, files in os.walk(self._folder):
            data = {}
            directory = None
            if is_top:
                root_top = root
                is_top = False
                directory = "" 
            else:
                directory  = os.path.relpath(root, root_top)
            file_data = {}
            file_paths = []
            for index, file in enumerate(files):
                current_path = os.path.join(directory, file)
                base_path = os.path.join(root_top, current_path)
                file_data.setdefault(str(index), open(base_path, "rb"))
                file_paths.append(current_path.replace(os.sep, "/"))
            data.setdefault("subdirectories", [os.path.join(directory, folder).replace(os.sep, "/") for folder in subdirectories])
            data.setdefault("paths", file_paths)
            try: 
                response = requests.post(self._url, {
                    "password": self._password,
                    "action": "sync",
                    "data": json.dumps(data)
                }, files=file_data)
                response = response.json()
                if not response["success"] == "true":
                    raise Exception()
            except Exception:
                logger.error("An unknown error has occurred.")
                exit()
