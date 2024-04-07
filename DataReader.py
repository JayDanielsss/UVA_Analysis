import numpy as np
import uproot

class DataReader:
    def __init__(self, filenames,grab):
        self.filenames = filenames
        self.current_index = 0

        self.grab = grab

    def read_data(self):
        filename = self.filenames[self.current_index]
        targettree = uproot.open(filename)['QA_ana']

        if self.grab == "VERTEX":
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

            elementid=targettree["elementID"].arrays(library="np")["elementID"]
            detectorid=targettree["detectorID"].arrays(library="np")["detectorID"]

            return elementid, detectorid
        else:
            print("DATA NOT SENT!")
    
    def next_file(self):
        self.current_index = (self.current_index + 1) % len(self.filenames)

