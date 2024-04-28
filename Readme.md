# Tense

This is planned to be a single mission dynamic campaign based on the ideas of Pretense.

## Development Workflow

### Prerequisites

To use the build tools, you need 
- `Python 3` with 
- `lrparsing` installed (`pip install lrparsing`)

### Workflow

0. check-out the git repo
1. build the mission by calling `build.py`. It will place the mission in your `Saved Games\DCS\Mission` folder.
2. open DCS Mission editor and start editing the mission.
3. at any time during your editing, you can save your current progress and transfer it to git by calling `update.py`. This will unzip and copy the files of the mission into the git repo. It does some normalizing to reduce the number of unintended changes in that process. You can then commit it to git.