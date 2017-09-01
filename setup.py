"""
Installation file for pynifgen module
"""

from setuptools import setup
import os
from io import open as io_open

package_name = 'pynifgen'

# Get version from tqdm/_version.py
__version__ = None
this_file = os.path.dirname(__file__)
version_file = os.path.join(this_file, package_name, '_version.py')
with io_open(version_file, mode='r') as fd:
    # execute file from raw string
    exec(fd.read())
    

# Actual setup
setup(
    name=package_name,
    packages = [package_name],#, 'nifgen.tests', 'nifgen.examples'],

    # Version
    version=__version__,

    description="Python Interface to National Instrument's NI-FGEN Driver",
    long_description=open('README.rst').read(),

    # Author details
    author='Alex Kaszynski',
    author_email='akascap@gmail.com',

    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    # Website
    url = 'https://github.com/akaszynski/pynifgen',
                           
    keywords='national instruments nifgen',
                           
#    package_data={'vtkInterface.examples': ['airplane.ply', 'ant.ply', 
#                                            'hexbeam.vtk', 'sphere.ply']},

    install_requires=['numpy'],

)
