import yaml
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import CutsomException
import os,sys
import numpy as np
import dill
import pickle

def read_yml_file(file_path: str) -> dict:
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CutsomException(e,sys)
    

def write_yml_file(file_path: str, contant: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(contant, file)
    except Exception as e:
        raise CutsomException(e, sys)