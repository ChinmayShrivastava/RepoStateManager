import os
import json

def map_repo(dir_map, data_dir, ignore):
    _dirmap = {}
    i = 0
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            filename = os.path.join(root, file)
            cont = False
            for i in ignore:
                if i in filename:
                    cont = True
                    break
            if cont:
                continue
            # add to the dirmap
            _dirmap[i] = filename
            i += 1
    # export the _dirmap into the dir_map file
    with open(dir_map, 'w') as f:
        json.dump(_dirmap, f)
    return _dirmap