#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import tessreduce as tr


# In[3]:


#Checking file location
import os 
dir_path = os.path.dirname(os.path.realpath('2020fqv_example'))
print(dir_path)


# In[9]:


class tesslcclass:
    
#How do I make it so that not all positional arguments are required
#If the arguments are less than a specefic number do this but irrespective of the number of arguments can 
#I set one of these parameters to nothing unless told otherwise: perhaps =None
    def __init__(self, sn_name, discovered, tessReduceRawDataFileName, subtraction_threshold):
        self.discovered = discovered
        self.snName = sn_name
        self.rawData = tessReduceRawDataFileName
        self.subtractionThreshold = subtraction_threshold
        self.tess = pd.read_csv(self.rawData)
        
    def run_tess_reduce(self):
    
        obs = tr.sn_lookup(self.snName, time = self.discovered)
        tess = tr.tessreduce(obs_list=obs,reduce=True,plot=True)
    
        tess.to_flux()
        #could also plot it in magnitudes but check the documentation for syntax
        #adding ground = True as an argument retrieves ground based data from ZTF
        tess.plotter() 
        
    def savelc(self):
        #saving the light curve data not the image
        self.tess.save_lc(self.rawData)
        
    #function to save lc image

    def mask_bad_data(self):
        # set flux value of bad data points to np.nan so that they won't influence later operations
        self.mask = self.tess.flux_err > 0.
        self.tess.flux[~self.mask] = np.nan
    
    def data_subtraction(self):
        self.mask_bad_data()
        first_n = self.subtractionThreshold
        calibration_array = np.zeros((first_n,1))
        for i in range(first_n):  
            calibration_array[i] = self.tess.flux[i]
    #np.transpose(calibration_array)
        calibration_dataframe = pd.DataFrame(calibration_array, columns = ['First_' + str(first_n) + '_Fluxes'])
    #print(calibration_dataframe)
        mean_of_first_n_values = calibration_dataframe.mean()
        for n in range(len(self.tess.flux)):
            self.tess.flux[n] = self.tess.flux[n] - mean_of_first_n_values
    #print(tess)
    #This plot should be shifted up by the value of the -(mean of the first n values) 
    
    #apply a better plotting routine using matplotlib functionalities
        self.tess.plot.scatter(x = 'time', y = 'flux')
        plt.show()
        
        


# In[1]:


#only needed when running from the command line
#if __name__ == '__main__':    

#object1_module4 = tesslcclass( 'sn2020adw' , 'disc', 'SN2020adw_lcdata_file', 300)

#uncomment the below

#object2_module4 = tesslcclass( 'sn2020fqv' , 'disc', '2020fqv_example', 300)
#object2_module4.data_subtraction()
#object2_module4.run_tess_reduce()


    #print(module4)
    #print(Module4Skeleton.data_subtraction(module4))
    #dataSub = module4.data_subtraction('2020fqv_example', 300)
    #parser = bla.define_options(usage='dummy.py is a dummy module')
    #print(module4)


# In[ ]:





# In[ ]:




