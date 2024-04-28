# script that builds a MIZ file from the scritps and mission folder
# Release Mode: embeds the scripts into the mission file
# Dev Mode: loads the scripts via assert to allow modification without rebuilding the mission file
import os
from build_utils import getMissionDir, zip_mission, getRepoDirectory

def main():
    # main
    source = os.path.join(getRepoDirectory(), "mission", "syria")
    destination = os.path.join(getMissionDir(), "tense_syria.miz")
    zip_mission(source, destination)

if __name__ == "__main__":
    main()  # execute only if run as a script