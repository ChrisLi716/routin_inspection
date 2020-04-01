import os


def create_file_if_not_exist(file_path_name):
    (file_path, file_name) = os.path.split(file_path_name)
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    if not os.path.exists(file_path_name):
        open(file_path_name, "x")
