#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 14:40:30 2023

@author: leah
"""

import pandas as pd
from plotnine import *
import os
import numpy as np


os.chdir("/Users/leah/Desktop/2450 Spyder/Notes")
dat = pd.read_csv("2017_Fuel_Economy_Data.csv")
dat  = dat["Combined Mileage (mpg)"]


class Boot_CI():
    def __init__(self, data = None):
        "Initialize the simulation"
        self.stat = "mean"
        self.dat = data
        self.n_boot = 0 
        self.boot_stat = []
        self.ci_level = .95

    #method for counting simulations    
    def add_sims(self):
         """
        Calculates number of simulations and appends statistic chosen by user

        Parameters
        ------
        n: int
            length of sample used in bootstrap.
        boot_sample: list
            Sample used within bootstrap.

        Returns
        -------
        None.

        """
        #assigns "n" (int) to length of sample data
        n = len(self.dat)

        #for i within number of times bootstrap sample runs
        for i in range(self.n_boot):
            #establishes sample for bootstrap as "boot_sample" (list)
            boot_sample = self.dat.sample(n, replace = True)
            
            #if chosen statistic is median
            if self.stat == "median":
                #append "boot_sample" median to "boot_stat" (list)
                self.boot_stat.append(float(boot_sample.median()))
            
            #else/if chosen statistic is mean
            elif self.stat == "mean":
                #append "boot_sample" mean to "boot_stat" (list)
                self.boot_stat.append(float(boot_sample.mean()))
            
            #else/if chosen statistic is standard deviation
            elif self.stat == "std dev":
                #append "boot_sample" standard deviation to "boot_stat" (list)
                self.boot_stat.append(float(boot_sample.std()))
            
            #else give User communicating an incorrect chosen statistic 
            else: 
                raise TypeError("Wrong Statistic name")
                
    def clear_sims(self):
        self.boot_stat = []
        
    def load_data(self,data): 
        self.dat = data
        
    def update_n_boot(self, new_n_boot):
        self.n_boot = new_n_boot
        
    def set_statistic(self, stat):
        self.boot_stat = []
        self.stat = stat
        
    def plot_boot(self):
        boot_df = pd.DataFrame({'x': self.boot_stat})
    
        p = (
            ggplot(boot_df, aes(x='x')) +
            geom_histogram()
            )
    
        return p
    
    #this is a method that creates a confidence interval from the list boot_stat
    def conf_interval(self):
        """Assumes boot_stat is a list. Calculates a confidence interval off the list
        returns the value of the confidence interval in an array """
        
        #if the length of boot_stat is 0, meaning nothing has run, then the
        #method will not work and print an error message
        if len(self.boot_stat) == 0:
            #the message that is printed if the length is 0
            print("Boot_stat is 0. Must run sample first")
        
        #if boot_stat is not 0, then this runs
        else: 
            
            #prompts user to input the level of confidence 
            alpha = float(input("Please enter confidence level percentage. Must be an integer: "))
            
            #alters alpha for a 2 tailed test
            alpha = alpha/2
            
            #uses the percentile function in numpy and returns a confidence interval
            ci = np.percentile(self.boot_stat, [alpha, 100-alpha])
        
        #returns the two values of confidence interval   
        return ci 
            
            
    
#creates the class       
test = Boot_CI()

#runs method to load data
test.load_data(data = dat)

#sets the number of times to bootstrap
test.update_n_boot(10000)

#actually runs the boot strap 
test.add_sims()

#creates a plot of the boot
test.plot_boot()

#calculates the confidence interval 
test.conf_interval()


    

#######


    











