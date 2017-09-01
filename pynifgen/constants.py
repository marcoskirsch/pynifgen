"""
Initialize the constants from the IVI header files

"""
import os
import re

def LoadConstants(include_path):
    """
    Grab constants from the NI-FGEN header files
    """
    hfiles = ['IviVisaType.h', 'ivi.h', 'iviFgen.h', 'niFgen.h', ]
    constant_list = []
    
    for hfile in hfiles:
        with open(os.path.join(include_path, hfile)) as include_file:
            constant_list.extend(ParseConstants(include_file))

    constant_pair = []
    for name, value in constant_list:
        
        try:
            exec('%s = %s' %(name, value))
            constant_pair.append([name, value])
        except NameError:
            continue
        
        except SyntaxError:
            continue
    
    return constant_pair


def ParseConstants(include_file):
    """
    Parse constants from a header file define statements
    """
#    define = re.compile(r'\#define\s+(\S+)\s+(".*"|\S+)')
    define = re.compile(r'\#define\s+(\S+)\s+(.+)')
#    m = define.match(line); print m.group(1), m.group(2)
    
    # search on each line
    constant_list = []
    for line in include_file:
        
        # remove comments within a line
        if '/*' in line:
            line = line[:line.find('/*')] + line[line.find('*/')+2:]

        # remove L after a long
        line = re.sub(r'((\d)L)',r"\2", line)

        m = define.match(line)

        if m:
            name = m.group(1)
            value = m.group(2).replace("(", "").replace(")", "")
            
            constant_list.append([name, value])
            
    return constant_list

