from __future__ import print_function

import inspect
import sys
import time

import pynifgen
import numpy as np

def RunAll():
    """ Runs all the functions within this module """
    testfunctions = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isfunction(obj) and name != 'RunAll':
              testfunctions.append(obj)      

    # run all the functions
#    any(f() for f in testfunctions)
    for f in testfunctions:
        print('#'*79)
        f()
    

def Simulate5402():
    """
    Tests if pynifgen can simulate a 5402 square wave sweep
    
    
    Parameters
    ----------
    None
    
    
    Returns
    -------
    None
    
    """
    
    # initialize a Simulate a PCI-5402
    option = 'Simulate=1,DriverSetup=Model:5402;BoardType:PCI'
    vi = pynifgen.PyViSession('simdev', optionString=option)
    
    # open channel 0
    vi.ConfigureChannels("0")
    
    # Abort generation of any previously generated signal
    vi.AbortGeneration()
    
    # Configure output mode to frequency list
    vi.ConfigureOutputMode("NIFGEN_VAL_OUTPUT_FREQ_LIST")
    
    # create frequency list
    npart = 100
    frequencyArray = np.linspace(100, 1000, npart)
    durationArray = np.empty_like(frequencyArray)
    durationArray[:] = 0.001                       # spend 1ms at each frequency
    vistatus, frequencyListHandle = vi.CreateFreqList("IVIFGEN_VAL_WFM_SQUARE",
                                                      frequencyArray,
                                                      durationArray)
    
    # set amplitude to 2V dcOffset to -0.1V
    vi.ConfigureFreqList('0', frequencyListHandle, amplitude=2.0, dcOffset=0.1, 
                         startPhase=0)
    
    
    # Enable
    vi.ConfigureOutputEnabled()
    vi.InitiateGeneration()
    
    # get hardware state
    vi.GetHardwareState()
    
    # print results
    print('Simulating a PCI-5402 sweeping a square wave with:')
    vistatus, driverRev, instrRev = vi.revision_query()
    for string in driverRev.split(', '):
        print(string)
    print('instrRev: {:s}'.format(instrRev))
        
    query = vi.QueryFreqListCapabilities()
    print('')
    print('Frequency List Capabilities Query:')
    print('\t maximumNumberOfFreqLists      {:d}'.format(query[1]))
    print('\t minimumFrequencyListLength    {:d}'.format(query[2]))
    print('\t maximumFrequencyListLength    {:d}'.format(query[3]))
    print('\t minimumFrequencyListDuration  {:.4E}'.format(query[4]))
    print('\t maximumFrequencyListDuration  {:f}'.format(query[5]))
    print('\t frequencyListDurationQuantum  {:.4E}'.format(query[6]))
    print('\n\n')    
    
    
def ClockPulse(resource='simdev', amplitude=1.8, frequency=40000000, 
               dutyCycle=50):
    """
    Simulates a PCI-5404 to produce a clock pulse (square wave)
    
    
    """

    print('Simulating a PCI-5404 to produce a clock pulse (square wave) with:')
    print("\tResource Name: %s "% resource);
    print("\tFrequency in Hz %lf "% frequency);
    print("\tAmplitude in Volts {1.8 | 3.3 | 5.0}: %lf "% amplitude);
    print("\tDuty Cycle in %%: %lf "% dutyCycle);
    
    # initialize a simulated a PCI-5404
    option = 'Simulate=1,DriverSetup=Model:5404;BoardType:PXI'
    vi = pynifgen.PyViSession(resource, optionString=option)
    
    
    # configure waveform
    vi.ConfigureStandardWaveform("0", 
                                 "NIFGEN_VAL_WFM_SQUARE", 
                                 amplitude=amplitude, # V 
                                 frequency=frequency) # hz
    
    # configure duty cycle
    vi.SetAttributeViReal64("0", 'NIFGEN_ATTR_FUNC_DUTY_CYCLE_HIGH', dutyCycle)
    vi.InitiateGeneration()
    vi.ConfigureOutputEnabled()
    
    # wait while sweep runs
    print ('\n\tGenerating clock pulse for one second... ', end='')
    time.sleep(1)
    print ('success\n\n')
    
    # close the session
    vi.close()


#%% Example of simulating a PCI-5404 to produce a sine wave
def StandardWaveform(resource='simdev', amplitude=1.8, frequency=40000000, 
                     startPhase=0, tgen=1.5, waveform='NIFGEN_VAL_WFM_SINE'):
    """"
    Allowable entries for waveform:
    "NIFGEN_VAL_WFM_SINE"            Sinusoidal waveform
    "NIFGEN_VAL_WFM_SQUARE	"          Square waveform
    "NIFGEN_VAL_WFM_TRIANGLE"        Triangular waveform
    "NIFGEN_VAL_WFM_RAMP_UP"         Positive ramp waveform
    "NIFGEN_VAL_WFM_RAMP_DOWN"       Negative ramp waveform
    "NIFGEN_VAL_WFM_DC Constant"     Constant voltage
    "NIFGEN_VAL_WFM_NOISE"           White noise
    """
    
    print('Simulating a PCI-5404 to produce a sine wave with:')
    print("\tResource Name: %s "% resource)
    print("\tFrequency in Hz %lf "% frequency)
    print("\tAmplitude in Volts {1.8 | 3.3 | 5.0}: %f "% amplitude)
    print("\tStart Phase in degrees: %f "% startPhase)
    print("\tFor: %f seconds"% tgen)
    
    # initialize a simulated a PCI-5404
    option = 'Simulate=1,DriverSetup=Model:5404;BoardType:PXI'
    vi = pynifgen.PyViSession(resource, optionString=option)
    
    # configure waveform
    vi.ConfigureStandardWaveform("0", 
                                 waveform, 
                                 amplitude=amplitude, # V 
                                 frequency=frequency,
                                 startPhase=startPhase)
    
    # start
    vi.InitiateGeneration()
    vi.ConfigureOutputEnabled()
    
    
    # wait while sweep runs
    print ('\n\tGenerating... ', end='')
    time.sleep(tgen)
    print ('success\n\n')
    
    # close the session
    vi.close()
    
def SineSweep(resource='simdev', amplitude=2.0, startFreq=1E6, stopFreq=10E6,
              numSteps=100, timeDelayInMilliseconds=10.0):
    """
    Example of using FGEN with the 5402 to produce a frequency sweep.
    Square wave generation using frequency list.
    A logarithmic scale is used to determine the frequencies to sweep over.
    """

    print('Simulating a PCI-5402 to produce a frequency sweep with:')
    print("\tResource Name: %s "% resource)
    print("\tAmplitude in Vp-p: %lf "% amplitude)
    print("\tStart Frequency in Hz: %lf "% startFreq)
    print("\tStop Frequency in Hz: %lf "% stopFreq)
    print("\tNumber of Frequency Steps: %d "% numSteps)
    print("\tDuration in ms / Step: %lf "% timeDelayInMilliseconds)
    
    # initialize a simulated a PCI-5402
    option = 'Simulate=1,DriverSetup=Model:5402;BoardType:PXI'
    resource = 'simdev'
    vi = pynifgen.PyViSession(resource, optionString=option)
    
    # configure waveform
    
    frequencyArray = np.logspace(np.log10(startFreq), np.log10(stopFreq))
    
    # create frequency array
    frequencyArray = np.linspace(100, 1000, numSteps)
    durationArray = np.empty_like(frequencyArray)
    durationArray[:] = timeDelayInMilliseconds / 1000 # in seconds
    
    # configure to use frequency list
    vi.ConfigureOutputMode("NIFGEN_VAL_OUTPUT_FREQ_LIST")
    vistatus, frequencyListHandle = vi.CreateFreqList("NIFGEN_VAL_WFM_SQUARE",
                                                      frequencyArray,
                                                      durationArray)
    vi.InitiateGeneration()
    vi.ConfigureOutputEnabled()
    
    # wait while sweep runs
    print ('\n\tSweeping... ', end='')
    time.sleep(durationArray.sum())
    print ('success\n\n')
    
    # close the session
    vi.close()
    
    
def BoardSync(frequency=40E6, amplitude=2.0, phase2=90, tgen=1.5):
    
    """
    Example of using FGEN to synchronize two 5404 boards
    """
    resource1 = "sim_PXI1Slot2"
    resource2 = "sim_PXI1Slot3"
    
    print('Simulating synchronized sine wave generation across two 5404 boards with:')
    print("\tResource 1: %s: "% resource1)
    print("\tResource 2: %s: "% resource2)
    print("\tBoth Devices Frequency in Hz: %f "% frequency)
    print("\tBoth Devices Amplitude in Vp-p: %lf "% amplitude)
    print("\tResource 2 Start Phase in degrees: %lf "% phase2)
    print("\tFor: %f seconds"% tgen)
    
    
    # initialize sessions on each of the two 5404 boards.
    option = 'Simulate=1,DriverSetup=Model:5404;BoardType:PXI'
    vi_1 = pynifgen.PyViSession(resource1, optionString=option)
    vi_2 = pynifgen.PyViSession(resource2, optionString=option)
    
    # configure the boards with sine waves each with the same given frequency and 
    # amplitude.  Device 2 also gets initialized with a starting phase value.
    vi_1.ConfigureStandardWaveform("0", "NIFGEN_VAL_WFM_SINE", amplitude, 0, 
                                   frequency, 0.00)
    vi_2.ConfigureStandardWaveform("0", "NIFGEN_VAL_WFM_SINE", amplitude, 0,
                                   frequency, phase2)
    
    # the following instructions are used to synchronize the two boards.
    
    # first, configure the reference clock source for each board
    vi_1.ConfigureReferenceClock("PXI_Clk10", 10e6)
    vi_2.ConfigureReferenceClock("PXI_Clk10", 10e6)
       
    
    # device 1 is set to start on a software trigger.  This trigger is also routed to RTSI 0
    # and the second device is told to wait for a trigger on this line (RTSI 0)
    vi_1.ConfigureSoftwareEdgeStartTrigger()
    vi_1.ExportSignal("NIFGEN_VAL_START_TRIGGER", "", "RTSI0")
    vi_2.ConfigureDigitalEdgeStartTrigger("RTSI0", "NIFGEN_VAL_RISING_EDGE")
    
    # This would normally cause the boards to start outputting the sine waves.  But
    # because of the triggers, it doesn't.  Here we set everything up so that 
    # they're both just waiting on the trigger.
    vi_2.InitiateGeneration()
    vi_2.ConfigureOutputEnabled()
    vi_1.InitiateGeneration()
    vi_1.ConfigureOutputEnabled()
    
    # once the trigger is fired, both boards start outputting at the same time.
    vi_1.SendSoftwareEdgeTrigger("NIFGEN_VAL_START_TRIGGER")
    
    # Note
    # At this point, in order to synchronize correctly, to bring the two waveforms 
    # in or out of phase, it would be necessary to add an on-the-fly correction for
    # phase shifts.  By changing the phase of the second device (remember, we're 
    # only in control of the second one), we can alter the phase difference of the 
    # two waveforms.
    
    # wait while sweep runs
    print ('\n\tGenerating... ', end='')
    time.sleep(tgen)
    print ('success\n\n')
    
    # close the sessions
    vi_1.close()
    vi_2.close()
    
    
def ArbitraryWaveform(sampleRate=40E6, gain=1.0, dcOffset=0.0, tgen=1.5):
    """
    Configures a simulated PCI-5421 to generate an arbitrary waveform
    """
    
    resource = "PXI1Slot2"
          
    print('Simulating a PCI-5421 to generate an arbitrary waveform')
    print("\tResource Name: %s "% resource);
    print("\tSample Rate in Hz: %f "% sampleRate);
    print("\tGain: %f "% gain);
    print("\tDC Offset: %lf "% dcOffset)
    
    # create a random waveform
    wfm_size = 2**8
    waveformDataArray = np.random.random(wfm_size) - 0.5
    
    # initialize the simulated device
    option = 'Simulate=1,DriverSetup=Model:5421;BoardType:PXI'
    vi = pynifgen.PyViSession(resource, optionString=option)
    # help(vi.QueryArbSeqCapabilities)
    #vi.QueryArbSeqCapabilities()
    #(0, 2097151, 1, 16777205, 16777215)
    
    # configure outputmode
    vi.ConfigureOutputMode("NIFGEN_VAL_OUTPUT_ARB")
    
    # create and configure waveform
    vi_status, waveformHandle = vi.CreateWaveformF64("0", waveformDataArray)
    vi.ConfigureArbWaveform('0', waveformHandle, gain, dcOffset)
    #vi.ConfigureArbSequence("0", waveformHandle, gain, dcOffset)
    
    # Configure sample clock mode and rate
    vi.ConfigureClockMode('NIFGEN_VAL_HIGH_RESOLUTION')
    vi.ConfigureSampleRate(sampleRate)
    
    # Enable output and start generating
    vi.InitiateGeneration()
    vi.ConfigureOutputEnabled()
    
    string = "\tGenerating sequence for %f seconds... "% tgen
    print(string, end='')
    time.sleep(tgen)
    print('success\n\n')
    
    vi.close()
    
    
def SelfCalibration():
    """
    Simulates a calibration
    """
    
    # initialize the simulated device
    option = 'Simulate=1,DriverSetup=Model:5421;BoardType:PXI'
    vi = pynifgen.PyViSession('simdev', optionString=option)
    
    print('Calibrating a simulated PCI-5421')
    
    try:
        vi.SelfCal() # will raise an error as this is a simulated device
    except:
        print('\tThis operation is not supported for a simulated device.\n\n')