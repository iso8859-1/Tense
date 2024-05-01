# script that builds a MIZ file from the scritps and mission folder
# Release Mode: embeds the scripts into the mission file
# Dev Mode: loads the scripts via assert to allow modification without rebuilding the mission file
import os
import shutil
from build_utils import getMissionDir, zip_mission, getRepoDirectory, load_file_into_string, replace_file_content, getMissionName, getSupportedTheaterList

def replace_git_repo_scripts_location(filename):
    content = load_file_into_string(filename)
    scripts_dir = os.path.join(getRepoDirectory(), "scripts")
    scripts_dir = scripts_dir.replace("\\", "\\\\\\\\")
    content = content.replace("{git_repo_scripts_location_text}", scripts_dir)
    scripts_dir = scripts_dir.replace("\\", "\\\\")
    content = content.replace("{git_repo_scripts_location}", scripts_dir)
    replace_file_content(filename, content)

def copy_to_temp(mission_dir):
    
    destination_dir = os.path.join(getRepoDirectory(), "temp")

    # Remove the destination directory if it exists
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)

    # Copy the source directory to the destination directory
    shutil.copytree(mission_dir, destination_dir)

def main():
    # main
    temp = os.path.join(getRepoDirectory(), "temp")
    missions = list(zip(getMissionName(), getSupportedTheaterList()))
    for mission, theater in missions:
        destination = os.path.join(getMissionDir(), mission)
        source_dir = os.path.join(getRepoDirectory(), "mission", theater)
        copy_to_temp(source_dir)
        # normalize the lua files
        replace_git_repo_scripts_location(os.path.join(temp, "mission"))
        replace_git_repo_scripts_location(os.path.join(temp, "options"))
        replace_git_repo_scripts_location(os.path.join(temp, "warehouses"))
        replace_git_repo_scripts_location(os.path.join(temp, "l10n", "DEFAULT", "dictionary"))
        replace_git_repo_scripts_location(os.path.join(temp, "l10n", "DEFAULT", "mapResource"))
        zip_mission(temp, destination)

if __name__ == "__main__":
    main()  # execute only if run as a script