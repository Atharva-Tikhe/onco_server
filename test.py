import os

class GetAllFiles:
    def __init__(self) -> None:
        pass

    def getFiles(self, path: str) -> dict:
        dir_tree = {}
        for root, d_names, f_names in os.walk(f'{path}', topdown=True):
            if len(d_names) > 0:
                dir_tree[root] = d_names
            else:
                dir_tree[root] = f_names
        return dir_tree


