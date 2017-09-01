import warnings
from pynifgen._version import __version__

# on default will raise error when an error is encountered with NI
raise_on_error = True

#Load libaries and path on module initialization
from pynifgen import config
from pynifgen import constants
from pynifgen import functions
#from functions import *

try:
    include_path = config.GetHeaderFiles()
    niFgenlib, niFgenlib_variadic = config.LoadniFgenLibary()
    
    # store constants
    constant_list = constants.LoadConstants(include_path)
    for name, value in constant_list:
        exec('%s = %s' %(name, value))
    
    # store functions
    func_list, func_strings = functions.FunctionFactory(include_path)
    for func_string in func_strings:
        exec(func_string)

except Exception as e:
    warnings.warn('Unable to load NI-FGEN libaries')
    print(e)
    
from pynifgen.functions import *
