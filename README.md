# SurfaceSciencePython
Rewrite of code for a high vaccuum surface science experiment from LabView to Python to improve readability by students.

On a note of how the program looks, most of the code was done as function calls to best condense the code, improve readability, and emulate the behavior of the LabView program.

The experiment utilizes an National Insturments DAQ so this project realies heavily on the nidaqmx package. The purpose of this project is to enable undergraduate and graduate students to be able to read and understand the code for this experiment which was previously a LabView virtual instrument with no comments at all.
National Instruments DAQmx and the corresponding python package is an important part of this code and warrants further reading for complete understanding of this project. A basic overview is provided at the wiki of this repository.

This program was tested with my personal NI USB-6009 to verify functionality before running on the actual apparatus.
