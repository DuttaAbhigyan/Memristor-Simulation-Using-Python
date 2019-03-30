#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 18:54:20 2019

@author: abhigyan
"""
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

"""Class to take in various paramters of the Memristors to be simulated"""
class set_memristor_parameters(QMainWindow):
    
    #Create and launch the main window
    def __init__(self, numberOfMemristors):
        super(set_memristor_parameters, self).__init__()
        self.setMemristorParametersOKButtonClicked = False
        self.numberOfMemristors = numberOfMemristors
        self.windowLength = 110 * self.numberOfMemristors + 280
        self.windowBreadth = 550
        self.setGeometry(300, 300, self.windowLength, self.windowBreadth)
        self.setWindowTitle('Memristor Parameters')
        self.setWindowIcon(QIcon('memristor_icon.ico'))
        
        #Sets backgorund Image
        backgroundImage =  QImage('memristor1.jpg')
        backgroundScaledImage = backgroundImage.scaled(QSize(self.windowLength,
                                                             self.windowBreadth))
        palette = QPalette()
        palette.setBrush(10, QBrush(backgroundScaledImage))                     
        self.setPalette(palette)
        
        #Sets Fonts 
        self.labelFont = QFont("Arial", 13, QFont.Bold)
        self.buttonFont = QFont('Times', 13)
        
        self.home()
        self.show()
        
     
    #Create the homescreen    
    def home(self):
        
        #Window title
        self.titleLabel = QLabel(self)
        self.titleLabel.setText('Memristor Parameters')
        self.titleFont = QFont("Times", 18, QFont.Bold)
        self.titleLabel.setStyleSheet('QLabel{color:purple}')
        self.titleFont.setUnderline(True)
        self.titleLabel.setFont(self.titleFont)
        self.titleLabel.setGeometry(QRect(self.windowLength/2 - 120, 10, 500, 50))
        
        #Device numbers title
        self.DeviceLabel = QLabel(self)
        self.DeviceLabel.setText('Device:')
        self.DeviceLabelFont = QFont("Calibri", 14, QFont.Bold)
        self.DeviceLabel.setStyleSheet('QLabel{color:blue}')
        self.DeviceLabel.setFont(self.DeviceLabelFont)
        self.DeviceLabel.setGeometry(QRect(35, 60, 100, 50))
        
        
        #Parameter labels
        self.DLabel = QLabel(self)
        self.DLabel.setText('D (nm):')
        self.DLabel.setFont(self.labelFont)
        self.DLabel.setGeometry(QRect(55, 100, 70, 50))
        
        self.RoNLabel = QLabel(self)
        self.RoNLabel.setText('R_on (\u03A9):')
        self.RoNLabel.setFont(self.labelFont)
        self.RoNLabel.setGeometry(QRect(37, 140, 90, 50))
        
        self.RoFFLabel = QLabel(self)
        self.RoFFLabel.setText('R_off (\u03A9):')
        self.RoFFLabel.setFont(self.labelFont)
        self.RoFFLabel.setGeometry(QRect(36, 180, 90, 50))
        
        self.WLabel = QLabel(self)
        self.WLabel.setText('W_0 (nm):')
        self.WLabel.setFont(self.labelFont)
        self.WLabel.setGeometry(QRect(33, 220, 90, 50))        
        
        self.mobLabel = QLabel(self)
        self.mobLabel.setText('Mobility (\u03BC):')
        self.mobLabel.setFont(self.labelFont)
        self.mobLabel.setGeometry(QRect(19, 260, 100, 50))        
        
        self.polLabel = QLabel(self)
        self.polLabel.setText('Polarity (\u03B7):')
        self.polLabel.setFont(self.labelFont)
        self.polLabel.setGeometry(QRect(22, 300, 100, 50))        
        
        self.typeLabel = QLabel(self)
        self.typeLabel.setText('Type:')
        self.typeLabel.setFont(self.labelFont)
        self.typeLabel.setGeometry(QRect(73, 340, 100, 50))
        
        
        #Stores widgets to take in parameters
        self.DValueFields = []
        self.R_onValueFields = []
        self.R_offValueFields = []
        self.W_0ValueFields = []
        self.mobilityValueFields = []
        self.polarityValueFields = []
        self.memristorTypeValueFields = []
        
        
        #Crestes the various widgets to take in Memristor Paramters
        for i in range(0, self.numberOfMemristors):
            
            numberLabel = QLabel(self)
            numberLabel.setText(str(i+1))
            numberLabelFont = QFont("Calibri", 14, QFont.Bold)
            numberLabel.setStyleSheet('QLabel{color:blue}')
            numberLabel.setFont(self.DeviceLabelFont)
            numberLabel.setGeometry(QRect(75 + (1+i)*120, 62, 50, 50))
            
            
            DVFBox = QLineEdit(self)
            DVFBox.move(55 + (1+i)*120, 112)
            DVFBox.resize(60,25)
            self.DValueFields.append(DVFBox)
            
            R_oNBox = QLineEdit(self)
            R_oNBox.move(55 + (1+i)*120, 152)
            R_oNBox.resize(60, 25)
            self.R_onValueFields.append(R_oNBox)
            
            R_offBox = QLineEdit(self)
            R_offBox.move(55 + (1+i)*120, 192)
            R_offBox.resize(60,25)
            self.R_offValueFields.append(R_offBox)
            
            W_0Box = QLineEdit(self)
            W_0Box.move(55 + (1+i)*120, 232)
            W_0Box.resize(60,25)
            self.W_0ValueFields.append(W_0Box)
            
            mobilityBox = QLineEdit(self)
            mobilityBox.move(55 + (1+i)*120, 272)
            mobilityBox.resize(60,25)
            self.mobilityValueFields.append(mobilityBox)
            
            polarityBox = QLineEdit(self)
            polarityBox.move(55 + (1+i)*120, 312)
            polarityBox.resize(60,25)
            self.polarityValueFields.append(polarityBox)
            
            comboBox = QComboBox(self)
            comboBox.addItem('Ideal')
            #comboBox3.addItem('Strukov')
            #comboBox.addItem('Prodromakis')
            #comboBox.addItem('Biolek')
            comboBox.move(55 + (1+i)*120, 353)
            comboBox.resize(80,25)
            self.memristorTypeValueFields.append(comboBox)
            
        #Creates OK and Cancel button
        self.OKButton = QPushButton('OK', self)
        self.OKButton.resize(100, 40)
        self.OKButton.move(self.windowLength/2 -150, 473)
        
        self.OKButton.setStyleSheet('QPushButton {color: darkgreen;}')
        self.OKButtonFont = QFont('Times', 13)
        self.OKButton.setFont(self.OKButtonFont)
        self.OKButton.clicked.connect(self.readParameters)
        
        self.cancelButton = QPushButton('Cancel', self)
        self.cancelButton.resize(100, 40)
        self.cancelButton.move(self.windowLength/2 , 473)
        
        self.cancelButton.setStyleSheet('QPushButton {color: darkgreen;}')
        self.cancelButtonFont = QFont('Times', 13)
        self.cancelButton.setFont(self.cancelButtonFont)
        self.cancelButton.clicked.connect(self.close)
        
    
    #Reads the parameters input by user
    def readParameters(self):
        self.setMemristorParametersOKButtonClicked = True
        
        self.D = []
        self.R_on = []
        self.R_off = []
        self.W_0 = []
        self.mobility = []
        self.polarity = []
        self.type = []
        self.pValues= []
        
        for i in range(0, self.numberOfMemristors):
            if(self.DValueFields[i].text() != ''):
                self.D.append(float(self.DValueFields[i].text()) * 10**-9)
            else:
                self.D.append(None)
                
            if(self.R_onValueFields[i].text() != ''):
                self.R_on.append(float(self.R_onValueFields[i].text()))
            else:
                self.R_on.append(None)
                
            if(self.R_offValueFields[i].text() != ''):
                self.R_off.append(float(self.R_offValueFields[i].text()))  
            else:
                self.R_off.append(None)
                
            if(self.W_0ValueFields[i].text() != ''):
                self.W_0.append(float(self.W_0ValueFields[i].text()))
            else:
                self.W_0.append(None)
                
            if(self.mobilityValueFields[i].text() != ''):
                self.mobility.append(float(self.mobilityValueFields[i].text() * 10**-12))
            else:
                self.mobility.append(None)
                
            if(self.polarityValueFields[i].text() != ''):
                self.polarity.append(float(self.polarityValueFields[i].text()))
            else:
                self.polarity.append(None)
            self.type.append(self.memristorTypeValueFields[i].currentText())
           
        self.close()
            
        
    #Getter functions
    def getMemristorParamters(self):
        parameterDictionary = {} 
        parameterDictionary['D'] = self.D[:]
        parameterDictionary['R_on'] = self.R_on[:]
        parameterDictionary['R_off'] = self.R_off[:]
        parameterDictionary['W_0'] = self.W_0[:]
        parameterDictionary['mobility'] = self.mobility[:]
        parameterDictionary['polarity'] = self.polarity[:]
        parameterDictionary['type'] = self.type[:]
        return parameterDictionary
    
    def getOKButton(self):
        return self.setMemristorParametersOKButtonClicked
