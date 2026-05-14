import json
import os

DIR_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_path(folder:str, name:str) -> str:
	return os.path.join(DIR_BASE, folder, name)

def file_exists(filename:str):
	return os.path.exists(filename)
