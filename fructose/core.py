import requests
import json
import os
import logging

logger = logging.getLogger(__name__)

class Core:
    def __init__(self, folder):
        if not os.path.isfile("config.json"):
            logger.error("Missing config file. Please specify config using \"fructose setup\".")
            exit()
        try:
            with open("config.json") as file:
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
            data["subdirectories"] = [os.path.join(directory, folder) for folder in subdirectories]
            file_data = {}
            for file in files:
                current_path = os.path.join(directory, file)
                base_path = os.path.join(root_top, current_path)
                file_data.setdefault(current_path, open(base_path, "rb"))
            data.setdefault("subdirectories", [])
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
