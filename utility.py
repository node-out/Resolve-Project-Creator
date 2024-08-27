import pickle
import pathlib
import shutil

# Save file
def save_paths_file(folder_dictionary):
    check_file = pathlib.Path("paths.txt")
    if check_file.is_file():
        with open('paths.txt', 'wb') as f:
                pickle.dump(folder_dictionary, f)
    else:
        with open('paths.txt', 'wb') as f:
            pickle.dump(folder_dictionary, f)
        f = open("paths.txt", "x")
        f.close()

def load_paths_file():
    check_file = pathlib.Path("paths.txt")
    if check_file.is_file():
        with open('paths.txt', 'rb') as f:
            paths = pickle.load(f)
        return paths

# Create Directories from Template Folder
def directorys_from_template(projects_folder_root, database_name, project_name):
    source = pathlib.Path(f"{projects_folder_root}/template")
    destination = pathlib.Path(f"{projects_folder_root}/{database_name}/{project_name}")
    shutil.copytree(source, destination)