import os
import shutil

def remove_file(folder, file):
    file_exists = os.path.exists(os.path.join(os.getcwd(), folder, file))
    if file_exists:
        try:
            os.remove(folder + "/" + file)
            print("successfully removed file:", folder + "/" + file)
        except Exception as error:
            raise ValueError(error)
        
def remove_directory(folder, directory):
    directory_exists = os.path.isdir(folder + "/" + directory)
    if directory_exists:
        try:
            shutil.rmtree(folder + "/" + directory)
            print("successfully removed directory:", folder + "/" + directory)
        except Exception as error:
            raise ValueError(error)
