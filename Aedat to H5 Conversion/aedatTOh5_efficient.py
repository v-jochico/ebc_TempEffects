from dv import AedatFile
import numpy as np
import scipy.io as sio
import h5py

# Input File Location
file_path = 'D:\\Documents\\Summer Scholarship\\Event-Based-HDF5-Video-Renderer-master\\HDF5 Converter\\Uncooled Cam Dark Setting\\Cooled Cam Dark\\0 Degrees Ambient\\dvSave-2020_01_28_11_52_15.aedat4'

# An empty list for data to be stored later
counter = 0
counter1 = 0
counter2 = 0

with AedatFile(file_path) as f:
    # list all the names of streams in the file
    print(f.names)
    
    # loop through the "events" stream
    for g in f['events']:
        counter+=1
        
    print('Number of Events:',counter)

    events_out = np.empty((4,counter), dtype=np.int64)
    for e in f['events']:
        # Creates a numpy array of zeros, 4 x the lenght of the list
        # Arranges the lists appended above to the numpy array
        if e.polarity == False:
            events_polarity = -1
        else:
            events_polarity = 1

        events_out[0,counter1]= e.x
        events_out[1,counter1] = e.y
        events_out[2,counter1] = events_polarity
        events_out[3,counter1] = e.timestamp
        
        counter1+=1
    
    timestamp = events_out[3,0]
    for x in events_out[3]:
        new_timestamp = x - timestamp
        events_out[3,counter2] = new_timestamp
        
        counter2+=1


# Outputs the data above to .h5
f=h5py.File('D:\\Documents\\Summer Scholarship\\Event-Based-HDF5-Video-Renderer-master\\HDF5 Converter\\Uncooled Cam Dark Setting\\Cooled Cam Dark\\0 Degrees Ambient\\0DegAmbientTest.h5',mode='w')
g=f.create_group('DAVIS_events')
g.create_dataset('recording000', data=(events_out))    
f.close()
