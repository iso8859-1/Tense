# Updates the mission files from the mission editor

import os
import zipfile
import shutil
from pathlib import Path

def getDCSPath():
    # get the DCS path
    return os.path.join(os.path.expanduser("~"), "Saved Games", "DCS")

def getMissionPath():
    # get the path to the mission folder
    return os.path.join(getDCSPath(), "Missions")

def getTenseDirectory():
    # get the path to the tense directory
    path = Path(os.path.realpath(__file__))
    parent = path.parent.parent.absolute()
    return parent

def unzip_file(zip_filepath, dest_dir):
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        zip_ref.extractall(dest_dir)

def normalize(file):
    # normalized the lua data file given by the file path
    # normalization sorts the tables according to their keys
    # this allows for easier comparison of the files in git
    pass

def main():
    # main
    missionPath = os.path.join(getMissionPath(), "tense_syria.miz")
    destination = os.path.join(getTenseDirectory(), "mission", "syria")
    unzip_file(missionPath, destination)      
    # normalize the lua files
    normalize(os.path.join(destination, "mission"))
    normalize(os.path.join(destination, "options"))
    normalize(os.path.join(destination, "warehouses"))
    normalize(os.path.join(destination, "l10n", "DEFAULT", "dictionary"))
    normalize(os.path.join(destination, "l10n", "DEFAULT", "mapResource"))

if __name__ == "__main__":
    main()  # execute only if run as a script