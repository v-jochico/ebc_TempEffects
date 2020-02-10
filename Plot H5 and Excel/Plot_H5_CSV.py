import h5py
import logging
import argparse
import numpy as np
import csv

# Graphics
import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

# Background for the plot
plt.style.use('dark_background')

# Importing h5 data
datafile = h5py.File('D://Documents//Summer Scholarship//Event-Based-HDF5-Video-Renderer-master//HDF5 Converter//Uncooled Cam Dark Setting//Cooled Cam Dark//0 Degrees Ambient//0DegreeDarkData2.h5', 'r')
datafile2 = h5py.File('D://Documents//Summer Scholarship//Event-Based-HDF5-Video-Renderer-master//HDF5 Converter//Uncooled Cam Dark Setting//Cooled Cam Dark//45 Degrees Ambient//45DegreeDarkData.h5', 'r')

# Calling imported data from datafile and getting through the key and group of the h5 structure
raw_event_file = datafile['DAVIS_events']['recording000']
#     sneaky performance boost, parses event stream straight to matrix
#     this avoids expensive calls to h5 
event_data = np.zeros_like(raw_event_file)
raw_event_file.read_direct(event_data)

# Calling imported data from datafile2 and getting through the key and group of the h5 structure
raw_event_file2 = datafile2['DAVIS_events']['recording000']
#     sneaky performance boost, parses event stream straight to matrix
#     this avoids expensive calls to h5 
event_data2 = np.zeros_like(raw_event_file2)
raw_event_file2.read_direct(event_data2)

# Get total number of events to render
n_events = np.shape(raw_event_file)[1]
n_events2 = np.shape(raw_event_file2)[1]

# Calculate update interval by camera sampling at 1 microseconds over 30fps
update_interval = np.floor(1e6 / 30) 

#  initialise frames and iterators  

finish = n_events
finish2 = n_events2
start = 0

# Datafile iterators and frames
event_count = 0
next_update = 0
frame_counter = 0
event_sum_list =[]
current_frame= []
timeElapsed=[]
temperature=[]
seconds=[]

# Datafile 2 iterators and frames
event_count2 = 0
next_update2 = 0
frame_counter2 = 0
event_sum_list2 =[]
current_frame2= []
timeElapsed2=[]
temperature2=[]
seconds2=[]
rate=30


#    Datafile for loop to count the number of events per frame
#    process events within specified event index range 
for event_index in range(start, finish):

#         Extract the event and create the frame
    x, y, p, t = event_data[:, event_index]
#    frame[x, y] = p
    event_count = event_count + 1

    if t >= next_update:
        frame_counter = frame_counter + 1

        current_frame.append(frame_counter)

        calculateseconds = round(frame_counter/rate, 2)
        timeElapsed.append(calculateseconds)
#         events_remaining = n_events - event_count

        next_update = t + update_interval

        if frame_counter > 1:
            event_sum_list.append(event_count)
        else:
            event_sum_list.append(0)

#    Datafile for loop to count the number of events per frame
#    process events within specified event index range 

for event_index2 in range(start, finish2):

#         Extract the event and create the frame
    x2, y2, p2, t2 = event_data2[:, event_index2]
#    frame[x, y] = p
    event_count2 = event_count2 + 1

    if t2 >= next_update2:
        frame_counter2 = frame_counter2 + 1

        current_frame2.append(frame_counter2)

        calculateseconds2 = round(frame_counter2/rate, 2)
        timeElapsed2.append(calculateseconds2)

#         events_remaining = n_events - event_count

        next_update2 = t2 + update_interval

        if frame_counter2 > 1:
            event_sum_list2.append(event_count2)
        else:
            event_sum_list2.append(0)

# Calculate the number of events per frame by doing a difference between y and x

#total = [y - x for x,y in zip(event_sum_list[:-1], event_sum_list[1:])]
#total.insert(0,0)

#total2 = [y - x for x,y in zip(event_sum_list2[:-1], event_sum_list2[1:])]
#total2.insert(0,0)

#print('Number of Events:', total)

#print('Total Lenght of Event_Data:', len(total))

# Prints total lenghts to check if they have the same size
print('Total Lenght of Frames for Event_Data:', len(current_frame))
print('Total Lenght of timeElapsed:', len(timeElapsed))

print('Total Lenght of Event_Data2:', len(current_frame2))
#print('Total Lenght of Frames for Event_Data2:', len(total2))
print('Total Lenght of timeElapsed2:', len(timeElapsed2))

# Opens the excel data of the temperature for datafile    
with open('D://Documents//Summer Scholarship//Event-Based-HDF5-Video-Renderer-master//HDF5 Converter//Uncooled Cam Dark Setting//Cooled Cam Dark//0 Degrees Ambient//0DegreeDarkData.csv', 'r', encoding="utf-8-sig") as csvfile:
     plots = csv.reader(csvfile, delimiter=',')
     for column in plots:
         temperature.append(float(column[0]))
         seconds.append(float(column[1]))

# Opens the excel data of the temperature for datafile 2
with open('D://Documents//Summer Scholarship//Event-Based-HDF5-Video-Renderer-master//HDF5 Converter//Uncooled Cam Dark Setting//Cooled Cam Dark//45 Degrees Ambient//45DegreeDarkData.csv', 'r', encoding="utf-8-sig") as csvfile:
     plots = csv.reader(csvfile, delimiter=',')
     for column in plots:
         temperature2.append(float(column[0]))
         seconds2.append(float(column[1]))

# Creates a plot to show Datafile, Datafile 2, Temperature for Datafile, and Temeperature for Datafile 2
fig, ax = plt.subplots()

color = 'tab:red'
ax.set_xlabel('Time(s)')
ax.set_ylabel('Events', color=color)
#ax1.plot(timeElapsed, total, color=color)
#ax1.plot(timeElapsed2, total2, color='m')
zeroevent_deg=ax.plot(timeElapsed,event_sum_list, color='m', label='0 Deg Events')
ffevent_deg=ax.plot(timeElapsed2,event_sum_list2, color='g', label='55 Deg Events')
#ax1.tick_params(axis='y', labelcolor=color)

ax2=ax.twinx()

color = 'tab:blue'
ax2.set_ylabel('Temperature', color=color)
zerotemp=ax2.plot(seconds, temperature, color=color, label='0 Deg Temp')
fftemp=ax2.plot(seconds2, temperature2, color='y', label='55 Deg Temp')

lns = zeroevent_deg+ffevent_deg+zerotemp+fftemp
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc='upper left')

ax.grid()
fig.tight_layout()
ax2.set_xlim(0,1200)
plt.show()