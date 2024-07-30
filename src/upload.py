import shutil
import shutil
from respond import initialize_chat_engine
import os


def upload_file(file_path):
    destination = f"./data/{os.path.basename(file_path)}"
    shutil.copy(file_path, destination)
    initialize_chat_engine()
    return destination
