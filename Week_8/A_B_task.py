#%% Import modules 
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import simpleaudio as sa
#%% Start the random number generator
from numpy import random 
rng = random.default_rng(seed = 21)
#%% decide on the output file name 
subjid = '001' #your the first subject! 
#filename = 'A_B_' + subjid + '.xlsx' # if you prefer an excel file 
filename = 'A_B_' + subjid + '.csv' #if you prefer a csv file 
#%%# fixed facts about the sine functions
sr = 44100     # how many samples per second 
duration = 0.5 # length of the sound in seconds. 
volume = 0.25   # DO NOT MAKE VOLUME LARGER THAN 0.5 
number_of_samples = duration*sr # since there are sr samples in each second, there are sr*duration samples in the sounds we are playing 
number_of_samples = int(number_of_samples) #converts into an integer if necessary.  
time_vec = np.linspace(0, duration, number_of_samples) # This makes a vector of the time step starting from 0 to duration
#%% Make the two notes 
fA = 440 
A_note = np.sin(fA * time_vec * 2 * np.pi)
fB = 494
B_note = np.sin(fB * time_vec * 2 * np.pi)
# the sample amplitude values must consequently fall in the range of -32768 to 32767.
# To do that I multiply by 32767 and divide by the largest value in A_note or B_note 
A_note  = volume*A_note*32767 / np.max(np.abs(A_note))  #I multiply by volume to control the volume 
B_note  = volume*B_note*32767 / np.max(np.abs(B_note)) 
#Convert to numpy 16 bit integers 
A_note = A_note.astype(np.int16)
B_note = B_note.astype(np.int16)
#%% Organize the experiment 
ntrials_per_condition = 3
trial_1 = np.ones(ntrials_per_condition) # an array with 3 ones
trial_2 = 2*np.ones(ntrials_per_condition) # an array with 3 twos
trial_order = np.concatenate((trial_1,trial_2)) # concatenate the array
ntrials = np.size(trial_order) #get the length of trial_order
shuffle = random.permutation(ntrials) # get a random order of trials
trial_order = trial_order[shuffle] # permute trial order 
trial_response = np.array(np.zeros(ntrials),dtype = 'str') #empty array to hold the responses of trype string
#%% Run the Experiment 
for j in range(ntrials):  #loop over trials, index is j
    if trial_order[j] == 1: #check the trial type for jth trial
        play_obj = sa.play_buffer(A_note , 1, 2, sr) # i created an object here. 
        play_obj.wait_done() # tells python to wait for the sound to finish before going any further.
    else:
        play_obj = sa.play_buffer(B_note , 1, 2, sr) # i created an object here. 
        play_obj.wait_done() # tells python to wait for the sound to finish before going any further.
    response_check = False #I set the response_check to false.  I will only change response_check if i get a valid response 
    while response_check == False: # This while loop runs until I get a valid response 
        response = input() #Get a keyboard input
        if (response =='a') | (response == 'b'): #check if its an a or b 
            response_check = True #if it is update response_check to true 
            print(response) # print the response 
            trial_response[j] = response # the jth trial response is response
        else:
            print('Invalid Response Try Again')
print('Done!')
#%%Organize the Data 
data = pd.DataFrame(columns = ['Condition','Response','Accuracy']) #create an empty data frame with three columns with column labels given
data['Condition'] = trial_order #place trial_order in the 'Condition' column
data['Response'] = trial_response #place trial_response in the 'Response' column
#%% Compute Accuracy 
accuracy = np.zeros(ntrials)  #make an empty array to hold accuracy information.  Set to zero for inaccurate
accuracy[(trial_order==1) & (trial_response == 'a')] = 1 #if trial_order is 1 and response is 'a' set accuracy to 1 for correct
accuracy[(trial_order==2) & (trial_response == 'b')] = 1 #if trial_order is 2 and response is 'b' set accutacy to 2 for correct 
data['Accuracy'] = accuracy
#%% Save the Data 
#You should only do 1 of these. 
data.to_csv(filename) #write it out to a csv file 
#data.to_excel(filename) #write it out to an excel file 
# %%