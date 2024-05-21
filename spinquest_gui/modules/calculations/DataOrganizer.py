# Made by Jay for Organizing and pulling modified QTracker into Gui

import numpy as np
import os
import sys
import uproot
from QTracker import QTracker

import time

class DataOrganizer:
    
    def __init__(self):
        
        self.reco = None
        self.hits = None
        self.target_track = None
        self.metadata = None
        self.detectorid = None
        self.elementid = None
        
        
        
    def organizeData(self):
        #finds the raw file
        raw_files = [os.path.join("Raw", f) for f in os.listdir("Raw") if os.path.isfile(os.path.join("Raw", f))]
        #sort by order of time mod
        raw_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)


        most_recent_raw_file = raw_files[0]


        #Do the same for the TSV file here

        #Pull information from QTracker
        predictions, filt, self.hits, drift,self.metadata, root_file, self.detectorid, self.elementid = QTracker.prediction(most_recent_raw_file)
        
        #Filter hits and tracks write output
        if(len(self.hits) > 0):
            self.reco, self.hits, self.target_track = QTracker.tracker(predictions, filt, self.hits, drift,self.metadata, root_file)

            self.sid = self.reco[:,34]
            self.EventID = self.reco[:,33]
            targetTrackProbabilty = self.reco[:,31]
            dumpTrackProbabilty = self.reco[:,30]

            #self.mom = self.reco[15:21][abs(self.reco[15:21]) < 120]
        
            sub_array = self.reco[15:21]
            self.mom = np.where(abs(sub_array) < 120, sub_array, 0)
            #self.mom = np.reshape[]
            #self.mom = self.mom.reshape(-1,6)
            # px_mup = self.reco[15][abs(self.reco[15]) < 120]
            # py_mup = self.reco[16][abs(self.reco[16]) < 120]
            # pz_mup = self.reco[17][abs(self.reco[17]) < 120]

            # px_mum = self.reco[18][abs(self.reco[18]) < 120]
            # py_mum = self.reco[19][abs(self.reco[19]) < 120]
            # pz_mum = self.reco[20][abs(self.reco[20]) < 120]

            # self.px = np.column_stack((px_mup,px_mum))
            # self.py = np.column_stack((py_mup,py_mum))
            # self.pz = np.column_stack((pz_mup,pz_mum))
            
            
            
            
            
            # self.px = np.concatenate((self.reco[15][abs(self.reco[15]) < 120],self.reco[18][abs(self.reco[18]) < 120]))
            # self.py = np.concatenate((self.reco[16][abs(self.reco[16]) < 120],self.reco[19][abs(self.reco[19]) < 120]))
            # self.pz = np.concatenate((self.reco[17][abs(self.reco[17]) < 120],self.reco[20][abs(self.reco[20]) < 120])) 

            self.vtx = self.reco[:,21][self.reco[:,21]<1e6]
            self.vty = self.reco[:,22][self.reco[:,22]<1e6]
            self.vtz = self.reco[:,23][self.reco[:,23]<1e6]

            probabilityTargetDimu = targetTrackProbabilty>=.9
            probabilityDumpDimu = dumpTrackProbabilty<=.001
            targetDimuIndex =   np.where(probabilityTargetDimu & probabilityDumpDimu)
            self.selectedEvents = self.EventID[targetDimuIndex]

            #clean memory?

            #return sid, EventID,selectedEvents, px, py, pz, vtx, vty, vtz, self.hits, self.target_track, self.elementid, self.detectorid

            

            
        else:
            print("No events meeting dimuon criteria.")  # If no events pass the filter, notify the user.
        

    def grab_Vertex(self):
        return self.vtx, self.vty, self.vtz, self.sid, self.EventID
    
    def grab_HitInfo(self):
        return self.elementid, self.detectorid, self.selectedEvents, self.sid, self.hits, self.EventID, self.target_track
    def grab_mom(self):
        return self.mom
    

# #Testing
# t0 = time.time()
#  #Create an instance of dataOrganizer
# organizer = dataOrganizer()

# # Call the organizeData() method to populate the necessary attributes
# organizer.organizeData()

# # Call the organizeData() method on the instance

# vtx, vty, vtz, sid, eventID = organizer.grab_Vertex()
# print(sid)
# t1 = time.time()

# total = t1 - t0
# print(total)



