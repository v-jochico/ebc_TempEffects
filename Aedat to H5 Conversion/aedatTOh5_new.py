from dv import AedatFile
import numpy as np
import scipy.io as sio
import h5py

# Input File Location
file_path = 'D:\\Documents\\Summer Scholarship\\Event-Based-HDF5-Video-Renderer-master\\HDF5 Converter\\Uncooled Cam Dark Setting\\Cooled Cam Dark\\0 Degrees Ambient\\dvSave-2020_01_28_11_52_15.aedat4'

# An empty list for data to be stored later
events_x=[]
events_y=[]
events_p=[]
events_ts=[]

with AedatFile(file_path) as f:
    # list all the names of streams in the file
            print(f.names)
    
    # loop through the "events" stream
    for e in f['events']:
        # Check For polarity data, if true == 1, if false == -1
        if e.polarity == True:
            events_3=1
        else:
            events_3=-1
        # Save data from "events" stream to a list
        events_x.append(e.x)
        events_y.append(e.y)
        events_p.append(events_3)
        events_ts.append(e.timestamp)
    # Storing the first row of events_ts as a variable
    timestamp_start = (events_ts[0])
    # Calculating the difference of all the rows of events_ts with timestamp_start and creating a new list
    timestamp=[x-timestamp_start for x in events_ts]
    # Finds lenght of the events_x list
    n_event=len(events_x)
    # Creates a numpy array of zeros, 4 x n_event
    events_out = np.zeros((4,n_event), dtype=np.int64)
    # Arranges the lists appended above to the numpy array
    events_out[0] = events_x
    events_out[1] = events_y
    events_out[2] = events_p
    events_out[3] = timestamp

# Outputs the data above to .h5
f=h5py.File('D:\\Documents\\Summer Scholarship\\Event-Based-HDF5-Video-Renderer-master\\HDF5 Converter\\Uncooled Cam Dark Setting\\Cooled Cam Dark\\0 Degrees Ambient\\0DegAmbient2.h5',mode='w')
g=f.create_group('DAVIS_events')
g.create_dataset('recording000', data=(events_out))    
f.close()
