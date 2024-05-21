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

def get_event_vertex_data_directory():

    current_dir = os.path.dirname(os.path.abspath(__file__))

    print(current_dir)
    
    # Construct the path to the 'event_vertex_data' directory
    event_vertex_dir = os.path.join(current_dir, '..', '..', 'event_vertex_data')

    print(event_vertex_dir)

    return event_vertex_dir


def get_spill_vertex_means_directory():

    current_dir = os.path.dirname(os.path.abspath(__file__))

    print(current_dir)
    
    # Construct the path to the 'event_vertex_data' directory
    spill_vertex_dir = os.path.join(current_dir, '..', '..', 'event_vertex_data')

    print(spill_vertex_dir)

    return spill_vertex_dir

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