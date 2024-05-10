# Updates the mission files from the mission editor
import os
from build_utils import getDCSSavedGamesPath, getRepoDirectory, unzip_file, getMissionName, getSupportedTheaterList
from normalize import normalize

def main():
    # main
    missions = list(zip(getMissionName(), getSupportedTheaterList()))
    for mission, theater in missions:
        missionPath = os.path.join(getDCSSavedGamesPath(), mission)
        destination = os.path.join(getRepoDirectory(), "mission", theater)
        unzip_file(missionPath, destination)      
        # normalize the lua files
        normalize(os.path.join(destination, "mission"))
        normalize(os.path.join(destination, "options"))
        normalize(os.path.join(destination, "warehouses"))
        normalize(os.path.join(destination, "l10n", "DEFAULT", "dictionary"))
        normalize(os.path.join(destination, "l10n", "DEFAULT", "mapResource"))

if __name__ == "__main__":
    main()  # execute only if run as a script