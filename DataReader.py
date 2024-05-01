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
            reco = np.load(filename,allow_pickle=True)
            eventID = reco['arr_0'][33]
            hits = reco['arr_1']

            return eventID, hits
            #return elementid, detectorid
        
        elif self.grab == "MOMENTUM":
            
            filename = self.filenames[self.current_index]
            reco = np.load(filename)
            reco = reco['arr_0']
            px = np.concatenate((reco[:,15][abs(reco[:,15]) < 120],reco[:,18][abs(reco[:,18]) < 120]))
            py = np.concatenate((reco[:,16][abs(reco[:,16]) < 120],reco[:,19][abs(reco[:,19]) < 120]))
            pz = np.concatenate((reco[:,17][abs(reco[:,17]) < 120],reco[:,20][abs(reco[:,20]) < 120]))                
            return px, py, pz, len(py)      

        elif self.grab == "XVERTEX":
            filename = self.filenames[self.current_index]
            reco = np.load(filename)
            reco = reco['arr_0']
            vtx = reco[:,21][reco[:,21]<1e6]
            return vtx
        elif self.grab == "YVERTEX":
            filename = self.filenames[self.current_index]
            reco = np.load(filename)
            reco = reco['arr_0']
            vty = reco[:,22][reco[:,22]<1e6]
            return vty
        elif self.grab == "ZVERTEX":
            filename = self.filenames[self.current_index]
            reco = np.load(filename)
            reco = reco['arr_0']
            vtz = reco[:,23][reco[:,23]<1e6]
            return vtz
        elif self.grab == "EVENT":
            filename = self.filenames[self.current_index]
            reco = np.load(filename)
            reco = reco['arr_0']
            eid = reco[:,33]
            return eid
        elif self.grab == "SPILL":
            filename = self.filenames[self.current_index]
            reco = np.load(filename)
            reco = reco['arr_0']
            sid = reco[:,34]
            return sid      
        
        elif self.grab == "MetaDATA":
            filename = self.filenames[self.current_index]
            reco = np.load(filename)
            reco = reco['arr_0']
            runID = reco[:,32]
            sid = reco[:,34]
            #targetPOS = reco[:,36]
            return runID, sid
            
        else:
            print("DATA NOT SENT!")
    
    def next_file(self):
        self.current_index = (self.current_index + 1) % len(self.filenames)

#For Testing

# import sys
# import os
# filenames = sorted([filename for filename in os.listdir("Reconstructed") if filename.endswith(".npy")])
# data_reader = DataReader([os.path.join("Reconstructed", filename) for filename in filenames],"MetaDATA")
# plot_data = data_reader.read_data()


# print(plot_data)

# hits = plot_data[1]
# detID=np.where(hits[0]==True)[0]
# print(detID[:53])
# event=1
# event = (event + 1) % len(hits)
# print(event)


#import matplotlib.pyplot as plt

#plt.hist(plot_data[0],10)

#plt.show()

#print(np.shape(plot_data[0]))
