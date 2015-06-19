# iota-osc-optimization

The contents of this directory is for the optimization of the Optical Stochastic Cooling Experiment to be demonstrated in the IOTA ring.

The longitudinal position of each particle in the bunch in transit from the pick-up to the kicker must not fall outside of the radiation length of the correcting pulse--0.2um. We describe the bypass in the file "iota9_18cm.madx". This is version 9 which includes 18cm-long dipoles.

To generate a matched beam for the bypass, the aforementioned file must first be run to generate the ring's eigenvectors. A file called "ptc_track" will be generated. With this file you may generate the beam distribution with "beamgen.py" or "sigma_eignevector". After running one of these files, input.beam** will be generated based on the variables specifed. 

You are now ready to run the matched particles through the bypass.
