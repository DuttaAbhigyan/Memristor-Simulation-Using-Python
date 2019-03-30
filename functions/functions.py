#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 00:19:39 2019

@author: abhigyan
"""

import scipy.integrate as spi
import numpy as np
import matplotlib.pyplot as plt

"""This is the function class which can be used to create user defined functions. 
   Currently the following functions are supported:
   -> Sine
   -> Cosine
   -> Unit Step function
   -> Pulse with uniform amplitude and uniform frequency
   -> Pulse with non-uniform amplitude and uniform frequency 
   -> Pulse with non-uniform amplitude, non-unifrom on time uniform frequency 
"""

class functions(object):
    
    #Initializaion of various parameters related to the functions
    def __init__(self, typeOfFunction, amplitude, omega, pulsewidth = None, 
                 start = None, stop = None):
        self.typeOfFunction = typeOfFunction
        self.amplitude = amplitude
        self.omega = omega
        self.period = 2 * np.pi/omega
        self.start = start
        self.stop = stop
        self.pulsewidth = pulsewidth
        
    #Sine function    
    def sine_function(self, t):
        func = self.amplitude * np.sin(self.omega*t)
        return func
    
    #Cosine Function
    def cosine_function(self, t):
        func = self.amplitude * np.cos(self.omega*t)
        return func
    
    #Unit Step function
    def unit_step_function(self, t):
        func = self.amplitude * np.where(t > self.start, 1, 0)
        return func
    
    #Pulse with uniform amplitude and uniform frequency
    def uniform_pulse_function(self, t):
        func = self.amplitude * np.where((t > self.start and t < self.stop and (t % self.period < (self.pulsewidth))),
                                          1, 0)
        return func
    
    #Pulse with non-uniform amplitude and uniform frequency 
    def uniform_time_pulse_function(self, t):
        func = self.amplitude[int(t//self.period) - self.start] \
               * np.where((t > self.start and t < self.stop and (t % self.period < (self.pulsewidth))), 1, 0)
        return func
    
    #Pulse with non-uniform amplitude, non-unifrom on time uniform frequency 
    def custom_pulse_function(self, t):
        func = (self.amplitude[int(t//self.period) - self.start]) * np.where((t > self.start and t < self.stop and \
               (t % self.period < (self.pulsewidth[int(t//self.period) - self.start]))), 1, 0)
        return func
    
    #Evaluates the function value at any given point in time
    def evaluate_function(self, time):
        func = getattr(self, self.typeOfFunction)
        self.funcValue = func(time)

    #Evaluates the function value of the integral function at any given point in time
    def evaluate_integration_function(self, time1, time2):
        options = {'limit':10000}
        func = self.return_function_address()
        self.funcIntegrationValue = spi.nquad(func, [[time1, time2]], opts=[options])
        
    #Calls the function specified by user    
    def return_function_address(self):
        func = getattr(self, self.typeOfFunction)
        return func
    
    #Returning functions
    def return_evaluation(self):
        return self.funcValue
    
    def return_integration_evaluation(self):
        return self.funcIntegrationValue

