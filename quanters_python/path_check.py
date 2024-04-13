import os

def isPath(path):
    if not os.path.exists(path):
        os.makedirs(path)