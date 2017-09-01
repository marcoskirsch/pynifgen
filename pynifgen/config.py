"""
Finds the header files for niFgen
"""

import sys
#import platform
import os
import ctypes

            
def GetHeaderFiles():
    """
    Returns the path of the niFgen header file
    
    
    Parameters
    ----------
    None
    
    
    Returns
    -------
    niFgen_hfile : string
        Full path of the niFgen.h header file.
        
    iviFgen_hfile : string
        Full path of the iviFgen.h header file.
    
    """

    # for windows
    if sys.platform.startswith('win') or sys.platform.startswith('cli'):

        if "IVIROOTDIR64" in os.environ:
            include_path = os.path.join(os.environ['IVIROOTDIR64'], r'Include')
            niFgen_hfile = os.path.join(include_path, 'niFgen.h')
            iviFgen_hfile = os.path.join(include_path, 'iviFgen.h')
            
        elif "IVIROOTDIR32" in os.environ:
            include_path = os.path.join(os.environ['IVIROOTDIR32'], r'Include')
            niFgen_hfile = os.path.join(include_path, 'niFgen.h')
            iviFgen_hfile = os.path.join(include_path, 'iviFgen.h')
            
        else:
            err_str = '\n\n\tMissing IVIROOTDIR environmental variable\n' + \
                      '\tNational Instruments NI-FGEN may not be installed\n' +\
                      '\tPlease download niFgen software from:\n' +\
                      '\twww.ni.com/download/ni-fgen-17.1/6751/en/'
            
            raise NotImplementedError(err_str)
    else:
            raise NotImplementedError('Sorry, only Windows supported (for now!)')
        
    if not os.path.isfile(niFgen_hfile):
        raise IOError("Header file missing at %s" & niFgen_hfile)
  
    if not os.path.isfile(iviFgen_hfile):
        raise IOError("Header file missing at %s" & iviFgen_hfile)
        
#    return niFgen_hfile, iviFgen_hfile
    return include_path
                      

def LoadniFgenLibary():
    """ Load NI-FGEN libaries """
    
    # for windows
    if sys.platform.startswith('win') or sys.platform.startswith('cli'):

        try:
            lib_name = "niFgen_64"
            niFgenlib = ctypes.windll.LoadLibrary(lib_name)
            niFgenlib_variadic = ctypes.cdll.LoadLibrary(lib_name)
            
        except:
            lib_name = "niFgen_32"
            niFgenlib = ctypes.windll.LoadLibrary(lib_name)
            niFgenlib_variadic = ctypes.cdll.LoadLibrary(lib_name)
            
    return niFgenlib, niFgenlib_variadic

