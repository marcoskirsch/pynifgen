Examples
========
The following examples were built using C examples from NI-FGEN and tested with NI-FGEN 17.1.1.  These examples use simulated hardware and can be used to test code configuration before applying them to actual hardware.


Standard Waveform
-----------------
This example generates a sine wave using the standard waveform generator in NI-FGEN.  The type of waveform is controlled by the ``waveform`` string parameter can one of the following strings:


=================================  =========================
   String                          Waveform
=================================  =========================
``"NIFGEN_VAL_WFM_SINE"``          Sinusoidal waveform
``"NIFGEN_VAL_WFM_SQUARE"``        Square waveform
``"NIFGEN_VAL_WFM_TRIANGLE"``      Triangular waveform
``"NIFGEN_VAL_WFM_RAMP_UP"``       Positive ramp waveform
``"NIFGEN_VAL_WFM_RAMP_DOWN"``     Negative ramp waveform
``"NIFGEN_VAL_WFM_DC"``            Constant voltage
``"NIFGEN_VAL_WFM_NOISE"``         White noise
=================================  =========================


This example uses a simulated PCI-5404 to generate a sine wave for 1.5 seconds.

.. code:: python

    from __future__ import print_function
    
    import pynifgen
    import time
    import numpy as np

    resource = 'simdev'
    frequency = 40000000
    amplitude = 1.8
    startPhase = 0
    tgen = 1.5
    waveform = "NIFGEN_VAL_WFM_SINE"
    
    print('Simulating a PCI-5404 to produce a sine wave with:')
    print("\tResource Name: %s "% resource)
    print("\tFrequency in Hz %lf "% frequency)
    print("\tAmplitude in Volts {1.8 | 3.3 | 5.0}: %lf "% amplitude)
    print("\tStart Phase in degrees: %f ", startPhase)
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
    print ('\n\tGenerating... ', end='\r')
    time.sleep(tgen)
    print ('success\n\n')
    
    # close the session
    vi.close()


This example can be run from ``pynifgen`` by running:

.. code::

    >>> from pynifgen import tests
    >>> tests.ClockPulse()
    
    Simulating a PCI-5404 to produce a sine wave with:
            Resource Name: simdev 
            Frequency in Hz 40000000.000000 
            Amplitude in Volts {1.8 | 3.3 | 5.0}: 1.800000 
            Start Phase in degrees: %f  0
            For: 1.500000 seconds
            
            Generating... success



Clock Pulse
-----------
This is an example of using FGEN with the PXI-5404 to produce a clock pulse (square wave) using ``pynifgen``'s ``visession`` object.

.. code:: python

    from __future__ import print_function
    
    import pynifgen
    import time
    import numpy as np
    
    resource = 'simdev'
    amplitude = 1.8
    frequency = 40000000
    dutyCycle = 50
    
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
    print ('\n\tGenerating clock pulse for one second... ', end='\r')
    time.sleep(1)
    print ('success\n\n')
    
    # close the session
    vi.close()


This example is built in an can be run with:

.. code::

    >>> from pynifgen import tests
    >>> tests.ClockPulse()
    
    Simulating a PCI-5404 to produce a clock pulse (square wave) with:
            Resource Name: simdev 
            Frequency in Hz 40000000.000000 
            Amplitude in Volts {1.8 | 3.3 | 5.0}: 1.800000 
            Duty Cycle in %: 50.000000 
    
            Generating clock pulse for one second... success
    


Frequency Sweep
---------------
This example demonstrates using ``pynifgen`` to produce a frequency sweep using a frequency array.

.. code:: python

    from __future__ import print_function
    
    import pynifgen
    import time
    import numpy as np

    resource = 'simdev'
    amplitude = 2.0
    startFreq = 1E+6
    stopFreq = 10E+6
    numSteps = 100
    timeDelayInMilliseconds = 10.0
    
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
    print ('\n\tGenerating clock pulse...', end='\r')
    time.sleep(durationArray.sum())
    print ('success\n\n')
    
    # close the session
    vi.close()


This example is built in an can be run with:

.. code::

    >>> from pynifgen import tests
    >>> tests.SineSweep()

    Simulating a PCI-5402 to produce a frequency sweep with:
            Resource Name: simdev 
            Amplitude in Vp-p: 2.000000 
            Start Frequency in Hz: 1000000.000000 
            Stop Frequency in Hz: 10000000.000000 
            Number of Frequency Steps: 100 
            Duration in ms / Step: 10.000000 
    
            Sweeping...success


Board Syncronization
--------------------
This example demonstrates how to synchronize the generation of two sine waves across two PXI-5404 boards.


.. code:: python

    from __future__ import print_function
    
    import pynifgen
    import time
    import numpy as np

    resource1 = "sim_PXI1Slot2"
    resource2 = "sim_PXI1Slot3"
    frequency = 40E+6
    amplitude = 2.0
    phase2 = 90.0
    tgen = 1.5
    
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
    print ('\n\tGenerating... ', end='\r')
    time.sleep(tgen)
    print ('success\n\n')
    
    # close the sessions
    vi_1.close()
    vi_2.close()


This example is built in an can be run with:

.. code::

    >>> from pynifgen import tests
    >>> tests.BoardSync()

    Simulating synchronized sine wave generation across two 5404 boards with:
            Resource 1: sim_PXI1Slot2: 
            Resource 2: sim_PXI1Slot3: 
            Both Devices Frequency in Hz: 40000000.000000 
            Both Devices Amplitude in Vp-p: 2.000000 
            Resource 2 Start Phase in degrees: 90.000000 
            For: 1.500000 seconds
    
            Generating... success


Basic Arbitrary Waveform
------------------------
The procedure below provides the basic steps required to configure Arbitrary Sequence mode within ``pynifgen``.

.. code:: python

    from __future__ import print_function
    
    import pynifgen
    import time
    import numpy as np

    resource = "PXI1Slot2"
    sampleRate = 40e+6
    gain = 1.0
    dcOffset = 0.0
    tgen = 1.5
          
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
    print(string, end='\r')
    time.sleep(tgen)
    print('success\n\n')
    
    vi.close()


This example is built in an can be run with:

.. code::

    >>> from pynifgen import tests
    >>> tests.ArbitraryWaveform()
    Simulating a PCI-5421 to generate an arbitrary waveform
            Resource Name: PXI1Slot2 
            Sample Rate in Hz: 40000000.000000 
            Gain: 1.000000 
            DC Offset: 0.000000 
            Generating sequence for 1.500000 seconds... success


Calibration
-----------
Calibration can be run from ``pynifgen`` via:

.. code::

    # initialize the simulated device
    option = 'Simulate=1,DriverSetup=Model:5421;BoardType:PXI'
    vi = pynifgen.PyViSession('simdev', optionString=option)
    vi.SelfCal() # will raise an error as this is a simulated device

Please note that simulated devices do not calibrate and an error will be raised.

