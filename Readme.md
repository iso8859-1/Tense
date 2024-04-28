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

## Scripting

### Dynamic loading of lua files

To be able to edit a `lua` script file while testing the scripts in DCS without the need for re-creating the trigger condition, you can use the `assert(loadfile(..))` trick. To do this, you need to:
- create a trigger condition
- as action, you choose `do_script` (not `do_script_file`)
- place your lua script into the `scripts` folder of the git repo
- you need to enter the following into `Text`: `assert(loadfile("<path to your repo>\scripts\<your script>.lua"))()`
    - replace `<path to your repo>` with the actual path to your repo e.g. `D:\DCS\Missions\Tense` and `<your script>.lua` with the name of your script e.g., `syria.lua`

`update.py` will replace this path with an internal constant when copying the files into the git repo. `build.py` will replace it back to the git repo location (in DEV mode). This ensures that multiple people can work together even if their git repositories are at different absolute paths on disc.