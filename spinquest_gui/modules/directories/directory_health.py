# Native Package | os
import os
import glob

from spinquest_gui.statics.constants import _DIRECTORY_DATA, _DIRECTORY_DATA_RAW, _DIRECTORY_DATA_RECONSTRUCTED, _SPINQUEST_GUI

def check_reconstructed_directory():
    
    try:

        path_to_spinquest_gui = f"{os.getcwd()}/{_SPINQUEST_GUI}"

        if not (os.path.exists(path_to_spinquest_gui)):
            os.mkdir(path_to_spinquest_gui)
        
        if not (os.path.exists(f"{path_to_spinquest_gui}/{_DIRECTORY_DATA}")):
            os.mkdir(f"{path_to_spinquest_gui}/{_DIRECTORY_DATA}")

        if not (os.path.exists(f"{path_to_spinquest_gui}/{_DIRECTORY_DATA}/{_DIRECTORY_DATA_RECONSTRUCTED}")):
            os.mkdir(f"{path_to_spinquest_gui}/{_DIRECTORY_DATA}/{_DIRECTORY_DATA_RECONSTRUCTED}")

        else:

            print(f"> Path {path_to_spinquest_gui}/{_DIRECTORY_DATA}/{_DIRECTORY_DATA_RECONSTRUCTED} exists!")

    except Exception as ERROR:
        print(f"> [ERROR]: {ERROR}")

def get_raw_directory():
    """
    ALl this function does is it references/finds the
    directory 
    /spinguest_gui/data/raw/
    """

    # Construct the path to the 'raw' directory

    path_to_spinquest_gui = f"{os.getcwd()}/{_SPINQUEST_GUI}"
    current_dir = f"{path_to_spinquest_gui}/{_DIRECTORY_DATA}/{_DIRECTORY_DATA_RAW}"


    return current_dir

def get_reconstructed_directory():
    """
    ALl this function does is it references/finds the
    directory 
    /spinguest_gui/data/reconstructed/
    """

    # Construct the path to the 'reconstructed' directory

    path_to_spinquest_gui = f"{os.getcwd()}/{_SPINQUEST_GUI}"
    current_dir = f"{path_to_spinquest_gui}/{_DIRECTORY_DATA}/{_DIRECTORY_DATA_RECONSTRUCTED}"


    return current_dir

def get_raw_contents():
   
    # Construct the path to the 'raw' directory
    raw_dir = get_raw_directory()

    try:
         #finds the raw file
        # List all files in the directory
        contents = glob.glob(os.path.join(raw_dir, '*'))

        # Sort files by modification time, most recent first
        contents.sort(key=os.path.getmtime, reverse=True)


        # contents = os.listdir(raw_dir)
        # contents.sort(key=lambda x: os.path.getmtime(x), reverse=True)


    except FileNotFoundError:

        contents = []
        print(f"The directory {raw_dir} does not exist.")
    
    return contents

