import os


def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        print("Creating directory {}".format(directory))
        os.makedirs(directory)
    return
