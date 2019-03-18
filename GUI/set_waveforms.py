#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 18:56:58 2019

@author: abhigyan
"""
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

"""Class to set paramters of the input waveforms"""
    
class set_waveforms(QMainWindow):
    
    #Create and launch the main window
    def __init__(self, numberOfMemristors):
        super(set_waveforms, self).__init__()
        self.setWaveformsOKButtonClicked = False
        self.numberOfMemristors = numberOfMemristors
        self.windowLength = 130 * self.numberOfMemristors + 210
        self.windowBreadth = 500
        self.setGeometry(300, 300, self.windowLength, self.windowBreadth)
        self.setWindowTitle('Input Waveforms')
        self.setWindowIcon(QIcon('memristor_icon.ico'))
        
        backgroundImage =  QImage('memristor1.jpg')
        backgroundScaledImage = backgroundImage.scaled(QSize(self.windowLength,
                                                                 self.windowBreadth))
        palette = QPalette()
        palette.setBrush(10, QBrush(backgroundScaledImage))                     
        self.setPalette(palette)
        self.show()
        self.home()
        
        
    #Create the homescreen
    def home(self):
        #Window title
        self.titleLabel = QLabel(self)
        self.titleLabel.setText('Input Waveforms')
        self.titleFont = QFont("Times", 18, QFont.Bold)
        self.titleLabel.setStyleSheet('QLabel{color:purple}')
        self.titleFont.setUnderline(True)
        self.titleLabel.setFont(self.titleFont)
        self.titleLabel.setGeometry(QRect(self.windowLength/2 - 120, 10, 500, 50))
        self.titleLabel.show()
        
        #Device numbers
        self.DeviceLabel = QLabel(self)
        self.DeviceLabel.setText('Device:')
        self.DeviceLabelFont = QFont("Calibri", 14, QFont.Bold)
        self.DeviceLabel.setStyleSheet('QLabel{color:blue}')
        self.DeviceLabel.setFont(self.DeviceLabelFont)
        self.DeviceLabel.setGeometry(QRect(35, 60, 100, 50))
        self.DeviceLabel.show()
        
        
        #Parameter labels
        self.typeLabel = QLabel(self)
        self.typeLabel.setText('Type:')
        self.typeLabelFont = QFont("Arial", 13, QFont.Bold)
        self.typeLabel.setFont(self.typeLabelFont)
        self.typeLabel.setGeometry(QRect(87, 100, 70, 50))
        self.typeLabel.show()
        
        self.amplitudeLabel = QLabel(self)
        self.amplitudeLabel.setText('Amplitude (V):')
        self.amplitudeLabelFont = QFont("Arial", 13, QFont.Bold)
        self.amplitudeLabel.setFont(self.amplitudeLabelFont)
        self.amplitudeLabel.setGeometry(QRect(15, 140, 120, 50))
        self.amplitudeLabel.show()
        
        self.omegaLabel = QLabel(self)
        self.omegaLabel.setText('Omega (\u03C9):')
        self.omegaLabelFont = QFont("Arial", 13, QFont.Bold)
        self.omegaLabel.setFont(self.omegaLabelFont)
        self.omegaLabel.setGeometry(QRect(37, 180, 100, 50))
        self.omegaLabel.show()
        
        self.pwLabel = QLabel(self)
        self.pwLabel.setText('Pulsewidth:')
        self.pwLabelFont = QFont("Arial", 13, QFont.Bold)
        self.pwLabel.setFont(self.pwLabelFont)
        self.pwLabel.setGeometry(QRect(35, 220, 100, 50))
        self.pwLabel.show()
        
        self.startLabel = QLabel(self)
        self.startLabel.setText('Start:')
        self.startLabelFont = QFont("Arial", 13, QFont.Bold)
        self.startLabel.setFont(self.startLabelFont)
        self.startLabel.setGeometry(QRect(85, 260, 100, 50))
        self.startLabel.show()
        
        self.stopLabel = QLabel(self)
        self.stopLabel.setText('Stop:')
        self.stopLabelFont = QFont("Arial", 13, QFont.Bold)
        self.stopLabel.setFont(self.stopLabelFont)
        self.stopLabel.setGeometry(QRect(85, 300, 100, 50))
        self.stopLabel.show()
        
        self.typeValueFields = []
        self.amplitudeValueFields = []
        self.omegaValueFields = []
        self.pwValueFields = []
        self.startValueFields = []
        self.stopValueFields = []
        #self.memristorTypeValueFields = []
        
        #Creates the widgets to take in paramters of the waveforms
        for i in range(0, self.numberOfMemristors):
            
            numberLabel = QLabel(self)
            numberLabel.setText(str(i+1))
            numberLabelFont = QFont("Calibri", 14, QFont.Bold)
            numberLabel.setStyleSheet('QLabel{color:blue}')
            numberLabel.setFont(self.DeviceLabelFont)
            numberLabel.setGeometry(QRect(75 + (1+i)*120, 62, 50, 50))
            numberLabel.show()
            numberLabel.show()
            
            
            typeBox = QComboBox(self)
            typeBox.addItem('Sine')
            typeBox.addItem('Cosine')
            typeBox.addItem('Uniform Pulse')
            typeBox.addItem('Non-Uniform Amplitude Pulse')
            typeBox.addItem('Custom Pulse')
            typeBox.move(55 + (1+i)*120, 112)
            typeBox.show()
            typeBox.resize(80,25)
            self.typeValueFields.append(typeBox)
            
            amplitudeBox = QLineEdit(self)
            amplitudeBox.move(55 + (1+i)*120, 152)
            amplitudeBox.resize(80, 25)
            amplitudeBox.show()
            self.amplitudeValueFields.append(amplitudeBox)
            
            omegaBox = QLineEdit(self)
            omegaBox.move(55 + (1+i)*120, 192)
            omegaBox.resize(80,25)
            omegaBox.show()
            self.omegaValueFields.append(omegaBox)
            
            pwBox = QLineEdit(self)
            pwBox.move(55 + (1+i)*120, 232)
            pwBox.resize(80,25)
            pwBox.show()
            self.pwValueFields.append(pwBox)
            
            startBox = QLineEdit(self)
            startBox.move(55 + (1+i)*120, 272)
            startBox.resize(80,25)
            startBox.show()
            self.startValueFields.append(startBox)
            
            stopBox = QLineEdit(self)
            stopBox.move(55 + (1+i)*120, 312)
            stopBox.resize(80,25)
            stopBox.show()
            self.stopValueFields.append(stopBox)
            
        #Creates OK button and Cancel button   
        self.OKButton = QPushButton('OK', self)
        self.OKButton.resize(100, 40)
        self.OKButton.move(self.windowLength/2 -150, 423)
        
        self.OKButton.setStyleSheet('QPushButton {color: darkgreen;}')
        self.OKButtonFont = QFont('Times', 13)
        self.OKButton.setFont(self.OKButtonFont)
        self.OKButton.show()
        self.OKButton.clicked.connect(self.readParameters)
        
        self.cancelButton = QPushButton('Cancel', self)
        self.cancelButton.resize(100, 40)
        self.cancelButton.move(self.windowLength/2 , 423)
        
        self.cancelButton.setStyleSheet('QPushButton {color: darkgreen;}')
        self.cancelButtonFont = QFont('Times', 13)
        self.cancelButton.setFont(self.cancelButtonFont)
        self.cancelButton.show()
        self.cancelButton.clicked.connect(self.close)
        
    
    #Reads the paramters input by the user    
    def readParameters(self):
        self.setWaveformsOKButtonClicked = True
        self.type = []
        self.amplitude = []
        self.omega = []
        self.pulsewidth = []
        self.start = []
        self.stop = []
   
        for i in range(0, self.numberOfMemristors):
            if(self.amplitudeValueFields[i].text() != ''):
                self.amplitude.append(float(self.amplitudeValueFields[i].text()))
            else:
                self.amplitude.append(None)
            if(self.omegaValueFields[i].text() != ''):
                self.omega.append(float(self.omegaValueFields[i].text()))
            else:
                self.omega.append(None)
            if(self.pwValueFields[i].text() != ''):
                self.pulsewidth.append(float(self.pwValueFields[i].text()))  
            else:
                self.pulsewidth.append(None)
            if(self.startValueFields[i].text() != ''):
                self.start.append(float(self.startValueFields[i].text()))
            else:
                self.start.append(None)
            if(self.stopValueFields[i].text() != ''):
                self.stop.append(float(self.stopValueFields[i].text()))
            else:
                self.stop.append(None)
            self.type.append(self.typeValueFields[i].currentText())
           
        self.close()
        
        
    #Getter function
    def getWaveParameters(self):
        parameterDictionary = {}
        parameterDictionary['type'] = self.type[:]
        parameterDictionary['amplitude'] = self.amplitude[:]
        parameterDictionary['omega'] = self.omega[:]
        parameterDictionary['pulsewidth'] = self.pulsewidth[:]
        parameterDictionary['start'] = self.start[:]
        parameterDictionary['stop'] = self.stop[:]
        return parameterDictionary
    
    def getOKButton(self):
        return self.setWaveformsOKButtonClicked