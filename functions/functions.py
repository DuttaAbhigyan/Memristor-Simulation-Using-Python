#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 00:19:39 2019

@author: abhigyan
"""

import scipy.integrate as spi
import numpy as np
import matplotlib.pyplot as plt

class functions(object):
    
    def __init__(self, typeOfFunction, amplitude, omega, pulsewidth = None, 
                 start = None, stop = None):
        self.typeOfFunction = typeOfFunction
        self.amplitude = amplitude
        self.omega = omega
        self.period = 2 * np.pi/omega
        self.start = start
        self.stop = stop
        self.pulsewidth = pulsewidth
        
        
    def sine_function(self, t):
        func = self.amplitude * np.sin(self.omega*t)
        return func
    
    def cosine_function(self, t):
        func = self.amplitude * np.cos(self.omega*t)
        return func
    
    def unit_step_function(self, t):
        func = self.amplitude * np.where(t > self.start, 1, 0)
        return func
    
    def uniform_pulse_function(self, t):
        func = self.amplitude * np.where((t > self.start and t < self.stop and (t % self.period < (self.pulsewidth))),
                                          1, 0)
        return func
    
    def uniform_time_pulse_function(self, t):
        func = self.amplitude[int(t//self.period) - self.start] \
               * np.where((t > self.start and t < self.stop and (t % self.period < (self.pulsewidth))), 1, 0)
        return func
    
    def custom_pulse_function(self, t):
        func = (self.amplitude[int(t//self.period) - self.start]) * np.where((t > self.start and t < self.stop and \
               (t % self.period < (self.pulsewidth[int(t//self.period) - self.start]))), 1, 0)
        return func
        
    def evaluate_function(self, time):
        func = getattr(self, self.typeOfFunction)
        self.funcValue = func(time)

    
    def evaluate_integration_function(self, time1, time2):
        options = {'limit':10000}
        func = self.return_function_address()
        self.funcIntegrationValue = spi.nquad(func, [[time1, time2]], opts=[options])
        
        
    def return_function_address(self):
        func = getattr(self, self.typeOfFunction)
        return func
    
    def return_evaluation(self):
        return self.funcValue
    
    def return_integration_evaluation(self):
        return self.funcIntegrationValue

