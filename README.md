# SpinQuest GUI Application

This is the GUI application that will run for the SpinQuest Experiment at Fermilab.

## Directory Structure
```
gui/
|-- main.py
|-- app/
    |-- data/
        |-- networks/
          |-- event_filter
          |-- Track_Finder_All
          |-- Reconstruction_All
          |-- Vertexing_All/
          |-- Track_Finder_Z/
          |-- Reconstruction_Z
          |-- Vertexing_Z
          |-- Track_Finder_Target
          |-- Reconstruction_Target
          |-- target_dump_filter
        |-- raw/
          |-- data1.root
          |-- data2.root
          |-- ...
        |-- reconstructed
          |-- recon1.npz
          |-- recon2.npz
          |-- ...
    |-- tabs/
        |-- tab1.py
        |-- tab2.py
    |-- modules/
        |-- calc.py
        |-- HitDisplay.py
        |-- ...
```

## Technical Information

### Tab1:

Tab1 includes HitDisplay only.

### QTracker:

We use this for reconstruction. It involves some TF models. These 10 models are already trained, and you will need to download them before you run the application otherwise things will explode.

