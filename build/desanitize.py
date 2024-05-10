import os
import shutil
import stat
import logging
from build_utils import getDCSInstallationPath

def desanitize():
    # Sanitizing MissionScripting.lua
    filename = os.path.join(getDCSInstallationPath(), 'Scripts', 'MissionScripting.lua')
    try:
        os.chmod(filename, stat.S_IWUSR)
    except PermissionError:
        logging.error(f"Can't desanitize {filename}, no write permissions!")
        raise
    backup = filename.replace('.lua', '.bak')
    try:
        with open(filename, mode='r', encoding='utf-8') as infile:
            orig = infile.readlines()
        output = []
        dirty = False
        for line in orig:
            if line.lstrip().startswith('--'):
                output.append(line)
                continue
            if "sanitizeModule('io')" in line or "sanitizeModule('lfs')" in line:
                line = line.replace('sanitizeModule', '--sanitizeModule')
                dirty = True
            # This is currently not needed, but might be in the future    
            # elif "_G['require'] = nil" in line or "_G['package'] = nil" in line:
            #     line = line.replace('_G', '--_G')
            #     dirty = True
            # elif "require = nil" in line:
            #     line = line.replace('require', '--require')
            #     dirty = True
            output.append(line)
        if dirty:
            logging.info(f'- Desanitizing {filename}')
            # backup original file
            shutil.copyfile(filename, backup)
            with open(filename, mode='w', encoding='utf-8') as outfile:
                outfile.writelines(output)
    except (OSError, IOError) as e:
        logging.error(f"Can't access {filename}. Make sure, the file is writable.")
        raise e
    
desanitize()