import numpy as np
import uproot

class DataReader:
    def __init__(self, filenames,grab):
        self.filenames = filenames
        self.current_index = 0

        self.grab = grab

    def read_data(self):
        

        if self.grab == "VERTEX":
            filename = self.filenames[self.current_index]
            targettree = uproot.open(filename)['QA_ana']
            gvx = targettree['gvx'].arrays(library='np')['gvx']
            gvy = targettree['gvy'].arrays(library='np')['gvy']
            gvz = targettree['gvz'].arrays(library='np')['gvz']

            vtx0 = [sublist[0] for sublist in gvx]
            vtx1 = [sublist[1] for sublist in gvx]
            vty0 = [sublist[0] for sublist in gvy]
            vty1 = [sublist[1] for sublist in gvy]
            vtz0 = [sublist[0] for sublist in gvz]
            vtz1 = [sublist[1] for sublist in gvz]

            vtx_data = np.array([vtx0, vtx1, vty0, vty1, vtz0, vtz1]).T
            
            return vtx_data
        elif self.grab == "HIT":
            filename = self.filenames[self.current_index]
            targettree = uproot.open(filename)['QA_ana']
            elementid=targettree["elementID"].arrays(library="np")["elementID"]
            detectorid=targettree["detectorID"].arrays(library="np")["detectorID"]
            mask = elementid < 300
            elementid = np.where(mask, elementid, 0)
            mask = detectorid < 300
            detectorid = np.where(mask, detectorid, 0)
            
            return elementid, detectorid
        
        elif self.grab == "MOMENTUM":
            
            filename = self.filenames[self.current_index]
            reco = np.load(filename)
            print(filename)
            px = np.concatenate((reco[15][reco[15] < 1e6],reco[18][reco[18] < 1e6]))
            py = np.concatenate((reco[16][reco[16] < 1e6],reco[19][reco[19] < 1e6]))
            pz = np.concatenate((reco[17][reco[17] < 1e6],reco[20][reco[20] < 1e6]))                   
            return px, py, pz            
            
        else:
            print("DATA NOT SENT!")
    
    def next_file(self):
        self.current_index = (self.current_index + 1) % len(self.filenames)

#For Testing

# import sys
# import os
# filenames = sorted([filename for filename in os.listdir("Data") if filename.endswith(".root")])
# data_reader = DataReader([os.path.join("Data", filename) for filename in filenames],"HIT")
# plot_data = data_reader.read_data()

# import matplotlib.pyplot as plt

# #plt.hist(plot_data[0],10)

# #plt.show()

# print(np.shape(plot_data[0]))
