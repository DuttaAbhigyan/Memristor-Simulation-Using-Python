#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 16:00:44 2019

@author: abhigyan
"""

import matplotlib.pyplot as plt
import functions as fn
import memristor_scipy as mem
import numpy as np

    
class create_memristor_circuit(object):
    
    def __init__(self, voltageFunction, memristor, time1, time2, samplingFrequency):
       self.voltageFunction = voltageFunction
       self.memristor = memristor
       self.memristor.calculate_fixed_parameters()
       self.time1 = time1
       self.time2 = time2
       self.samples = int(samplingFrequency * (self.time2 - self.time1))
       self.timeInstants = np.linspace(self.time1, self.time2, self.samples)
       
       
    def calculate_voltage_dependent_params(self, time1, time2):
       self.voltageFunction.evaluate_function(time2)
       self.voltageFunction.evaluate_integration_function(time1, time2)
       self.instantaneousVoltage = self.voltageFunction.return_evaluation()
       self.delFlux = self.voltageFunction.return_integration_evaluation()
       
       self.memristor.calculate_time_variable_parameters(self.delFlux[0])
       self.memristor.calculate_current(self.instantaneousVoltage)
       self.memristor.calculate_charge()
       
       self.memristor.save_flux_history()
       self.instantaneousCurrent = self.memristor.get_current()
       self.instantaneousTime = time2
       self.instantaneousCharge = self.memristor.get_charge()
       self.instantaneousFlux = self.memristor.get_flux()
       self.instantaneousResistance = self.memristor.get_resistance()
       
    def create_value_matrix(self):
        self.current = np.array([])
        self.charge = np.array([])
        self.voltage = np.array([])
        self.flux = np.array([])
        self.resistance = np.array([])
        self.time = np.array([])
        
        for i in range(0, self.samples-1):
            self.calculate_voltage_dependent_params(self.timeInstants[i], self.timeInstants[i+1])
            self.current = np.append(self.current, self.instantaneousCurrent)
            self.charge = np.append(self.charge, self.instantaneousCharge)
            self.voltage = np.append(self.voltage, self.instantaneousVoltage)
            self.flux = np.append(self.flux, self.instantaneousFlux)
            self.resistance = np.append(self.resistance, self.instantaneousResistance)
            self.time = np.append(self.time, self.instantaneousTime)
        
            
    def plot_function(self, x, y, label_x, label_y):
        self.x = getattr(self, x)
        self.y = getattr(self, y)
        plt.plot(self.x, self.y, linewidth = 0.7)
        plt.xlabel(label_x)
        plt.ylabel(label_y)
    
    def get_current(self):
        return self.current
    
    def get_charge(self):
        return self.charge
    
    def get_voltage(self):
        return self.voltage
    
    def get_flux(self):
        return self.flux
    
    def get_resistance(self):
        return self.resistance




class multiple_memristor_circuits(object):
    
    waveDictionary = {'Sine':'sine_function', 'Cosine':'cosine_function', 
                      'Uniform Pulse':'uniform_pulse_function', 
                      'Non-Uniform Amplitude Pulse':'uniform_time_pulse_function', 
                      'Custom Pulse':'custom_pulse_function'}
    
    valueDictionary = {'Current':'current', 'Voltage':'voltage', 'Charge':'charge', 
                       'Flux':'flux', 'Time':'time', 'Resistance':'resistance'}
    
    def __init__(self, data):
        self.data = data
        print(self.data)
        self.memristorParameters = self.data['memristor_parameters']
        self.waveParameters = self.data['wave_parameters']
        self.preferences = self.data['preferences']
        self.numberOfMemristors = self.data['preferences']['number']
        self.defaultMemristor = False
        self.defaultWave = False
        
        
        if(self.numberOfMemristors != len(self.data['memristor_parameters']['D'])):
            self.defaultMemristor = True
            
        if(self.numberOfMemristors != len(self.data['wave_parameters']['type'])):
            self.defaultWave = True
    
        self.equalize_parameters()
        self.run_circuit()

    
    def equalize_parameters(self):
        self.memristors = []
        self.waveFunctions = []
        self.memristorCircuits = []
        
        for i in self.memristorParameters:
            if(len(self.memristorParameters[i]) != self.numberOfMemristors):
                self.memristorParameters[i] = self.memristorParameters[i] * self.numberOfMemristors
                
        for i in self.waveParameters:
            if(len(self.waveParameters[i]) != self.numberOfMemristors):
                self.waveParameters[i] = self.waveParameters[i] * self.numberOfMemristors
                
        for i in range(0, self.numberOfMemristors):
            if(self.memristorParameters['type'][i] == 'Ideal'):
                memristor = mem.ideal_memristor(self.memristorParameters['D'][i],
                                                self.memristorParameters['W_0'][i],
                                                self.memristorParameters['R_on'][i],
                                                self.memristorParameters['R_off'][i],
                                                self.memristorParameters['mobility'][i],
                                                self.memristorParameters['polarity'][i])
                self.memristors.append(memristor)
            
                
        for i in range(0, self.numberOfMemristors):
            wave = fn.functions(self.waveDictionary[self.waveParameters['type'][i]],
                                self.waveParameters['amplitude'][i],
                                self.waveParameters['omega'][i],
                                self.waveParameters['pulsewidth'][i],
                                self.waveParameters['start'][i] - 2,
                                self.waveParameters['stop'][i] + 2)
            self.waveFunctions.append(wave)

        for i in range(0, self.numberOfMemristors):
            cmc = create_memristor_circuit(self.waveFunctions[i], self.memristors[i], 
                                           self.waveParameters['start'][i], self.waveParameters['stop'][i],
                                           self.preferences['sampling_frequency'])
            self.memristorCircuits.append(cmc)
            
            
        
    def run_circuit(self):
        for i in self.memristorCircuits:
            i.create_value_matrix()
            
        yAxis = self.valueDictionary[self.preferences['y_axis']]
        xAxis = self.valueDictionary[self.preferences['x_axis']]
        yLabel = self.preferences['y_axis']
        xLabel = self.preferences['x_axis']
        
        
        if(self.preferences['dspc'] == True and self.preferences['dwpc'] == True):
            for i in self.memristorCircuits:
                i.plot_function(xAxis, yAxis, xLabel, yLabel)
            if(self.preferences['spc'] == True):
                plt.savefig(self.preferences['save_path'] + 'memrsitor_graph' + self.preferences['format'], 
                            self.preferences['dpi'])
            plt.show()
          
            
        elif(self.preferences['dspc'] == True and self.preferences['dwpc'] == False):
            for i in self.memristorCircuits:
                i.plot_function(xAxis, yAxis, xLabel, yLabel)
            if(self.preferences['spc'] == True):
                plt.savefig(self.preferences['save_path'] + 'memrsitor_graph' + self.preferences['format'], 
                            self.preferences['dpi'])
            
        elif(self.preferences['dspc'] == False and self.preferences['dwpc'] == True):
            count = 0
            for i in self.memristorCircuits:
                i.plot_function(xAxis, yAxis, xLabel, yLabel)
                if(self.preferences['spc'] == True):
                    plt.savefig(self.preferences['save_path'] + 'memrsitor_graph'+ str(count) + self.preferences['format'], 
                                self.preferences['dpi'])
                    count += 1
                plt.show()
                
        
        elif(self.preferences['dspc'] == False and self.preferences['dwpc'] == False):
            count = 0
            for i in self.memristorCircuits:
                i.plot_function(xAxis, yAxis, xLabel, yLabel)
                if(self.preferences['spc'] == True):
                    plt.savefig(self.preferences['save_path'] + 'memrsitor_graph'+ str(count) + self.preferences['format'], 
                                self.preferences['dpi'])
                    count += 1
