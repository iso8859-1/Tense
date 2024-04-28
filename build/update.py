# Updates the mission files from the mission editor
import os
from build_utils import getMissionDir, getRepoDirectory, unzip_file
from normalize import normalize



def main():
    # main
    missionPath = os.path.join(getMissionDir(), "tense_syria.miz")
    destination = os.path.join(getRepoDirectory(), "mission", "syria")
    unzip_file(missionPath, destination)      
    # normalize the lua files
    normalize(os.path.join(destination, "mission"))
    normalize(os.path.join(destination, "options"))
    normalize(os.path.join(destination, "warehouses"))
    normalize(os.path.join(destination, "l10n", "DEFAULT", "dictionary"))
    normalize(os.path.join(destination, "l10n", "DEFAULT", "mapResource"))

if __name__ == "__main__":
    main()  # execute only if run as a script