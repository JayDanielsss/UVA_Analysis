# Native Package | os
import os

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

def check_raw_directory():
    try:

        path_to_spinquest_gui = f"{os.getcwd()}/{_SPINQUEST_GUI}"

        if not (os.path.exists(path_to_spinquest_gui)):
            os.mkdir(path_to_spinquest_gui)
        
        if not (os.path.exists(f"{path_to_spinquest_gui}/{_DIRECTORY_DATA}")):
            os.mkdir(f"{path_to_spinquest_gui}/{_DIRECTORY_DATA}")

        if not (os.path.exists(f"{path_to_spinquest_gui}/{_DIRECTORY_DATA}/{_DIRECTORY_DATA_RAW}")):
            os.mkdir(f"{path_to_spinquest_gui}/{_DIRECTORY_DATA}/{_DIRECTORY_DATA_RAW}")
        else:

            print(f"> Path {path_to_spinquest_gui}/{_DIRECTORY_DATA}/{_DIRECTORY_DATA_RAW} exists!")

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

def get_reconstructed_contents():
   
    # Construct the path to the 'reconstructed' directory
    reconstructed_dir = get_reconstructed_directory()

    try:

        contents = os.listdir(reconstructed_dir)

    except FileNotFoundError:

        contents = []
        print(f"The directory {reconstructed_dir} does not exist.")
    
    return contents