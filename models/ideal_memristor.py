#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 16:56:20 2019

@author: abhigyan
"""

"""We have created an ideal memristor here with inspiration from the paper titled:
    
   'The elusive memristor: properties of basic electrical circuits - Y Joglekar and S Wolf'
   
   The paramters for the memristor are as defined in the aforementioned paper but defined 
   here again for convenience with typical values (for TiO2) mentioned in the brackets:
   
   voltage = Voltage function (A SymPy function object)
   D = Length of Memristor (~ 10nm)
   w_0 = Length of doped region of the memristor
   R_off = Resistance of undoped Memristor of length D (~ > 100 kOhm)
   R_on = Resistance of doped Memristor of length D (∼ 1 kOhm)
   mobility_u = Mobility of the dopants (∼ 10^−10 cm2 V−1 s−1 )
   polarity_n = Value of polarity determines expansion or contraction of the 
                doped region (+1 for expansion)
"""
                

class ideal_memristor(object):
    
    #Initialize the ideal memristor with paramters to be used
    def __init__(self, D = 10 ** -9, w_0 = 0.5 * 10 ** -9, R_on = 16000, R_off = 100, 
                 mobility_u = 10 ** -14, polarity_n = +1):
        self.D = D
        self.w_0 = w_0 
        self.R_off = R_off
        self.R_on = R_on
        self.mobility_u = mobility_u
        self.polarity_n = polarity_n
        self.flux_history = 0
        
        #print(self.D, self.w_0,self.R_off, self.mobility_u)
        
    #Calculate parameters which are not time varying
    def calculate_fixed_parameters(self):
        self.Q_0 = (self.D ** 2) / (self.mobility_u * self.R_on)
        self.R_delta = self.R_off - self.R_on
        self.R_0 = self.R_on * (self.w_0 / self.D) + self.R_off * (1 - self.w_0 / self.D)
        
    #Calculate time variable paramters
    def calculate_time_variable_parameters(self, flux):
        self.flux = self.flux_history + flux
        self.drift_factor = (2 * self.polarity_n * self.R_delta * self.flux) / \
                            (self.Q_0 * (self.R_0 ** 2))
    
    #Calculate current through memristor        
    def calculate_current(self, voltage):
        self.current = (voltage / self.R_0) / ((1 - self.drift_factor) ** 0.5) 
        self.resistance = self.R_0 *  ((1 - self.drift_factor) ** 0.5) 
    
    #Calculate charge through Memristor    
    def calculate_charge(self):
        self.charge = ((self.Q_0 * self.R_0) / self.R_delta) * \
                               (1 - (1 - self.drift_factor) ** 0.5)
                               
    #Update flux history        
    def save_flux_history(self):
        self.flux_history = self.flux
        
    
    #Getter functions    
    def get_current(self):
        return self.current    
    
    def get_charge(self):
        return self.charge   
    
    def get_flux(self):
        return self.flux
    
    def get_resistance(self):
        return self.resistance
    
#End of Ideal Memristor class definition
    
    

        
        
        
        
        
        
        
