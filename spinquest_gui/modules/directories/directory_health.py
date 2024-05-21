# Native Package | os
import os

if not (os.path.exists("raw")):
    path = os.path.join("raw")
    os.mkdir(path)
    print("> raw directory created, make sure the files from QTracker are sent here\n")

def get_raw_directory():

    current_dir = os.path.dirname(os.path.abspath(__file__))

    print(current_dir)
    
    # Construct the path to the 'raw' directory
    raw_dir = os.path.join(current_dir, '..', '..', 'raw')

    print(raw_dir)

    return raw_dir

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

def get_raw_contents():
   
    # Construct the path to the 'raw' directory
    raw_dir = get_raw_directory()

    try:
        contents = os.listdir(raw_dir)
    except FileNotFoundError:
        contents = []
        print(f"The directory {raw_dir} does not exist.")

    #print(contents)
    
    return contents

