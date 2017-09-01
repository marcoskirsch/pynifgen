Tests
=====
The ``pynifgen`` package contains several built in tests to test the functionality of the NI-FGEN drivers and the Python install.  These tests use simulated devices and can be used to verify the proper installation of ``pynifgen``.  Run all tests with:

.. code::

    >>> from pynifgen import tests
    >>> tests.RunAll()

    ###############################################################################
    Simulating a PCI-5421 to generate an arbitrary waveform
            Resource Name: PXI1Slot2 
            Sample Rate in Hz: 40000000.000000 
            Gain: 1.000000 
            DC Offset: 0.000000 
            Generating sequence for 1.500000 seconds... success
    
    
    ###############################################################################
    Simulating synchronized sine wave generation across two 5404 boards with:
            Resource 1: sim_PXI1Slot2: 
            Resource 2: sim_PXI1Slot3: 
            Both Devices Frequency in Hz: 40000000.000000 
            Both Devices Amplitude in Vp-p: 2.000000 
            Resource 2 Start Phase in degrees: 90.000000 
            For: 1.500000 seconds
    
            Generating... success
    
    
        ###############################################################################
        Simulating a PCI-5404 to produce a clock pulse (square wave) with:
                Resource Name: simdev 
                Frequency in Hz 40000000.000000 
                Amplitude in Volts {1.8 | 3.3 | 5.0}: 1.800000 
                Duty Cycle in %: 50.000000 
        
                Generating clock pulse for one second... success
        
        
        ################################################################
        Calibrating a simulated PCI-5421
                This operation is not supported for a simulated device.
        
        
        ###############################################################################
        Simulating a PCI-5402 sweeping a square wave with:
        Driver: niFgen 17.1.1
        Engine: IVI 17.00
        Compiler: MSVC 13.00
        Components: VISA-Spec 5.70
        instrRev: Not available while simulating
        
        Frequency List Capabilities Query:
                 maximumNumberOfFreqLists      9999
                 minimumFrequencyListLength    1
                 maximumFrequencyListLength    58253
                 minimumFrequencyListDuration  1.2800E-06
                 maximumFrequencyListDuration  1250973.574906
                 frequencyListDurationQuantum  8.0000E-08
        
        
        
        ###############################################################################
        Simulating a PCI-5402 to produce a frequency sweep with:
                Resource Name: simdev 
                Amplitude in Vp-p: 2.000000 
                Start Frequency in Hz: 1000000.000000 
                Stop Frequency in Hz: 10000000.000000 
                Number of Frequency Steps: 100 
                Duration in ms / Step: 10.000000 
        
                Sweeping... success
        
        
        ###############################################################################
        Simulating a PCI-5404 to produce a sine wave with:
                Resource Name: simdev 
                Frequency in Hz 40000000.000000 
                Amplitude in Volts {1.8 | 3.3 | 5.0}: 1.800000 
                Start Phase in degrees: 0.000000 
                For: 1.500000 seconds
        
                Generating... success