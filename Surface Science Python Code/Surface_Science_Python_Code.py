from time import sleep
import nidaqmx
import numpy as np
import scipy as sp
from matplotlib import pyplot as plt
from datetime import datetime
"""
TO DO:
    !!!!REWRITE PLOTTING TO BE REAL TIME!!!!

    Save Settings
    Timing precise to better than 1 millisecond
    Alignment mode 
    Averaging
    Dead time for reset
    Use both counting and lock in for data
    Autoscaling on or off
    Multiplex mode (scan different regions)

"""
"""
WORKING ON ERROR HANDLING PRESENTLY
    Program should reset upon error (ask user if reset? yee)
    continuous running until user set defined stop
    Add averaging function

"""

def acq(start,stop,step,steptime):
    #Code for acquisition based on start and stop and step eV values
    arr = np.arange(start,stop+step,step) #sets up the array of eV values
    val = np.zeros(len(arr)) #predefines the readings array
    with nidaqmx.Task() as anOt, nidaqmx.Task() as anIn:    #Uses nidaqmx to assign channels as analogue out and analogue in
        """
        MAKE SURE TO CHANGE MAX VAL TO 10 FOR ACTUAL DEVICE
        """
        anOt.ao_channels.add_ao_voltage_chan("Dev1/ao0",min_val=0,max_val=10)
        anIn.ai_channels.add_ai_voltage_chan("Dev1/ai0")

        i = int(0)
        for i in range(len(arr)):
            anOt.write(0.00293*arr[i])#Sets the DAQ output voltage. TBH, I have no idea what this multiplicative constant is, but its in the LabView code, so here it is. 
            #sleep(.01)
            val[i]=anIn.read()
            sleep(steptime/1000)
    return np.array([arr,val])

def save(vals):
    now = datetime.now()
    current_time = now.strftime("%d_%m_%Y--%H-%M-%S")
    #print(current_time)
    np.savetxt(current_time+".csv",(vals[:][:]), delimiter=',')

def plotin(vals):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(vals[0],vals[1])
    plt.show()
    sleep(.1)
    plt.close()


def HMI(userInput):
    if userInput == "y" or userInput == "Y" or userInput == "1":
        return 1
    elif userInput == "n" or userInput == "N" or userInput == "2":
        return 0
    else:
        print("Please input either one of the listed options")
        return -1

def numHMI(userInput):
    try:
        return float(userInput)
    except ValueError as ve:
        return "Err"
        print("Incorrect entry")

"""
def peakDet(values,thrshold,width):
    return scipy.signal.find_peaks(values[0][:])
"""


def startup():
    startEV = numHMI(input("Input start eV value: "))
    stopEV = numHMI(input("Input stop eV: "))
    stepEV = numHMI(input("Input step eV: "))
    stepTime = numHMI(input("Input time per step in ms: "))
    singCont = input("Single sweep(1) or continuous(2)?: ")
    if HMI(singCont) == 2:
        sweepNum = numHMI(input("How many sweeps to do?: ")) #Need to work on
        for i in range(int(sweepNum)):
            values=acq(startEV,stopEV,stepEV,stepTime)
            plotin(values)
            #saveYN = HMI(input("Do you want to save? (Y/N): "))
            #if saveYN == 1: 
            #    save(values)
        #print("Data acquisition finished")
    elif HMI(singCont) == 1:
        values=acq(startEV,stopEV,stepEV,stepTime)
        plotin(values)
        saveYN = HMI(input("Do you want to save? (Y/N): "))
        if saveYN == 1: 
            save(values)
        
        
startup()


"""    
values=acq(0,5,.25,10)
save(values)
plotin(values)
"""