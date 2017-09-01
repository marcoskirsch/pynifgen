pynifgen Documentation
======================

Overview
--------
This Python package allows users to interface National Instruments signal generation hardware dirctly from Python and provides a viable alternative to using `LabVIEW <www.ni.com/en-us/shop/labview.html>`_ or the `MATLAB Instrument Control Toolbox <https://www.mathworks.com/products/instrument.html>`_.

To use this software you must install the NI-FGEN drivers provided by National Instruments, which can be downloaded at `NI-FGEN <http://www.ni.com/download/ni-fgen-17.1/6751/en/>`_.  Be aware that these drivers are not open-source and carry licensing restrictions, but still can be downloaded for free without purchasing LabVIEW.

This module supports Python2.7 and Python 3.3+ only under Windows.  National Instruments has not released a x64 version of their drivers for Linux or Mac OS.  Please ask them to support it.

This code was inspired by Pierre Cladé's `PyDAQmx <https://pypi.python.org/pypi/PyDAQmx>`_ and uses much of its documentation from National Instruments.  Thanks to all who directly and indirectly contributed to this code.

Feel free to contribute or report bugs on `GitHub <https://github.com/akaszynski/pynifgen/>`_.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   examples
   ViSession
   tests



Installation
------------

This package requires ``numpy`` and the NI-FGEN drivers.  Installation is straightforward using PyPi:

.. code::

    pip install pynifgen

The source code can also be downloaded from `GitHub <https://github.com/akaszynski/pynifgen/>`_ and installed with:

.. code::

    python setup.py install

Test installation with:

.. code::

    >>> import pynifgen
    >>> pynifgen.GetSoftwareInfo()

    [u'Driver: niFgen 17.1.1',
     u'Engine: IVI 17.00',
     u'Compiler: MSVC 13.00',
     u'Components: VISA-Spec 5.70']


Documentation
-------------

Detailed documentation and examples can be found at `pynifgen Documentation <http://pynifgen.readthedocs.io/en/latest/>`_.

Functions and classes are documented.  Run ``help`` on an individual function to see its doc_string.

.. code::

    >>> help(vi.ConfigureOutputEnabled)

    Help on method ConfigureOutputEnabled in module pynifgen.functions:
    
    ConfigureOutputEnabled(self, channelName='0', enabled=True) method of pynifgen.functions.PyViSession instance
        Configures the signal generator to generate a signal at the channel 
        output connector.
        
        
        Parameters
        ----------
        channelName : string, optional
            Specifies the channel name for which you want to enable the output.
            Defaults to "0"
            
        enabled : bool, optional
            Specifies whether you want to enable or disable the output.  
            Defaults to True.
        
        
        Returns
        -------
        vistatus : int
            Status code of this operation

Documentation was built from National Instruments documentation web pages.  Please see their documentation for additional help at `NI Signal Generators Help <http://zone.ni.com/reference/en-XX/help/370524P-01/fgencref/nifgen_functions/>`_.


Quick Example
-------------
The ``pynifgen`` package allows you to build code using both the C approach as well as a more convenient object-orientated approach in which the user creates a ``PyViSession`` object to store ViSession variables.

The following two examples show how you can setup a simulated PCI-5402 to sweep a square wave between 100 and 1000.  The first approach demonstrates the object orientated approach, while the second shows how one would generate the signal using the classic C approach.

The ``PyViSession`` approach:

.. code:: python

    import pynifgen
    import numpy as np

    # initialize a simulated PCI-5402
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


Again, the same example, except directly using the C functions.

.. code:: python

    import pynifgen
    import numpy as np
    import ctypes
    
    # initialize a simulated PCI-5402
    resourceName = 'simdev'
    optionString = 'Simulate=1,DriverSetup=Model:5402;BoardType:PCI'
    vi = ctypes.c_uint(0)
    pynifgen.niFgen_InitWithOptions(resourceName, True, True, optionString,
                                    vi)
    
    # Open channel 0
    pynifgen.niFgen_ConfigureChannels(vi, '0')
    
    # Abort generation of any previously generated signal
    pynifgen.niFgen_AbortGeneration(vi)
    
    # Configure output mode to frequency list
    pynifgen.niFgen_ConfigureOutputMode(vi, pynifgen.NIFGEN_VAL_OUTPUT_FREQ_LIST)
    
    # Clear frequency list
    pynifgen.niFgen_ClearFreqList(vi, -1)
    
    # Create frequency list
    npart = 100
    frequencyArray = np.linspace(100, 1000, npart)
    durationArray = np.empty_like(frequencyArray)
    durationArray[:] = 0.001                       # spend 1ms at each frequency
    fListHandle = ctypes.c_int() # frequency list handle
    pynifgen.niFgen_CreateFreqList(vi, pynifgen.IVIFGEN_VAL_WFM_SQUARE,
                                   frequencyArray.size, frequencyArray,
                                   durationArray,
                                   fListHandle)
    
    # set amplitude to 2V dcOffset to -0.1V
    pynifgen.niFgen_ConfigureFreqList(vi, '0', fListHandle, 2.0, -0.1, 0)
    
        # Enable and start generation
    pynifgen.niFgen_ConfigureOutputEnabled(vi, '0', True)
    pynifgen.niFgen_InitiateGeneration(vi)
    
    # get hardware state
    state = ctypes.c_int() # frequency list handle
    pynifgen.niFgen_GetHardwareState(vi, state)
    print(state.value)

The biggest difference between the two examples is the ``PyViSession`` is that the ctypes interface takes place "under the hood".  For example, checking the hardware status is more pythonic as the state of the hardware is returned as an integer and the variable does not need to be created by the user or have its underlying value accessed.

Supported Hardware
------------------
The hardware supported by this software depends on the version of the NI-FGEN drivers and the OS being used.  NI-FGEN v17.1 supports:

- PCI-5401
- PCI-5402
- PCI-5406
- PCI-5411
- PCI-5412
- PCI-5421
- PCI-5431
- PXI-5401
- PXI-5402
- PXI-5404
- PXI-5406
- PXI-5411
- PXI-5412
- PXI-5421
- PXI-5422
- PXI-5431
- PXI-5441
- PXIe-5413
- PXIe-5423
- PXIe-5433
- PXIe-5442
- PXIe-5450
- PXIe-5451


Bug Reporting and Feature Requests
----------------------------------
If you find a bug, please open an issue here: `Issues <https://github.com/akaszynski/pynifgen/issues/>`_.  For feature requests or other questions, please contact me at akascap@gmail.com.


License
-------
This this Python software is under the MIT License.  See the ``LICENSE`` file.


