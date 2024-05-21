# Native Package | os
import os

if not (os.path.exists("reconstructed")):
    path = os.path.join("reconstructed")
    os.mkdir(path)
    print("> reconstructed directory created, make sure the files from QTracker are sent here\n")

def get_reconstructed_directory():

    current_dir = os.path.dirname(os.path.abspath(__file__))

    print(current_dir)
    
    # Construct the path to the 'reconstructed' directory
    reconstructed_dir = os.path.join(current_dir, '..', '..', 'reconstructed')

    print(reconstructed_dir)

    return reconstructed_dir

def get_reconstructed_contents():
   
    # Construct the path to the 'reconstructed' directory
    reconstructed_dir = get_reconstructed_directory()

    try:
        contents = os.listdir(reconstructed_dir)
    except FileNotFoundError:
        contents = []
        print(f"The directory {reconstructed_dir} does not exist.")

    print(contents)
    
    return contents