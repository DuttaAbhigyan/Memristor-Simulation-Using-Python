#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 19:20:06 2019

@author: abhigyan
"""

import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import controller as cntrl
import set_memristor_parameters as semp
import set_waveforms as sew

"""Class to implement the functionalities of the Home screen. It also has getter
   functions to get the inputs from the user from all windows"""

class memristor_GUI(QMainWindow):
    
    #Default parameters of a Memristor and Input Wave
    numberOfMemristors = 1
    samplingFrequency = 10000
    dpi = 720
    savePath = ''
    sw = None
    smp = None
    
    D = 10 ** -9
    R_on = 100
    R_off = 16000
    W_0 = 0.5 * D
    mobility = 0.01 * 10**-12
    polarity = +1
    memristorType = 'Ideal'
    Q_0 = 10**-6
    R_delta = 15900
    R_0 = 8050
    defaultMemristorParameters = {'D':[D], 'R_on':[R_on], 'R_off':[R_off],
                                  'W_0':[W_0], 'mobility':[mobility], 'polarity':[polarity],
                                  'type': [memristorType]}
    
    
    waveType = 'Sine'
    amplitude = 1
    omega = 1000
    pulsewidth = 0.5
    start = 0
    stop = 1
    defaultWaveParameters = {'type':[waveType], 'amplitude':[amplitude], 'omega':[omega], 
                             'pulsewidth':[pulsewidth], 'start':[start], 'stop':[stop]}
    
    
    #Creates the main window
    def __init__(self, windowLength, windowBreadth):
        
        #Create the main window
        super(memristor_GUI, self).__init__()
        self.windowLength = windowLength
        self.windowBreadth = windowBreadth
        self.setGeometry(200, 200, self.windowLength, self.windowBreadth)
        self.setWindowTitle('Memristor Simulation')
        self.setWindowIcon(QIcon('memristor_icon.ico'))
        
        #Set default buttons pressed to False
        self.setMemristorParametersOKButtonClicked = False
        self.setWaveformsOKButtonClicked = False
        
        #Set Fontstyles
        self.titleFont = QFont("Times", 22, QFont.Bold)
        self.titleFont.setUnderline(True)
        self.writingFont = QFont("Calibri", 15)
        self.otherWritingFont = QFont("Arial", 13)
        self.buttonFont = QFont('Times', 13)
        
        #Used for small question icon
        self.pixmap = QPixmap('question1.png')
        
        #Draw background Image and the home screen
        self.drawBackgroundImage()
        self.home()
        self.show()
        
        
    #Draws the background Image    
    def drawBackgroundImage(self):
        backgroundImage =  QImage('memristor1.jpg')
        backgroundScaledImage = backgroundImage.scaled(QSize(900,700))
        palette = QPalette()
        palette.setBrush(10, QBrush(backgroundScaledImage))                     
        self.setPalette(palette)
        
    
    #Draws the homescreen    
    def home(self):
        
        #Set home window Title at top
        self.titleLabel = QLabel(self)
        self.titleLabel.setText('Memristor Simulation')
        self.titleLabel.setStyleSheet('QLabel{color:purple}')
        self.titleLabel.setFont(self.titleFont)
        self.titleLabel.setGeometry(QRect(self.windowLength/2 - 150, 10, 500, 50))
        
        
        #Create text box for number of Memristors to be simulated
        self.memristorLabel = QLabel(self)
        self.memristorLabel.setText('Memristors: ')
        self.memristorLabel.setFont(self.writingFont)
        self.memristorLabel.setGeometry(QRect(30, 75, 120, 50))
        
        self.memristorQLabel = QLabel(self)
        self.memristorQLabel.setPixmap(self.pixmap)
        self.memristorQLabel.setToolTip('Enter the number of Memristors \nyou' +
                                         ' want to simulate. Maximum = 10')
        self.memristorQLabel.move(370,85)
        
        self.memristorBox = QLineEdit(self)
        self.memristorBox.move(305, 88)
        self.memristorBox.resize(60,25)
        
        
        #Create Change parameters button to change default Memristor parameters
        self.changeParamButton = QPushButton('Change Parameters', self)
        self.changeParamButton.resize(140, 40)
        self.changeParamButton.move(665, 400)
        self.changeParamButton.clicked.connect(self.changeDefaultParameters)
        
        self.changeParamQLabel = QLabel(self)
        self.changeParamQLabel.setPixmap(self.pixmap)
        self.changeParamQLabel.setToolTip('Change Default Parameters')
        self.changeParamQLabel.move(815,402)
        
        
        #Create text box for Sampling Frequency of the simulation
        self.samplingFrequencyLabel = QLabel(self)
        self.samplingFrequencyLabel.setText('Sampling Frequency:')
        self.samplingFrequencyLabel.setFont(self.writingFont)
        self.samplingFrequencyLabel.setGeometry(QRect(30, 125, 220, 50))
        
        self.samplingFrequencyQLabel = QLabel(self)
        self.samplingFrequencyQLabel.setPixmap(self.pixmap)
        self.samplingFrequencyQLabel.setToolTip(' Sampling Frequency for \n output waveforms. Higher\n'+
                                                ' Frequency gives better \n results but require more \n'+
                                                ' time to compute')
        self.samplingFrequencyQLabel.move(370,135)
        
        self.samplingFrequencyBox = QLineEdit(self)
        self.samplingFrequencyBox.move(305, 138)
        self.samplingFrequencyBox.resize(60,25)
        
        
        #Display Default parameters in the homescreen
        self.displayDefaultParameters()
        
        
        #Create drop down lists for values to be plotted
        self.valueLabel = QLabel(self)
        self.valueLabel.setText('Plot Values: ')
        self.valueLabel.setFont(self.writingFont)
        self.valueLabel.setGeometry(QRect(30, 177, 220, 50))
        
        self.comboBox1 = QComboBox(self)
        self.comboBox1.addItem('Voltage')
        self.comboBox1.addItem('Current')
        self.comboBox1.addItem('Charge')
        self.comboBox1.addItem('Flux')
        self.comboBox1.addItem('Time')
        self.comboBox1.addItem('Resistance')
        self.comboBox1.move(305, 188)
        
        self.vsLabel = QLabel(self)
        self.vsLabel.setText('vs')
        self.vsLabelFont = QFont("Calibri", 12)
        self.vsLabel.setFont(self.vsLabelFont)
        self.vsLabel.setGeometry(QRect(420, 177, 80, 50))
        
        self.comboBox2 = QComboBox(self)
        self.comboBox2.addItem('Current')
        self.comboBox2.addItem('Voltage')
        self.comboBox2.addItem('Charge')
        self.comboBox2.addItem('Flux')
        self.comboBox2.addItem('Time')
        self.comboBox2.addItem('Resistance')
        self.comboBox2.move(455, 188)
        
        self.valueQLabel = QLabel(self)
        self.valueQLabel.setPixmap(self.pixmap)
        self.valueQLabel.setToolTip(' Values to be plotted. \n 1st Argument will \n' +
                                    ' be on the x-axis and \n 2nd argument on \n y-axis')
        self.valueQLabel.move(563,185)
        
        
        #Display On same plot checkbox?
        self.dispSamePlotLabel = QLabel(self)
        self.dispSamePlotLabel.setText('Display on Same Plot:')
        self.dispSamePlotLabel.setFont(self.otherWritingFont)
        self.dispSamePlotLabel.setGeometry(QRect(30, 257 + 40, 220, 50))
        
        self.dispSamePlotCheck = QCheckBox(self)
        self.dispSamePlotCheck.move(220, 267 + 40)
        
        self.dispSamePlotQLabel = QLabel(self)
        self.dispSamePlotQLabel.setPixmap(self.pixmap)
        self.dispSamePlotQLabel.setToolTip(' Display all the output \n Waveforms in the' + 
                                           ' same plot')
        self.dispSamePlotQLabel.move(237,307)
        
        #Display Waveform checkbox?
        self.dispWavePlotLabel = QLabel(self)
        self.dispWavePlotLabel.setText('Display Waveform Now:')
        self.dispWavePlotLabel.setFont(self.otherWritingFont)
        self.dispWavePlotLabel.setGeometry(QRect(265, 257 + 40, 220, 50))
        
        self.dispWavePlotCheck = QCheckBox(self)
        self.dispWavePlotCheck.move(453, 267 + 40)
        
        self.dispWaveQLabel = QLabel(self)
        self.dispWaveQLabel.setPixmap(self.pixmap)
        self.dispWaveQLabel.setToolTip(' Show Waveforms now?')
        self.dispWaveQLabel.move(470,307)
        
        
        #Save Waveform checkbox?
        self.savePlotLabel = QLabel(self)
        self.savePlotLabel.setText('Save Waveform:')
        self.savePlotLabel.setFont(self.otherWritingFont)
        self.savePlotLabel.setGeometry(QRect(30, 297 + 40, 220, 50))
        
        self.savePlotCheck = QCheckBox(self)
        self.savePlotCheck.move(220, 307 + 40)
        
        self.savePlotQLabel = QLabel(self)
        self.savePlotQLabel.setPixmap(self.pixmap)
        self.savePlotQLabel.setToolTip(' Save the plots?')
        self.savePlotQLabel.move(237,347)
        
        
        #Dropdown list File Extension for saving the waveform
        self.fileExtPlotLabel = QLabel(self)
        self.fileExtPlotLabel.setText('File Extension:')
        self.fileExtPlotLabel.setFont(self.otherWritingFont)
        self.fileExtPlotLabel.setGeometry(QRect(265, 297 + 40, 220 + 40, 50))
        
        self.comboBox3 = QComboBox(self)
        self.comboBox3.addItem('.pdf')
        self.comboBox3.addItem('.jpeg')
        self.comboBox3.addItem('.png')
        self.comboBox3.move(453, 307 + 40)
        self.comboBox3.resize(60,30)
        
        self.savePlotQLabel = QLabel(self)
        self.savePlotQLabel.setPixmap(self.pixmap)
        self.savePlotQLabel.setToolTip(' Extension of file for \n saving the plots.')
        self.savePlotQLabel.move(520,347)
        
        
        #Save path for saving the waveform
        self.savePathLabel = QLabel(self)
        self.savePathLabel.setText('Save Path:')
        self.savePathLabel.setFont(self.otherWritingFont)
        self.savePathLabel.setGeometry(QRect(30, 342 + 40, 220, 50))
        
        self.savePathBox = QLineEdit(self)
        self.savePathBox.move(140, 352 + 40)
        self.savePathBox.resize(400,29)
        
        self.savePathQLabel = QLabel(self)
        self.savePathQLabel.setPixmap(self.pixmap)
        self.savePathQLabel.setToolTip(' Save path for the plots.')
        self.savePathQLabel.move(550,392)
        
        
        #DPI
        self.dpiLabel = QLabel(self)
        self.dpiLabel.setText('DPI:')
        self.dpiLabel.setFont(self.otherWritingFont)
        self.dpiLabel.setGeometry(QRect(30, 382 + 40, 220, 50))
        
        self.dpiBox = QLineEdit(self)
        self.dpiBox.move(140, 392 + 40)
        self.dpiBox.resize(60,25)
        
        self.dpiQLabel = QLabel(self)
        self.dpiQLabel.setPixmap(self.pixmap)
        self.dpiQLabel.setToolTip(' Save path for the plots.')
        self.dpiQLabel.move(210,432)
        
        
        #Set Device Parameters (launches window for setting parameters for multiple Memristors)
        self.setParamButton = QPushButton('Set Device \n Parameters', self)
        self.setParamButton.resize(130, 50)
        self.setParamButton.move(240, 500)
        
        self.setParamButton.setStyleSheet('QPushButton {background-color: #A3C1DA; color: darkgreen;}')
        self.setParamButton.setFont(self.buttonFont)
        self.setParamButton.clicked.connect(self.setMemristorParameters)
        
        self.setParamQLabel = QLabel(self)
        self.setParamQLabel.setPixmap(self.pixmap)
        self.setParamQLabel.setToolTip(' Set parameters for all \n' +
                                       ' the Memristors')
        self.setParamQLabel.move(380,510)
        
        
        #Set waveforms (launches window to input waveform for multiple Memristors)
        self.setWavesButton = QPushButton('Set Waveforms', self)
        self.setWavesButton.resize(130, 50)
        self.setWavesButton.move(490, 500)
        
        self.setWavesButton.setStyleSheet('QPushButton {background-color: #A3C1DA; color: darkgreen;}')
        self.setWavesButton.setFont(self.buttonFont)
        self.setWavesButton.clicked.connect(self.setWaveforms)
        
        self.setWavesQLabel = QLabel(self)
        self.setWavesQLabel.setPixmap(self.pixmap)
        self.setWavesQLabel.setToolTip(' Set input Waveforms \n'+
                                       ' for different Memristors')
        self.setWavesQLabel.move(630,510)
        
        
        #Run Simulation
        self.runSimButton = QPushButton('Run Simulation', self)
        self.runSimButton.resize(130, 50)
        self.runSimButton.move(370, 570)
        
        self.runSimButton.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
        self.runSimButton.setFont(self.buttonFont)
        self.runSimButton.clicked.connect(self.runSimulation)
        
        self.runSimQLabel = QLabel(self)
        self.runSimQLabel.setPixmap(self.pixmap)
        self.runSimQLabel.setToolTip(' Run the simulations. \n'+
                                     ' Can take some time depending \n' +
                                     ' on comutational resources')
        self.runSimQLabel.move(510,580)
        
        
    #Form to change the paramters of the default Memristor    
    def changeDefaultParameters(self):
        self.txtD = QLineEdit(self)
        self.txtR_on = QLineEdit(self)
        self.txtR_off = QLineEdit(self)
        self.txtW = QLineEdit(self)
        self.txtMobility = QLineEdit(self)
        self.txtPolarity = QLineEdit(self)
        self.memristorTypeCB = QComboBox(self)
        self.memristorTypeCB.addItem('Ideal')
        btnOk = QPushButton('OK', self)
        
        self.DPGroupBox = QGroupBox("Default Paramters:")
        self.DPGroupBox.setStyleSheet('QGroupBox  {color: blue; font:bold 14px}')
        self.DPGroupBox.move(300, 300)
        layout = QFormLayout()
        
        layout.addRow(QLabel("D (nm):"), self.txtD)        
        layout.addRow(QLabel("R_on (\u03A9):"), self.txtR_on)  
        layout.addRow(QLabel("R_off (\u03A9):"), self.txtR_off)  
        layout.addRow(QLabel("W_0 (nm):"), self.txtW)  
        layout.addRow(QLabel("Mobility (pm/s):"), self.txtMobility)  
        layout.addRow(QLabel("Polarity (\u03B7):"), self.txtPolarity) 
        layout.addRow(QLabel("Type:"), self.memristorTypeCB) 
        layout.addRow(QLabel(), btnOk)
        self.DPGroupBox.setLayout(layout)
        
        btnOk.clicked.connect(self.readAndUpdateDefaultParameters)
        
    
    #Reads and updates the paramters of the default Memristor
    def readAndUpdateDefaultParameters(self):
        if(self.txtD.text() != ''):
            self.D = float(self.txtD.text()) * 10**-9
        if(self.txtR_on.text() != ''):
            self.R_on = float(self.txtR_on.text())
        if(self.txtR_off.text() != ''):
            self.R_off = float(self.txtR_off.text())
        if(self.txtW.text() != ''):
            self.W_0 = float(self.txtW.text()) * 10**-9
        if(self.txtMobility.text() != ''):
            self.mobility = float(self.txtMobility.text()) * 10**-12
        if(self.txtPolarity.text() != ''):
            self.polarity = int(self.txtPolarity.text())
        self.calculateFixedParameters()
        self.memristorType = self.memristorTypeCB.currentText()
        self.drawBackgroundImage()
        self.close()
        self.DPGroupBox.close()
        self.__init__(self.windowLength, self.windowBreadth)
        
    
    #Calculates default fixed dependent parameters
    def calculateFixedParameters(self):
        self.Q_0 = (self.D ** 2) / (self.mobility * self.R_on)
        self.R_delta = self.R_off - self.R_on
        self.R_0 = self.R_on * (self.W_0 / self.D) + self.R_off * (1 - self.W_0 / self.D)    
        
 
    #Displays the default paramters of a memristor    
    def displayDefaultParameters(self):
        #Create Default Parameters
        self.useDFParamsLabel = QLabel(self)
        self.useDFParamsLabel.setText('Default Parameters:')
        #self.useDFParamsLabelFont.setUnderline(True)
        self.useDFParamsLabel.setFont(self.writingFont)
        self.useDFParamsLabel.setGeometry(QRect(650, 75, 220, 50))
        
        self.DFParamsQLabel = QLabel(self)
        self.DFParamsQLabel.setPixmap(self.pixmap)
        self.DFParamsQLabel.setToolTip('Default Parameters when \nno input is provided.')
        self.DFParamsQLabel.move(860,85)
        
        self.paramFont = QFont("Arial", 12, QFont.Bold)
        self.DLabel = QLabel(self)
        self.DLabel.setText('D = ' + str(self.D / 10**-9) + ' nm')
        self.DLabel.setFont(self.paramFont)
        self.DLabel.setGeometry(QRect(675, 110, 220, 50))
        
        self.RoNLabel = QLabel(self)
        self.RoNLabel.setText('R_on = ' + str(self.R_on) + ' \u03A9')
        self.RoNLabel.setFont(self.paramFont)
        self.RoNLabel.setGeometry(QRect(675, 135, 220, 50))
        
        self.RoFFLabel = QLabel(self)
        self.RoFFLabel.setText('R_off = ' + str(self.R_off) + ' \u03A9')
        self.RoFFLabel.setFont(self.paramFont)
        self.RoFFLabel.setGeometry(QRect(675, 160, 220, 50))
        
        self.WLabel = QLabel(self)
        self.WLabel.setText('W_0 = ' + str(self.W_0/10**-9) +' nm')
        self.WLabel.setFont(self.paramFont)
        self.WLabel.setGeometry(QRect(675, 185, 220, 50))
        
        self.mobilityLabel = QLabel(self)
        self.mobilityLabel.setText('Mobility (\u03BC) = '+str(self.mobility/10**-12) + ' pm/s')
        self.mobilityLabel.setFont(self.paramFont)
        self.mobilityLabel.setGeometry(QRect(675, 210, 220, 50))
        
        self.polarityLabel = QLabel(self)
        self.polarityLabel.setText('Polarity (\u03B7) = ' + str(self.polarity))
        self.polarityLabel.setFont(self.paramFont)
        self.polarityLabel.setGeometry(QRect(675, 235, 220, 50))
        
        self.QLabel = QLabel(self)
        self.QLabel.setText('Q_0 = '+str(self.Q_0/10**-6) +' \u03BCC')
        self.QLabel.setFont(self.paramFont)
        self.QLabel.setGeometry(QRect(675, 260, 220, 50))
        
        self.R0Label = QLabel(self)
        self.R0Label.setText('R_0 = '+str(self.R_0)+' \u03A9')
        self.R0Label.setFont(self.paramFont)
        self.R0Label.setGeometry(QRect(675, 285, 220, 50))
        
        self.polarityLabel = QLabel(self)
        self.polarityLabel.setText('\u0394R = '+str(self.R_delta)+' \u03A9')
        self.polarityLabel.setFont(self.paramFont)
        self.polarityLabel.setGeometry(QRect(675, 310, 220, 50))
        
        self.typeLabel = QLabel(self)
        self.typeLabel.setText('Type : ' + str(self.memristorType))
        self.typeLabel.setFont(self.paramFont)
        self.typeLabel.setGeometry(QRect(675, 335, 220, 50))
        
    
    #Reads all the values in the different fields of the home screen
    def readValues(self):
        self.preferences = {}
        
        if(self.memristorBox.text() != ''):
            self.numberOfMemristors = int(self.memristorBox.text())
        self.preferences['number'] = self.numberOfMemristors
        
        if(self.samplingFrequencyBox.text() != ''):
            self.samplingFrequency = int(self.samplingFrequencyBox.text())
        self.preferences['sampling_frequency'] = self.samplingFrequency  
        
        if(self.dpiBox.text() != ''):
            self.dpi = int(self.dpiBox.text())
        self.preferences['dpi'] = self.dpi
        
        if(self.savePathBox.text() != ''):
            self.savePath = self.savePathBox.text()
        self.preferences['save_path'] = self.savePath
            
        self.preferences['x_axis'] = self.comboBox1.currentText()
        self.preferences['y_axis'] = self.comboBox2.currentText()
        self.preferences['format'] = self.comboBox3.currentText()
        
        self.preferences['display_same_plot'] = self.dispSamePlotCheck.isChecked()
        self.preferences['display_wave'] = self.dispWavePlotCheck.isChecked()
        self.preferences['save_plot'] = self.savePlotCheck.isChecked()  
        
    
     #Calls the core function and runs all the associated methods    
    def runSimulation(self):
        if(self.smp != None):
            self.setMemristorParametersOKButtonClicked = self.smp.getOKButton()
        if(self.sw != None):
            self.setWaveformsOKButtonClicked = self.sw.getOKButton()
            
        self.readValues()
        self.collectUserInput()
        self.data = {}
        if(self.setMemristorParametersOKButtonClicked == False and self.setWaveformsOKButtonClicked == False):
            self.data['memristor_parameters'] = self.defaultMemristorParameters
            self.data['wave_parameters'] = self.defaultWaveParameters
            
        elif(self.setMemristorParametersOKButtonClicked == True and self.setWaveformsOKButtonClicked == False):
            self.data['memristor_parameters'] = self.memristorParameters
            self.data['wave_parameters'] = self.defaultWaveParameters
            
        elif(self.setMemristorParametersOKButtonClicked == False and self.setWaveformsOKButtonClicked == True):
            self.data['memristor_parameters'] = self.defaultMemristorParameters
            self.data['wave_parameters'] = self.waveParameters
            
        elif(self.setMemristorParametersOKButtonClicked == True and self.setWaveformsOKButtonClicked == True):
            self.data['memristor_parameters'] = self.memristorParameters
            self.data['wave_parameters'] = self.waveParameters
            
        self.data['preferences'] = self.preferences
            
        cntrl.multiple_memristor_circuits(self.data)
                
        
           
    #Launches window to set the default paramters of the Memristor (connected to Set Paramters button)    
    def setMemristorParameters(self):
        self.readValues()
        self.smp = semp.set_memristor_parameters(self.numberOfMemristors)
        
        
    #Launches window to set the waveforms (connected to Set Waveforms button)    
    def setWaveforms(self):
        self.readValues()
        self.sw = sew.set_waveforms(self.numberOfMemristors)
        
        
    #Getter functions
    def collectUserInput(self):
        print(self.setWaveformsOKButtonClicked)
        if(self.setMemristorParametersOKButtonClicked == True): 
            self.memristorParameters = self.smp.getMemristorParamters()
            for i in self.memristorParameters:
                self.memristorParameters[i] = [self.defaultMemristorParameters[i][0] if x == None else x for x in self.memristorParameters[i]]
        
        if(self.setWaveformsOKButtonClicked == True):
            self.waveParameters = self.sw.getWaveParameters()
            for i in self.waveParameters:
                self.waveParameters[i] = [self.defaultWaveParameters[i][0] if x == None else x for x in self.waveParameters[i]]

    
    def getMemristorInput(self):
        return self.memristorParameters
    
    def getWaveInput(self):
        return self.waveParameters
    
    def getUserPreferences(self):
        return self.preferences
      
            
if __name__ == '__main__':   
    windowLength = 900
    windowBreadth = 800        
    app = 0
    app = QApplication(sys.argv)
    gui = memristor_GUI(windowLength, windowBreadth)
    sys.exit(app.exec_())
