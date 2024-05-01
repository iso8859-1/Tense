import os
import zipfile
import shutil
from pathlib import Path

def get_directories(path):
    return [entry.name for entry in os.scandir(path) if entry.is_dir()]

def is_directory_empty(dir_path):
    with os.scandir(dir_path) as it:
        return not any(True for _ in it)

def getSupportedTheaterList():
    git_mission_dir = os.path.join(getRepoDirectory(), "mission")
    if is_directory_empty(git_mission_dir) or os.path.exists(os.path.join(git_mission_dir, "mission")) == True:
        return []
    else:
        return get_directories(git_mission_dir)

def getMissionName():
    git_dir = os.path.basename(getRepoDirectory())
    if len(getSupportedTheaterList()) == 0:
        return [f"{git_dir}.miz"]
    else: 
        return [f"{git_dir}_{item}.miz" for item in getSupportedTheaterList()]

def getDCSPath():
    # get the DCS path
    return os.path.join(os.path.expanduser("~"), "Saved Games", "DCS")

def getMissionDir():
    # get the path to the mission folder
    return os.path.join(getDCSPath(), "Missions")

def getRepoDirectory():
    # get the path to the tense directory
    path = Path(os.path.realpath(__file__))
    parent = path.parent.parent.absolute()
    return parent

def unzip_file(zip_filepath, dest_dir):
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        zip_ref.extractall(dest_dir)

def remove_file_if_exists(filename):
    if os.path.exists(filename):
        os.remove(filename)

def rename_file(old_name, new_name):
    if os.path.exists(old_name):
        os.rename(old_name, new_name)
    else:
        print(f"The file {old_name} does not exist")

def load_file_into_string(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data

def replace_file_content(file_path, new_content):
    with open(file_path, 'w') as file:
        file.write(new_content)

def zip_mission(mission_dir, destination_filename):
    remove_file_if_exists(destination_filename)
    remove_file_if_exists(destination_filename + ".zip")
    shutil.make_archive(destination_filename, 'zip', mission_dir)
    rename_file(destination_filename + ".zip", destination_filename)
