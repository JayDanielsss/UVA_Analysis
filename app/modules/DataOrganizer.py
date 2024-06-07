# Made by Jay for Organizing and pulling modified QTracker into Gui

# Native Package | os
import os

# Native Package | glob
import glob

# External Packages | NumPy
import numpy as np

# Modules | Directories
from app.modules.QTracker import QTracker

class DataOrganizer:
    
    def __init__(self):
        
        self.reco = None
        self.hits = None
        self.target_track = None
        self.metadata = None
        self.detectorid = None
        self.elementid = None

        # Get the directory of the current file
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

        # Get the parent directory of the current directory
        self.parent_dir = os.path.dirname(self.current_dir)

        
        
    def get_raw_contents(self):
        """
        # Description:
        All we do here is organize the relevant data and
        store it in the class.

        # Parameters:
        
        None

        # Returns:

        None -- remember this!
        """

        path_to_raw_directory = os.path.join("app/data/raw")

        try:
            #finds the raw file
            # List all files in the directory
            contents = glob.glob(os.path.join(path_to_raw_directory, '*'))

            # Sort files by modification time, most recent first
            contents.sort(key=os.path.getmtime, reverse=True)

        except FileNotFoundError:

            contents = []
            print(f"The directory {path_to_raw_directory} does not exist or no files in raw/")
        
        return contents

    def organizeData(self):
        """
        # Description:
        All we do here is organize the relevant data and
        store it in the class.

        # Parameters:
        
        None

        # Returns:

        None -- remember this!
        """

        #finds the raw file
        raw_files = self.get_raw_contents()

        # Get the most recent file path
        if raw_files:
            most_recent_raw_file = raw_files[0]
            #print("Most recent file:", most_recent_raw_file)
        else:
            most_recent_raw_file = None
            #print("The directory is empty")

        #Do the same for the TSV file here

        #Pull information from QTracker
        predictions, filt, self.hits, drift,self.metadata, root_file, self.detectorid, self.elementid = QTracker.prediction(most_recent_raw_file,self.parent_dir)
        
        #Filter hits and tracks write output
        if(len(self.hits) > 0):
            self.reco, self.hits, self.target_track = QTracker.tracker(predictions, filt, self.hits, drift,self.metadata, root_file,self.parent_dir)

            self.sid = self.reco[:,34]
            self.rid = self.reco[:,32]
            self.EventID = self.reco[:,33]
            targetTrackProbabilty = self.reco[:,31]
            dumpTrackProbabilty = self.reco[:,30]
        
            sub_array = self.reco[15:21]
            self.mom = np.where(abs(sub_array) < 120, sub_array, 0)
            self.mom =self.mom.T

            self.vtx = self.reco[:,21][self.reco[:,21]<1e6]
            self.vty = self.reco[:,22][self.reco[:,22]<1e6]
            self.vtz = self.reco[:,23][self.reco[:,23]<1e6]

            probabilityTargetDimu = targetTrackProbabilty>=.9
            probabilityDumpDimu = dumpTrackProbabilty<=.001
            targetDimuIndex =   np.where(probabilityTargetDimu & probabilityDumpDimu)
            self.selectedEvents = self.EventID[targetDimuIndex]

        else:

            print("No events meeting dimuon criteria.")  # If no events pass the filter, notify the user.
        

    def grab_Vertex(self):
        """
        # Description:
        Once organizeData() has been run, we use
        this modular function to obtain vertex information.

        # Parmeters:
        
        None

        # Returns:

        vtx: Any
        vty: Any
        vtz: Any
        sid: Any
        EventID: Any

        """

        return self.vtx, self.vty, self.vtz, self.sid, self.EventID
    
    def grab_HitInfo(self):
        """
        # Description:
        Once organizeData() has been run, we use
        this modular function to obtain hit information.

        # Parmeters:
        
        None

        # Returns

        elementid: Any
        detectorid: Any
        selectedEvents: Any
        sid: Any
        hits: Any
        EventID: Any
        target_track: Any

        """

        return self.elementid, self.detectorid, self.selectedEvents, self.sid, self.hits, self.EventID, self.target_track
    
    def grab_mom(self):
        """
        # Description:
        Once organizeData() has been run, we use
        this modular function to obtain momentum information.

        # Parmeters:
        
        None

        # Returns:

        mom: Any

        """
    
        return self.mom, self.sid, self.selectedEvents
    
    def grab_meta(self):
        """
        # Description:
        Once organizeData() has been run, we use
        this modular function to obtain sID and something
        called ridOn

        # Parmeters:
        
        None

        # Returns:

        sid: Any
        ridOn: Any

        """
    
        return self.sid, self.rid



