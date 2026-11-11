"""
======
NIMBLE - a large-scale Hartree-Fock program
===========================================
Nearsighted Integral-Optimized Matrix-Based Large-Scale Electronic Structure Prediction
=           =                  =      =     =           =
=======================================================================================
version 3.10

This Hartree-Fock program is focused on fast calculations for large systems.

The key priciples:
    - Nearsightedness: Based on this principle by Walter Kohn, irrelevant and long-range interactions can be ignored.
    - Integral-Optimized: The integral calculation algorithm can ignore integrals with only small contributions to the result.
    - Matrix-Based: A matrix formalism can be derived which enables an electron repulsion integral scheme which is highly parallelizable.
    - Large-Scale Systems: Sparse formalisms and memory constraints allow fast calculations for systems with multiple of hundereds of atoms.

The key features:
    - electronic structure calculations for large-scale systems with >1,000,000 atoms
    - very fast calculations for systems with a few hundred to a few thousand atoms
    - subsystem/clustering approach for linear scalability
    - visualization of electonic densities
    - UV/Vis spectra for systems containing hundreds or thousands of atoms

To run this program:
1. Read the program configurations below the variable selections and change variables according to your needs. The default values will work fine in most cases.
2. Read the section ---MAIN--- at the very end of the program and follow the instructions there.

Author/Contact information:
Luc Wieners
Institute of Physics, University of Kassel, Heinrich-Plett-Straße 40, 34132 Kassel, Germany
lucwieners@physik.uni-kassel.de
"""

"""
--------------------
MAIN CONFIGURATIONS 
--------------------
"""

# SCF CONFIGURATIONS
max_scf_steps=100
scf_tolerance_density=1.0e-6
max_DIIS_linear_equations=max_scf_steps
pulay_mixing_rate=0.7
DIIS_penalty=1.05
added_electrons=0
level_shift_enabled=False
level_shift_value=0.3

# PRECISION CONFIGURATIONS
density_threshold=1.0e-4
coulomb_threshold=10.0
coulomb_threshold_low=8.0

# BASIS FUNCTION CONFIGURATIONS
sto_precision=3
lobe_precision=6

# VERBOSITY
verbosity=1

# THREADING
num_threads=4
max_electron_integrals=100000000

# TIME-DEPENDENT HARTREE-FOCK
time_steps=2000
delta_t=0.25
pulse_standard_deviation=0.2
pulse_shift_factor=10
e_field_max=2.0e-5
update=1

# DIVIDE-AND-CONQUER HARTREE-FOCK
partition_length=12.5
partition_cut_off=8.0
section_cut_off=10.0

# DENSITY PLOTTING CONFIGURATIONS
pixel_size=0.5
basis_function_space=5.0
additional_space=7.0
hide_core_electrons=True

# ALPHA-FOLD PREDICTIONS
amino_acids_per_cluster=5




"""
-------------------------------
ADDITIONAL CONFIGURATIONS 
(changes usually not necessary)
-------------------------------
"""

# PRECISION CONFIGURATIONS
density_threshold_2=density_threshold
densities_threshold=density_threshold
densities_threshold_2=density_threshold

# THREADING
num_threads_G=num_threads
num_threads_integrals=num_threads
e_tensor_datatype='float64'

# BASIS SET CONFIGURATIONS
overlap_sto_precision=6
overlap_part_precision=7

# ADVANCED VERBOSITY
print_ERI_relevance=False
display_runtimes=False
display_eigenenergies=False



"""
================
Paramater Manual
================


--------------------
MAIN CONFIGURATIONS:
--------------------
Change these parameters according to the calculation. If in doubt, use the default values.



SCF CONFIGURATIONS:

max_scf_steps: the maximum number of scf steps after which the calculation is stopped regardless of the convergence value. 
Default of max_scf_steps is 100, much higher values are not recommended as convergence should usually occur at latest after this amount of steps if no other error is present.

scf_tolerance_density: The convergence threshold value which terminates the calculation if the threshold is passed.
For the convergence value the RMSD of the density matrix is used i.e. sqrt(mean((P_{i-1}-P_{i})^2)). 
The default value is 1.0e-6. For more precise calculations (especially for real-time Hartree-Fock!) a stricter convergence threshold is recommended as for example 1.0e-8 or 1.0e-9.
For less precise calculations a higher value (for example 1.0e-4) can be used.

max_DIIS_linear_equations: The number of DIIS (direct inversion in the iterative subspace also called Pulay mixing) equations which is used to construct a new density matrix via Pulay mixing. 
The default is max_scf_steps which leads to stable results even for large systems (>1,000 atoms) which are otherwise extremely difficult to converge.

pulay_mixing_rate: The mixing rate of the density matrices during Pulay mixing. The mixing is done as P_new = pulay_mixing_rate*P_Pulay + (1-pulay_mixing_rate)*P_old, 
where P_old is the old density matrix and P_Pulay the newly constructed density matrix via Pulay mixing. The default value is 0.7. A higher mixing rate accelerates the scf procedure
but can lead to instabilities as wells. The mixing rate can be increased if the system contains a lot of water which often stabilizes the calculation. 

DIIS_penalty: A paramter which pushes the DIIS towards a final solution by favouring the lowest-energy state. This parameter stabilizes calculations where a switching between two or more
states occurs (also sometimes called charge sloshing). Very helpful for systems with small HOMO-LUMO (highes/lowest occupied molecular orbital) gaps. The default and recommended value is: 1.05.
Can be disabled by setting the parameter to 1.0 which corresponds to normal mixing. Values >=1.0 are valid, higher values than 1.5 are discouraged. 
The use of this parameter is highly recommended since there are no downsides.

added_electrons: Adds electrons to the system. A negative value removes electrons from the system. 
Is used to add charges to systems which is often done in real-time time-dependet Hartree-Fock calculations. A good measure of added_electrons is the difference between the number of electrons
in the system and the calculated position of the HOMO-LUMO gap.

level_shift_enabled: Artificially increases the HOMO-LUMO gap by adding an energy shift to the Fock matrix. This can help to converge calculation with small HOMO-LUMO gaps.
The default is 'False' since using only the parameter DIIS_penalty works well in most cases.

level_shift_value: The value by which the virtual orbital energies are shifted if level_shift_enabled=True. This parameter is only used if level_shift_enabled=True.
Default and recommended value: 0.3. Values are given in Hartree. Note that 1 Ha = 27.211 eV (electron volts).



THRESHOLDS:

density_threshold: sets the value below which electronic density contributions will be ignored.
Recommended values: standard precision: 1.0e-4
                    higher precision: 1.0e-6
                    minimum: 1.0e-10 (lower values will likely not influence calculation results)
                    maximum: 3.0e-4 (high accuracy loss for higher values)

coulomb_threshold and coulomb_threshold_low: sets the values above which the Coulomb interaction will be ignored or dampened, respectively. Values are in Angstrom!
Recommended values: 10 Angstrom and 8 Angstrom



BASIS FUNCTION CONFIGURATIONS:

sto_precision: determines how from how many Gaussian functions a STO-nG basis function is built.
Currently supported are 2,3,6 (corresponding to STO-2G, STO-3G, STO-6G). Default and recommendend: 3.
Note that this value only influences s-type orbitals since orbitals of higher angular momenta are treated with the Gaussian lobe function expansion algorithm.

lobe_precision: Determines the amount of Gaussian functions in a Gaussian lobe function expansion of a p-type orbital.
Currently supported are 4,6 (approximately corresponds to STO-2G, STO-3G). Default and recommended: 6.
Note that double the amount of Gaussians are needed here since one p-type orbital contains two lobes which are treated independently.



VERBOSITY: 

verbosity: 1 for run-time and integral-count outputs, 0 for no outputs at all (default: 1)



THREADING:

num_threads: the number of threads which will be started for the parallelized computation of the electron repulsion integrals and the G-matrix
             should correspond to the number of CPU cores available

max_electron_integrals: the maximum number of electron repulsion integrals that are used in a calculation



OPTIONAL: TIME-DEPENDENT HARTREE-FOCK
Note: all parameters below are ONLY used if a real-time time-dependent Hartree-Fock (RT-TDHF) calculation is done and will be ignored otherwise.

time_steps: The amount of time steps over which a real-time time-dependent Hartree-Fock calculation is propagated. The default value is: 2000.
Multiplied with delta_t (see below) the total propagation time can be calculated. This time should be around 500 atomic units of time (=~12.1 femtoseconds).
If absorption peaks towards infra-red are computed a higher time might be needed for a better resolution of low-frequency oscillations. A value of 1000 atomic units of time should be enough.
For ultra-violet calculations lower values than 500 might be used.

delta_t: The time of one time step. Default and recommended values is: 0.25. Given in atomic units of time. See also 'time_steps'.
A higher time step can lead to numerical instabilities (starting at around 0.3) and should therefore be avoided!
Lower time steps are possible but have no advantage and should therefore not be used.

pulse_standard_deviation: The standard deviation of the Gaussian pulse with which the system is excited in the calculation. Default and recommended value: 0.2. Given in atomic units of time.
A higher value can lead to different results since the RT-TDHF approach uses only a very small excitation.

pulse_shift_factor: Shifts the pulse forward on the time axis. Default value: 10. Given as a multiple of pulse_standard_deviation.
A much lower value leads to parts of the pulse not being on the positive side of the time axis and a much higher value leads to a large time span before the pulse in which no dynamics occur.

e_field_max: The electric field strength of the pulse. Default and recommended: 1.0e-5 (given in atomic units). This is the maximum value of the electric field.
This value should be chosen dependent on the size and dipole moment of the system which is studied. 
The values of the dipole moment during the time evolution should be between 1.0e-3 and 1.0e-6. They scale proportionally to e_field_max and e_field_max should therefore be chosen accordingly.
Too high values lead the system from linear to non-linear dynamics which is undesired and too low values make the time evolution susceptible to numerical instabilities.

update: How often an update during the time evolution is displayed in form of a console output. Default: 1. Given in the amount of time steps after which in update is shown.
The update contains information about the coorindate (x,y or z) of the evolution, the time step and the corresponding percentage of completion, 
the current dipole moment and the numerical stability (trace deviation of the density matrix). Especially for testing update=1 is recommended.



OPTIONAL: DIVIDE-AND-CONQUER HARTREE-FOCK
Note: all parameters below are ONLY used if a divide-and-conquer calculation is done and will be ignored otherwise.

Additional information for the parameters:
All values are in the variable section should be given in Angstrom!
The divide-and-conquer scheme for dividing into clusters using a 3D grid:
xxxxxxxxxx|---------------------|-----------------------|-----------0----------|-----------------------|---------------------|xxxxxxxxxxx
(ignored) |<--section_cut_off-->|<--partition_cut_off-->|<--partition_length-->|<--partition_cut_off-->|<--section_cut_off-->| (ignored)

partition_length: atoms in this partition/box are determined by the partition num (default: 12.5 Angstrom, variable always given in Angstrom)

partition_cut_off: atoms that are neighbors to atoms in the partition/box (default: 10 Angstrom, variable always given in Angstrom)

section_cut_off: atoms that could be added to avoid bond breaking (default: 10 Angstrom, variable always given in Angstrom)



OPTIONAL: DENSITY PLOTTING CONFIGURATIONS
Note: all parameters below are ONLY used if a density plotting calculation is done and will be ignored otherwise.

pixel_size: The size of one pixel / length of the 3D grid used for the visualization of the electronic density. Default: 0.5 Bohr atomic units. 
For larger systems a value of 1.0 or even 1.5 should be considered due to the high memory requirements of density grids.
For small sytems values up to 0.1 might work. Memory requirements scale cubical with the inverse of pixel_size since we use a 3D grid.

basis_function_space: Space around basis functions on their local grids. Basis functions grids get precomputed for better performance.
Default value: 5.0 Bohr atomic units.
Important: Has to be a multiple of pixel_size!

additional_space: Additional space around the computed structure. Should be larger than basis_function_space and can be used to generate empty outer regions on the grid.
Default value: 7.0 Bohr atomic units.

hide_core_electrons: Core electron basis functions will not be plotted during the density grid calculation. Default and recommended: True.
Core electrons have their electronic density concentrated to a small region which is problematic for visualizing electronic densities since only the core electron densities would be visible
since valence electron densities occupy more space but have lower values.



OPTIONAL: ALPHA-FOLD PREDICTIONS
Note: the parameter below are ONLY used if an atomic energy calculation for comparison with AlphaFold is done and will be ignored otherwise.

amino_acids_per_cluster: The clustering for atomic energy calculations for comparison with AlphaFold is done by 





--------------------------
ADDITIONAL CONFIGURATIONS:
--------------------------
Configurations which usually do not need to changed. Defaults are recommended.



# PRECISION CONFIGURATIONS

density_threshold_2: A lower cut-off for the density relevance value. Can be used to apply a smooth cut-off function for density cut-offs which is usually not done 
since the cut-off values are already small.
Default: density_threshold

densities_threshold: A different threshold value for the combination of two densities. A threshold is used both for the relevance of single densities and for the product of two densities.
Usually the same threshold value is used but the value for the product can be chosen differently if wanted.
Default: density_threshold

densities_threshold_2: A lower cut-off for the relevance value of the product of two densities (i.e. densities_threshold, see above). See also the explanation of density_threshold_2.
Default: density_threshold



# THREADING

num_threads_G: Number of threads for the G matrix computation. In most cases identical to num_threads. 
Note that on some compute nodes a higher number of threads can slow down calculations for large systems since the memory usage during G matrix computations can get very high.
Default: num_threads.

num_threads_integrals: Number of threads for the integral computation. In most cases identical to num_threads. 
Note that on some compute nodes a higher number of threads can slow down calculations for large systems since the memory usage during the integral computation can get very high.
Default: num_threads.

e_tensor_datatype: Datatype of the electron repulsion tensor in which the electron repulsion intgrals (ERIs) are stored. 
This is usually done in double precision but can be changed to single precision if the memory for double precision is not high enough. This can however influence the accuracy of the calculation.
Default: 'float64'.



# BASIS SET CONFIGURATIONS

overlap_sto_precision: The precision of s-type basis functions used to estimate the relevance of electronic densities can be chosen.
Lower values increase the computational speed of this part slightly but the relevance computation part is not performance-critical.
Default: 6. Currently 2,3,6 is supported.

overlap_part_precision: The precision of individual lobes of p-type basis functions used to estimate the relevance of electronic densities can be chosen.
Default: 7. Currently only 7 is supported.



ADVANCED VERBOSITY:

display_runtimes: more detailed outputs for scf runtimes. Useful for runtime analysis.
Default: False

display_eigenenergies: displays eigenenergies around the Fermi edge. Useful to locate the HOMO-LUMO gap.
default: False

print_ERI_relevance: prints detailed information about the distribution of absolute values of ERIs which cooresponds to their relevance.
Can be used to see how many ERIs get ignored in the relevance calculations. 
Default: False.





-------
OUTPUT:
-------
The console output of Nimble consists of run-time logs and density/ERI counts.
Below is an examplary output for beta-carotene (96 atoms) on an intel i5 processor using default paramenters:

Preparations:           23.6352 s
Overlap/Kinetic matrix: 3.6987 s
Nuclei matrix:          7.5813 s
Electron-electron integrals:
    |Relevant densities: 7819
    |Relevant density combinations: 4504594
  >Relevance computations:        4.5151 s
  >ERI computations:              22.3655 s
  >Second relevance computations: 0.1991 s
    |Total integrals:         4294967296
    |Unique integrals:        541089856
    |With relevant densities: 30572290
    |With relevant values:    3946243
  >Process ERIs:                  4.7365 s
Electron tensor:        34.8972 s
Ionic energy:           1.1126 s
Starting SCF cycle: 
SCF step | convergence measure:
       1 | 5.72175e-2  | -4339.2166657470425
       2 | 1.75679e-2  | -4342.3203387113235
       3 | 7.31540e-3  | -4343.106737365173
       4 | 3.79263e-3  | -4343.323867045995
       5 | 1.87254e-3  | -4343.37383228906
       6 | 8.65668e-4  | -4343.383901291234
       7 | 3.69166e-4  | -4343.3856308814475
       8 | 1.43351e-4  | -4343.385883556393
       9 | 5.24774e-5  | -4343.385916932791
      10 | 1.88662e-5  | -4343.385921231835
      11 | 7.04501e-6  | -4343.385921828226
      12 | 2.96648e-6  | -4343.385921929285
      13 | 1.45412e-6  | -4343.385921950744
      14 | 7.58954e-7  | -4343.385921955811
SCF times:
    |Core Hamiltonian: 0.0 s
    |Square root of inverse: 0.0226 s
    |SAD guess: 0.0007 s
    |G tensor: 5.6212 s
    |Fock matrix construction: 0.0 s
    |Commutator SPF-FPS: 0.0483 s
    |Save Fock matrix: 0.0 s
    |Error matrix calculation: 0.0 s
    |Energy calculation: 0.001 s
    |Transform Fock matrix: 0.004 s
    |Eigenvalue calculation: 0.0831 s
    |Transform eigenorbitals: 0.005 s
    |Density matrix: 0.0351 s
    |DIIS coefficients: 0.0104 s
    |DIIS equations: 0.0023 s
    |Mix new Fock matrix: 0.005 s
    |Convergence criterium: 0.0162 s
SCF cycle:              6.1007 s
_______________________________________
Total time:             77.0256 s
Total energy: -1528.5474502578945 Ha





------------------
PROGRAM STRUCTURE:
------------------
Main sections for the different applications are seperated with multi-line comments containing two lines of '======='.
Subsections for functions with usage in similar program parts are declared with comments containing lines of '-------'.
Functions contain a comment with further explanation.





------------
DISCLAIMERS:
------------
- We cannot guarantee that NIMBLE runs smoothly on every device as it is still in a testing phase. Consider contacting us
via the given contact information at the start of the program in case of difficulties.
- There are currently several functions with unused/dead variables. These are mostly attributed to force calculations which were suppported
in previous versions but not in version 3.10. Code for force calculations is still left in some places as forces will be implemented in the future.
It was removed in all cases where it would reduce the performance of the code.
"""





"""
=========================
=========================
START OF THE MAIN PROGRAM
=========================
=========================
"""




"""
--------
Imports:
--------

numpy for various mathematical calculations
np.set_printoptions(suppress=True) enables more convenient print outputs of arrays.

numba.njit for just-in-time compilation to massively speed up calculations

matplotlib for plotting

time timekeeping of various parts of the program

torch for matrix operations (better parallelization results for high CPU core counts than numpy)
torch.set_grad_enabled(False) ensures that torch does not compute gradients which are used in machine learning to update models which is unnecessary here.

json for data loading (optional, depending on coordinate file type)

sys for large-scale calculations on clusters to load in job numbers from slurm files (optional, only if large-scale calculations (>1,000,000 atoms) are done) 

Datatype defines the datatype for most operations. Double precision i.e. 64-bit floating point numbers should be used.
"""


import numpy as np
np.set_printoptions(suppress=True)
from numba import njit,prange
import matplotlib.pyplot as plt
import time
import torch
torch.set_grad_enabled(False)
import json
import sys 
datatype='float64'









"""
--------------------------------
constants and derived quantities
--------------------------------
"""

angstrom_to_bohr=1.88973
nanometer_to_bohr=18.8973
k_b=3.166811563e-6
speed_of_light=137.03599

eV_to_Hertz=241799050402417.0
nm_to_Hertz=2.99792458E+17
hertz_to_atomic_units=2.4188843265864e-16

single='float32'

coulomb_threshold*=angstrom_to_bohr
coulomb_threshold_low*=angstrom_to_bohr

partition_length*=angstrom_to_bohr
partition_cut_off*=angstrom_to_bohr
section_cut_off*=angstrom_to_bohr

density_threshold_difference,densities_threshold_difference,coulomb_threshold_difference=density_threshold_2-density_threshold,densities_threshold_2-densities_threshold,coulomb_threshold-coulomb_threshold_low
coulomb_threshold_times_2=coulomb_threshold*2

delta_t=0.5*delta_t

basis_set_configs=np.array([[[1,0,0,0,0],[1,0,0,0,0],[sto_precision,0            ,0             ,0            ,0             ]],
                            [[1,2,3,0,0],[1,1,1,0,0],[sto_precision,sto_precision,lobe_precision,0            ,0             ]],
                            [[1,2,3,4,5],[1,1,1,1,1],[sto_precision,sto_precision,lobe_precision,sto_precision,lobe_precision]]],dtype='int32')
basis_set_configs_len=np.array([1,3,5],dtype='int32')
basis_function_type_length_list=np.array(basis_set_configs[2][2],dtype='int32') 
implemented_orbital_types_num=5

parts_sto_precision_1s=overlap_sto_precision
parts_sto_precision_2s=overlap_sto_precision
parts_sto_precision_2p=overlap_part_precision
parts_sto_precision_3s=overlap_sto_precision
parts_sto_precision_3p=overlap_part_precision

num_basis_function_types=len(basis_function_type_length_list)
num_basis_function_types_sqaure=num_basis_function_types*num_basis_function_types
max_gaussian_functions=int(np.max(basis_function_type_length_list))
max_gaussian_functions_square=max_gaussian_functions*max_gaussian_functions

nuclei_hyp1f1_prefactor=np.sqrt(np.pi)/2.0
V_ee_prefactor_sqrt=np.sqrt(2.0*np.pi*np.pi*np.sqrt(np.pi))*np.sqrt(np.sqrt(np.pi)/2.0)





"""
-------------------
Coefficient section
-------------------


Coefficients and exponents for Gaussian-type basis functions
Values are set after the array definition. Values are taken from: https://www.basissetexchange.org/.
Literature: 
A New Basis Set Exchange: An Open, Up-to-date Resource for the Molecular Sciences Community. 
Benjamin P. Pritchard, Doaa Altarawy, Brett Didier, Tara D. Gibson, Theresa L. Windus. J. Chem. Inf. Model. 2019, 59(11), 4814-4820, doi:10.1021/acs.jcim.9b00725. 

Explanation of the array format:
Coefficient array for Slater-type orbitals:
Axis 1: Element (1 for H, 2 for He, ...), currently implemented: H,C,N,O;
Axis 2: Number of primitve Gaussians (e.g. STO-3, STO-6), currently implemented: STO-3G, STO-6G;
Axis 3: coeffs: Orbital type: 0: 1s, 1: 2s, 2: 2p, 3: 3s, 4: 3p;
        exponents/norms: Orbital type: 0: 1s, 1: 2s/2p, 2: 3s/3p;
Axis 4: Coefficients for selected element, precision and orbital
"""

sto_coefs=np.zeros((19,7,3,6),dtype=datatype)
sto_exps=np.zeros((19,7,3,6),dtype=datatype)
sto_norms=np.zeros((19,7,3,6),dtype=datatype)


sto_coefs[1,3,0,:3]=np.array([0.1543289673E+00,0.5353281423E+00,0.4446345422E+00],dtype=datatype)
sto_exps[1,3,0,:3]=np.array([0.3425250914E+01,0.6239137298E+00,0.1688554040E+00],dtype=datatype)
sto_norms[1,3,0,:3]=np.array([1.7944418,0.50032645,0.18773545],dtype=datatype)
sto_coefs[6,3,:2,:3]=np.array([[0.1543289673E+00,0.5353281423E+00,0.4446345422E+00],
                              [-0.9996722919E-01,0.3995128261E+00,0.7001154689E+00]],dtype=datatype) 
sto_exps[6,3,:2,:3]=np.array([[0.7161683735E+02,0.1304509632E+02,0.3530512160E+01],
                             [0.2941249355E+01,0.6834830964E+00,0.2222899159E+00]],dtype=datatype)
sto_norms[6,3,:2,:3]=np.array([[17.54573,4.8921027,1.8356436],
                              [1.6006964,0.5357423,0.23072779]],dtype=datatype) 
sto_coefs[7,3,:2,:3]=np.array([[0.1543289673E+00,0.5353281423E+00,0.4446345422E+00],
                              [-0.9996722919E-01,0.3995128261E+00,0.7001154689E+00]],dtype=datatype) 
sto_exps[7,3,:2,:3]=np.array([[0.9910616896E+02,0.1805231239E+02,0.4885660238E+01],
                             [0.3780455879E+01,0.8784966449E+00,0.2857143744E+00]],dtype=datatype)
sto_norms[7,3,:2,:3]=np.array([[22.386469,6.2417984,2.3420842],
                              [1.9322718,0.6467183,0.27852178]],dtype=datatype) 
sto_coefs[8,3,:2,:3]=np.array([[0.1543289673E+00,0.5353281423E+00,0.4446345422E+00],
                              [-0.9996722919E-01,0.3995128261E+00,0.7001154689E+00]],dtype=datatype) 
sto_exps[8,3,:2,:3]=np.array([[0.1307093214E+03,0.2380886605E+02,0.6443608313E+01],
                             [0.5033151319E+01,0.1169596125E+01,0.3803889600E+00]],dtype=datatype)
sto_norms[8,3,:2,:3]=np.array([[27.551168,7.68182,2.882418],
                              [2.3949149,0.80156183,0.3452081]],dtype=datatype) 

sto_coefs[15,3,:2,:3]=np.array([[0.1543289673E+00,0.5353281423E+00,0.4446345422E+00],
                                [-0.9996722919E-01,0.3995128261E+00,0.7001154689E+00]],dtype=datatype) 
sto_coefs[15,3,2,:3]=np.array([-0.2196203690E+00,0.2255954336E+00,0.9003984260E+00],dtype=datatype)
sto_exps[15,3,:2,:3]=np.array([[0.4683656378E+03,0.8531338559E+02,0.2308913156E+02],
                               [0.2803263958E+02,0.6514182577E+01,0.2118614352E+01]],dtype=datatype)
sto_exps[15,3,2,:3]=np.array([0.1743103231E+01,0.4863213771E+00,0.1903428909E+00],dtype=datatype)
sto_norms[15,3,:2,:3]=np.array([[71.75445349,20.00658552,7.5069892],
                                [8.6827658,2.90606308,1.25155236]],dtype=datatype)
sto_norms[15,3,2,:3]=np.array([1.081191,0.4150521,0.2053821],dtype=datatype)
sto_coefs[16,3,:2,:3]=np.array([[0.1543289673E+00,0.5353281423E+00,0.4446345422E+00],
                                [-0.9996722919E-01,0.3995128261E+00,0.7001154689E+00]],dtype=datatype) 
sto_coefs[16,3,2,:3]=np.array([-0.2196203690E+00,0.2255954336E+00,0.9003984260E+00],dtype=datatype)
sto_exps[16,3,:2,:3]=np.array([[0.5331257359E+03,0.9710951830E+02,0.2628162542E+02],
                               [0.3332975173E+02,0.7745117521E+01,0.2518952599E+01]],dtype=datatype)
sto_exps[16,3,2,:3]=np.array([0.2029194274E+01,0.5661400518E+00,0.2215833792E+00],dtype=datatype)
sto_norms[16,3,:2,:3]=np.array([[79.07374871,22.04735231,8.27273777],
                                [9.88630834,3.30888064,1.42503355]],dtype=datatype)
sto_norms[16,3,2,:3]=np.array([1.2117215,0.46516069,0.23017756],dtype=datatype)


sto_coefs[1,6,0,:]=np.array([0.9163596281E-02,0.4936149294E-01,0.1685383049E+00,0.3705627997E+00,0.4164915298E+00,0.1303340841E+00],dtype=datatype)
sto_exps[1,6,0,:]=np.array([0.3552322122E+02,0.6513143725E+01,0.1822142904E+01,0.6259552659E+00,0.2430767471E+00,0.1001124280E+00],dtype=datatype)
sto_norms[1,6,0,:]=np.array([10.370372,2.9057155,1.1177558,0.50155383,0.24672756,0.12684579],dtype=datatype)
sto_coefs[6,6,:2,:]=np.array([[0.9163596281E-02,0.4936149294E-01,0.1685383049E+00,0.3705627997E+00,0.4164915298E+00,0.1303340841E+00],
                              [-0.1325278809E-01,-0.4699171014E-01,-0.3378537151E-01,0.2502417861E+00,0.5951172526E+00,0.2407061763E+00]],dtype=datatype) 
sto_exps[6,6,:2,:]=np.array([[0.7427370491E+03,0.1361800249E+03,0.3809826352E+02,0.1308778177E+02,0.5082368648E+01,0.2093200076E+01],
                             [0.3049723950E+02,0.6036199601E+01,0.1876046337E+01,0.7217826470E+00,0.3134706954E+00,0.1436865550E+00]],dtype=datatype)
sto_norms[6,6,:2,:]=np.array([[101.399635,28.411564,10.929215,4.9041033,2.412458,1.2402754],
                              [9.2492285,2.7446237,1.1424646,0.5581037,0.298578,0.1663306]],dtype=datatype) 
sto_coefs[7,6,:2,:]=np.array([[0.9163596281E-02,0.4936149294E-01,0.1685383049E+00,0.3705627997E+00,0.4164915298E+00,0.1303340841E+00],
                              [-0.1325278809E-01,-0.4699171014E-01,-0.3378537151E-01,0.2502417861E+00,0.5951172526E+00,0.2407061763E+00]],dtype=datatype) 
sto_exps[7,6,:2,:]=np.array([[0.1027828458E+04,0.1884512226E+03,0.5272186097E+02,0.1811138217E+02,0.7033179691E+01,0.2896651794E+01],
                             [0.3919880787E+02,0.7758467071E+01,0.2411325783E+01,0.9277239437E+00,0.4029111410E+00,0.1846836552E+00]],dtype=datatype)
sto_norms[7,6,:2,:]=np.array([[129.37506,36.25011,13.944506,6.2571096,3.0780375,1.5824584],
                              [11.165154,3.3131573,1.3791199,0.67371184,0.36042675,0.20078509]],dtype=datatype) 
sto_coefs[8,6,:2,:]=np.array([[0.9163596281E-02,0.4936149294E-01,0.1685383049E+00,0.3705627997E+00,0.4164915298E+00,0.1303340841E+00],
                              [-0.1325278809E-01,-0.4699171014E-01,-0.3378537151E-01,0.2502417861E+00,0.5951172526E+00,0.2407061763E+00]],dtype=datatype) 
sto_exps[8,6,:2,:]=np.array([[0.1355584234E+04,0.2485448855E+03,0.6953390229E+02,0.2388677211E+02,0.9275932609E+01,0.3820341298E+01],
                             [0.5218776196E+02,0.1032932006E+02,0.3210344977E+01,0.1235135428E+01,0.5364201581E+00,0.2458806060E+00]],dtype=datatype)
sto_norms[8,6,:2,:]=np.array([[159.22269,44.613235,17.16159,7.700664,3.7881596,1.9475415],
                              [13.838423,4.106425,1.709322,0.83501834,0.4467236,0.24885897]],dtype=datatype) 

sto_coefs[15,6,:2,:]=np.array([[0.9163596281E-02,0.4936149294E-01,0.1685383049E+00,0.3705627997E+00,0.4164915298E+00,0.1303340841E+00],
                               [-0.1325278809E-01,-0.4699171014E-01,-0.3378537151E-01,0.2502417861E+00,0.5951172526E+00,0.2407061763E+00]],dtype=datatype) 
sto_coefs[15,6,2,:]=np.array([-0.7943126362E-02,-0.7100264172E-01,-0.1785026925E+00,0.1510635058E+00,0.7354914767E+00,0.2760593123E+00],dtype=datatype)
sto_exps[15,6,:2,:]=np.array([[0.4857412371E+04,0.8906012410E+03,0.2491581331E+03,0.8559254335E+02,0.3323808927E+02,0.1368928069E+02],
                              [0.2906649590E+03,0.5753018103E+02,0.1788033738E+02,0.6879210280E+01,0.2987645712E+01,0.1369456623E+01]],dtype=datatype)
sto_exps[15,6,2,:]=np.array([0.1111939652E+02,0.2977874272E+01,0.1116734493E+01,0.4998708868E+00,0.2473606277E+00,0.1274811462E+00],dtype=datatype)
sto_norms[15,6,:2,:]=np.array([[414.68070016,116.19101999,44.69576689,20.0556638,9.86590955,5.07219059],
                               [50.17121301,14.88784702,6.19714809,3.02735974,1.61959681,0.90223839]],dtype=datatype)
sto_norms[15,6,2,:]=np.array([4.33981289,1.61562238,0.77423454,0.42369513,0.24998159,0.15205285],dtype=datatype)
sto_coefs[16,6,:2,:]=np.array([[0.9163596281E-02,0.4936149294E-01,0.1685383049E+00,0.3705627997E+00,0.4164915298E+00,0.1303340841E+00],
                               [-0.1325278809E-01,-0.4699171014E-01,-0.3378537151E-01,0.2502417861E+00,0.5951172526E+00,0.2407061763E+00]],dtype=datatype) 
sto_coefs[16,6,2,:]=np.array([-0.7943126362E-02,-0.7100264172E-01,-0.1785026925E+00,0.1510635058E+00,0.7354914767E+00,0.2760593123E+00],dtype=datatype)
sto_exps[16,6,:2,:]=np.array([[0.5529038289E+04,0.1013743118E+04,0.2836087927E+03,0.9742727471E+02,0.3783386178E+02,0.1558207360E+02],
                              [0.3455896791E+03,0.6840121655E+02,0.2125904712E+02,0.8179121699E+01,0.3552198128E+01,0.1628232301E+01]],dtype=datatype)
sto_exps[16,6,2,:]=np.array([0.1294439442E+02,0.3466625105E+01,0.1300021248E+01,0.5819134077E+00,0.2879592903E+00,0.1484042983E+00],dtype=datatype)
sto_norms[16,6,:2,:]=np.array([[456.98010207,128.04305616,49.25494751,22.10143681,10.87227921,5.58957813],
                               [57.12558561,16.95149327,7.05615217,3.44699057,1.84409367,1.02730019]],dtype=datatype)
sto_norms[16,6,2,:]=np.array([4.8637517,1.81067394,0.86770666,0.47484718,0.28016147,0.17040995],dtype=datatype)

sto_coefs=sto_coefs*sto_norms



"""
Coefficients, exponents and offsets for the Gaussian lobe function basis functions
Similar structure as before.
Implemented are precisions 2,4,6 (i.e. 1,2,3 Gaussian functions per lobe).
Implemented for elements C,N,O,P,S (note that H does not have p-orbitals in minimal basis calculations).
"""
lobe_coefs=np.zeros((19,5,2,8),dtype=datatype)
lobe_exps=np.zeros((19,5,2,8),dtype=datatype)
lobe_offsets=np.zeros((19,5,2,8),dtype=datatype)
lobe_norms=np.zeros((19,5,2,8),dtype=datatype)

lobe_coefs[6,3,0,:6]=np.array([0.64520464,0.88439881,0.33605098,0.64520464,0.88439881,0.33605098],dtype=datatype)
lobe_exps[6,3,0,:6]=np.array([0.2670606,0.81133893,3.29524071,0.2670606,0.81133893,3.29524071],dtype=datatype)
lobe_offsets[6,3,0,:6]=np.array([0.2,0.2,0.2,-0.2,-0.2,-0.2],dtype=datatype)
lobe_norms[6,3,0,:6]=np.array([-1.0,-1.0,-1.0,1.0,1.0,1.0],dtype=datatype)*1.000657885155526
lobe_coefs[7,3,0,:6]=np.array([0.64054726,0.9684976,0.39050546,0.64054726,0.9684976,0.39050546],dtype=datatype)
lobe_exps[7,3,0,:6]=np.array([0.3292863,0.9914091,4.04400941,0.3292863,0.9914091,4.04400941],dtype=datatype)
lobe_offsets[7,3,0,:6]=np.array([0.2,0.2,0.2,-0.2,-0.2,-0.2],dtype=datatype)
lobe_norms[7,3,0,:6]=np.array([-1.0,-1.0,-1.0,1.0,1.0,1.0],dtype=datatype)*1.0004310541198355
lobe_coefs[8,3,0,:6]=np.array([0.64437286,1.06711325,0.45753199,0.64437286,1.06711325,0.45753199],dtype=datatype)
lobe_exps[8,3,0,:6]=np.array([0.42241359,1.26459378,5.20158956,0.42241359,1.26459378,5.20158956],dtype=datatype)
lobe_offsets[8,3,0,:6]=np.array([0.2,0.2,0.2,-0.2,-0.2,-0.2],dtype=datatype)
lobe_norms[8,3,0,:6]=np.array([-1.0,-1.0,-1.0,1.0,1.0,1.0],dtype=datatype)*1.000318589703924

lobe_coefs[15,3,0,:6]=np.array([3.20780205,2.22347651,1.35755385,3.20780205,2.22347651,1.35755385],dtype=datatype)
lobe_exps[15,3,0,:6]=np.array([7.67937533,2.51881708,32.39705451,7.67937533,2.51881708,32.39705451],dtype=datatype)
lobe_offsets[15,3,0,:6]=np.array([0.1,0.1,0.1,-0.1,-0.1,-0.1],dtype=datatype)
lobe_norms[15,3,0,:6]=np.array([-1.0,-1.0,-1.0,1.0,1.0,1.0],dtype=datatype)*1.000702490931977
lobe_coefs[15,3,1,:6]=np.array([0.73776749,0.08185985,0.64707098,0.73776749,0.08185985,0.64707098],dtype=datatype)
lobe_exps[15,3,1,:6]=np.array([0.2525002,0.11081551,0.59072838,0.2525002,0.11081551,0.59072838],dtype=datatype)
lobe_offsets[15,3,1,:6]=np.array([0.2,0.2,0.2,-0.2,-0.2,-0.2],dtype=datatype)
lobe_norms[15,3,1,:6]=np.array([-1.0,-1.0,-1.0,1.0,1.0,1.0],dtype=datatype)*1.0000599599379631
lobe_coefs[16,3,0,:6]=np.array([3.42244003,2.2028318,1.53763642,3.42244003,2.2028318,1.53763642],dtype=datatype)
lobe_exps[16,3,0,:6]=np.array([8.79554437,2.90676936,37.24211708,8.79554437,2.90676936,37.24211708],dtype=datatype)
lobe_offsets[16,3,0,:6]=np.array([0.1,0.1,0.1,-0.1,-0.1,-0.1],dtype=datatype)
lobe_norms[16,3,0,:6]=np.array([-1.0,-1.0,-1.0,1.0,1.0,1.0],dtype=datatype)*1.0006429068471574
lobe_coefs[16,3,1,:6]=np.array([0.75966712,0.09877814,0.66719658,0.75966712,0.09877814,0.66719658],dtype=datatype)
lobe_exps[16,3,1,:6]=np.array([0.29789993,0.13715709,0.69077193,0.29789993,0.13715709,0.69077193],dtype=datatype)
lobe_offsets[16,3,1,:6]=np.array([0.2,0.2,0.2,-0.2,-0.2,-0.2],dtype=datatype)
lobe_norms[16,3,1,:6]=np.array([-1.0,-1.0,-1.0,1.0,1.0,1.0],dtype=datatype)*1.0000721729039534

lobe_coefs[6,2,0,:4]=np.array([0.96413977,0.82547949,0.96413977,0.82547949],dtype=datatype)
lobe_exps[6,2,0,:4]=np.array([0.33941932,1.41201315,0.33941932,1.41201315],dtype=datatype)
lobe_offsets[6,2,0,:4]=np.array([0.2,0.2,-0.2,-0.2],dtype=datatype)
lobe_norms[6,2,0,:4]=np.array([-1.0,-1.0,1.0,1.0],dtype=datatype)*1.0028886026340327
lobe_coefs[7,2,0,:4]=np.array([0.99478787,0.91921183,0.99478787,0.91921183],dtype=datatype)
lobe_exps[7,2,0,:4]=np.array([0.42224616,1.75218641,0.42224616,1.75218641],dtype=datatype)
lobe_offsets[7,2,0,:4]=np.array([0.2,0.2,-0.2,-0.2],dtype=datatype)
lobe_norms[7,2,0,:4]=np.array([-1.0,-1.0,1.0,1.0],dtype=datatype)*1.002071766276696
lobe_coefs[8,2,0,:4]=np.array([1.04707358,1.0237873,1.04707358,1.0237873],dtype=datatype)
lobe_exps[8,2,0,:4]=np.array([0.5507524,2.29001396,0.5507524,2.29001396],dtype=datatype)
lobe_offsets[8,2,0,:4]=np.array([0.2,0.2,-0.2,-0.2],dtype=datatype)
lobe_norms[8,2,0,:4]=np.array([-1.0,-1.0,1.0,1.0],dtype=datatype)*1.001730293227881

lobe_coefs[15,2,0,:4]=np.array([3.40067464,3.06307294,3.40067464,3.06307294],dtype=datatype)
lobe_exps[15,2,0,:4]=np.array([3.23569931,13.74354402,3.23569931,13.74354402],dtype=datatype)
lobe_offsets[15,2,0,:4]=np.array([0.1,0.1,-0.1,-0.1],dtype=datatype)
lobe_norms[15,2,0,:4]=np.array([-1.0,-1.0,1.0,1.0],dtype=datatype)*1.0028505105813497
lobe_coefs[15,2,1,:4]=np.array([0.6686712,0.79181905,0.6686712,0.79181905],dtype=datatype)
lobe_exps[15,2,1,:4]=np.array([0.21070418,0.54247792,0.21070418,0.54247792],dtype=datatype)
lobe_offsets[15,2,1,:4]=np.array([0.2,0.2,-0.2,-0.2],dtype=datatype)
lobe_norms[15,2,1,:4]=np.array([-1.0,-1.0,1.0,1.0],dtype=datatype)*1.0002723419325867
lobe_coefs[16,2,0,:4]=np.array([3.32374337,3.47888193,3.32374337,3.47888193],dtype=datatype)
lobe_exps[16,2,0,:4]=np.array([16.01219981,3.76474575,16.01219981,3.76474575],dtype=datatype)
lobe_offsets[16,2,0,:4]=np.array([0.1,0.1,-0.1,-0.1],dtype=datatype)
lobe_norms[16,2,0,:4]=np.array([-1.0,-1.0,1.0,1.0],dtype=datatype)*1.0023555392051022
lobe_coefs[16,2,1,:4]=np.array([0.68440713,0.83493367,0.68440713,0.83493367],dtype=datatype)
lobe_exps[16,2,1,:4]=np.array([0.24322328,0.62787788,0.24322328,0.62787788],dtype=datatype)
lobe_offsets[16,2,1,:4]=np.array([0.2,0.2,-0.2,-0.2],dtype=datatype)
lobe_norms[16,2,1,:4]=np.array([-1.0,-1.0,1.0,1.0],dtype=datatype)*1.0002133800470114

lobe_coefs=lobe_coefs*lobe_norms


"""
Coefficients, exponents and offsets for orbital parts. Used for estimating the relevance of wave function interactions.
The shifted direction has the index 1 
"""
orbital_parts_coeffs=np.zeros((18,2,7),dtype=datatype)
orbital_parts_exps=np.zeros((18,2,7,2),dtype=datatype)
orbital_parts_offsets=np.zeros((18,2,7),dtype=datatype)

orbital_parts_coeffs[6,0]=np.array([0.21020597,-0.10733293,0.12119919,0.07106207,-0.05400071,0.05048129,0.18935931],dtype=datatype)*1.0072001798871546
orbital_parts_exps[6,0,:,0]=np.array([0.5764236,0.87086635,4.74752682,0.22863708,0.32374581,1.46137983,1.516823],dtype=datatype)
orbital_parts_exps[6,0,:,1]=np.array([0.96949833,18.27707337,14.12262395,0.34975632,2.30160144,56.80367948,3.43478416],dtype=datatype)
orbital_parts_offsets[6,0]=np.array([0.96183788,0.02043568,0.36447395,1.53245644,-0.14208569,0.16136831,0.63376153],dtype=datatype)

orbital_parts_coeffs[7,0]=np.array([0.12594915,0.2063496,3.0087257,-0.0877023,-2.99593826,0.03994704,0.40324338],dtype=datatype)*1.0041560691795643
orbital_parts_exps[7,0,:,0]=np.array([0.55053191,4.45342761,0.56341201,0.96059725,0.58047751,0.24416567,1.23328148],dtype=datatype)
orbital_parts_exps[7,0,:,1]=np.array([1.77288519,13.06354044,4.0972497,41.14980098,4.26751697,0.62358979,3.60332721],dtype=datatype)
orbital_parts_offsets[7,0]=np.array([1.47613285,0.32624442,0.8411654,-0.02996572,0.84364999,2.04000418,0.72411866],dtype=datatype)

orbital_parts_coeffs[8,0]=np.array([0.05957721,0.25223747,0.28753908,0.29850678,-0.08915678,0.21772122,-0.12416925],dtype=datatype)*1.0112732552315165
orbital_parts_exps[8,0,:,0]=np.array([0.3262607,0.75808978,1.85098,14.39296814,0.53665137,4.5566118,1.58209237],dtype=datatype)
orbital_parts_exps[8,0,:,1]=np.array([0.47470149,1.2008111,3.70769177,209.21137127,4.4360045,13.24945624,38.02792748],dtype=datatype)
orbital_parts_offsets[8,0]=np.array([1.26686064,0.82636302,0.57807172,0.17249301,-0.08838873,0.36008857,-0.02014936],dtype=datatype)

orbital_parts_coeffs[15,0]=np.array([1.22961756,8.39115404,-2.57565278,0.81374749,0.24589321,-8.55022728,2.69403254],dtype=datatype)*1.0115313380573823
orbital_parts_exps[15,0,:,0]=np.array([11.56045365,8.33496245,2.5728766,4.88488294,1.87827802,8.21259311,2.62899862],dtype=datatype)
orbital_parts_exps[15,0,:,1]=np.array([23.1630487,80.60350661,12.16498862,8.63369543,3.12080396,78.57470156,12.14378531],dtype=datatype)
orbital_parts_offsets[15,0]=np.array([0.20994224,0.05841471,0.12521072,0.40181425,0.57244225,0.05325301,0.14185866],dtype=datatype)
orbital_parts_coeffs[15,1]=np.array([0.09597981,0.05056336,-0.06168637,0.08630214,0.07481595,-0.03724176,0.12060358],dtype=datatype)*1.0057201407894794
orbital_parts_exps[15,1,:,0]=np.array([0.63966982,0.32623491,0.2678816,0.19522489,0.47314754,0.19298332,0.43613297],dtype=datatype)
orbital_parts_exps[15,1,:,1]=np.array([3.07613523,16.30538177,4.42319665,0.22930567,7.94012517,0.77526177,0.91420862],dtype=datatype)
orbital_parts_offsets[15,1]=np.array([1.03604633,0.2836936,0.20146867,1.28010504,0.59456785,-0.36530171,1.44961309],dtype=datatype)

orbital_parts_coeffs[16,0]=np.array([-10.13669092,-0.66666356,-0.24129124,9.51745308,1.03294444,0.19423795,1.85596052],dtype=datatype)*1.0152183206062153
orbital_parts_exps[16,0,:,0]=np.array([8.71597986,14.00945829,3.00237973,8.83381982,4.57601809,2.01192887,12.22370701],dtype=datatype)
orbital_parts_exps[16,0,:,1]=np.array([70.28919659,22.01410401,15.36844365,74.26872175,6.95223015,3.11401983,14.06196848],dtype=datatype)
orbital_parts_offsets[16,0]=np.array([0.05482271,-0.05780663,-0.04124501,0.0603514,0.30744847,0.52949946,0.12796264],dtype=datatype)
orbital_parts_coeffs[16,1]=np.array([0.15694047,0.10590538,0.05370748,0.0740629,0.05082452,1.11074957,-1.07687433],dtype=datatype)*1.0017166478392552
orbital_parts_exps[16,1,:,0]=np.array([0.72395277,0.48092914,0.21892612,0.24555874,0.36743536,0.40806574,0.40162075],dtype=datatype)
orbital_parts_exps[16,1,:,1]=np.array([2.90350593,1.37808715,0.53086674,1.53910575,20.90254615,6.50731129,6.44015996],dtype=datatype)
orbital_parts_offsets[16,1]=np.array([0.92661667,1.64834863,2.22262194,1.10123271,0.25207419,0.39454945,0.37554786],dtype=datatype)




"""
Array with atomic masses for all elements.
"""
atomic_masses=np.array([0.0,1.0080,4.00260,7.0,9.012183,10.81,12.011,14.007,15.999,18.99840316,20.180,22.9897693,24.305,26.981538,28.085,30.97376200,32.07,35.45,39.9],dtype=datatype)


element_cuts=np.zeros((9,9),dtype=datatype)
element_cuts[6,7]=2.67
element_cuts[6,8]=2.48
element_cuts[7,8]=4.0
element_cuts+=element_cuts.T
element_cuts[6,6]=2.76
element_cuts[7,7]=4.0
element_cuts[8,8]=4.0
element_h_bond_distances=np.zeros(19,dtype=datatype)
element_h_bond_distances[6]=2.0598
element_h_bond_distances[7]=1.9087
element_h_bond_distances[8]=1.8142
element_h_bond_distances[16]=2.5247



"""
Single atom density arrays which are used for the single atom density guess.
These arrays are obtained via runnning a Hartree-Fock calculation for a single atom.
Currently, only STO-3G calculations are supported.
"""
single_atom_densities=np.zeros((19,9,9),dtype=datatype)
single_atom_densities[1,0,0]=1.0
single_atom_densities[6,:5,:5]=np.array([[ 2.1257596 ,-0.51704437,-0.        ,-0.        , 0.        ],
                                         [-0.51704437, 2.1257598 , 0.        , 0.        ,-0.        ],
                                         [-0.        , 0.        , 0.66666141, 0.66673975, 0.66659095],
                                         [-0.        , 0.        , 0.66673975, 0.66681809, 0.66666928],
                                         [ 0.        ,-0.        , 0.66659095, 0.66666928, 0.6665205 ]])
single_atom_densities[7,:5,:5]=np.array([[ 2.11111116,-0.48432224,-0.        , 0.        ,-0.        ],
                                         [-0.48432224, 2.11111129, 0.        ,-0.        , 0.        ],
                                         [-0.        , 0.        , 1.        , 0.36364542, 0.35919786],
                                         [ 0.        ,-0.        , 0.36364542, 0.99999899, 0.36142164],
                                         [-0.        , 0.        , 0.35919786, 0.36142164, 1.00000101]])
single_atom_densities[8,:5,:5]=np.array([[ 2.11288737,-0.48838309,-0.        , 0.        ,-0.        ],
                                         [-0.48838309, 2.11288734, 0.        ,-0.        , 0.        ],
                                         [-0.        , 0.        , 1.33333698, 0.33333328, 0.33295953],
                                         [ 0.        ,-0.        , 0.33333328, 1.33332968, 0.33370704],
                                         [-0.        , 0.        , 0.33295953, 0.33370704, 1.33333333]])
single_atom_densities[15]=np.array([[ 2.24915541,-0.77208348,-0.        ,-0.        , 0.        , 0.16024315, 0.        , 0.        ,-0.        ],
                                    [-0.77208348, 2.39627112, 0.        , 0.        ,-0.        ,-0.58386231,-0.        ,-0.        , 0.        ],
                                    [-0.        , 0.        , 2.00017364,-0.00096016, 0.05029112,-0.        ,-0.15059793, 0.00110663,-0.14668533],
                                    [-0.        , 0.        ,-0.00096016, 1.99794802, 0.11250314,-0.        , 0.00110662,-0.14713737,-0.32812355],
                                    [ 0.        ,-0.        , 0.05029112, 0.11250314, 1.99739123, 0.        ,-0.14668495,-0.32812338,-0.14627048],
                                    [ 0.16024315,-0.58386231,-0.        ,-0.        , 0.        , 2.1426492 , 0.        , 0.        ,-0.        ],
                                    [ 0.        ,-0.        ,-0.15059793, 0.00110662,-0.14668495, 0.        , 1.0729779 , 0.0017765 , 0.42783984],
                                    [ 0.        ,-0.        , 0.00110663,-0.14713737,-0.32812338, 0.        , 0.0017765 , 1.07183876, 0.95699552],
                                    [-0.        , 0.        ,-0.14668533,-0.32812355,-0.14627048,-0.        , 0.42783984, 0.95699552, 1.07154692]])
single_atom_densities[16]=np.array([[ 2.26601244,-0.79971199,-0.        , 0.        , 0.        , 0.16211699, 0.        ,-0.        ,-0.        ],
                                    [-0.79971199, 2.40784747, 0.        ,-0.        ,-0.        ,-0.57394584,-0.        , 0.        , 0.        ],
                                    [-0.        , 0.        , 2.04283706, 0.07500791, 0.07539494,-0.        ,-0.27033786,-0.22892389,-0.23010518],
                                    [ 0.        ,-0.        , 0.07500791, 2.04360807,-0.07500844, 0.        ,-0.22892397,-0.27269107, 0.22892558],
                                    [ 0.        ,-0.        , 0.07539494,-0.07500844, 2.042836  , 0.        ,-0.23010518, 0.2289255 ,-0.27033462],
                                    [ 0.16211699,-0.57394584,-0.        , 0.        , 0.        , 2.13721461, 0.        ,-0.        ,-0.        ],
                                    [ 0.        ,-0.        ,-0.27033786,-0.22892397,-0.23010518, 0.        , 1.41595597, 0.69867516, 0.70228044],
                                    [-0.        , 0.        ,-0.22892389,-0.27269107, 0.2289255 ,-0.        , 0.69867516, 1.42313819,-0.69868007],
                                    [-0.        , 0.        ,-0.23010518, 0.22892558,-0.27033462,-0.        , 0.70228044,-0.69868007, 1.41594609]])







"""
-----------------------
preprocessing functions
-----------------------
"""


@njit
def calculate_num_basis_functions(element_list,num_atoms):
    """
    Calculates the number of basis functions for an array of elements.
    For example: In the STO-3G minimal basis the number of basis functions is 1, 5 or 9 for Z<=2, 2<Z<=10 and 10<Z<=18, respectively. The orbital types are 1s, 2s, 2px, 2py, 2pz, 3s, 3px, 3py, 3pz.
    Inputs are a list of elements and number of atoms and the output the number of basis functions
    """

    num_atom_types=3
    basis_function_lengths_per_atom_type=np.zeros(num_atom_types,dtype='int32')

    for atom_type in range(num_atom_types):
        for i in range(basis_set_configs_len[atom_type]):
            
            current_type=basis_set_configs[atom_type,0,i]
            current_class=basis_set_configs[atom_type,1,i]
            if ((current_type==1 or current_type==2 or current_type==4) and current_class==1):
                basis_function_lengths_per_atom_type[atom_type]+=1
            elif ((current_type==3 or current_type==5) and current_class==1):
                basis_function_lengths_per_atom_type[atom_type]+=3

    num_basis_functions=0
    for i in range(num_atoms):

        if (element_list[i]<=2): num_basis_functions+=basis_function_lengths_per_atom_type[0]
        elif (element_list[i]<=10): num_basis_functions+=basis_function_lengths_per_atom_type[1]
        elif (element_list[i]<=18): num_basis_functions+=basis_function_lengths_per_atom_type[2]

    return num_basis_functions



@njit
def calculate_num_gaussian_functions(element_list,num_atoms,num_basis_functions):
    """
    Calculates the number of basis functions for an array of elements.
    For example: Basis function type list for minimal basis STO-3: 1: 1s, 2: 2s, 3: 2p, 4: 3s, 5: 3p.
    Inputs are a list of elements, number of atoms, number of basis functions.
    """

    num_gaussian_functions=0
    basis_functions_index_list=np.zeros(num_atoms+1,dtype='int32')
    gaussian_functions_index_list=np.zeros(num_basis_functions+1,dtype='int32')
    gaussian_functions_atom_index_list=np.zeros(num_atoms+1,dtype='int32')
    atom_of_basisfunction=np.zeros(num_basis_functions,dtype='int32')
    type_of_basis_function=np.zeros(num_basis_functions,dtype='int32')
    basis_functions_count=0

    for i in range(num_atoms):

        basis_functions_index_list[i]=basis_functions_count
        gaussian_functions_atom_index_list[i]=num_gaussian_functions
        if (element_list[i]<=2): atom_type=0
        elif (element_list[i]<=10): atom_type=1
        elif (element_list[i]<=18): atom_type=2
        
        for j in range(basis_set_configs_len[atom_type]):
            orbital_type=basis_set_configs[atom_type,0,j]
            orbital_class=basis_set_configs[atom_type,1,j]
            orbital_num_gaussians=basis_set_configs[atom_type,2,j]
            
            if ((orbital_type==1 or orbital_type==2 or orbital_type==4) and orbital_class==1):
                gaussian_functions_index_list[basis_functions_count]=num_gaussian_functions
                atom_of_basisfunction[basis_functions_count]=i
                type_of_basis_function[basis_functions_count]=j+1
                num_gaussian_functions+=orbital_num_gaussians
                basis_functions_count+=1

            elif ((orbital_type==3 or orbital_type==5) and orbital_class==1):
                gaussian_functions_index_list[basis_functions_count:basis_functions_count+3]\
                                =[num_gaussian_functions,num_gaussian_functions+orbital_num_gaussians,num_gaussian_functions+2*orbital_num_gaussians]
                atom_of_basisfunction[basis_functions_count:basis_functions_count+3]=[i,i,i]
                type_of_basis_function[basis_functions_count:basis_functions_count+3]=[j+1,j+1,j+1]
                num_gaussian_functions+=3*orbital_num_gaussians
                basis_functions_count+=3
    
    gaussian_functions_index_list[-1]=num_gaussian_functions
    basis_functions_index_list[-1]=num_basis_functions
    gaussian_functions_atom_index_list[-1]=num_gaussian_functions

    return num_gaussian_functions,basis_functions_index_list,gaussian_functions_index_list,atom_of_basisfunction,type_of_basis_function



@njit
def sto_ng_functions_for_s_orbitals(gaussian_functions_coordinates,gaussian_functions_coefficients,gaussian_functions_exponents,gaussian_function_count,
                                    current_atom,current_element,coordinates,sto_precision,n_number):
    """
    Sets up STO-nG functions for s-type orbitals.
    """
    
    gaussian_functions_coordinates[gaussian_function_count:gaussian_function_count+sto_precision]=np.zeros((sto_precision,3),dtype=datatype)+coordinates[current_atom]
    gaussian_functions_coefficients[gaussian_function_count:gaussian_function_count+sto_precision]=sto_coefs[current_element,sto_precision,n_number-1,:sto_precision]
    gaussian_functions_exponents[gaussian_function_count:gaussian_function_count+sto_precision]=sto_exps[current_element,sto_precision,n_number-1,:sto_precision]
    gaussian_function_count+=sto_precision
    
    return gaussian_functions_coordinates,gaussian_functions_coefficients,gaussian_functions_exponents,gaussian_function_count



@njit
def sto_ng_functions_for_p_orbitals(gaussian_functions_coordinates,gaussian_functions_coefficients,gaussian_functions_exponents,gaussian_function_count,
                                    current_atom,current_element,coordinates,lobe_precision,n_number):
    """
    Sets up STO-nG functions for p-type orbitals.
    """
    
    n_number-=2
    half_lobe_precision=int(lobe_precision/2)
    
    for i in range(3):

        x_part=np.zeros(lobe_precision,dtype=datatype)+coordinates[current_atom,0]
        y_part=np.zeros(lobe_precision,dtype=datatype)+coordinates[current_atom,1]
        z_part=np.zeros(lobe_precision,dtype=datatype)+coordinates[current_atom,2]
        if (i==0): x_part-=lobe_offsets[current_element,half_lobe_precision,n_number,:lobe_precision]
        elif (i==1): y_part-=lobe_offsets[current_element,half_lobe_precision,n_number,:lobe_precision]
        else: z_part-=lobe_offsets[current_element,half_lobe_precision,n_number,:lobe_precision]
        gaussian_functions_coordinates[gaussian_function_count:gaussian_function_count+lobe_precision,0]=x_part.T
        gaussian_functions_coordinates[gaussian_function_count:gaussian_function_count+lobe_precision,1]=y_part.T
        gaussian_functions_coordinates[gaussian_function_count:gaussian_function_count+lobe_precision,2]=z_part.T

        gaussian_functions_coefficients[gaussian_function_count:gaussian_function_count+lobe_precision]=lobe_coefs[current_element,half_lobe_precision,n_number-2,:lobe_precision]

        gaussian_functions_exponents[gaussian_function_count:gaussian_function_count+lobe_precision]=lobe_exps[current_element,half_lobe_precision,n_number-2,:lobe_precision]
        
        gaussian_function_count+=lobe_precision
    
    return gaussian_functions_coordinates,gaussian_functions_coefficients,gaussian_functions_exponents,gaussian_function_count




@njit
def calculate_gaussian_function_inputs(element_list,coordinates,num_atoms,num_gaussian_functions):
    """
    Calculates the coordinates, coefficients and exponents for all Gaussian functions.
    Inputs are elements, coordinates and number of basis functions.
    """
    
    gaussian_functions_coordinates=np.zeros((num_gaussian_functions,3),dtype=datatype)
    gaussian_functions_coefficients=np.zeros((num_gaussian_functions),dtype=datatype)
    gaussian_functions_exponents=np.zeros((num_gaussian_functions),dtype=datatype)
    gaussian_function_count=0
    
    for i in range(num_atoms):
        
        current_element=element_list[i]
        if (current_element<=2): atom_type=0
        elif (current_element<=10): atom_type=1
        elif (current_element<=18): atom_type=2

        num_atom_orbitals=basis_set_configs_len[atom_type]

        for j in range(num_atom_orbitals):
            
            orbital_type=basis_set_configs[atom_type,0,j]
            orbital_class=basis_set_configs[atom_type,1,j]
            orbital_num_gaussians=basis_set_configs[atom_type,2,j]

            if ((orbital_type==1 or orbital_type==2 or orbital_type==4) and orbital_class==1):

                if (orbital_type==1): n_value=1
                elif (orbital_type==2): n_value=2
                elif (orbital_type==4): n_value=3

                gaussian_functions_coordinates,gaussian_functions_coefficients,gaussian_functions_exponents,gaussian_function_count\
                                =sto_ng_functions_for_s_orbitals(gaussian_functions_coordinates,gaussian_functions_coefficients,gaussian_functions_exponents,gaussian_function_count,
                                                                 i,current_element,coordinates,orbital_num_gaussians,n_value)

            elif ((orbital_type==3 or orbital_type==5) and orbital_class==1):

                if (orbital_type==3): n_value=2
                elif (orbital_type==5): n_value=3
                
                gaussian_functions_coordinates,gaussian_functions_coefficients,gaussian_functions_exponents,gaussian_function_count\
                                =sto_ng_functions_for_p_orbitals(gaussian_functions_coordinates,gaussian_functions_coefficients,gaussian_functions_exponents,gaussian_function_count,
                                                                 i,current_element,coordinates,orbital_num_gaussians,n_value)
            
    return gaussian_functions_coordinates,gaussian_functions_coefficients,gaussian_functions_exponents





@njit
def calculate_num_orbital_parts(element_list,num_atoms,num_basis_functions):
    """
    Calculate the number of orbital parts in total and create an index list for the indices of the orbital parts at each basis function.
    This gives information about the number of orbital parts per basis function and which orbital part belongs to which basis function. 
    This is necessary to know for part-based approximations as used in the calculation of V_ee.
    There is one orbital part for s-orbitals and two for p-orbitals (four for d-orbitals).
    Inputs are list of elements, number of atoms, number of basis functions and returned are the total number of orbital parts and the orbital parts index list.
    """

    basis_functions_count=0
    num_orbital_parts=0
    orbital_parts_index_list=np.zeros(num_basis_functions+1,dtype='int32')
    
    for i in range(num_atoms):

        current_element=element_list[i]
        if (current_element<=2): atom_type=0
        elif (current_element<=10): atom_type=1
        elif (current_element<=18): atom_type=2
        
        for j in range(basis_set_configs_len[atom_type]):

            orbital_type=basis_set_configs[atom_type,0,j]
            orbital_class=basis_set_configs[atom_type,1,j]
            
            if ((orbital_type==1 or orbital_type==2 or orbital_type==4) and orbital_class==1):
                orbital_parts_index_list[basis_functions_count]=num_orbital_parts
                basis_functions_count+=1
                num_orbital_parts+=1

            elif ((orbital_type==3 or orbital_type==5) and orbital_class==1):
                orbital_parts_index_list[basis_functions_count:basis_functions_count+3]=[num_orbital_parts,num_orbital_parts+2,num_orbital_parts+4]
                basis_functions_count+=3
                num_orbital_parts+=6
    
    orbital_parts_index_list[-1]=num_orbital_parts

    return num_orbital_parts,orbital_parts_index_list



@njit
def calculate_gaussians_for_orbital_parts(element_list,num_atoms,num_orbital_parts):
    """
    Calculates the number of Gaussian functions for all orbital parts and creates an index list for the orbital parts.
    This index list lists the starting index of the Gaussian functions list for each orbital part.
    """

    num_parts_gaussian_functions=0
    orbital_parts_gaussian_index_list=np.zeros(num_orbital_parts+1,dtype='int32')
    orbital_part_count=0

    for i in range(num_atoms):

        current_element=element_list[i]
        if (current_element<=2): atom_type=0
        elif (current_element<=10): atom_type=1
        elif (current_element<=18): atom_type=2

        for j in range(basis_set_configs_len[atom_type]):

            orbital_type=basis_set_configs[atom_type,0,j]
            orbital_class=basis_set_configs[atom_type,1,j]
            
            if ((orbital_type==1 or orbital_type==2 or orbital_type==4) and orbital_class==1):
                orbital_parts_gaussian_index_list[orbital_part_count]=num_parts_gaussian_functions
                num_parts_gaussian_functions+=overlap_sto_precision
                orbital_part_count+=1
            
            elif ((orbital_type==3 or orbital_type==5) and orbital_class==1):
                orbital_parts_gaussian_index_list[orbital_part_count:orbital_part_count+6]=[num_parts_gaussian_functions,num_parts_gaussian_functions+overlap_part_precision,
                                                                                            num_parts_gaussian_functions+2*overlap_part_precision,num_parts_gaussian_functions+3*overlap_part_precision,
                                                                                            num_parts_gaussian_functions+4*overlap_part_precision,num_parts_gaussian_functions+5*overlap_part_precision]
                num_parts_gaussian_functions+=6*overlap_part_precision
                orbital_part_count+=6
        
    orbital_parts_gaussian_index_list[-1]=num_parts_gaussian_functions

    return num_parts_gaussian_functions,orbital_parts_gaussian_index_list




@njit
def sto_ng_functions_for_s_orbital_parts(orbital_parts_coordinates,orbital_parts_coefficients,orbital_parts_exponents,gaussian_function_count,
                                         current_atom,current_element,coordinates,parts_sto_precision,n_number):
    """
    Updates the coordinates, coefficients and exponents of orbital parts as well as the total number of gaussian functions for an s-orbital.
    Inputs are the coordinates, coefficients and exponents of orbital parts (the main list) to be updated, gaussian function count to indicate the start of the update, 
    number of the current atom, element of the current atom, coordinates, number of gaussian functions per orbital part, the main quantum number n and returned are 
    updated coordinates, coefficients and exponents of orbital parts (the main list)
    """
    
    orbital_parts_coordinates[gaussian_function_count:gaussian_function_count+parts_sto_precision]=np.zeros((parts_sto_precision,3),dtype=datatype)+coordinates[current_atom]
    orbital_parts_coefficients[gaussian_function_count:gaussian_function_count+parts_sto_precision]=sto_coefs[current_element,parts_sto_precision,n_number-1,:parts_sto_precision]
    orbital_parts_exponents[gaussian_function_count:gaussian_function_count+parts_sto_precision]=(np.zeros((3,parts_sto_precision))+sto_exps[current_element,parts_sto_precision,n_number-1,:parts_sto_precision]).T

    gaussian_function_count+=parts_sto_precision
    
    return orbital_parts_coordinates,orbital_parts_coefficients,orbital_parts_exponents,gaussian_function_count



@njit
def sto_ng_functions_for_p_orbital_parts(orbital_parts_coordinates,orbital_parts_coefficients,orbital_parts_exponents,gaussian_function_count,
                                         current_atom,current_element,coordinates,parts_sto_precision,n_number):
    """
    Updates the coordinates, coefficients and exponents of orbital parts as well as the total number of gaussian functions for a p-orbital.
    """
    
    n_number-=2
    
    for i in range(6):

        x_part=np.zeros(parts_sto_precision,dtype=datatype)+coordinates[current_atom,0]
        y_part=np.zeros(parts_sto_precision,dtype=datatype)+coordinates[current_atom,1]
        z_part=np.zeros(parts_sto_precision,dtype=datatype)+coordinates[current_atom,2]
        if (i==0 or i==1): x_part+=(-1)**(i+1)*orbital_parts_offsets[current_element,n_number]
        elif (i==2 or i==3): y_part+=(-1)**(i+1)*orbital_parts_offsets[current_element,n_number]
        else: z_part+=(-1)**(i+1)*orbital_parts_offsets[current_element,n_number]
        orbital_parts_coordinates[gaussian_function_count:gaussian_function_count+parts_sto_precision,0]=x_part.T
        orbital_parts_coordinates[gaussian_function_count:gaussian_function_count+parts_sto_precision,1]=y_part.T
        orbital_parts_coordinates[gaussian_function_count:gaussian_function_count+parts_sto_precision,2]=z_part.T
        orbital_parts_coefficients[gaussian_function_count:gaussian_function_count+parts_sto_precision]=(-1)**(i+1)*orbital_parts_coeffs[current_element,n_number]
        if (i==0 or i==1): x_exps,y_exps,z_exps=1,0,0
        elif (i==2 or i==3): x_exps,y_exps,z_exps=0,1,0
        else: x_exps,y_exps,z_exps=0,0,1

        orbital_parts_exponents[gaussian_function_count:gaussian_function_count+parts_sto_precision,0]=orbital_parts_exps[current_element,n_number,:,x_exps]
        orbital_parts_exponents[gaussian_function_count:gaussian_function_count+parts_sto_precision,1]=orbital_parts_exps[current_element,n_number,:,y_exps]
        orbital_parts_exponents[gaussian_function_count:gaussian_function_count+parts_sto_precision,2]=orbital_parts_exps[current_element,n_number,:,z_exps]

        gaussian_function_count+=parts_sto_precision
    
    return orbital_parts_coordinates,orbital_parts_coefficients,orbital_parts_exponents,gaussian_function_count




@njit
def calculate_orbital_parts_preprocessing(element_list,coordinates,num_parts_gaussian_functions,num_atoms):
    """
    Generates arrays of the coordinates, coefficients and exponents for all orbtial parts. 
    The coordinates, coefficients and exponents are for the Gaussian functions which characterize the orbital parts.
    """

    orbital_parts_coordinates=np.zeros((num_parts_gaussian_functions,3),dtype=datatype)
    orbital_parts_coefficients=np.zeros((num_parts_gaussian_functions),dtype=datatype)
    orbital_parts_exponents=np.zeros((num_parts_gaussian_functions,3),dtype=datatype)
    gaussian_function_count=0

    for i in range(num_atoms):
        
        current_element=element_list[i]
        if (current_element<=2): atom_type=0
        elif (current_element<=10): atom_type=1
        elif (current_element<=18): atom_type=2

        num_atom_orbitals=basis_set_configs_len[atom_type]

        for j in range(num_atom_orbitals):
            
            orbital_type=basis_set_configs[atom_type,0,j]
            orbital_class=basis_set_configs[atom_type,1,j]

            if ((orbital_type==1 or orbital_type==2 or orbital_type==4) and orbital_class==1):

                if (orbital_type==1): n_value=1
                elif (orbital_type==2): n_value=2
                elif (orbital_type==4): n_value=3

                orbital_parts_coordinates,orbital_parts_coefficients,orbital_parts_exponents,gaussian_function_count\
                                =sto_ng_functions_for_s_orbital_parts(orbital_parts_coordinates,orbital_parts_coefficients,orbital_parts_exponents,gaussian_function_count,
                                                                      i,current_element,coordinates,parts_sto_precision_1s,n_value)

            elif ((orbital_type==3 or orbital_type==5) and orbital_class==1):

                if (orbital_type==3): n_value=2
                elif (orbital_type==5): n_value=3
                
                orbital_parts_coordinates,orbital_parts_coefficients,orbital_parts_exponents,gaussian_function_count\
                                =sto_ng_functions_for_p_orbital_parts(orbital_parts_coordinates,orbital_parts_coefficients,orbital_parts_exponents,gaussian_function_count,
                                                                      i,current_element,coordinates,parts_sto_precision_2p,n_value) 
    
    return orbital_parts_coordinates,orbital_parts_coefficients,orbital_parts_exponents



@njit
def asymmetric_overlap_integral_reduced(gaussian_functions_coefficients_i,gaussian_functions_coefficients_j,
                                        gaussian_functions_exponents_i_x,gaussian_functions_exponents_j_x,
                                        gaussian_functions_exponents_i_y,gaussian_functions_exponents_j_y,
                                        gaussian_functions_exponents_i_z,gaussian_functions_exponents_j_z,
                                        gaussian_functions_coordinates_i_x,gaussian_functions_coordinates_i_y,gaussian_functions_coordinates_i_z,
                                        gaussian_functions_coordinates_j_x,gaussian_functions_coordinates_j_y,gaussian_functions_coordinates_j_z):
    """
    Calculates an overlap integral for two Gaussian functions. 
    In this function the Gaussians can have different exponents for the three spatial dimensions.
    This is used for the processing of the orbital parts where the corresponding Gaussian functions have a different exponent for one dimension.
    """
    
    prefactor=gaussian_functions_coefficients_i*gaussian_functions_coefficients_j
    exp_sum_x=gaussian_functions_exponents_i_x+gaussian_functions_exponents_j_x
    exp_product_x=gaussian_functions_exponents_i_x*gaussian_functions_exponents_j_x
    product_sum_quotient_x=exp_product_x/exp_sum_x
    exp_sum_y=gaussian_functions_exponents_i_y+gaussian_functions_exponents_j_y
    exp_product_y=gaussian_functions_exponents_i_y*gaussian_functions_exponents_j_y
    product_sum_quotient_y=exp_product_y/exp_sum_y
    exp_sum_z=gaussian_functions_exponents_i_z+gaussian_functions_exponents_j_z
    exp_product_z=gaussian_functions_exponents_i_z*gaussian_functions_exponents_j_z
    product_sum_quotient_z=exp_product_z/exp_sum_z

    distance_x=gaussian_functions_coordinates_i_x-gaussian_functions_coordinates_j_x
    distance_y=gaussian_functions_coordinates_i_y-gaussian_functions_coordinates_j_y
    distance_z=gaussian_functions_coordinates_i_z-gaussian_functions_coordinates_j_z

    pi_divided_by_sum_x=np.pi/exp_sum_x
    pi_divided_by_sum_y=np.pi/exp_sum_y
    pi_divided_by_sum_z=np.pi/exp_sum_z
    exp_part=np.exp(-product_sum_quotient_x*distance_x*distance_x-product_sum_quotient_y*distance_y*distance_y-product_sum_quotient_z*distance_z*distance_z)
    result_s=prefactor*np.sqrt(pi_divided_by_sum_x)*np.sqrt(pi_divided_by_sum_y)*np.sqrt(pi_divided_by_sum_z)*exp_part
    
    return result_s


@njit(parallel=False,fastmath=True)
def calculate_relevant_densities(gaussian_functions_coefficients,gaussian_functions_exponents,gaussian_functions_coordinates,
                                 orbital_parts_index_list,orbital_parts_gaussian_index_list,atom_of_basisfunction,gaussian_functions_index_list,coordinates,num_gaussian_functions,num_basis_functions):
    """
    Evaluates which densities are relevant for the density screening. This is done by calculating the overlap of all orbital parts of a basis function.
    The overlap of two orbital parts is computed by calculating the asymmetric overlap integrals of all Gaussian function combinations in the orbtial parts.
    Works faster with parallel=False.
    """
    
    relevance_matrix=np.zeros((int(num_basis_functions*(num_basis_functions+1)/2)),dtype=datatype)
    relevance_matrix_derivative=0
    ij_list_no_duplicates=np.zeros((int((num_basis_functions*(num_basis_functions+1))/2.0),2),dtype='int32')
    gaussians_for_densities=np.zeros((int((num_gaussian_functions*(num_gaussian_functions+1))/1.0),2),dtype='int32')
    gaussians_for_densities_index_list=np.zeros(int((num_basis_functions*(num_basis_functions+1))/2.0),dtype='int32')
    count_no_duplicates=0
    gaussians_count_no_duplicates=0

    dist_threshold=10.0
    dist_threshold_squared=dist_threshold**2

    for i in range(num_basis_functions):
        for j in range(i,num_basis_functions):

            x_dist=coordinates[atom_of_basisfunction[i],0]-coordinates[atom_of_basisfunction[j],0]
            y_dist=coordinates[atom_of_basisfunction[i],1]-coordinates[atom_of_basisfunction[j],1]
            z_dist=coordinates[atom_of_basisfunction[i],2]-coordinates[atom_of_basisfunction[j],2]

            if (np.abs(x_dist)>dist_threshold):
                continue
            if (np.abs(y_dist)>dist_threshold):
                continue
            if (np.abs(z_dist)>dist_threshold):
                continue
            if (x_dist*x_dist+y_dist*y_dist+z_dist*z_dist>dist_threshold_squared):
                continue


            for pi in range(orbital_parts_index_list[i],orbital_parts_index_list[i+1]):
                for pj in range(orbital_parts_index_list[j],orbital_parts_index_list[j+1]):
                    orbital_parts_overlap=0

                    for gi in prange(orbital_parts_gaussian_index_list[pi],orbital_parts_gaussian_index_list[pi+1]):
                        for gj in prange(orbital_parts_gaussian_index_list[pj],orbital_parts_gaussian_index_list[pj+1]):
                            integral_value=asymmetric_overlap_integral_reduced(gaussian_functions_coefficients[gi],gaussian_functions_coefficients[gj],
                                                                               gaussian_functions_exponents[gi,0],gaussian_functions_exponents[gj,0],
                                                                               gaussian_functions_exponents[gi,1],gaussian_functions_exponents[gj,1],
                                                                               gaussian_functions_exponents[gi,2],gaussian_functions_exponents[gj,2],
                                                                               gaussian_functions_coordinates[gi,0],gaussian_functions_coordinates[gi,1],gaussian_functions_coordinates[gi,2],
                                                                               gaussian_functions_coordinates[gj,0],gaussian_functions_coordinates[gj,1],gaussian_functions_coordinates[gj,2])
                            orbital_parts_overlap+=integral_value

                    if (orbital_parts_overlap>=0):
                        relevance_matrix[count_no_duplicates]+=orbital_parts_overlap
                    else:
                        relevance_matrix[count_no_duplicates]-=orbital_parts_overlap

            if (relevance_matrix[count_no_duplicates]>density_threshold):
                ij_list_no_duplicates[count_no_duplicates,0],ij_list_no_duplicates[count_no_duplicates,1]=i,j
                count_no_duplicates+=1

                for gi in range(gaussian_functions_index_list[i],gaussian_functions_index_list[i+1]):
                    for gj in range(gaussian_functions_index_list[j],gaussian_functions_index_list[j+1]):
                        gaussians_for_densities[gaussians_count_no_duplicates,0],gaussians_for_densities[gaussians_count_no_duplicates,1]=gi,gj
                        gaussians_count_no_duplicates+=1
                
                gaussians_for_densities_index_list[count_no_duplicates]=gaussians_count_no_duplicates

    relevance_matrix=relevance_matrix[:count_no_duplicates]
    
    ij_list_no_duplicates=ij_list_no_duplicates[:count_no_duplicates]
    gaussians_for_densities=gaussians_for_densities[:gaussians_count_no_duplicates]

    gaussians_for_densities_index_list=gaussians_for_densities_index_list[:count_no_duplicates+1]

    return ij_list_no_duplicates,gaussians_for_densities,gaussians_for_densities_index_list,gaussians_count_no_duplicates,count_no_duplicates,relevance_matrix,relevance_matrix_derivative





@njit
def calculate_center_of_mass(coordinates,elements,num_atoms):
    """
    Calculates the center of mass for a set of nuclei positions. The nuclei are weighted with the atomic mass values stored in the array atomic_masses (see variables section).
    Inputs are nuclei coordinates, elements (for weights) and number of atoms and it returns the center of mass
    """

    center_of_mass=np.zeros(3,dtype=datatype)
    total_mass=0.0
    for i in range(num_atoms):
        current_atomic_mass=atomic_masses[elements[i]]
        center_of_mass+=current_atomic_mass*coordinates[i]
        total_mass+=current_atomic_mass
    center_of_mass/=total_mass
    return center_of_mass





"""
--------------------------
hyp1f1 function evaluation
--------------------------
"""




@njit
def erf(x):
    """
    Calculates an approximation for the error function erf(x) for x>=0 and also returns exp(-x^2).
    Has a maximum error aroung 1.0e-14. Only use for calculations which have to be very accurate
    Input: x (x>=0)
    Returns: erf(x), exp(-x^2)
    """

    x2=x*x
    exp_val=np.exp(-x2)
    erf_val=1-exp_val*(0.56418958354775629/(x+2.06955023132914151)*\
            (x2+2.71078540045147805*x+ 5.80755613130301624)/(x2+3.47954057099518960*x+12.06166887286239555)*\
            (x2+3.47469513777439592*x+12.07402036406381411)/(x2+3.72068443960225092*x+ 8.44319781003968454)*\
            (x2+4.00561509202259545*x+ 9.30596659485887898)/(x2+3.90225704029924078*x+ 6.36161630953880464)*\
            (x2+5.16722705817812584*x+ 9.12661617673673262)/(x2+4.03296893109262491*x+ 5.13578530585681539)*\
            (x2+5.95908795446633271*x+ 9.19435612886969243)/(x2+4.11240942957450885*x+ 4.48640329523408675))

    return erf_val

@njit
def erf2(x):
    """
    Calculates an approximation for the error function erf(x) for x>=0 and also returns exp(-x^2).
    Has a lower accuracy than erf() - the maximum error is around 1.0e-7 which is still good enough for most calculations.
    Input: x (x>=0)
    Returns: erf(x), exp(-x^2)
    """

    t=1.0/(1.0+0.3275911*x)
    x2,t2=x*x,t*t
    exp_val=np.exp(-x2)
    erf_val=1-(0.254829592*t-0.284496736*t2+1.421413741*t*t2-1.453152027*t2*t2+1.061405429*t2*t2*t)*exp_val
    
    return erf_val,exp_val

@njit
def erf2_val(x):
    """
    Calculates an approximation for the error function erf(x) for x>=0 and also returns exp(-x^2).
    Input: x (x>=0)
    Returns: erf(x), exp(-x^2)
    """

    t=1.0/(1.0+0.3275911*x)
    x2,t2=x*x,t*t
    erf_val=1-(0.254829592*t-0.284496736*t2+1.421413741*t*t2-1.453152027*t2*t2+1.061405429*t2*t2*t)*np.exp(-x2)
    
    return erf_val

prefactor_hyp1f1=np.sqrt(np.pi) 
@njit
def erf_hyp1f1_with_arrays(x):
    """
    Calculates an approximation for the hyp1f1 function which uses the error function.
    hyp1f1(x)=sqrt(pi)*erf(sqrt(x))/(2*sqrt(x))
    hyp1f1'(x)=d/dx((sqrt(pi)*erf(sqrt(x)))/(2*sqrt(x)))=exp(-x)/(2*x)-(sqrt(pi)*erf(sqrt(x)))/(4*x^(3/2))
    Input is x, x>=0 and
    returned is erf(x)
    """
    
    if (x>16):
        return 1.0/np.sqrt(x)
    else:
        sx=np.sqrt(x+1.0e-7)
        erf_val=erf2_val(sx)
        return erf_val/sx




"""
-----------------------------------------------------
Overlap, kinetic and nuclei matrices and ionic energy
-----------------------------------------------------
"""



@njit(fastmath=True)
def overlap_and_kinetic_integral(gaussian_functions_coefficients_i,gaussian_functions_coefficients_j,gaussian_functions_exponents_i,gaussian_functions_exponents_j,
                                 gaussian_functions_coordinates_i_x,gaussian_functions_coordinates_i_y,gaussian_functions_coordinates_i_z,
                                 gaussian_functions_coordinates_j_x,gaussian_functions_coordinates_j_y,gaussian_functions_coordinates_j_z):
    """
    Calculates the overlap intgeral and the kinetic integral of two Gaussian functions i and j as well as its derivatives with respect to a change in the coordinates of the Gaussian function i.
    In addition to this, prefactors for the nuclei integrals are calculated.
    Additionally, the center coordinates/weighted coordinates of the new Gaussian functions, which are created by the combination of the Gaussian functions i and j, are calculated.
    Inputs are coefficients (i/j), exponents (i/j), coordinates (i/j) and 
    retured will be the overlap intergral <i|j>, its derivatives in x/y/z-direction,
    the kinetic integral <i|T^|j>, its derivatives in x/y/z-direction,
    the nuclei prefactor ~<i|V_en_atom|j>, its derivatives in x/y/z-direction and
    the x/y/z-coordinate of the center coordinates (Gaussian center).
    """
    
    prefactor=gaussian_functions_coefficients_i*gaussian_functions_coefficients_j
    exp_sum=gaussian_functions_exponents_i+gaussian_functions_exponents_j
    exp_product=gaussian_functions_exponents_i*gaussian_functions_exponents_j
    product_sum_quotient=exp_product/exp_sum

    distance_x=gaussian_functions_coordinates_i_x-gaussian_functions_coordinates_j_x
    distance_y=gaussian_functions_coordinates_i_y-gaussian_functions_coordinates_j_y
    distance_z=gaussian_functions_coordinates_i_z-gaussian_functions_coordinates_j_z
    coordinate_distance=distance_x*distance_x+distance_y*distance_y+distance_z*distance_z

    pi_divided_by_sum=np.pi/exp_sum
    result_s=prefactor*pi_divided_by_sum*np.sqrt(pi_divided_by_sum)*np.exp(-product_sum_quotient*coordinate_distance)

    result_t=3.0*result_s*gaussian_functions_exponents_j*(1.0-gaussian_functions_exponents_j/exp_sum)-\
             2.0*result_s*product_sum_quotient*product_sum_quotient*coordinate_distance

    derivative_const_part=-2.0*product_sum_quotient*result_s
    derivative_s_i_x=derivative_const_part*distance_x
    derivative_s_i_y=derivative_const_part*distance_y
    derivative_s_i_z=derivative_const_part*distance_z
    derivative_s_j_x,derivative_s_j_y,derivative_s_j_z=-derivative_s_i_x,-derivative_s_i_y,-derivative_s_i_z


    derivative_const_part_t_1=3.0*gaussian_functions_exponents_j*(1.0-gaussian_functions_exponents_j/exp_sum)
    derivative_const_part_t_2=-2.0*product_sum_quotient*product_sum_quotient*coordinate_distance
    derivative_const_part_t_3=-2.0*result_s*product_sum_quotient*product_sum_quotient
    derivative_t_i_x=(derivative_const_part_t_1+derivative_const_part_t_2)*derivative_s_i_x+derivative_const_part_t_3*2.0*distance_x
    derivative_t_i_y=(derivative_const_part_t_1+derivative_const_part_t_2)*derivative_s_i_y+derivative_const_part_t_3*2.0*distance_y
    derivative_t_i_z=(derivative_const_part_t_1+derivative_const_part_t_2)*derivative_s_i_z+derivative_const_part_t_3*2.0*distance_z
    derivative_t_j_x,derivative_t_j_y,derivative_t_j_z=-derivative_t_i_x,-derivative_t_i_y,-derivative_t_i_z

    result_n=-prefactor*(2.0*np.pi/exp_sum)*np.exp(-product_sum_quotient*coordinate_distance)

    weighted_coords_ij_x=(gaussian_functions_exponents_i*gaussian_functions_coordinates_i_x+gaussian_functions_exponents_j*gaussian_functions_coordinates_j_x)/exp_sum
    weighted_coords_ij_y=(gaussian_functions_exponents_i*gaussian_functions_coordinates_i_y+gaussian_functions_exponents_j*gaussian_functions_coordinates_j_y)/exp_sum
    weighted_coords_ij_z=(gaussian_functions_exponents_i*gaussian_functions_coordinates_i_z+gaussian_functions_exponents_j*gaussian_functions_coordinates_j_z)/exp_sum

    return result_s,derivative_s_i_x,derivative_s_i_y,derivative_s_i_z,derivative_s_j_x,derivative_s_j_y,derivative_s_j_z,\
           result_t,derivative_t_i_x,derivative_t_i_y,derivative_t_i_z,derivative_t_j_x,derivative_t_j_y,derivative_t_j_z,\
           result_n,weighted_coords_ij_x,weighted_coords_ij_y,weighted_coords_ij_z,np.abs(prefactor)



@njit(fastmath=True,parallel=True)
def calculate_overlap_and_kinetic_matrix(gaussian_functions_coefficients,gaussian_functions_exponents,gaussian_functions_coordinates,
                                         gaussian_functions_index_list,gaussians_for_densities,gaussians_for_densities_index_list,ij_list_no_duplicates,
                                         num_gaussians_for_densities,relevant_densities_no_duplicates,num_basis_functions,num_gaussian_functions):
    """
    Calculates the overlap matrix with all basis functions i and j which can be decomposed into Gaussian functions gi and gj:
    Inputs are coordinates, coefficients, exponents of the Gaussian functions,
    basis function <-> Gaussian function list, basis function <-> atom list, number of atoms/basis functions and Gaussian functions
    This function will return the overlap matrix S with S_ij = <phi_i|phi_j> and its derivative w.r.t. phi_i,
    the kinetic matrix T with T_ij = <phi_i|-1/2*d^2/dr^2|phi_j> and its derivative w.r.t. phi_i,
    a nuclei prefactor matrix which is used for the computation of the nuclei potential matrix V_en,
    the center coordinates of all combinations of two Gaussian functions (also used later).
    """

    overlap_matrix=np.zeros((relevant_densities_no_duplicates),dtype=datatype)
    kinetic_matrix=np.zeros((relevant_densities_no_duplicates),dtype=datatype)
    overlap_matrix_derivative=np.zeros((relevant_densities_no_duplicates,6),dtype=datatype)
    kinetic_matrix_derivative=np.zeros((relevant_densities_no_duplicates,6),dtype=datatype)
    nuclei_prefactor=np.zeros((num_gaussians_for_densities),dtype=datatype)
    weighted_coords=np.zeros((num_gaussians_for_densities,3),dtype=datatype)
    orbitals_center_coords=np.zeros((relevant_densities_no_duplicates,3),dtype=datatype)

    for d in range(relevant_densities_no_duplicates):
        i,j=ij_list_no_duplicates[d]
        prefactor_sum=0
        for gd in range(gaussians_for_densities_index_list[d],gaussians_for_densities_index_list[d+1]):
            gi,gj=gaussians_for_densities[gd,0],gaussians_for_densities[gd,1]

            integral_value_s,derivative_s_i_x,derivative_s_i_y,derivative_s_i_z,\
                            derivative_s_j_x,derivative_s_j_y,derivative_s_j_z,\
            integral_value_t,derivative_t_i_x,derivative_t_i_y,derivative_t_i_z,\
                            derivative_t_j_x,derivative_t_j_y,derivative_t_j_z,\
            integral_value_n,weighted_coords_ij_x,weighted_coords_ij_y,weighted_coords_ij_z,prefactor \
                            =overlap_and_kinetic_integral(gaussian_functions_coefficients[gi],gaussian_functions_coefficients[gj],gaussian_functions_exponents[gi],gaussian_functions_exponents[gj],
                                                          gaussian_functions_coordinates[gi,0],gaussian_functions_coordinates[gi,1],gaussian_functions_coordinates[gi,2],
                                                          gaussian_functions_coordinates[gj,0],gaussian_functions_coordinates[gj,1],gaussian_functions_coordinates[gj,2])
            
            overlap_matrix[d]+=integral_value_s
            kinetic_matrix[d]+=integral_value_t
            nuclei_prefactor[gd]=integral_value_n
            prefactor_sum+=prefactor

            overlap_matrix_derivative[d,0]+=derivative_s_i_x
            overlap_matrix_derivative[d,1]+=derivative_s_i_y
            overlap_matrix_derivative[d,2]+=derivative_s_i_z
            overlap_matrix_derivative[d,3]+=derivative_s_j_x
            overlap_matrix_derivative[d,4]+=derivative_s_j_y
            overlap_matrix_derivative[d,5]+=derivative_s_j_z

            kinetic_matrix_derivative[d,0]+=derivative_t_i_x
            kinetic_matrix_derivative[d,1]+=derivative_t_i_y
            kinetic_matrix_derivative[d,2]+=derivative_t_i_z
            kinetic_matrix_derivative[d,3]+=derivative_t_j_x
            kinetic_matrix_derivative[d,4]+=derivative_t_j_y
            kinetic_matrix_derivative[d,5]+=derivative_t_j_z

            orbitals_center_coords[d,0]+=prefactor*weighted_coords_ij_x
            orbitals_center_coords[d,1]+=prefactor*weighted_coords_ij_y
            orbitals_center_coords[d,2]+=prefactor*weighted_coords_ij_z

            weighted_coords[gd,0]=weighted_coords_ij_x
            weighted_coords[gd,1]=weighted_coords_ij_y
            weighted_coords[gd,2]=weighted_coords_ij_z
        
        orbitals_center_coords[d,0]/=prefactor_sum
        orbitals_center_coords[d,1]/=prefactor_sum
        orbitals_center_coords[d,2]/=prefactor_sum

    return overlap_matrix,overlap_matrix_derivative,kinetic_matrix,kinetic_matrix_derivative,nuclei_prefactor,weighted_coords,orbitals_center_coords



@njit(fastmath=True)
def nuclei_integral(prefactor_n,exp_sum,weighted_coords_x,weighted_coords_y,weighted_coords_z,atom_coords_x,atom_coords_y,atom_coords_z,element):
    """
    Calculates a nuclei integral n_ija of the form <phi_i|Z_a/(r-r_a)|phi_j>.
    Additionally the derivatives w.r.t. r_a, phi_i and phi_j are calculated.
    Inputs are a prefactor, Gaussian functions exponents sums (precomputed), derivative prefactors, orbital distance (distance between the two Gaussian functions),
    center coordinates/weighted coordinates of the combination of the two Gaussians, coordinates of the atom a, element of the atom a and returned will be
    the nuclei integral n_ija.
    """

    distance_x=weighted_coords_x-atom_coords_x
    distance_y=weighted_coords_y-atom_coords_y
    distance_z=weighted_coords_z-atom_coords_z
    atom_distance=distance_x*distance_x+distance_y*distance_y+distance_z*distance_z
    hyp1f1_value=nuclei_hyp1f1_prefactor*erf_hyp1f1_with_arrays(exp_sum*atom_distance)

    result_n=prefactor_n*element*hyp1f1_value

    return result_n 


@njit(fastmath=True,parallel=True)
def calculate_nuclei_matrix_and_derivatives(gaussian_functions_exponents,gaussian_functions_coordinates,
                                            ij_list_no_duplicates,gaussians_for_densities,gaussians_for_densities_index_list,num_gaussians_for_densities,relevant_densities_no_duplicates,
                                            gaussian_functions_index_list,atom_of_basisfunction,coordinates,elements,
                                            relevance_matrix,relevance_matrix_derivative,
                                            nuclei_prefactor,weighted_coords,orbitals_center_coords,num_atoms,num_basis_functions):
    """
    Calculates the nuclei potential matix V_en or N with V_en_ij=N_ij=Sum_a[n_ija] where n_ija are calculated in the function nuclei_integral().
    Instead of the double loop formalism over all combinations of two basis functions:
        for i in range(num_basis_functions):
            for j in range(i,num_basis_functions):
    we only loop over the relevant densities.
    Inputs are Exponents and coordinates of Gaussian functions, basis function <-> Gaussian function list, basis function <-> atom list,
    coordinates of the atoms, elements of the atoms, precomputed nuclei prefactor matrix, precomputed center/weighted coordinates, number of atoms/basis functions and returned
    will be the nuclei potential matrix V_en.
    """

    nuclei_matrix=np.zeros((relevant_densities_no_duplicates),dtype=datatype)
    nuclei_matrix_nuclei_derivative=np.zeros((1,1,6),dtype=datatype) 
    nuclei_matrix_wavefunction_derivative=np.zeros((1,6),dtype=datatype)

    for d in prange(relevant_densities_no_duplicates):
        i,j=ij_list_no_duplicates[d,0],ij_list_no_duplicates[d,1]
        for gd in range(gaussians_for_densities_index_list[d],gaussians_for_densities_index_list[d+1]):
            gi,gj=gaussians_for_densities[gd,0],gaussians_for_densities[gd,1]

            exp_sum=gaussian_functions_exponents[gi]+gaussian_functions_exponents[gj]
            atom_1,atom_2=atom_of_basisfunction[i],atom_of_basisfunction[j]
            coordinates_a1,coordinates_a2=coordinates[atom_1],coordinates[atom_2]
            distance_12_x=0.5*(coordinates_a1[0]+coordinates_a2[0])
            distance_12_y=0.5*(coordinates_a1[1]+coordinates_a2[1])
            distance_12_z=0.5*(coordinates_a1[2]+coordinates_a2[2])
            
            for atom in range(num_atoms):
                
                distance_12_n_x=distance_12_x-coordinates[atom,0]
                distance_12_n_y=distance_12_y-coordinates[atom,1]
                distance_12_n_z=distance_12_z-coordinates[atom,2]
                distance_12_n_2=distance_12_n_x*distance_12_n_x+distance_12_n_y*distance_12_n_y+distance_12_n_z*distance_12_n_z
                distance_12_n=np.sqrt(distance_12_n_2)
                if (distance_12_n>coulomb_threshold):
                    continue
                elif (distance_12_n<coulomb_threshold_low):
                    relevance_12_n=1.0
                else:
                    fraction_12_n=1.0-(distance_12_n-coulomb_threshold_low)/coulomb_threshold_difference
                    fraction_square_12_n=fraction_12_n*fraction_12_n
                    relevance_12_n=-2.0*fraction_square_12_n*fraction_12_n+3.0*fraction_square_12_n
                
                relevance_12_value=relevance_matrix[d]
                if (relevance_12_value>density_threshold_2):
                    relevance_12=1.0
                else:
                    fraction_12=(relevance_12_value-density_threshold)/density_threshold_difference
                    fraction_square_12=fraction_12*fraction_12
                    relevance_12=-2.0*fraction_square_12*fraction_12+3.0*fraction_square_12

                relevance_prefactor=relevance_12*relevance_12_n

                integral_value_n=nuclei_integral(nuclei_prefactor[gd],exp_sum,
                                                 weighted_coords[gd,0],weighted_coords[gd,1],weighted_coords[gd,2],
                                                 coordinates[atom,0],coordinates[atom,1],coordinates[atom,2],elements[atom])
                
                nuclei_matrix[d]+=integral_value_n*relevance_prefactor

    return nuclei_matrix,nuclei_matrix_nuclei_derivative,nuclei_matrix_wavefunction_derivative


@njit(fastmath=True,parallel=True)
def calculate_ionic_energy(coordinates,elements,num_atoms):
    """
    Calculates the ionic energy i.e. the repulsion of the atom cores.
    """
    ionic_energy=0
    for i in prange(num_atoms):
        for j in range(i+1,num_atoms):

            distance_x=coordinates[i,0]-coordinates[j,0]
            distance_y=coordinates[i,1]-coordinates[j,1]
            distance_z=coordinates[i,2]-coordinates[j,2]
            r=np.sqrt(distance_x*distance_x+distance_y*distance_y+distance_z*distance_z)
            
            if (r>coulomb_threshold):
                relevance_n_n=0.0
            elif (r<coulomb_threshold_low):
                relevance_n_n=1.0
            else:
                fraction=1.0-(r-coulomb_threshold_low)/coulomb_threshold_difference
                fraction_square=fraction*fraction
                relevance_n_n=-2.0*fraction_square*fraction+3.0*fraction_square
            
            ionic_energy+=relevance_n_n*elements[i]*elements[j]*1.0/r
    return ionic_energy





"""
-----------------------------------
Electron repulsion tensor functions
-----------------------------------
"""


"""
Additional information for thies section:

phi_1-phi_2 interaction -> cut-off via density threshold
phi_3-phi_4 interaction -> cut-off via density threshold
(phi_1|phi_2)-(phi_3|phi_4) interaction -> cut-off via coulomb threshold

The naive implementation for the electron tensor (V_ee) and its derivative (d_V_ee) as a 4-dimensional object is shown below.
We see the 8-fold symmetry of the electron repulsion integrals.
V_ee[i,j,k,l]=v_ijkl
V_ee[i,j,l,k]=v_ijkl
V_ee[j,i,k,l]=v_ijkl
V_ee[j,i,l,k]=v_ijkl
V_ee[k,l,i,j]=v_ijkl
V_ee[k,l,j,i]=v_ijkl
V_ee[l,k,i,j]=v_ijkl
V_ee[l,k,j,i]=v_ijkl
d_V_ee[i,j,l,k,atom_of_basisfunction[i],0],d_V_ee[i,j,l,k,atom_of_basisfunction[i],1],d_V_ee[i,j,l,k,atom_of_basisfunction[i],2]=v_ijkl_i_dx,v_ijkl_i_dy,v_ijkl_i_dz
d_V_ee[i,j,k,l,atom_of_basisfunction[i],0],d_V_ee[i,j,k,l,atom_of_basisfunction[i],1],d_V_ee[i,j,k,l,atom_of_basisfunction[i],2]=v_ijkl_i_dx,v_ijkl_i_dy,v_ijkl_i_dz
d_V_ee[j,i,k,l,atom_of_basisfunction[j],0],d_V_ee[j,i,k,l,atom_of_basisfunction[j],1],d_V_ee[j,i,k,l,atom_of_basisfunction[j],2]=v_ijkl_j_dx,v_ijkl_j_dy,v_ijkl_j_dz
d_V_ee[j,i,l,k,atom_of_basisfunction[j],0],d_V_ee[j,i,l,k,atom_of_basisfunction[j],1],d_V_ee[j,i,l,k,atom_of_basisfunction[j],2]=v_ijkl_j_dx,v_ijkl_j_dy,v_ijkl_j_dz
d_V_ee[k,l,i,j,atom_of_basisfunction[k],0],d_V_ee[k,l,i,j,atom_of_basisfunction[k],1],d_V_ee[k,l,i,j,atom_of_basisfunction[k],2]=v_ijkl_k_dx,v_ijkl_k_dy,v_ijkl_k_dz
d_V_ee[k,l,j,i,atom_of_basisfunction[k],0],d_V_ee[k,l,j,i,atom_of_basisfunction[k],1],d_V_ee[k,l,j,i,atom_of_basisfunction[k],2]=v_ijkl_k_dx,v_ijkl_k_dy,v_ijkl_k_dz
d_V_ee[l,k,i,j,atom_of_basisfunction[l],0],d_V_ee[l,k,i,j,atom_of_basisfunction[l],1],d_V_ee[l,k,i,j,atom_of_basisfunction[l],2]=v_ijkl_l_dx,v_ijkl_l_dy,v_ijkl_l_dz
d_V_ee[l,k,j,i,atom_of_basisfunction[l],0],d_V_ee[l,k,j,i,atom_of_basisfunction[l],1],d_V_ee[l,k,j,i,atom_of_basisfunction[l],2]=v_ijkl_l_dx,v_ijkl_l_dy,v_ijkl_l_dz
"""




@njit(parallel=True,fastmath=True)
def overlap_contributions(gaussian_functions_coefficients,gaussian_functions_exponents,gaussian_functions_coordinates,
                          gaussians_for_densities,gaussians_for_densities_index_list,num_gaussians_for_densities,relevant_densities_no_duplicates,num_gaussian_functions):
    """
    Precalculations for the electron repulsion integral evaluation.
    """

    S_terms=np.zeros((num_gaussians_for_densities),dtype=datatype)
    S_terms_derivatives=np.zeros((num_gaussians_for_densities,3),dtype=datatype)
    exp_sums=np.zeros((num_gaussians_for_densities),dtype=datatype)
    exp_products=np.zeros((num_gaussians_for_densities),dtype=datatype)
    center_coords=np.zeros((num_gaussians_for_densities,3),dtype=datatype)
    for d in prange(relevant_densities_no_duplicates):
        for gd in range(gaussians_for_densities_index_list[d],gaussians_for_densities_index_list[d+1]):
            i,j=gaussians_for_densities[gd,0],gaussians_for_densities[gd,1]
            exp_sums[gd]=gaussian_functions_exponents[i]+gaussian_functions_exponents[j]
            exp_products[gd]=gaussian_functions_exponents[i]*gaussian_functions_exponents[j]
            quotient=exp_products[gd]/exp_sums[gd]
            coords_i,coords_j=gaussian_functions_coordinates[i],gaussian_functions_coordinates[j]
            distance_x=coords_i[0]-coords_j[0]
            distance_y=coords_i[1]-coords_j[1]
            distance_z=coords_i[2]-coords_j[2]
            coordinate_difference=distance_x*distance_x+distance_y*distance_y+distance_z*distance_z
            center_coords[gd]=(gaussian_functions_exponents[i]*gaussian_functions_coordinates[i]+
                               gaussian_functions_exponents[j]*gaussian_functions_coordinates[j])/exp_sums[gd]
            S_terms[gd]=np.exp(-quotient*coordinate_difference)*gaussian_functions_coefficients[i]*gaussian_functions_coefficients[j]/exp_sums[gd]*V_ee_prefactor_sqrt/np.sqrt(exp_sums[gd])
            S_terms_derivatives[gd,0]=-2.0*distance_x*quotient*np.exp(-quotient*coordinate_difference)\
                                            *gaussian_functions_coefficients[i]*gaussian_functions_coefficients[j]/exp_sums[gd]*V_ee_prefactor_sqrt/np.sqrt(exp_sums[gd])
            S_terms_derivatives[gd,1]=-2.0*distance_y*quotient*np.exp(-quotient*coordinate_difference)\
                                            *gaussian_functions_coefficients[i]*gaussian_functions_coefficients[j]/exp_sums[gd]*V_ee_prefactor_sqrt/np.sqrt(exp_sums[gd])
            S_terms_derivatives[gd,2]=-2.0*distance_z*quotient*np.exp(-quotient*coordinate_difference)\
                                            *gaussian_functions_coefficients[i]*gaussian_functions_coefficients[j]/exp_sums[gd]*V_ee_prefactor_sqrt/np.sqrt(exp_sums[gd])
            
    return S_terms,S_terms_derivatives,1.0/exp_sums,center_coords











@njit
def electron_integrals_list_generation(gaussian_functions_exponents,S_terms,S_terms_derivatives,exp_sums,center_coords,gaussians_for_densities,gaussians_for_densities_index_list,
                                       ij_list_no_duplicates,gaussian_functions_index_list,type_of_basis_function,relevant_densities_no_duplicates):
    """
    Preprocessing for the ERI evaluation. Here various values which only depend on one density are precomputed and stored in arrays.
    These will be accessed during the actual evaluation of the ERIs which speeds up the calculation since they do not need to be calculated again.
    """

    gaussian_functions_exponents_i_list,gaussian_functions_exponents_j_list\
        =np.zeros((max_gaussian_functions_square,relevant_densities_no_duplicates),dtype=e_tensor_datatype),\
         np.zeros((max_gaussian_functions_square,relevant_densities_no_duplicates),dtype=e_tensor_datatype)
    overlap_list=np.zeros((max_gaussian_functions_square,relevant_densities_no_duplicates),dtype=e_tensor_datatype)
    overlap_derivative_i_x_list,overlap_derivative_i_y_list,overlap_derivative_i_z_list,overlap_derivative_j_x_list,overlap_derivative_j_y_list,overlap_derivative_j_z_list\
        =np.zeros((max_gaussian_functions_square,relevant_densities_no_duplicates),dtype=e_tensor_datatype),\
         np.zeros((max_gaussian_functions_square,relevant_densities_no_duplicates),dtype=e_tensor_datatype),\
         np.zeros((max_gaussian_functions_square,relevant_densities_no_duplicates),dtype=e_tensor_datatype),\
         np.zeros((max_gaussian_functions_square,relevant_densities_no_duplicates),dtype=e_tensor_datatype),\
         np.zeros((max_gaussian_functions_square,relevant_densities_no_duplicates),dtype=e_tensor_datatype),\
         np.zeros((max_gaussian_functions_square,relevant_densities_no_duplicates),dtype=e_tensor_datatype)
    exp_sum_list=np.zeros((max_gaussian_functions_square,relevant_densities_no_duplicates),dtype=e_tensor_datatype)
    center_coords_list=np.zeros((max_gaussian_functions_square,relevant_densities_no_duplicates,3),dtype=e_tensor_datatype)
    
    ij_list_no_duplicates_new=np.zeros((relevant_densities_no_duplicates,2),dtype='int32')
    
    combinations_limits=np.zeros(num_basis_function_types_sqaure,dtype='int32')
    gaussians_limits=np.zeros(max_gaussian_functions_square,dtype='int32')
    type_combination_lengths=np.zeros(num_basis_function_types_sqaure,dtype='int32')
    type_combinations_i=np.zeros(num_basis_function_types_sqaure,dtype='int32')
    type_combinations_j=np.zeros(num_basis_function_types_sqaure,dtype='int32')

    for ti in range(0,num_basis_function_types):
        for tj in range(0,num_basis_function_types):
            index=ti*num_basis_function_types+tj
            type_combinations_i[index],type_combinations_j[index]=ti+1,tj+1
            type_combination_lengths[index]=basis_function_type_length_list[ti]*basis_function_type_length_list[tj]
    type_combination_lengths_indexing=np.flip(type_combination_lengths.argsort())
    type_combination_lengths=np.flip(np.sort(type_combination_lengths))
    type_combinations_i=type_combinations_i[type_combination_lengths_indexing]
    type_combinations_j=type_combinations_j[type_combination_lengths_indexing]

    count_densities=-1
    for t in range(len(type_combinations_i)):
        ti,tj=type_combinations_i[t],type_combinations_j[t]
        for density in range(relevant_densities_no_duplicates):
            i,j=ij_list_no_duplicates[density]
            if (type_of_basis_function[i]==ti and type_of_basis_function[j]==tj):
                count_densities+=1
                ij_list_no_duplicates_new[count_densities,0],ij_list_no_duplicates_new[count_densities,1]=i,j
                count_gaussians=-1
                for gd in range(gaussians_for_densities_index_list[density],gaussians_for_densities_index_list[density+1]):
                    gi,gj=gaussians_for_densities[gd,0],gaussians_for_densities[gd,1]
                    count_gaussians+=1
                    gaussian_functions_exponents_i_list[count_gaussians,count_densities],gaussian_functions_exponents_j_list[count_gaussians,count_densities]\
                        =gaussian_functions_exponents[gi],gaussian_functions_exponents[gj]
                    overlap_list[count_gaussians,count_densities]=S_terms[gd]
                    exp_sum_list[count_gaussians,count_densities]=exp_sums[gd]
                    center_coords_list[count_gaussians,count_densities,0],center_coords_list[count_gaussians,count_densities,1],center_coords_list[count_gaussians,count_densities,2]\
                        =center_coords[gd,0],center_coords[gd,1],center_coords[gd,2]
        combinations_limits[t]=count_densities+1

    for gi in range(max_gaussian_functions_square):
        gaussians_limits[gi]=combinations_limits[-1]
        for t in range(1,len(type_combination_lengths)):
            if (type_combination_lengths[t]<=gi):
                gaussians_limits[gi]=combinations_limits[t-1]
                break
    
    return gaussian_functions_exponents_i_list,gaussian_functions_exponents_j_list,overlap_list,\
           overlap_derivative_i_x_list,overlap_derivative_i_y_list,overlap_derivative_i_z_list,overlap_derivative_j_x_list,overlap_derivative_j_y_list,overlap_derivative_j_z_list,\
           exp_sum_list,center_coords_list,ij_list_no_duplicates_new,gaussians_limits





@njit(fastmath=True,parallel=True)
def electron_integrals_distance_relevance(relevance_matrix,ij_list_no_duplicates,atom_of_basisfunction,coordinates,orbitals_center_coords,relevant_densities_no_duplicates):
    """
    Calculates estimates for the relevance of density/density interactions. This is done by iterating over all density/density pairs.
    Only relevant densities (tabulated in the ij_list_no_duplicates) are used for this.
    For each density/density combination an estimate of the distance of the density pairs is calculated. We approximate that a density is located at the mean position of the atomic coordinates
    associated with each of the two basis functions which together form an electronic density.
    Then the difference of the two density locations is calculated and the Coulomb cut-off is used to calculate if a density combination is relevant.
    """
    
    if (verbosity==1): print('    |Relevant densities: '+str(relevant_densities_no_duplicates))
    
    relevance_d1d2=np.empty((num_threads_integrals,int(max_electron_integrals/num_threads_integrals),2),dtype='int32') 
    relevance_mask=np.full((1,1),False,dtype='bool')
    
    count=np.zeros(num_threads_integrals,dtype='int32')

    for t in prange(num_threads_integrals):
        for d1 in range(t,relevant_densities_no_duplicates,num_threads_integrals):
            i,j=ij_list_no_duplicates[d1,0],ij_list_no_duplicates[d1,1]
            for d2 in range(d1,relevant_densities_no_duplicates):
                k,l=ij_list_no_duplicates[d2,0],ij_list_no_duplicates[d2,1]

                relevance_1234_value_upper_bound=relevance_matrix[d1]*relevance_matrix[d2]
                if (relevance_1234_value_upper_bound<densities_threshold):
                    continue
                
                atom_1,atom_2,atom_3,atom_4=atom_of_basisfunction[i],atom_of_basisfunction[j],atom_of_basisfunction[k],atom_of_basisfunction[l]
                coordinates_a1,coordinates_a2,coordinates_a3,coordinates_a4=coordinates[atom_1],coordinates[atom_2],coordinates[atom_3],coordinates[atom_4]

                distance_12_34_x=coordinates_a1[0]+coordinates_a2[0]-coordinates_a3[0]-coordinates_a4[0]
                if (np.abs(distance_12_34_x)>coulomb_threshold_times_2): continue
                distance_12_34_y=coordinates_a1[1]+coordinates_a2[1]-coordinates_a3[1]-coordinates_a4[1]
                if (np.abs(distance_12_34_y)>coulomb_threshold_times_2): continue
                distance_12_34_z=coordinates_a1[2]+coordinates_a2[2]-coordinates_a3[2]-coordinates_a4[2]
                if (np.abs(distance_12_34_z)>coulomb_threshold_times_2): continue
                distance_12_34_x*=0.5
                distance_12_34_y*=0.5
                distance_12_34_z*=0.5      
                distance_12_34=np.sqrt(distance_12_34_x*distance_12_34_x+distance_12_34_y*distance_12_34_y+distance_12_34_z*distance_12_34_z)
                if (distance_12_34>coulomb_threshold):
                    continue
                elif (distance_12_34<coulomb_threshold_low):
                    relevance_12_34=1.0
                else:
                    fraction_12_34=1.0-(distance_12_34-coulomb_threshold_low)/coulomb_threshold_difference
                    fraction_square_12_34=fraction_12_34*fraction_12_34
                    relevance_12_34=-2.0*fraction_square_12_34*fraction_12_34+3.0*fraction_square_12_34

                relevance_1234_value=relevance_matrix[d1]*relevance_matrix[d2]/(distance_12_34+1.0)
                if (relevance_1234_value>densities_threshold_2):
                    relevance_1234=1.0
                elif (relevance_1234_value<densities_threshold):
                    continue
                else:
                    fraction_1234=(relevance_1234_value-densities_threshold)/densities_threshold_difference
                    fraction_square_1234=fraction_1234*fraction_1234
                    relevance_1234=-2.0*fraction_square_1234*fraction_1234+3.0*fraction_square_1234

                relevance_12_value=relevance_matrix[d1]
                if (relevance_12_value>density_threshold_2):
                    relevance_12=1.0
                else:
                    fraction_12=(relevance_12_value-density_threshold)/density_threshold_difference
                    fraction_square_12=fraction_12*fraction_12
                    relevance_12=-2.0*fraction_square_12*fraction_12+3.0*fraction_square_12

                relevance_34_value=relevance_matrix[d2]
                if (relevance_34_value>density_threshold_2):
                    relevance_34=1.0
                else:
                    fraction_34=(relevance_34_value-density_threshold)/density_threshold_difference
                    fraction_square_34=fraction_34*fraction_34
                    relevance_34=-2.0*fraction_square_34*fraction_34+3.0*fraction_square_34

                relevance_prefactor=relevance_12*relevance_34*relevance_12_34*relevance_1234

                if (relevance_prefactor>0):

                    relevance_d1d2[t,count[t],0],relevance_d1d2[t,count[t],1]=d1,d2
                    count[t]+=1
    
    relevance_d1d2_unfolded=np.empty((max_electron_integrals,2),dtype='int32')
    current_start,current_end=0,0
    for t in range(num_threads_integrals):
        current_end+=count[t]
        relevance_d1d2_unfolded[current_start:current_end]=relevance_d1d2[t,:count[t]] 
        current_start+=count[t]
    relevance_d1d2_unfolded=relevance_d1d2_unfolded[:np.sum(count)]
    
    if (verbosity==1): print('    |Relevant density combinations: '+str(np.sum(count)))
    
    return relevance_mask,relevance_d1d2_unfolded,np.sum(count)



@njit(parallel=True,fastmath=True)
def electron_arrays_calculation_loops(gaussian_functions_exponents_i_list,gaussian_functions_exponents_j_list,
                                      overlap_list,exp_sum_list,
                                      overlap_derivative_i_x_list,overlap_derivative_i_y_list,overlap_derivative_i_z_list,
                                      overlap_derivative_j_x_list,overlap_derivative_j_y_list,overlap_derivative_j_z_list,
                                      center_coords_list,relevance_mask,relevance_d1d2,num_relevant,
                                      ij_list_no_duplicates,gaussians_limits,atom_of_basisfunction,orbital_parts_index_list,coordinates,
                                      relevant_densities_no_duplicates,num_orbital_parts,num_basis_functions):
    """
    The main routine for electron repulsion integral (ERI) evaluation.
    """


    result=np.zeros((num_relevant),dtype=e_tensor_datatype)
    derivative=np.zeros((1,12),dtype=e_tensor_datatype) 

    
    for d1 in range(max_gaussian_functions_square):
        for d2 in range(max_gaussian_functions_square):
            
            matrix_cut_d1=gaussians_limits[d1]
            matrix_cut_d2=gaussians_limits[d2]
            overlap_list_d1,overlap_list_d2=overlap_list[d1,:matrix_cut_d1],overlap_list[d2,:matrix_cut_d2]
            exp_sum_list_d1,exp_sum_list_d2=exp_sum_list[d1,:matrix_cut_d1],exp_sum_list[d2,:matrix_cut_d2]
            center_coords_list_d1,center_coords_list_d2=center_coords_list[d1,:matrix_cut_d1],center_coords_list[d2,:matrix_cut_d2]
            

            for d1d2 in prange(num_relevant):
                i,j=relevance_d1d2[d1d2,0],relevance_d1d2[d1d2,1]
                if (i<matrix_cut_d1):
                    if(j<matrix_cut_d2):  
        
                        exp_sum=1.0/(exp_sum_list_d1[i]+exp_sum_list_d2[j])
                        
                        center_coords_d1,center_coords_d2=center_coords_list_d1[i],center_coords_list_d2[j]
                        coulomb_distance_x=center_coords_d1[0]-center_coords_d2[0]
                        coulomb_distance_y=center_coords_d1[1]-center_coords_d2[1]
                        coulomb_distance_z=center_coords_d1[2]-center_coords_d2[2]
                        coulomb_distance=(coulomb_distance_x*coulomb_distance_x+coulomb_distance_y*coulomb_distance_y+coulomb_distance_z*coulomb_distance_z)*exp_sum
                    
                        result[d1d2]+=np.sqrt(exp_sum)*overlap_list_d1[i]*overlap_list_d2[j]*erf_hyp1f1_with_arrays(coulomb_distance)
                        
    
    return result,derivative






@njit(fastmath=True,parallel=True)
def electron_integrals_with_arrays(result,derivative,relevance_d1d2,
                                   relevance_matrix,relevance_matrix_derivative,relevance_mask,num_relevant,
                                   ij_list_no_duplicates,gaussians_limits,atom_of_basisfunction,orbital_parts_index_list,coordinates,orbitals_center_coords,
                                   relevant_densities_no_duplicates,num_orbital_parts,num_basis_functions):
    """
    Screens electron repulsion intgrals (ERIs) for relevance based on a Coulomb cut-off and the product of the relevance values of their densities.
    """


    electron_tensor=np.zeros(num_relevant,dtype='float64') 
    electron_tensor_derivative=np.zeros((1,3),dtype='float64') 
    ijkl_list=np.zeros((num_relevant,4),dtype='int16') 


    for d1d2 in prange(num_relevant):
        d1,d2=relevance_d1d2[d1d2]
        i,j=ij_list_no_duplicates[d1,0],ij_list_no_duplicates[d1,1]
        k,l=ij_list_no_duplicates[d2,0],ij_list_no_duplicates[d2,1]
    
        
        relevance_1234_value_upper_bound=relevance_matrix[d1]*relevance_matrix[d2]

        if (relevance_1234_value_upper_bound<densities_threshold):
            continue
        
        atom_1,atom_2,atom_3,atom_4=atom_of_basisfunction[i],atom_of_basisfunction[j],atom_of_basisfunction[k],atom_of_basisfunction[l]
        coordinates_a1,coordinates_a2,coordinates_a3,coordinates_a4=coordinates[atom_1],coordinates[atom_2],coordinates[atom_3],coordinates[atom_4]

        distance_12_34_x=0.5*(coordinates_a1[0]+coordinates_a2[0]-coordinates_a3[0]-coordinates_a4[0])
        if (np.abs(distance_12_34_x)>coulomb_threshold): continue
        distance_12_34_y=0.5*(coordinates_a1[1]+coordinates_a2[1]-coordinates_a3[1]-coordinates_a4[1])
        if (np.abs(distance_12_34_y)>coulomb_threshold): continue
        distance_12_34_z=0.5*(coordinates_a1[2]+coordinates_a2[2]-coordinates_a3[2]-coordinates_a4[2])
        if (np.abs(distance_12_34_z)>coulomb_threshold): continue
        distance_12_34=np.sqrt(distance_12_34_x*distance_12_34_x+distance_12_34_y*distance_12_34_y+distance_12_34_z*distance_12_34_z)
        if (distance_12_34>coulomb_threshold):
            continue
        elif (distance_12_34<coulomb_threshold_low):
            relevance_12_34=1.0
        else:
            fraction_12_34=1.0-(distance_12_34-coulomb_threshold_low)/coulomb_threshold_difference
            fraction_square_12_34=fraction_12_34*fraction_12_34
            relevance_12_34=-2.0*fraction_square_12_34*fraction_12_34+3.0*fraction_square_12_34

        relevance_1234_value=relevance_matrix[d1]*relevance_matrix[d2]/(distance_12_34+1.0)
        if (relevance_1234_value>densities_threshold_2):
            relevance_1234=1.0
        elif (relevance_1234_value<densities_threshold):
            continue
        else:
            fraction_1234=(relevance_1234_value-densities_threshold)/densities_threshold_difference
            fraction_square_1234=fraction_1234*fraction_1234
            relevance_1234=-2.0*fraction_square_1234*fraction_1234+3.0*fraction_square_1234

        relevance_12_value=relevance_matrix[d1]
        if (relevance_12_value>density_threshold_2):
            relevance_12=1.0
        else:
            fraction_12=(relevance_12_value-density_threshold)/density_threshold_difference
            fraction_square_12=fraction_12*fraction_12
            relevance_12=-2.0*fraction_square_12*fraction_12+3.0*fraction_square_12

        relevance_34_value=relevance_matrix[d2]
        if (relevance_34_value>density_threshold_2):
            relevance_34=1.0
        else:
            fraction_34=(relevance_34_value-density_threshold)/density_threshold_difference
            fraction_square_34=fraction_34*fraction_34
            relevance_34=-2.0*fraction_square_34*fraction_34+3.0*fraction_square_34

        relevance_prefactor=relevance_12*relevance_34*relevance_12_34*relevance_1234

        v_ijkl=result[d1d2]
        
        v_ijkl=v_ijkl*relevance_prefactor

        i,j=ij_list_no_duplicates[d1,0],ij_list_no_duplicates[d1,1]
        k,l=ij_list_no_duplicates[d2,0],ij_list_no_duplicates[d2,1]

        electron_tensor[d1d2]=v_ijkl
        ijkl_list[d1d2,0],ijkl_list[d1d2,1],ijkl_list[d1d2,2],ijkl_list[d1d2,3]=i,j,k,l


    unique_integrals=int((num_basis_functions*(num_basis_functions+1.0)/2.0)*(num_basis_functions*(num_basis_functions+1.0)/2.0+1.0)/2.0)
    if (verbosity==1):
        print('    |Total integrals:         '+str(num_basis_functions**4))
        print('    |Unique integrals:        '+str(unique_integrals))
        print('    |With relevant densities: '+str(int((relevant_densities_no_duplicates+1)*relevant_densities_no_duplicates/2)))
        print('    |With relevant values:    '+str(num_relevant))

    return electron_tensor,electron_tensor_derivative,ijkl_list,num_relevant








"""
----------------------------------------------------------------
Functions of the scf-procedure (energy and density calculations)
----------------------------------------------------------------
"""



@njit(parallel=True,fastmath=True)
def calculate_G(P,V_ee,ijkl_list,num_basis_functions,relevant_V_ee_elements):
    """
    Calculates the two-center part of the Fock matrix.
    The naive implementation is shown below for a better understanding.
    
    for i in range(num_basis_functions):
        for j in range(num_basis_functions):
            for k in range(num_basis_functions):
                for l in range(num_basis_functions):
                    density=P[k,l]
                    J=V_ee[i,j,k,l]
                    K=V_ee[i,l,k,j]
                    G[i,j]+=density*(J-0.5*K)
    """

    num_parts=num_threads_G
    part_length=int(np.ceil(relevant_V_ee_elements/num_parts))
    G=np.zeros((num_parts,num_basis_functions,num_basis_functions),dtype=datatype)
    if (num_basis_functions==1): return np.sum(G,axis=0)
    
    for part in prange(num_parts):
        max_index=min((part+1)*part_length,relevant_V_ee_elements)
        ijkl_list_part=ijkl_list[part*part_length:max_index]
        V_ee_part=V_ee[part*part_length:max_index]
        for ee in range(max_index-part*part_length):
            ijkl_list_ee=ijkl_list_part[ee]
            i,j,k,l=ijkl_list_ee[0],ijkl_list_ee[1],ijkl_list_ee[2],ijkl_list_ee[3]
            V_ee_ee=V_ee_part[ee]
            
            P_ij_V_ee=P[i,j]*V_ee_ee
            P_kl_V_ee=P[k,l]*V_ee_ee

            if (k!=l):
                G[part,i,j]+=2.0*P_kl_V_ee
                G[part,i,k]-=0.5*P[l,j]*V_ee_ee
            else:
                G[part,i,j]+=P_kl_V_ee
            G[part,i,l]-=0.5*P[k,j]*V_ee_ee

            if (i!=j):
                if (k!=l):
                    G[part,j,i]+=2.0*P_kl_V_ee
                    G[part,j,k]-=0.5*P[l,i]*V_ee_ee
                else:
                    G[part,j,i]+=P_kl_V_ee
                G[part,j,l]-=0.5*P[k,i]*V_ee_ee
                        
            b=not(i==k and j==l)
            if (b):
                if (i!=j):
                    G[part,k,l]+=2.0*P_ij_V_ee
                    G[part,k,i]-=0.5*P[j,l]*V_ee_ee
                else:
                    G[part,k,l]+=P_ij_V_ee
                G[part,k,j]-=0.5*P[i,l]*V_ee_ee
                
            if (b and k!=l):
                if (i!=j):
                    G[part,l,k]+=2.0*P_ij_V_ee
                    G[part,l,i]-=0.5*P[j,k]*V_ee_ee
                else:
                    G[part,l,k]+=P_ij_V_ee
                G[part,l,j]-=0.5*P[i,k]*V_ee_ee
                
    G=np.sum(G,axis=0)
    return G




@njit(parallel=True,fastmath=True)
def calculate_P(eigenorbitals,occupied_orbitals,occupancies,radical,T_e,num_basis_functions):
    """
    Calculates the density matrix P from the eigenorbitals.
    """

    P=np.zeros((num_basis_functions,num_basis_functions),dtype=datatype)
    if (not radical):
        for i in prange(num_basis_functions):
            for j in prange(num_basis_functions):
                for o in prange(occupied_orbitals):
                    C=eigenorbitals[i,o]
                    C_dagger=eigenorbitals[j,o]
                    P[i,j]+=2*C*C_dagger 
    else:
        for i in prange(num_basis_functions):
            for j in prange(num_basis_functions):
                for o in prange(int(np.floor(occupied_orbitals))):
                    C=eigenorbitals[i,o]
                    C_dagger=eigenorbitals[j,o]
                    P[i,j]+=2*C*C_dagger 
                o=int(np.floor(occupied_orbitals))
                C=eigenorbitals[i,o]
                C_dagger=eigenorbitals[j,o]
                P[i,j]+=C*C_dagger
    return P









"""
-------------------------------------------
scf-function and Hartree-Fock main function
-------------------------------------------
"""


@njit
def sparse_to_dense(sparse_indices,sparse_values,dense_len):
    """
    Transforms a sparse matrix to dense matrix.
    """

    dense=np.zeros((dense_len,dense_len),dtype=datatype)
    sparse_len=len(sparse_values)
    for i in range(sparse_len):
        current_indices=sparse_indices[i]
        i1,i2=current_indices[0],current_indices[1]
        dense[i1,i2]=sparse_values[i]
        dense[i2,i1]=sparse_values[i]
    return dense



@njit
def matrix_new_indexing_order(sparse_indices,sparse_indices_new,sparse_values,dense_len):
    """
    Changes the indexing order of a matrix. This is used if matrices are transformed to the second densities-list.
    """

    dense=np.zeros((dense_len,dense_len),dtype=datatype)
    sparse_len=len(sparse_values)
    for i in range(sparse_len):
        current_indices=sparse_indices[i]
        i1,i2=current_indices[0],current_indices[1]
        dense[i1,i2]=sparse_values[i]
        dense[i2,i1]=sparse_values[i]
    sparse=np.zeros(sparse_len,dtype=datatype)
    for i in range(sparse_len):
        current_indices=sparse_indices_new[i]
        i1,i2=current_indices[0],current_indices[1]
        sparse[i]=dense[i1,i2]
    return sparse



def calculate_occupations(eigenenergies,num_basis_functions,num_electrons,radical,pseudo_finite_temp=0,relevant_orbitals=-1):
    """
    Calculations the electronic occupations of all orbitals.
    """

    occupations=np.zeros(num_basis_functions,dtype=datatype)

    if (pseudo_finite_temp==0):
        if (not radical):
            occupations[:int(num_electrons/2.0)]=2.0
        else:
            occupations[:int(np.floor(num_electrons/2.0))]=2.0
            occupations[int(np.floor(num_electrons/2.0))]=1.0
    
    else:
        if (not radical):
            homo_energy=eigenenergies[int(num_electrons/2.0)-1]
            lumo_energy=eigenenergies[int(num_electrons/2.0)]
            chemical_potential=(homo_energy+lumo_energy)/2.0
            lower_border=int(num_electrons/2.0)-relevant_orbitals
            upper_border=int(num_electrons/2.0)+relevant_orbitals
        else:
            chemical_potential=eigenenergies[int(np.floor(num_electrons/2.0))]
            lower_border=int(np.floor(num_electrons/2.0))-relevant_orbitals
            upper_border=int(np.floor(num_electrons/2.0))+relevant_orbitals+1

        if (relevant_orbitals==-1):
            occupations=2.0/(np.exp(np.minimum((eigenenergies-chemical_potential)/(k_b*pseudo_finite_temp+1.0e-100),100))+1.0)
        else: 
            if (not radical):
                occupations[:int(num_electrons/2.0)]=2.0
            else:
                occupations[:int(np.floor(num_electrons/2.0))]=2.0
                occupations[int(np.floor(num_electrons/2.0))]=1.0
            occupations[lower_border:upper_border]=2.0/(np.exp(np.minimum((eigenenergies[lower_border:upper_border]-chemical_potential)/(k_b*pseudo_finite_temp+1.0e-100),100))+1.0)
        occupations=occupations/np.sum(occupations)*num_electrons

    return occupations



def scf(S,T,V_en,V_ee,nuclei_matrix_hamiltonian_derivative,overlap_matrix_wavefunction_derivative,kinetic_matrix_wavefunction_derivative,nuclei_matrix_wavefunction_derivative,
        electron_matrix_wavefunction_derivative,atom_of_basisfunction,basis_functions_index_list,ijkl_list,coordinates,elements,occupied_orbitals,radical,
        num_atoms,num_basis_functions,relevant_V_ee_elements,linear_mixing=False):
    """
    Performs the self-consistent field iterations for the Hartree-Fock calculation. 
    Takes all inputs which were computed previously, i.e. overlap matrix, kinetic matrix, nuclei attraction matrix and electron repulsion tensor. 
    
    With linear mixing enables: identical to the other mode but uses linear mixing instead of DIIS.
    This function should normally used with linear_mixing=False since linear mixing is much slower than DIIS! However, DIIS is more susceptible to errors and instabilities.
    Therefore, linear_mixing=True can be used as a comparison if problems in the DIIS of scf() occur since linear mixing (with a sufficiently small mixing factor) is numerically very stable. 

    Info:
    Test:
       level-shift,    DIIS penalty, max DIIS equations: good convergence
       level-shift,    DIIS penalty, avg DIIS equations: no convergence
       level-shift, no DIIS penalty, max DIIS equations: medium convergence
       level-shift, no DIIS penalty, avg DIIS equations: no convergence
    no level-shift,    DIIS penalty, max DIIS equations: good convergence
    no level-shift,    DIIS penalty, avg DIIS equations: no convergence
    no level-shift, no DIIS penalty, max DIIS equations: no convergence
    no level-shift, no DIIS penalty, avg DIIS equations: no convergence
    Pulay mixing factor 0.5 was used

       level-shift,    DIIS penalty, max DIIS equations: good convergence (converged: 25)
    no level-shift,    DIIS penalty, max DIIS equations: good convergence (converged: 16)
    Pulay mixing factor 1.0 was used 

    recommended:
    Pulay mixing: enabled, factor 0.7
    DIIS penalty: enabled, weight 1.05
    level-shift: disabled, if enabled: recommended to set to 0.3 Hartree
    max DIIS equations: num_scf_steps, otherwise difficult convergence for large-scale systems
    num scf steps: ~10-100 to observe maximal convergence (depending on the system)
    """

    energy=0
    scf_tolerance=scf_tolerance_density

    H_core_time=0.0
    Inverse_time=0.0
    SAD_time=0.0
    G_time=0.0
    F_time=0.0
    SPF_time=0.0
    store_F_time=0.0
    error_matrix_time=0.0
    energy_time=0.0
    F_transform_time=0.0
    eigenvalue_time=0.0
    eigenorbitals_time=0.0
    P_time=0.0
    DIIS_coef_time=0.0
    DIIS_time=0.0
    new_F_time=0.0
    conv_crit_time=0.0
    
    if (not linear_mixing):
        S=torch.from_numpy(S)
        T=torch.from_numpy(T)
        V_en=torch.from_numpy(V_en)

        t1=time.time()
        H_core=torch.add(T,V_en)
        t2=time.time()
        if (display_runtimes): print('Caclculate H_core: ',t2-t1)
        H_core_time+=t2-t1
        
        commutator_matrices=torch.zeros((max_scf_steps,num_basis_functions,num_basis_functions),dtype=torch.float32) 
        stored_fock_matrices=torch.zeros((max_scf_steps,num_basis_functions,num_basis_functions),dtype=torch.float32) 
        error_matrix=np.zeros((max_scf_steps,max_scf_steps),dtype=datatype)

        saved_energies=np.zeros(max_scf_steps,dtype=datatype)
        min_j=0
        min_energy=1.0
        
        current_DIIS_linear_equations=max_DIIS_linear_equations

        num_electrons=np.sum(elements)+added_electrons
        electronic_occupations=np.zeros(num_basis_functions,dtype=datatype)
        count_electrons=0
        for i in range(num_basis_functions):
            if (count_electrons<num_electrons-1):
                count_electrons+=2
                electronic_occupations[i]=2
            elif (count_electrons==num_electrons-1):
                count_electrons+=1
                electronic_occupations[i]=1
                break
            else:
                break
        electronic_occupations=np.diag(electronic_occupations)
        
        t1=time.time()
        evals,evecs=torch.linalg.eigh(S)
        evpow=evals**(-1/2) 
        S_inverse_sqrt=torch.matmul(evecs,torch.matmul(torch.diag(evpow),torch.inverse(evecs)))
        t2=time.time()
        if (display_runtimes): print('Inverse square matrix: ',t2-t1)
        Inverse_time+=t2-t1

        t1=time.time()
        P=np.zeros((num_basis_functions,num_basis_functions),dtype=datatype)
        for atom in range(num_atoms):
            element=elements[atom]
            if (element<=2):
                P[basis_functions_index_list[atom]:basis_functions_index_list[atom+1],basis_functions_index_list[atom]:basis_functions_index_list[atom+1]]=single_atom_densities[element,0,0]
            elif (element>2 and element<=10):
                P[basis_functions_index_list[atom]:basis_functions_index_list[atom+1],basis_functions_index_list[atom]:basis_functions_index_list[atom+1]]=single_atom_densities[element,:5,:5]
            elif (element>10 and element<=18):
                P[basis_functions_index_list[atom]:basis_functions_index_list[atom+1],basis_functions_index_list[atom]:basis_functions_index_list[atom+1]]=single_atom_densities[element,:9,:9]
        P_0=np.copy(P)
        t2=time.time()
        if (display_runtimes): print('SAD guess: ',t2-t1)
        SAD_time+=t2-t1
        
        t1=time.time()
        G=calculate_G(P,V_ee,ijkl_list,num_basis_functions,relevant_V_ee_elements)
        G_0=np.copy(G)
        t2=time.time()
        if (display_runtimes): print('Caclculate G: ',t2-t1)
        G_time+=t2-t1
        t1=time.time()
        G=torch.from_numpy(G)
        F=torch.add(H_core,G)
        t2=time.time()
        if (display_runtimes): print('Caclculate F: ',t2-t1)
        F_time+=t2-t1

        t1=time.time()

        P=torch.from_numpy(P)
        SPF=torch.matmul(S.to(torch.float32),(torch.matmul(P.to(torch.float32),F.to(torch.float32))))
        commutator_matrices[0]=SPF-SPF.t()
        t2=time.time()
        if (display_runtimes): print('Caclculate SPF-FPS: ',t2-t1)
        SPF_time+=t2-t1
        t1=time.time()
        stored_fock_matrices[0]=F
        t2=time.time()
        if (display_runtimes): print('Store F: ',t2-t1)
        store_F_time+=t2-t1
        t1=time.time()
        error_matrix[0,0]=torch.sum(torch.mul(commutator_matrices[0],commutator_matrices[0]))
        t2=time.time()
        if (display_runtimes): print('Caclculate error matrix: ',t2-t1)
        error_matrix_time+=t2-t1

        t1=time.time()
        E_0=torch.add(H_core,0.5*G)
        saved_energies[0]=torch.sum(torch.mul(P,E_0)).numpy() 
        t2=time.time()
        if (display_runtimes): print('Calculate energy: ',t2-t1)
        energy_time+=t2-t1

        for i in range(1,max_scf_steps):
            old_P=P
            old_F=F

            t1=time.time()
            F_transformed=torch.matmul(S_inverse_sqrt,torch.matmul(F,S_inverse_sqrt))
            if (level_shift_enabled):
                F_transformed=F_transformed.numpy()
                for j in range(int(occupied_orbitals),num_basis_functions):
                    F_transformed[j,j]+=level_shift_value
                F_transformed=torch.from_numpy(F_transformed)
            t2=time.time()
            if (display_runtimes): print('Transform F: ',t2-t1)
            F_transform_time+=t2-t1
            t1=time.time()
            eigenenergies,eigenvectors=torch.linalg.eigh(F_transformed)
            t2=time.time()
            if (display_runtimes): print('Eigenvalue calculation: ',t2-t1)
            eigenvalue_time+=t2-t1
            t1=time.time()
            eigenorbitals=torch.matmul(S_inverse_sqrt,eigenvectors)
            t2=time.time()
            if (display_runtimes): print('Calculate eigenorbitals: ',t2-t1)
            eigenorbitals_time+=t2-t1

            occupancies=np.zeros(num_basis_functions,dtype=datatype)
            t1=time.time()
            if (display_runtimes): print('Eigenvalues around Fermi level')
            if (display_runtimes or display_eigenenergies): 
                print(np.round(np.reshape(eigenenergies[int(occupied_orbitals)-20:int(occupied_orbitals)+20].numpy(),(4,10))*27.2114079527,3))
                
            occupation_numbers=calculate_occupations(eigenenergies.numpy(),num_basis_functions,num_electrons,radical,pseudo_finite_temp=0,relevant_orbitals=-1)
            occupation_numbers=torch.from_numpy(occupation_numbers)
            P=torch.matmul(eigenorbitals[:,:int(np.ceil(occupied_orbitals))],(eigenorbitals[:,:int(np.ceil(occupied_orbitals))].T)*occupation_numbers[:int(np.ceil(occupied_orbitals)),None])
            t2=time.time()
            if (display_runtimes): print('Calculate P: ',t2-t1)
            P_time+=t2-t1
            t1=time.time()
            G=calculate_G(P.numpy(),V_ee,ijkl_list,num_basis_functions,relevant_V_ee_elements)
            t2=time.time()
            if (display_runtimes): print('Caclculate G: ',t2-t1)
            G_time+=t2-t1
            t1=time.time()
            G=torch.from_numpy(G)
            F=torch.add(H_core,G)
            t2=time.time()
            if (display_runtimes): print('Caclculate F: ',t2-t1)
            F_time+=t2-t1

            t1=time.time()
            SPF=torch.matmul(S,(torch.matmul(P,F)))
            commutator_matrices[i]=SPF-SPF.t()
            t2=time.time()
            if (display_runtimes): print('Caclculate SPF-FPS: ',t2-t1)
            SPF_time+=t2-t1
            t1=time.time()
            stored_fock_matrices[i]=F
            t2=time.time()
            if (display_runtimes): print('Store F: ',t2-t1)
            store_F_time+=t2-t1

            t1=time.time()
            for j in range(i+1):
                error_ij=torch.sum(torch.mul(commutator_matrices[i],commutator_matrices[j]))
                error_matrix[i,j]=error_ij
                error_matrix[j,i]=error_ij
            t2=time.time()
            if (display_runtimes): print('Calculate DIIS coeffs: ',t2-t1)
            DIIS_coef_time+=t2-t1
            
            t1=time.time()
            lhs=np.zeros((i+2,i+2),dtype=datatype)+1
            lhs[i+1,i+1]=0
            lhs[:i+1,:i+1]=error_matrix[:i+1,:i+1]
            min_energy=1.0
            for j in range(max(0,i+1-current_DIIS_linear_equations),i+1):
                if (saved_energies[j]<min_energy):
                    min_energy=saved_energies[j]
                    min_j=j
            for j in range(max(0,i+1-current_DIIS_linear_equations),i+1):
                if (j!=min_j):
                    lhs[j,j]*=DIIS_penalty
                    
            rhs=np.zeros(i+2,dtype=datatype)
            rhs[i+1]=1
            if (error_matrix[i,i]<1.0e-20):
                energy=torch.sum(torch.mul(P,torch.add(H_core,0.5*G))).numpy()
                saved_energies[i]=energy
                return energy,P.numpy(),P_0,G.numpy(),G_0,H_core.numpy(),F.numpy(),eigenorbitals.numpy(),eigenenergies.numpy(),occupancies
            coef_start=max(0,i+1-current_DIIS_linear_equations)
            DIIS_coeffs=np.linalg.solve(lhs[coef_start:,coef_start:],rhs[coef_start:])
            t2=time.time()
            if (display_runtimes): print('Calculate DIIS: ',t2-t1)
            DIIS_time+=t2-t1
            
            t1=time.time()
            DIIS_coeffs=torch.from_numpy(DIIS_coeffs)
            F_new=torch.sum(DIIS_coeffs[:i+1-coef_start].to(torch.float32)[:,None,None]*stored_fock_matrices[coef_start:i+1],0)
            F=pulay_mixing_rate*F_new+(1.0-pulay_mixing_rate)*old_F
            t2=time.time()
            if (display_runtimes): print('Construct new F: ',t2-t1)
            new_F_time+=t2-t1

            t1=time.time()
            energy=torch.sum(torch.mul(P,torch.add(H_core,0.5*G))).numpy()
            t2=time.time()
            if (display_runtimes): print('Calculate energy: ',t2-t1)
            energy_time+=t2-t1
            t1=time.time()
            delta_P=old_P-P
            scf_evaluation=(torch.sqrt(torch.mean(delta_P*delta_P))).numpy()             
            t2=time.time()
            if (display_runtimes): print('Calculate convergence crit: ',t2-t1)
            conv_crit_time+=t2-t1
            if (verbosity==1):
                if (i<10): print(' ',end='')
                scf_evaluation_log=int(np.floor(np.log10(scf_evaluation)))
                if (scf_evaluation_log<0):
                    if (scf_evaluation_log>=-9):
                        print('      '+str(i)+' | '+str('{0:.5f}'.format(scf_evaluation/(10**scf_evaluation_log)))+'e'+str(scf_evaluation_log)+'  | '+str(energy))
                    else: 
                        print('      '+str(i)+' | '+str('{0:.5f}'.format(scf_evaluation/(10**scf_evaluation_log)))+'e'+str(scf_evaluation_log)+' | '+str(energy))
                else:
                    print('      '+str(i)+' | '+str('{0:.5f}'.format(scf_evaluation))+' | '+str(energy))
            if (scf_evaluation<scf_tolerance):
                if (verbosity==1): 
                    print('SCF times:')
                    print('    |Core Hamiltonian: '+str(np.round(H_core_time,4))+' s')
                    print('    |Square root of inverse: '+str(np.round(Inverse_time,4))+' s')
                    print('    |SAD guess: '+str(np.round(SAD_time,4))+' s')
                    print('    |G tensor: '+str(np.round(G_time,4))+' s')
                    print('    |Fock matrix construction: '+str(np.round(F_time,4))+' s')
                    print('    |Commutator SPF-FPS: '+str(np.round(SPF_time,4))+' s')
                    print('    |Save Fock matrix: '+str(np.round(store_F_time,4))+' s')
                    print('    |Error matrix calculation: '+str(np.round(error_matrix_time,4))+' s')
                    print('    |Energy calculation: '+str(np.round(energy_time,4))+' s')
                    print('    |Transform Fock matrix: '+str(np.round(F_transform_time,4))+' s')
                    print('    |Eigenvalue calculation: '+str(np.round(eigenvalue_time,4))+' s')
                    print('    |Transform eigenorbitals: '+str(np.round(eigenorbitals_time,4))+' s')
                    print('    |Density matrix: '+str(np.round(P_time,4))+' s')
                    print('    |DIIS coefficients: '+str(np.round(DIIS_coef_time,4))+' s')
                    print('    |DIIS equations: '+str(np.round(DIIS_time,4))+' s')
                    print('    |Mix new Fock matrix: '+str(np.round(new_F_time,4))+' s')
                    print('    |Convergence criterium: '+str(np.round(conv_crit_time,4))+' s')
                return energy,P.numpy(),P_0,G.numpy(),G_0,H_core.numpy(),F.numpy(),eigenorbitals.numpy(),eigenenergies.numpy(),occupancies
        
        if (verbosity==1): 
            print('SCF cycle did not meet specified tolerance.')
            if (verbosity==1): 
                print('SCF times:')
                print('    |Core Hamiltonian: '+str(np.round(H_core_time,4))+' s')
                print('    |Square root of inverse: '+str(np.round(Inverse_time,4))+' s')
                print('    |SAD guess: '+str(np.round(SAD_time,4))+' s')
                print('    |G tensor: '+str(np.round(G_time,4))+' s')
                print('    |Fock matrix construction: '+str(np.round(F_time,4))+' s')
                print('    |Commutator SPF-FPS: '+str(np.round(SPF_time,4))+' s')
                print('    |Save Fock matrix: '+str(np.round(store_F_time,4))+' s')
                print('    |Error matrix calculation: '+str(np.round(error_matrix_time,4))+' s')
                print('    |Energy calculation: '+str(np.round(energy_time,4))+' s')
                print('    |Transform Fock matrix: '+str(np.round(F_transform_time,4))+' s')
                print('    |Eigenvalue calculation: '+str(np.round(eigenvalue_time,4))+' s')
                print('    |Transform eigenorbitals: '+str(np.round(eigenorbitals_time,4))+' s')
                print('    |Density matrix: '+str(np.round(P_time,4))+' s')
                print('    |DIIS coefficients: '+str(np.round(DIIS_coef_time,4))+' s')
                print('    |DIIS equations: '+str(np.round(DIIS_time,4))+' s')
                print('    |Mix new Fock matrix: '+str(np.round(new_F_time,4))+' s')
                print('    |Convergence criterium: '+str(np.round(conv_crit_time,4))+' s')
        
        return energy,P.numpy(),P_0,G.numpy(),G_0,H_core.numpy(),F.numpy(),eigenorbitals.numpy(),eigenenergies.numpy(),occupancies







def run_HF(coordinates,elements,enable_plotting=False,rthf=False,partitioning=False,early_stopping=False):
    """
    Main routine to run a Hartree-Fock calculation.
    Inputs: Coordinates and periodic numbers of an atomic configuration. 
            coordinates: Array of coordinates (num_atoms x 3), 
            elements: Array of the element of each atom (integer) 
            enable_plotting: returns additional parts of the HF calculation to enable plotting electronic quantities like the density or molecular orbitals
    Returns: energy of the given configuration
    """
    alpha_fold=False


    start_preparations=time.time()

    if (rthf):
        center_of_mass=calculate_center_of_mass(coordinates,elements,len(elements))

    num_atoms=len(coordinates)
    num_basis_functions=calculate_num_basis_functions(elements,num_atoms)

    radical=False
    if ((np.sum(elements)+added_electrons)%2==0):
        occupied_orbitals=int(np.floor(0.5*(np.sum(elements)+added_electrons)+0.1))
    else:
        occupied_orbitals=0.5*(np.sum(elements)+added_electrons)
        radical=True
    
    num_gaussian_functions,basis_functions_index_list,gaussian_functions_index_list,atom_of_basisfunction,type_of_basis_function\
                    =calculate_num_gaussian_functions(elements,num_atoms,num_basis_functions)
    gaussian_functions_coordinates,gaussian_functions_coefficients,gaussian_functions_exponents\
                    =calculate_gaussian_function_inputs(elements,coordinates,num_atoms,num_gaussian_functions)

    
    num_orbital_parts,orbital_parts_index_list=calculate_num_orbital_parts(elements,num_atoms,num_basis_functions) 
    num_parts_gaussian_functions,orbital_parts_gaussian_index_list\
                    =calculate_gaussians_for_orbital_parts(elements,num_atoms,num_orbital_parts)
    orbital_parts_coordinates,orbital_parts_coefficients,orbital_parts_exponents=calculate_orbital_parts_preprocessing(elements,coordinates,num_parts_gaussian_functions,num_atoms)
    
    ij_list_no_duplicates,gaussians_for_densities,gaussians_for_densities_index_list,num_gaussians_for_densities,relevant_densities_no_duplicates,relevance_matrix,relevance_matrix_derivative\
                    =calculate_relevant_densities(orbital_parts_coefficients,orbital_parts_exponents,orbital_parts_coordinates,
                                                  orbital_parts_index_list,orbital_parts_gaussian_index_list,atom_of_basisfunction,gaussian_functions_index_list,
                                                  coordinates,num_gaussian_functions,num_basis_functions)
    
    if (early_stopping):
        return gaussian_functions_coefficients,gaussian_functions_exponents,gaussian_functions_coordinates,\
                        ij_list_no_duplicates,atom_of_basisfunction,gaussian_functions_index_list,type_of_basis_function,num_basis_functions

    S_terms,S_terms_derivatives,exp_sums,center_coords\
                    =overlap_contributions(gaussian_functions_coefficients,gaussian_functions_exponents,gaussian_functions_coordinates,
                                           gaussians_for_densities,gaussians_for_densities_index_list,num_gaussians_for_densities,relevant_densities_no_duplicates,num_gaussian_functions)    
    

    del relevance_matrix_derivative,S_terms_derivatives
    relevance_matrix_derivative=np.zeros((1,3),dtype=datatype)
    S_terms_derivatives=np.zeros((1,3),dtype=datatype)

    stop_preparations=time.time()
    if (verbosity==1):
        print('Preparations:           '+str(np.round(stop_preparations-start_preparations,4))+' s')
    


    start_overlap_kinetic=time.time()
    S,overlap_matrix_wavefunction_derivative,T,kinetic_matrix_wavefunction_derivative,\
                nuclei_prefactor,weighted_coords,orbitals_center_coords=calculate_overlap_and_kinetic_matrix(gaussian_functions_coefficients,gaussian_functions_exponents,gaussian_functions_coordinates,
                                                                                      gaussian_functions_index_list,gaussians_for_densities,gaussians_for_densities_index_list,
                                                                                      ij_list_no_duplicates,num_gaussians_for_densities,relevant_densities_no_duplicates,num_basis_functions,num_gaussian_functions)

    del overlap_matrix_wavefunction_derivative,kinetic_matrix_wavefunction_derivative
    overlap_matrix_wavefunction_derivative=np.zeros((1,3),dtype=datatype)
    kinetic_matrix_wavefunction_derivative=np.zeros((1,3),dtype=datatype)

    stop_overlap_kinetic=time.time()
    if (verbosity==1):
        print('Overlap/Kinetic matrix: '+str(np.round(stop_overlap_kinetic-start_overlap_kinetic,4))+' s')

    start_nuclei=time.time()
    V_en,nuclei_matrix_hamiltonian_derivative,nuclei_matrix_wavefunction_derivative\
                    =calculate_nuclei_matrix_and_derivatives(gaussian_functions_exponents,gaussian_functions_coordinates,
                                                             ij_list_no_duplicates,gaussians_for_densities,gaussians_for_densities_index_list,num_gaussians_for_densities,relevant_densities_no_duplicates,
                                                             gaussian_functions_index_list,atom_of_basisfunction,coordinates,elements,
                                                             relevance_matrix,relevance_matrix_derivative,
                                                             nuclei_prefactor,weighted_coords,orbitals_center_coords,num_atoms,num_basis_functions)


    stop_nuclei=time.time()
    if (verbosity==1):
        print('Nuclei matrix:          '+str(np.round(stop_nuclei-start_nuclei,4))+' s') 
        print('Electron-electron integrals:')
    start_electrons=time.time()

    gaussian_functions_exponents_i_list,gaussian_functions_exponents_j_list,overlap_list,\
                    overlap_derivative_i_x_list,overlap_derivative_i_y_list,overlap_derivative_i_z_list,overlap_derivative_j_x_list,overlap_derivative_j_y_list,overlap_derivative_j_z_list,\
                    exp_sum_list,center_coords_list,ij_list_no_duplicates_new,gaussians_limits=\
                    electron_integrals_list_generation(gaussian_functions_exponents,S_terms,S_terms_derivatives,exp_sums,center_coords,gaussians_for_densities,gaussians_for_densities_index_list,
                                                       ij_list_no_duplicates,gaussian_functions_index_list,type_of_basis_function,relevant_densities_no_duplicates)
    

    relevance_matrix=matrix_new_indexing_order(ij_list_no_duplicates,ij_list_no_duplicates_new,relevance_matrix,num_basis_functions)

    t_relevance_start=time.time()
    relevance_mask,relevance_d1d2,num_relevant=electron_integrals_distance_relevance(relevance_matrix,ij_list_no_duplicates_new,atom_of_basisfunction,coordinates,
                                                                                     orbitals_center_coords,relevant_densities_no_duplicates)
    t_relevance_stop=time.time()
    if (verbosity==1): print('  >Relevance computations:        '+str(np.round(t_relevance_stop-t_relevance_start,4))+' s')
    

    t_eri_start=time.time()
    result,derivative=electron_arrays_calculation_loops(gaussian_functions_exponents_i_list,gaussian_functions_exponents_j_list,
                                                        overlap_list,exp_sum_list,
                                                        overlap_derivative_i_x_list,overlap_derivative_i_y_list,overlap_derivative_i_z_list,
                                                        overlap_derivative_j_x_list,overlap_derivative_j_y_list,overlap_derivative_j_z_list,
                                                        center_coords_list,relevance_mask,relevance_d1d2,num_relevant,
                                                        ij_list_no_duplicates,gaussians_limits,atom_of_basisfunction,orbital_parts_index_list,coordinates,
                                                        relevant_densities_no_duplicates,num_orbital_parts,num_basis_functions)

    if (print_ERI_relevance):
        result_abs=np.abs(result)
        print('Total values: '+str((result_abs>-0.1).sum()))
        print('Nonzero values: '+str((result_abs>0.0).sum()))
        print('Values > 1.0e-10: '+str((result_abs>1.0e-10).sum()))
        print('Values > 1.0e-9: '+str((result_abs>1.0e-9).sum()))
        print('Values > 1.0e-8: '+str((result_abs>1.0e-8).sum()))
        print('Values > 1.0e-7: '+str((result_abs>1.0e-7).sum()))
        print('Values > 1.0e-6: '+str((result_abs>1.0e-6).sum()))
        print('Values > 1.0e-5: '+str((result_abs>1.0e-5).sum()))
        print('Values > 1.0e-4: '+str((result_abs>1.0e-4).sum()))
        print('Values > 1.0e-3: '+str((result_abs>1.0e-3).sum()))
        print('Values > 1.0e-2: '+str((result_abs>1.0e-2).sum()))
        print('Values > 1.0e-1: '+str((result_abs>1.0e-1).sum()))
        print('Values > 1.0e0 : '+str((result_abs>1.0e0 ).sum()))

    t_eri_stop=time.time()
    if (verbosity==1): print('  >ERI computations:              '+str(np.round(t_eri_stop-t_eri_start,4))+' s')

    t_mask_start=time.time()
    result=torch.from_numpy(result)
    relevance_d1d2=torch.from_numpy(relevance_d1d2)
    mask_V_ee=torch.where(torch.abs(result)>1.0e-5,1.0,0.0)
    result=result*mask_V_ee
    nonzeros=result.nonzero().reshape(-1)
    result=(result[nonzeros]).numpy()
    relevance_d1d2=(relevance_d1d2[nonzeros]).numpy()
    num_relevant=len(result)
    t_mask_stop=time.time()

    if (verbosity==1): print('  >Second relevance computations: '+str(np.round(t_mask_stop-t_mask_start,4))+' s')


    t_loop_start=time.time()
    V_ee,electron_matrix_wavefunction_derivative,ijkl_list,relevant_V_ee_elements\
                    =electron_integrals_with_arrays(result,derivative,relevance_d1d2,
                                                    relevance_matrix,relevance_matrix_derivative,relevance_mask,num_relevant,
                                                    ij_list_no_duplicates_new,gaussians_limits,atom_of_basisfunction,orbital_parts_index_list,coordinates,orbitals_center_coords,
                                                    relevant_densities_no_duplicates,num_orbital_parts,num_basis_functions)
    t_loop_stop=time.time()
    if (verbosity==1): print('  >Process ERIs:                  '+str(np.round(t_loop_stop-t_loop_start,4))+' s')

    del relevance_d1d2
    relevance_d1d2=np.zeros((1,3),dtype=datatype)
    del relevance_d1d2

    del result,S_terms,S_terms_derivatives,exp_sums,center_coords
    
    stop_electrons=time.time()
    if (verbosity==1):
        print('Electron tensor:        '+str(np.round(stop_electrons-start_electrons,4))+' s')

    start_ions=time.time()
    E_nn=calculate_ionic_energy(coordinates,elements,num_atoms)
    stop_ions=time.time()
    if (verbosity==1):
        print('Ionic energy:           '+str(np.round(stop_ions-start_ions,4))+' s')
        print('Starting SCF cycle: ')
        print('SCF step | convergence measure:')
    
    
    start_scf=time.time()

    S=sparse_to_dense(ij_list_no_duplicates,S,num_basis_functions)
    T=sparse_to_dense(ij_list_no_duplicates,T,num_basis_functions)

    V_en=sparse_to_dense(ij_list_no_duplicates,V_en,num_basis_functions)

    electronic_energy,P,P_0,G,G_0,H_core,F,eigenorbitals,eigenenergies,occupancies=scf(S,T,V_en,V_ee,nuclei_matrix_hamiltonian_derivative,overlap_matrix_wavefunction_derivative,kinetic_matrix_wavefunction_derivative,
                                                        nuclei_matrix_wavefunction_derivative,electron_matrix_wavefunction_derivative,atom_of_basisfunction,basis_functions_index_list,ijkl_list,
                                                        coordinates,elements,occupied_orbitals,radical,num_atoms,num_basis_functions,relevant_V_ee_elements)
 
    stop_scf=time.time()
    if (verbosity==1):
        print('SCF cycle:              '+str(np.round(stop_scf-start_scf,4))+' s')
    
    energy=electronic_energy+E_nn
    if (verbosity==1):
        print('_______________________________________')
        print('Total time:             '+str(np.round(stop_scf-start_preparations,4))+' s')
        print('Total energy: '+str(energy)+' Ha')
        print()
        print()


    if (alpha_fold):
        return energy,P,P_0,G,G_0,H_core,eigenorbitals,gaussian_functions_coefficients,gaussian_functions_exponents,gaussian_functions_coordinates,\
               ij_list_no_duplicates,atom_of_basisfunction,gaussian_functions_index_list,type_of_basis_function,num_basis_functions

    if (rthf):
        return gaussian_functions_coefficients,gaussian_functions_exponents,gaussian_functions_coordinates,gaussians_for_densities,gaussians_for_densities_index_list,\
               F,S,P,eigenenergies,eigenorbitals,occupancies,H_core,ij_list_no_duplicates,relevant_densities_no_duplicates,V_ee,ijkl_list,relevant_V_ee_elements,num_basis_functions,center_of_mass,\
               gaussian_functions_index_list,atom_of_basisfunction,type_of_basis_function
    if (partitioning):
            return energy,P,F,eigenorbitals,eigenenergies,gaussian_functions_coefficients,gaussian_functions_exponents,gaussian_functions_coordinates,\
                   ij_list_no_duplicates,atom_of_basisfunction,gaussian_functions_index_list,type_of_basis_function,num_basis_functions
    if (not enable_plotting):
        return energy
    else:
        return energy,E_nn,P,F,eigenorbitals,eigenenergies,gaussian_functions_coefficients,gaussian_functions_exponents,gaussian_functions_coordinates,\
               ij_list_no_duplicates,atom_of_basisfunction,gaussian_functions_index_list,type_of_basis_function,num_basis_functions











"""
--------------------------------
Functions for input file loading
--------------------------------
"""




def load_coordinates(coordinate_file_path):
    """
    Loads in coordinates, elements and connections which are stored in a .json file.
    Input is the file path of a json file (.json) which gets loaded and coordinates, elements and connections are returned as numpy arrays.
    """

    structure_elements=[]
    structure_connections=[]
    structure_coordinates=[]
    with open(coordinate_file_path+'.json') as f:
        d=json.load(f)
    structure_elements=np.array(d['PC_Compounds'][0]['atoms']['element'],dtype='float32').astype('int32')
    structure_connections=np.stack([np.array(d['PC_Compounds'][0]['bonds']['aid1'],dtype='float32'),
                                    np.array(d['PC_Compounds'][0]['bonds']['aid2'],dtype='float32')]).T
    structure_connections=structure_connections.astype('int')
    structure_coordinates=np.stack([np.array(d['PC_Compounds'][0]['coords'][0]['conformers'][0]['x'],dtype='float32'),
                                    np.array(d['PC_Compounds'][0]['coords'][0]['conformers'][0]['y'],dtype='float32'),
                                    np.array(d['PC_Compounds'][0]['coords'][0]['conformers'][0]['z'],dtype='float32')]).T*angstrom_to_bohr
    
    return structure_coordinates,structure_elements,structure_connections


def load_coordinates_pdb(file_path,discard_hetatoms=False,file_type=2):
    """
    Loads in coordinates and elements which are stored in the .pdb file format.
    The file path of a text file (.txt) which gets loaded is the input and the coordinates, elements and connections are plotted.
    For older PDB formats file_type=1 might be used.
    Several edge cases are included to ensure correct outputs but due to irregularities in PDB files, especially for very large systems, errors can occur in this function.
    If input coordinates seem off, it is advised to check this function.
    The same holds if a Hartree-Fock run terminates due to singularities (often encountered in the form of invalid inputs for a logarithm). Then the error can be identical
    coordinates for two atoms. This can also be the case in PDB entries were there exist two different models for one or more amino acids.
    """

    structure_elements=[]
    structure_coordinates=[]
    element_strings=['H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar']

    with open(file_path+'.txt','r') as file:
        reading_coords=False
        stop_reading=False

        count=0
        for line in file:
            count+=1
            words=line.split()

            if (words[0]=='ATOM' or words[0]=='HETATM'):
                reading_coords=True
            if (reading_coords and words[0]=='#'):
                break
            
            if (reading_coords):
                if (words[0]=='TER' or words[0]=='END' or words[0]=='IGN' or words[0]=='CONECT' or words[0]=='ANISOU'):
                    continue
                if ((words[0]=='HETATM' and discard_hetatoms)
                    or (words[0]=='ENDMDL')
                    or (words[0]=='MODEL' and words[1]=='2')):
                    stop_reading=True
                    break

                if (file_type==1):
                    structure_coordinates.append([words[10],words[11],words[12]])
                    for i in range(len(element_strings)):
                        if (words[2]==element_strings[i]):
                            structure_elements.append(i+1)
                            break
                elif (file_type==2):
                    if (words[3]=='WAT' or words[2]=='WAT'):
                        if (words[0]=='HETATM'):
                            structure_coordinates.append([words[5],words[6],words[7]])
                        else:
                            structure_coordinates.append([words[4],words[5],words[6]])
                    elif ((words[2]=='H1' or words[2]=='H2' or words[2]=='OH2') and count>10000):
                        if (len(words[3])>5):
                            structure_coordinates.append([words[4],words[5],words[6]])
                        else:
                            structure_coordinates.append([words[5],words[6],words[7]])
                        if (words[2]=='OH2'):
                            structure_elements.append(8)
                        else:
                            structure_elements.append(1)
                        continue
                    else:
                        if (len(words[2])<5):
                            structure_coordinates.append([words[6],words[7],words[8]])
                        else:
                            structure_coordinates.append([words[5],words[6],words[7]])
                    if (len(words[-1])>2):
                        structure_elements.append(1)
                    else:
                        for i in range(len(element_strings)):
                            if (words[-1]==element_strings[i]):
                                structure_elements.append(i+1)
                                break
            
            if (stop_reading): break

    structure_coordinates=np.array(structure_coordinates,dtype=datatype)*angstrom_to_bohr
    structure_elements=np.array(structure_elements,dtype='int32')

    return structure_coordinates,structure_elements









"""
--------
Plotting
--------
"""



@njit
def calculate_connections(coordinates,elements,cut=4.0,cut_H=2.6,cut_H_H=0.0):
    """
    Calculates atomic bonds for a given set of coordinates and elements. 
    This is used for plotting atomic bonds in the functions plot_structure() and single_plot().
    """

    num_atoms=len(elements)
    connections=np.zeros((int(num_atoms*(num_atoms+1)/2.0),2),dtype='int32')
    connection_count=0
    for i in range(num_atoms):
        for j in range(i,num_atoms):
            if (i!=j):
                coordinate_distance_x=coordinates[i,0]-coordinates[j,0]
                coordinate_distance_y=coordinates[i,1]-coordinates[j,1]
                coordinate_distance_z=coordinates[i,2]-coordinates[j,2]
                coordinate_distance=np.sqrt(coordinate_distance_x*coordinate_distance_x+coordinate_distance_y*coordinate_distance_y+coordinate_distance_z*coordinate_distance_z)
                if (elements[i]>1 and elements[j]>1):
                    if (coordinate_distance<cut):
                        connections[connection_count,0],connections[connection_count,1]=i,j
                        connection_count+=1
                elif (elements[i]==1 and elements[j]==1):
                    if (coordinate_distance<cut_H_H):
                        connections[connection_count,0],connections[connection_count,1]=i,j
                        connection_count+=1
                else:
                    if (coordinate_distance<cut_H):
                        connections[connection_count,0],connections[connection_count,1]=i,j
                        connection_count+=1
    connections=connections[:connection_count]
    return connections



def plot_structure(coordinates,elements,structure):
    """
    Plots the electronic structure of a system. The electronic structure is hereby given as as real-space grid in three dimensions.
    The coordinates and elements of the atoms of the system are also given and are plotted similar to the function single_plot() below.
    The parametrization of the scatter plot - especially the point size - might need to be changed depending on the size of the system that is plotted.
    """

    dir_1 = 0 
    dir_2 = 1 
    dir_3 = 2 

    density_mean_value=0.3
    density_variation=0.15

    edge_cut=3.0
    edge_cut_pixels=int(edge_cut/pixel_size)
    structure=structure[edge_cut_pixels:-edge_cut_pixels,edge_cut_pixels:-edge_cut_pixels,edge_cut_pixels:-edge_cut_pixels]
    
    x_min=np.min(coordinates[:,dir_1])-additional_space+edge_cut
    y_min=np.min(coordinates[:,dir_2])-additional_space+edge_cut
    z_min=np.min(coordinates[:,dir_3])-additional_space+edge_cut
    points_x=structure.shape[dir_1]
    points_y=structure.shape[dir_2]
    points_z=structure.shape[dir_3]
    pixel_length=pixel_size
    interpolation_num=1
    offset_pixels=0

    str_xyz = ['x [$a_0$]','y [$a_0$]','z [$a_0$]']
    coord_str = [str_xyz[dir_1],str_xyz[dir_2],str_xyz[dir_3]]

    x = np.indices(structure.shape)[dir_1]
    y = np.indices(structure.shape)[dir_2]
    z = np.indices(structure.shape)[dir_3]

    fig = plt.figure(figsize=(20, 20))
    ax3D = fig.add_subplot(projection='3d',computed_zorder=False)
    points_size = 0.1*50000.0*pixel_size*pixel_size/(points_x*points_y*points_z)**(2.0/3.0)
    ax3D.scatter(x,y,z,s=points_size,cmap='hot_r',c=np.where(np.abs(np.abs(structure)-density_mean_value)<density_variation,structure,None))
    
    atom_scaling=0.015
    for atom in range(len(elements)):
        ax = ((coordinates[atom,dir_1]-x_min)/pixel_length-offset_pixels)*interpolation_num
        ay = ((coordinates[atom,dir_2]-y_min)/pixel_length-offset_pixels)*interpolation_num
        az = ((coordinates[atom,dir_3]-z_min)/pixel_length-offset_pixels)*interpolation_num
        if (elements[atom]==1):
            ax3D.scatter(ax,ay,az,s=200*atom_scaling,color='black',zorder=10) 
            ax3D.scatter(ax,ay,az,s=150*atom_scaling,color='white',zorder=10)    
        if (elements[atom]==6):
            ax3D.scatter(ax,ay,az,s=350*atom_scaling,color='black',zorder=10) 
            ax3D.scatter(ax,ay,az,s=270*atom_scaling,color='grey',zorder=10)   
        if (elements[atom]==7):
            ax3D.scatter(ax,ay,az,s=350*atom_scaling,color='black',zorder=10) 
            ax3D.scatter(ax,ay,az,s=270*atom_scaling,color='blue',zorder=10)      
        if (elements[atom]==8):
            ax3D.scatter(ax,ay,az,s=350*atom_scaling,color='black',zorder=10) 
            ax3D.scatter(ax,ay,az,s=270*atom_scaling,color='red',zorder=10)     
        if (elements[atom]==16):
            ax3D.scatter(ax,ay,az,s=600*atom_scaling,color='black',zorder=10) 
            ax3D.scatter(ax,ay,az,s=500*atom_scaling,color='yellow',zorder=10)    

    connections_plot=calculate_connections(coordinates,elements)
    
    for line in range(len(connections_plot)):
        plt.plot([((coordinates[connections_plot[line][0]][dir_1]-x_min)/pixel_length-offset_pixels)*interpolation_num,
                  ((coordinates[connections_plot[line][1]][dir_1]-x_min)/pixel_length-offset_pixels)*interpolation_num],
                 [((coordinates[connections_plot[line][0]][dir_2]-y_min)/pixel_length-offset_pixels)*interpolation_num,
                  ((coordinates[connections_plot[line][1]][dir_2]-y_min)/pixel_length-offset_pixels)*interpolation_num],
              zs=[((coordinates[connections_plot[line][0]][dir_3]-z_min)/pixel_length-offset_pixels)*interpolation_num,
                  ((coordinates[connections_plot[line][1]][dir_3]-z_min)/pixel_length-offset_pixels)*interpolation_num],
              color='black',linewidth=1.0) 
        plt.plot([((coordinates[connections_plot[line][0]][dir_1]-x_min)/pixel_length-offset_pixels)*interpolation_num,
                  ((coordinates[connections_plot[line][1]][dir_1]-x_min)/pixel_length-offset_pixels)*interpolation_num],
                 [((coordinates[connections_plot[line][0]][dir_2]-y_min)/pixel_length-offset_pixels)*interpolation_num,
                  ((coordinates[connections_plot[line][1]][dir_2]-y_min)/pixel_length-offset_pixels)*interpolation_num],
              zs=[((coordinates[connections_plot[line][0]][dir_3]-z_min)/pixel_length-offset_pixels)*interpolation_num,
                  ((coordinates[connections_plot[line][1]][dir_3]-z_min)/pixel_length-offset_pixels)*interpolation_num],
              color='grey',linewidth=0.5) 

    tick_spacing=10
    x_ticks=[]
    x_ticks_pos=[]
    for xt in range(int(np.floor(np.min(coordinates[:,dir_1]))),int(np.ceil(np.max(coordinates[:,dir_1]))),tick_spacing):
        x_ticks.append(xt)
        x_ticks_pos.append(((additional_space-edge_cut)/pixel_length+(xt-int(np.floor(np.min(coordinates[:,dir_1]))))/pixel_length)*interpolation_num)
    y_ticks=[]
    y_ticks_pos=[]
    for yt in range(int(np.floor(np.min(coordinates[:,dir_2]))),int(np.ceil(np.max(coordinates[:,dir_2]))),tick_spacing):
        y_ticks.append(yt)
        y_ticks_pos.append(((additional_space-edge_cut)/pixel_length+(yt-int(np.floor(np.min(coordinates[:,dir_2]))))/pixel_length)*interpolation_num)
    z_ticks=[]
    z_ticks_pos=[]
    for zt in range(int(np.floor(np.min(coordinates[:,dir_3]))),int(np.ceil(np.max(coordinates[:,dir_3]))),tick_spacing):
        z_ticks.append(zt)
        z_ticks_pos.append(((additional_space-edge_cut)/pixel_length+(zt-int(np.floor(np.min(coordinates[:,dir_3]))))/pixel_length)*interpolation_num)

    ax3D.set_aspect('equal')
    fig.subplots_adjust(top=1.1)
    ax3D.set_xlabel(coord_str[0],fontsize=16)
    ax3D.set_ylabel(coord_str[1],fontsize=16)
    ax3D.set_zlabel(coord_str[2],fontsize=16)
    ax3D.set_xticks(x_ticks_pos,x_ticks,fontsize=10)
    ax3D.set_yticks(y_ticks_pos,y_ticks,fontsize=10)
    ax3D.set_zticks(z_ticks_pos,z_ticks,fontsize=10)
    ax3D.view_init(0,0)
    plt.show()
    plt.close()




def single_plot(coordinates,elements):
    """
    Plots a structure of atoms - the coordinates and elements are given.
    Bonds are calculated and displayed as well as the atoms which are coloured with respect to their species.
    """

    coordinates_step=coordinates

    dir_1 = 0
    dir_2 = 1
    dir_3 = 2

    edge_cut=0.0
    
    x_min=0
    y_min=0
    z_min=0
    pixel_length=1
    interpolation_num=1
    offset_pixels=0

    str_xyz = ['x [$a_0$]','y [$a_0$]','z [$a_0$]']
    coord_str = [str_xyz[dir_1],str_xyz[dir_2],str_xyz[dir_3]]

    fig = plt.figure(figsize=(15, 15))
    ax3D = fig.add_subplot(projection='3d',computed_zorder=False) 

    atom_scaling=0.03
    for atom in range(len(elements)):
        ax = ((coordinates_step[atom,dir_1]-x_min)/pixel_length-offset_pixels)*interpolation_num
        ay = ((coordinates_step[atom,dir_2]-y_min)/pixel_length-offset_pixels)*interpolation_num
        az = ((coordinates_step[atom,dir_3]-z_min)/pixel_length-offset_pixels)*interpolation_num
        if (elements[atom]==1):
            p3d = ax3D.scatter(ax,ay,az,s=200*atom_scaling,color='black',zorder=10) 
            p3d = ax3D.scatter(ax,ay,az,s=150*atom_scaling,color='white',zorder=10)    
        if (elements[atom]==6):
            p3d = ax3D.scatter(ax,ay,az,s=350*atom_scaling,color='black',zorder=10) 
            p3d = ax3D.scatter(ax,ay,az,s=270*atom_scaling,color='green',zorder=10)   
        if (elements[atom]==7):
            p3d = ax3D.scatter(ax,ay,az,s=350*atom_scaling,color='black',zorder=10) 
            p3d = ax3D.scatter(ax,ay,az,s=270*atom_scaling,color='blue',zorder=10)      
        if (elements[atom]==8):
            p3d = ax3D.scatter(ax,ay,az,s=350*atom_scaling,color='black',zorder=10) 
            p3d = ax3D.scatter(ax,ay,az,s=270*atom_scaling,color='red',zorder=10)     
        if (elements[atom]==16):
            p3d = ax3D.scatter(ax,ay,az,s=600*atom_scaling,color='black',zorder=10) 
            p3d = ax3D.scatter(ax,ay,az,s=500*atom_scaling,color='yellow',zorder=10)    

    connections_plot=calculate_connections(coordinates_step,elements)
    
    for line in range(len(connections_plot)):
        plt.plot([((coordinates_step[connections_plot[line][0]][dir_1]-x_min)/pixel_length-offset_pixels)*interpolation_num,
                  ((coordinates_step[connections_plot[line][1]][dir_1]-x_min)/pixel_length-offset_pixels)*interpolation_num],
                 [((coordinates_step[connections_plot[line][0]][dir_2]-y_min)/pixel_length-offset_pixels)*interpolation_num,
                  ((coordinates_step[connections_plot[line][1]][dir_2]-y_min)/pixel_length-offset_pixels)*interpolation_num],
              zs=[((coordinates_step[connections_plot[line][0]][dir_3]-z_min)/pixel_length-offset_pixels)*interpolation_num,
                  ((coordinates_step[connections_plot[line][1]][dir_3]-z_min)/pixel_length-offset_pixels)*interpolation_num],
              color='black',linewidth=1.0) 
        plt.plot([((coordinates_step[connections_plot[line][0]][dir_1]-x_min)/pixel_length-offset_pixels)*interpolation_num,
                  ((coordinates_step[connections_plot[line][1]][dir_1]-x_min)/pixel_length-offset_pixels)*interpolation_num],
                 [((coordinates_step[connections_plot[line][0]][dir_2]-y_min)/pixel_length-offset_pixels)*interpolation_num,
                  ((coordinates_step[connections_plot[line][1]][dir_2]-y_min)/pixel_length-offset_pixels)*interpolation_num],
              zs=[((coordinates_step[connections_plot[line][0]][dir_3]-z_min)/pixel_length-offset_pixels)*interpolation_num,
                  ((coordinates_step[connections_plot[line][1]][dir_3]-z_min)/pixel_length-offset_pixels)*interpolation_num],
              color='grey',linewidth=0.5) 

    tick_spacing=2
    x_ticks=[]
    x_ticks_pos=[]
    for xt in range(int(np.floor(np.min(coordinates_step[:,dir_1]))),int(np.ceil(np.max(coordinates_step[:,dir_1]))),tick_spacing):
        x_ticks.append(xt)
        x_ticks_pos.append(((additional_space-edge_cut)/pixel_length+(xt-int(np.floor(np.min(coordinates_step[:,dir_1]))))/pixel_length)*interpolation_num)
    y_ticks=[]
    y_ticks_pos=[]
    for yt in range(int(np.floor(np.min(coordinates_step[:,dir_2]))),int(np.ceil(np.max(coordinates_step[:,dir_2]))),tick_spacing):
        y_ticks.append(yt)
        y_ticks_pos.append(((additional_space-edge_cut)/pixel_length+(yt-int(np.floor(np.min(coordinates_step[:,dir_2]))))/pixel_length)*interpolation_num)
    z_ticks=[]
    z_ticks_pos=[]
    for zt in range(int(np.floor(np.min(coordinates_step[:,dir_3]))),int(np.ceil(np.max(coordinates_step[:,dir_3]))),tick_spacing):
        z_ticks.append(zt)
        z_ticks_pos.append(((additional_space-edge_cut)/pixel_length+(zt-int(np.floor(np.min(coordinates_step[:,dir_3]))))/pixel_length)*interpolation_num)

    ax3D.set_aspect('equal')
    fig.subplots_adjust(top=1.1)
    ax3D.set_xlabel(coord_str[0],fontsize=16)
    ax3D.set_ylabel(coord_str[1],fontsize=16)
    ax3D.set_zlabel(coord_str[2],fontsize=16)
    ax3D.set_xticks(x_ticks_pos,x_ticks,fontsize=10)
    ax3D.set_yticks(y_ticks_pos,y_ticks,fontsize=10)
    ax3D.set_zticks(z_ticks_pos,z_ticks,fontsize=10)
    ax3D.set_xlim(np.min(coordinates[:,0])-4, np.max(coordinates[:,0])+4)
    ax3D.set_ylim(np.min(coordinates[:,1])-4, np.max(coordinates[:,1])+4)
    ax3D.set_zlim(np.min(coordinates[:,2])-4, np.max(coordinates[:,2])+4)
    ax3D.view_init(0,0) 

    plt.show()
    plt.close()















"""
===============================
===============================
DIVIDE-AND-CONQUER HARTREE-FOCK
===============================
===============================
"""



"""
-----------------------------------------------------
Functions for k-means divide-and-conquer Hartree-Fock
-----------------------------------------------------
"""


@njit
def naive_neighbor_list(coordinates,cut_off,max_neighbors):
    """
    A naive implementation of a neighbourhood algorithm.
    """
    num_atoms=len(coordinates)
    n_list=np.zeros((num_atoms,max_neighbors),dtype=datatype)
    n_list_lengths=np.zeros(num_atoms,dtype='int32')
    for i in range(num_atoms):
        for j in range(num_atoms):
            dist_x=coordinates[i,0]-coordinates[j,0]
            if (dist_x>cut_off): continue
            dist_y=coordinates[i,1]-coordinates[j,1]
            if (dist_y>cut_off): continue
            dist_z=coordinates[i,2]-coordinates[j,2]
            if (dist_z>cut_off): continue
            dist=np.sqrt(dist_x*dist_x+dist_y*dist_y+dist_z*dist_z)
            if (dist>cut_off): continue
            n_list[i,n_list_lengths[i]]=j
            n_list_lengths[i]+=1
    if (verbosity==1):
        print('Mean neigbors: ',np.mean(n_list_lengths))
        print('Maximum neigbors: ',np.max(n_list_lengths))
    n_list=n_list[:,:np.max(n_list_lengths)]
    return n_list,n_list_lengths


@njit
def k_means_clustering(coordinates,n_list,n_list_lengths,num_clusters,max_optimization_steps=100):
    """
    Calculates clusters for a divide-and-conquer Hartree-Fock calculation based on the k-means algorithm.
    """

    if (len(coordinates)<num_clusters):
        print('Error: More clusters than points.')
        return None
    
    num_points=len(coordinates)
    means_origins=np.zeros((num_clusters,3),dtype=datatype)
    means_origins_new=np.zeros((num_clusters,3),dtype=datatype)
    index_list=np.zeros(num_clusters,dtype='int32')-1
    assignment_list=np.zeros(num_points,dtype='int32')-1
    assignment_list_old=np.zeros(num_points,dtype='int32')-2

    for i in range(num_clusters):
        valid_index=False
        while (not valid_index):
            index=np.random.randint(num_points)
            if (index not in index_list):
                valid_index=True
                index_list[i]=index
                means_origins[i]=coordinates[index]
    means_origins=coordinates[::int(len(coordinates)/num_clusters)]
    
    for i in range(max_optimization_steps):
        cluster_counts=np.zeros(num_clusters,dtype='int32')

        for p in range(num_points):
            min_distance=1.0e100
            current_cluster=-1
            for c in range(num_clusters):
                distance_x=coordinates[p,0]-means_origins[c,0]
                distance_y=coordinates[p,1]-means_origins[c,1]
                distance_z=coordinates[p,2]-means_origins[c,2]
                distance=np.sqrt(distance_x*distance_x+distance_y*distance_y+distance_z*distance_z)
                if (distance<min_distance):
                    current_cluster=c
                    min_distance=distance
            assignment_list[p]=current_cluster
            cluster_counts[current_cluster]+=1
        
        for p in range(num_points):
            current_cluster=assignment_list[p]
            current_coordinates=coordinates[p]
            means_origins_new[current_cluster,0]+=current_coordinates[0]
            means_origins_new[current_cluster,1]+=current_coordinates[1]
            means_origins_new[current_cluster,2]+=current_coordinates[2]
        for c in range(num_clusters):
            means_origins_new[c]/=cluster_counts[c]

        means_origins=means_origins_new
        if (np.array_equal(assignment_list_old,assignment_list)):
            break
        assignment_list_old=np.copy(assignment_list)

    indices_for_clusters=np.zeros((num_clusters,np.max(cluster_counts)),dtype='int32')
    indices_for_overlapping_clusters=np.zeros((num_clusters,10*np.max(cluster_counts)),dtype='int32')-1
    temp_cluster_index_list=np.zeros(num_clusters,dtype='int32')
    for i in range(num_points):
        current_cluster=assignment_list[i]
        indices_for_clusters[current_cluster,temp_cluster_index_list[current_cluster]]=i
        indices_for_overlapping_clusters[current_cluster,temp_cluster_index_list[current_cluster]]=i
        temp_cluster_index_list[current_cluster]+=1
    
    
    for i in range(num_points):
        current_cluster=assignment_list[i]
        for j in range(n_list_lengths[i]):
            current_n_atom=n_list[i,j]
            if (current_n_atom not in indices_for_overlapping_clusters[current_cluster]):
                indices_for_overlapping_clusters[current_cluster,temp_cluster_index_list[current_cluster]]=current_n_atom
                temp_cluster_index_list[current_cluster]+=1

    if (verbosity==1):
        print('Cluster sizes')
        print(np.sort(temp_cluster_index_list))   
        print('Mean cluster size: ',np.mean(temp_cluster_index_list))         

    return means_origins,assignment_list,indices_for_overlapping_clusters,indices_for_clusters






"""
--------------------------------------------------
Functions for grid divide-and-conquer Hartree-Fock
--------------------------------------------------
"""


def calculate_parts_center_coordinates(coordinates,partition_length,partition_cut_off):
    """
    Calculates the central coordinates of the subsystems of a divide-and-conquer Hartree-Fock calculation.
    """

    account_for_surface=0.0
    x_min,x_max=np.min(coordinates[:,0])+partition_cut_off*account_for_surface,np.max(coordinates[:,0])-partition_cut_off*account_for_surface
    y_min,y_max=np.min(coordinates[:,1])+partition_cut_off*account_for_surface,np.max(coordinates[:,1])-partition_cut_off*account_for_surface
    z_min,z_max=np.min(coordinates[:,2])+partition_cut_off*account_for_surface,np.max(coordinates[:,2])-partition_cut_off*account_for_surface
    x_length,y_length,z_length=x_max-x_min,y_max-y_min,z_max-z_min
    x_boxes,y_boxes,z_boxes=int(np.ceil(x_length/partition_length)),int(np.ceil(y_length/partition_length)),int(np.ceil(z_length/partition_length))
    num_boxes=x_boxes*y_boxes*z_boxes
    print('Partitioning dimensions (x/y/z/total):',x_boxes,y_boxes,z_boxes,num_boxes)
    x_space=0.5*(np.linspace(x_min,x_min+(x_boxes-1)*partition_length,x_boxes)+np.linspace(x_max-(x_boxes-1)*partition_length,x_max,x_boxes))
    y_space=0.5*(np.linspace(y_min,y_min+(y_boxes-1)*partition_length,y_boxes)+np.linspace(y_max-(y_boxes-1)*partition_length,y_max,y_boxes))
    z_space=0.5*(np.linspace(z_min,z_min+(z_boxes-1)*partition_length,z_boxes)+np.linspace(z_max-(z_boxes-1)*partition_length,z_max,z_boxes))
    xyz=np.meshgrid(x_space,y_space,z_space,indexing='ij')
    xyz=np.reshape(xyz,(3,num_boxes)).T

    return xyz



@njit
def select_relevant_atoms(coordinates,elements,center_coordinate,cut_off):
    """
    Selects atoms which are within a cubical (!) cut-off cut_off of a central coordinate center_coordinate.
    """

    num_atoms_total=len(coordinates)
    relevant_atoms=np.zeros(20000,dtype='int32')
    relevant_atom_count=0
    center_coordinate_x,center_coordinate_y,center_coordinate_z=center_coordinate[0],center_coordinate[1],center_coordinate[2]

    for i in range(num_atoms_total):
        current_coordinates=coordinates[i]
        dist_x=current_coordinates[0]-center_coordinate_x
        if (np.abs(dist_x)>cut_off): continue
        dist_y=current_coordinates[1]-center_coordinate_y
        if (np.abs(dist_y)>cut_off): continue
        dist_z=current_coordinates[2]-center_coordinate_z
        if (np.abs(dist_z)>cut_off): continue
        relevant_atoms[relevant_atom_count]=i
        relevant_atom_count+=1
    
    relevant_atoms=relevant_atoms[:relevant_atom_count]
    relevant_coordinates=coordinates[relevant_atoms]
    relevant_elements=elements[relevant_atoms]

    return relevant_atoms,relevant_coordinates,relevant_elements



@njit
def partition_naive_neighbor_list(partition_atoms,partition_coordinates,padded_partition_coordinates,padded_partition_elements,cut_off,
                                  parts_center_coordinates,partition_length,partition_num,max_neighbors=10000):
    """
    Calculates the neighbouring atoms of a given selection of atoms. The neighbouring atoms are taken from another selection of atoms which
    contains more atoms than the first selection of atoms.
    """

    num_atoms_partition=len(partition_coordinates)
    num_atoms_section=len(padded_partition_coordinates)

    n_list=np.zeros((num_atoms_partition*max_neighbors),dtype='int32')
    n_list_length=0
    for i in range(num_atoms_partition):
        for j in range(num_atoms_section):
            coordinates_i=partition_coordinates[i]
            coordinates_j=padded_partition_coordinates[j]
            dist_x=coordinates_i[0]-coordinates_j[0]
            if (np.abs(dist_x)>cut_off): continue
            dist_y=coordinates_i[1]-coordinates_j[1]
            if (np.abs(dist_y)>cut_off): continue
            dist_z=coordinates_i[2]-coordinates_j[2]
            if (np.abs(dist_z)>cut_off): continue
            dist=np.sqrt(dist_x*dist_x+dist_y*dist_y+dist_z*dist_z)
            if (dist>cut_off): continue
            n_list[n_list_length]=j
            n_list_length+=1
    
    partition_center_coordinates=np.copy(parts_center_coordinates[partition_num])
    parts_center_coordinates[partition_num]=np.array([1.0e10,1.0e10,1.0e10])
    mask=np.where(np.sqrt((parts_center_coordinates[:,0]-partition_center_coordinates[0])**2
                         +(parts_center_coordinates[:,1]-partition_center_coordinates[1])**2
                         +(parts_center_coordinates[:,2]-partition_center_coordinates[2])**2)<2*partition_length)[0]
    relevant_center_coordinates=parts_center_coordinates[mask]
    num_relevant_center_coordinates=len(relevant_center_coordinates)
    add_to_unique=np.zeros(num_atoms_section,dtype='int32')
    added_atoms=0
    for i in range(num_atoms_section):
        coordinates_i=padded_partition_coordinates[i]
        current_partition_center_difference=np.sqrt((coordinates_i[0]-partition_center_coordinates[0])**2
                                                   +(coordinates_i[1]-partition_center_coordinates[1])**2
                                                   +(coordinates_i[2]-partition_center_coordinates[2])**2)
        
        add_section_atom=True
        for j in range(num_relevant_center_coordinates):
            coordinates_j=relevant_center_coordinates[j]
            dist_x=coordinates_i[0]-coordinates_j[0]
            dist_y=coordinates_i[1]-coordinates_j[1]
            dist_z=coordinates_i[2]-coordinates_j[2]
            other_partition_center_difference=np.sqrt(dist_x*dist_x+dist_y*dist_y+dist_z*dist_z)
            if (other_partition_center_difference<current_partition_center_difference):
                add_section_atom=False

        if (add_section_atom):
            n_list[n_list_length]=i
            n_list_length+=1
            add_to_unique[added_atoms]=i
            added_atoms+=1
    parts_center_coordinates[partition_num]=partition_center_coordinates
    add_to_unique=add_to_unique[:added_atoms]
    len_partition_atoms=len(partition_atoms)
    partition_unique=np.zeros(added_atoms+len_partition_atoms,dtype=datatype)
    partition_unique[:len_partition_atoms]=partition_atoms
    partition_unique[len_partition_atoms:]=add_to_unique
    partition_unique=np.unique(partition_unique)
    
    n_list=n_list[:n_list_length]
    padded_partition_atoms=np.unique(n_list)
    padded_partition_coordinates=padded_partition_coordinates[padded_partition_atoms]
    padded_partition_elements=padded_partition_elements[padded_partition_atoms]
    return padded_partition_atoms,padded_partition_coordinates,padded_partition_elements,partition_unique



@njit
def calculate_bonds(coordinates,elements,cut=4.0,cut_H=2.6):
    """
    Calculates the bonds of an atomic structure.
    """

    num_atoms=len(coordinates)
    max_bonds=12
    bonds=np.zeros((num_atoms,max_bonds),dtype='int32')-1
    bond_types=np.zeros((num_atoms,max_bonds),dtype='int32')
    bond_distances=np.zeros((num_atoms,max_bonds),dtype=datatype)
    element_distances=np.zeros((num_atoms,max_bonds,19,19),dtype=datatype)
    bond_nums=np.zeros(num_atoms,dtype='int32')
    for i in range(num_atoms):
        for j in range(i,num_atoms):
            if (i!=j):
                coordinate_distance_x=coordinates[i,0]-coordinates[j,0]
                if (np.abs(coordinate_distance_x)>cut): continue
                coordinate_distance_y=coordinates[i,1]-coordinates[j,1]
                if (np.abs(coordinate_distance_y)>cut): continue
                coordinate_distance_z=coordinates[i,2]-coordinates[j,2]
                if (np.abs(coordinate_distance_z)>cut): continue
                coordinate_distance=np.sqrt(coordinate_distance_x*coordinate_distance_x+coordinate_distance_y*coordinate_distance_y+coordinate_distance_z*coordinate_distance_z)
                if (coordinate_distance>cut): continue
                element_i,element_j=elements[i],elements[j]
                if (element_i>1 and element_j>1): 
                    bonds[i,bond_nums[i]]=j
                    bond_types[i,bond_nums[i]]=1
                    bond_distances[i,bond_nums[i]]=coordinate_distance
                    element_distances[i,bond_nums[i],element_i,element_j]=coordinate_distance
                    bond_nums[i]+=1
                    bonds[j,bond_nums[j]]=i
                    bond_types[j,bond_nums[j]]=1
                    bond_distances[j,bond_nums[j]]=coordinate_distance
                    element_distances[j,bond_nums[j],element_j,element_i]=coordinate_distance
                    bond_nums[j]+=1
                elif ((element_i==1 and element_j>1) or (element_i>1 and element_j==1)):
                    if (coordinate_distance<cut_H):
                        bonds[i,bond_nums[i]]=j
                        bond_types[i,bond_nums[i]]=2
                        bond_distances[i,bond_nums[i]]=coordinate_distance
                        element_distances[i,bond_nums[i],element_i,element_j]=coordinate_distance
                        bond_nums[i]+=1
                        bonds[j,bond_nums[j]]=i
                        bond_types[j,bond_nums[j]]=2
                        bond_distances[j,bond_nums[j]]=coordinate_distance
                        element_distances[j,bond_nums[j],element_j,element_i]=coordinate_distance
                        bond_nums[j]+=1

    return bonds,bond_types,bond_distances,bond_nums,element_distances



@njit
def avoid_bond_cutting(selection,total_coordinates,total_elements,bonds,bond_nums):
    """
    Function that avoids the cutting of atomic bonds during the selection of subsystems for a large-scale divide-and-conquer Hartree-Fock calculation.
    This is done by adding atoms to the system to avoid cutting double bonds and terminating the cutting of singly bonds by adding Hydrogen atoms instead 
    which are placed at a distance corresponding to the usual bond length of the atomic species to hydrogen.
    Bonds with hydrogen atoms are never cut.
    The algorithm iterates over the subsystem multiple times and adds the necessary atoms in each iteration. The process is stopped if no new atoms got added.
    """

    max_iterations=10
    num_atoms_selection=len(selection)
    current_atoms=num_atoms_selection
    new_length=max(2*num_atoms_selection,num_atoms_selection+200)
    coordinates_new=np.zeros((new_length,3),dtype=datatype)
    coordinates_new[:num_atoms_selection]=total_coordinates[selection]
    elements_new=np.zeros(new_length,dtype='int32')
    elements_new[:num_atoms_selection]=total_elements[selection]
    selection_new=np.zeros(new_length,dtype='int32')
    selection_new[:num_atoms_selection]=selection
    h_replacements=np.zeros(new_length,dtype='int32')-1

    no_bonds_cut=False

    start=0
    for iteration in range(max_iterations):
        last_iteration=False
        if (iteration==max_iterations-1):
            last_iteration=True
        if (no_bonds_cut): 
            break

        no_new_bonds=True
        start_new=current_atoms
        end=current_atoms
        for i in range(start,end):
            atom_i=selection_new[i]
            if (atom_i==-1): 
                continue
            element_i=total_elements[atom_i]
            coordinates_i=total_coordinates[atom_i]

            for j in range(bond_nums[atom_i]):
                atom_j=bonds[atom_i,j]
                if (atom_j not in selection_new):
                    if (atom_j in h_replacements):
                        change_h_modelling=True
                    else: change_h_modelling=False

                    keep_bond=True
                    element_j=total_elements[atom_j]
                    if (element_i==6 and (element_j==6 or element_j==7 or element_j==8)): 
                        coordinates_j=total_coordinates[atom_j]
                        dist_x=coordinates_i[0]-coordinates_j[0]
                        dist_y=coordinates_i[1]-coordinates_j[1]
                        dist_z=coordinates_i[2]-coordinates_j[2]
                        dist=np.sqrt(dist_x*dist_x+dist_y*dist_y+dist_z*dist_z)
                        if (dist>element_cuts[element_i,element_j]):
                            keep_bond=False
                    
                    if (last_iteration and not (element_i==1 or element_j==1)):
                        keep_bond=False

                    if (not change_h_modelling):
                        if (keep_bond):
                            selection_new[current_atoms]=atom_j
                            coordinates_new[current_atoms]=total_coordinates[atom_j]
                            elements_new[current_atoms]=total_elements[atom_j]
                            current_atoms+=1
                            no_new_bonds=False
                        else:
                            coordinates_j=total_coordinates[atom_j]
                            dist_x=coordinates_i[0]-coordinates_j[0]
                            dist_y=coordinates_i[1]-coordinates_j[1]
                            dist_z=coordinates_i[2]-coordinates_j[2]
                            dist=np.sqrt(dist_x*dist_x+dist_y*dist_y+dist_z*dist_z)
                            new_dist=element_h_bond_distances[element_i]/dist
                            dist_x*=new_dist
                            dist_y*=new_dist
                            dist_z*=new_dist

                            h_replacements[current_atoms]=atom_j
                            selection_new[current_atoms]=-1
                            coordinates_new[current_atoms,0]=coordinates_i[0]-dist_x
                            coordinates_new[current_atoms,1]=coordinates_i[1]-dist_y
                            coordinates_new[current_atoms,2]=coordinates_i[2]-dist_z
                            elements_new[current_atoms]=1
                            current_atoms+=1
                    else:
                        replace_h=np.where(h_replacements==atom_j)[0][0]
                        selection_new[replace_h]=-2
                        h_replacements[replace_h]=-1
                        selection_new[current_atoms]=atom_j
                        coordinates_new[current_atoms]=total_coordinates[atom_j]
                        elements_new[current_atoms]=total_elements[atom_j]
                        current_atoms+=1
                        no_new_bonds=False

        if (no_new_bonds): 
            break
        start=start_new
    
    selection_new=selection_new[:current_atoms]
    coordinates_new=coordinates_new[:current_atoms]
    elements_new=elements_new[:current_atoms]
    mask=np.where(selection_new>=-1)[0]
    selection_new=selection_new[mask]
    coordinates_new=coordinates_new[mask]
    elements_new=elements_new[mask]

    return selection_new,coordinates_new,elements_new



def initialize_divide_conquer_HF(total_coordinates,total_elements,partition_num):
    """
    Initializes a divide-and-conquer Hartree-Fock run. This is done by calling all of the relevant preprocessing functions (see the functions above this function).
    This serves the purpose of computing the atoms which are included in the subsystem Hartree-Fock run.
    """
    
    parts_center_coordinates=calculate_parts_center_coordinates(total_coordinates,partition_length,partition_cut_off)
    
    center_coordinate=parts_center_coordinates[partition_num]
    
    _,section_coordinates,section_elements=select_relevant_atoms(total_coordinates,total_elements,center_coordinate,0.5*partition_length+partition_cut_off+section_cut_off)
    
    partition_atoms,partition_coordinates,_=select_relevant_atoms(section_coordinates,section_elements,center_coordinate,0.5*partition_length)
    
    padded_partition_atoms,_,_,partition_unique\
        =partition_naive_neighbor_list(partition_atoms,partition_coordinates,section_coordinates,section_elements,partition_cut_off,parts_center_coordinates,partition_length,partition_num)
    
    bonds,_,_,bond_nums,_=calculate_bonds(section_coordinates,section_elements,cut=4.0,cut_H=2.6)
    atoms_final,coordinates_final,elements_final=avoid_bond_cutting(padded_partition_atoms,section_coordinates,section_elements,bonds,bond_nums)
    partition_atoms_unique=partition_unique
    print('Number of atoms in this subsystem:',len(atoms_final))
    
    print('Unique atoms in this subsystem:',len(partition_atoms_unique))
    
    return coordinates_final,elements_final,atoms_final,partition_atoms_unique,center_coordinate



@njit
def calculate_intersection(box_center,point_inside,point_outside,box_length=partition_length):
    """
    Calculate the intersection point of the line connecting two points with the surface of a cubical box.
    """

    length_one_half=0.5*box_length
    direction=point_outside-point_inside
    direction=direction/np.linalg.norm(direction)

    min_bounds=box_center-length_one_half
    max_bounds=box_center+length_one_half

    for i in range(3):  
        border_array=np.array([min_bounds[i],max_bounds[i]])
        for j in range(2):
            current_border=border_array[j]
            if (direction[i]!=0):  
                t=(current_border-point_inside[i])/direction[i]
                if (t>0):  
                    possible_intersection=point_inside+t*direction
                    correct_intersection=True
                    for j in range(3):
                        if (j!=i):
                            if (not (min_bounds[j]<=possible_intersection[j]<=max_bounds[j])):
                                correct_intersection=False
                    if (correct_intersection):
                        return possible_intersection

    return None  



def run_HF_for_partition(coordinates,elements,partition_indices,partition_unique_indices,partition_num,center_coordinate,saving_path='SavedPartitioningResults'):
    """
    The main function for a single Hartree-Fock run in a divide-and-conquer Hartree-Fock calculation.
    """

    print('----------------')
    print(' SUBSYSTEM '+str(partition_num))
    print('----------------')

    print(len(np.where(elements==1)[0]),'H')
    print(len(np.where(elements==6)[0]),'C')
    print(len(np.where(elements==7)[0]),'N')
    print(len(np.where(elements==8)[0]),'O')
    print(len(np.where(elements==16)[0]),'S')
    print()

    box_center=center_coordinate
    
    partition_coordinates=coordinates
    partition_elements=elements
    
    pulay_mixing_rate=0.7  

    if (len(np.where(elements==1)[0])+len(np.where(elements==8)[0])>=0.9*len(elements)):
        pulay_mixing_rate=0.8
    
    if (len(np.where(elements==1)[0])+len(np.where(elements==8)[0])==len(elements)):
        pulay_mixing_rate=1.0

    _,P,_,_,eigenenergies,_,_,_,ij_list_no_duplicates,atom_of_basisfunction,_,_,_=\
                    run_HF(partition_coordinates,partition_elements,partitioning=True,pulay_mixing_rate=pulay_mixing_rate)
    
    relevant_densities=len(ij_list_no_duplicates)
    relevant_densities_no_overlap=np.zeros((relevant_densities,2),dtype='int32')
    relevant_densities_no_overlap_values=np.zeros(relevant_densities,dtype=datatype)
    no_overlap_count=0
    for d in range(relevant_densities):
        i,j=ij_list_no_duplicates[d]
        atom_i,atom_j=atom_of_basisfunction[i],atom_of_basisfunction[j]
        system_atom_i,system_atom_j=partition_indices[atom_i],partition_indices[atom_j]
        i_included,j_included=False,False
        if (system_atom_i in partition_unique_indices): i_included=True
        if (system_atom_j in partition_unique_indices): j_included=True
        
        if (i_included and j_included):
            relevant_densities_no_overlap[no_overlap_count,0],relevant_densities_no_overlap[no_overlap_count,1]=i,j
            relevant_densities_no_overlap_values[no_overlap_count]=P[i,j]
            no_overlap_count+=1
        elif ((i_included and not j_included) or (not i_included and j_included)):
            relevant_densities_no_overlap[no_overlap_count,0],relevant_densities_no_overlap[no_overlap_count,1]=i,j
            if (i_included):
                point_inside=partition_coordinates[atom_i]
                point_outside=partition_coordinates[atom_j]
            else:
                point_inside=partition_coordinates[atom_j]
                point_outside=partition_coordinates[atom_i]
            intersection_point=calculate_intersection(box_center,point_inside,point_outside)
            if (intersection_point is not None):
                total_distance=np.linalg.norm(point_outside-point_inside)
                distance_in_partition=np.linalg.norm(intersection_point-point_inside)
                distance_fraction=distance_in_partition/total_distance
                relevance_fraction=-2*distance_fraction**3+3*distance_fraction**2
            else:
                relevance_fraction=0.0
            
            relevant_densities_no_overlap_values[no_overlap_count]=relevance_fraction*P[i,j]
            no_overlap_count+=1
        
    relevant_densities_no_overlap=relevant_densities_no_overlap[:no_overlap_count]
    relevant_densities_no_overlap_values=relevant_densities_no_overlap_values[:no_overlap_count]
    
    np.save(saving_path+'/Energies/'+str(partition_num)+'_eigenenergies.npy',eigenenergies.astype('float32'))
    np.save(saving_path+'/Densities/'+str(partition_num)+'_relevant_densities.npy',relevant_densities_no_overlap_values.astype('float32'))

    print()
    print()



def array_number_to_partition_numbers(num_jobs,num_nodes,current_node,job_num_start=0,job_num_stop=-1):
    """
    Calculates which subsystems are processed by a given node.
    For example for 10 nodes and 100 subsystems the distributin would look like
    Node 1:  0,10,20,...,90
    Node 2:  1,11,21,...,91
    ...
    Node 10: 9,19,29,...,99
    This splitting guarantees relatively similar runtimes for each node which might not be the case if the first node computes the subsystems 0-9
    because subsystems at the edges are often faster to compute (as they contain more water).
    """

    if (job_num_stop==-1):
        job_num_stop=num_jobs
    num_jobs=job_num_stop-job_num_start
    job_array=np.arange(num_jobs)
    jobs_per_node=int(np.ceil(num_jobs/num_nodes))
    job_arrays_for_nodes=np.zeros(jobs_per_node*num_nodes,dtype='int32')-1
    job_arrays_for_nodes[:num_jobs]=job_array
    job_arrays_for_nodes=job_arrays_for_nodes.reshape(jobs_per_node,num_nodes).T
    
    jobs_to_current_node=job_arrays_for_nodes[current_node]
    mask=np.where(jobs_to_current_node>=0)
    jobs_to_current_node=jobs_to_current_node[mask]
    
    return jobs_to_current_node 



def initialize_and_run_HF(total_coordinates,total_elements,saving_path,num_jobs,num_nodes,job_array_number):
    """
    The main function which is called for a large-scale divide-and-conquer Hartree-Fock calculation.
    """

    partition_numbers_array=array_number_to_partition_numbers(num_jobs,num_nodes,current_node=job_array_number)
    print()
    print('LOG NUMBER '+str(job_array_number))
    print('This node runs a Hartree-Fock calculation for the following partition numbers: ')
    print(partition_numbers_array)
    print()
    print()
    
    for p_num in range(len(partition_numbers_array)):
        partition_num=partition_numbers_array[p_num]
        coordinates_partition,elements_partition,atoms_partition,partition_atoms_unique,center_coordinate=initialize_divide_conquer_HF(total_coordinates,total_elements,partition_num)
        run_HF_for_partition(coordinates_partition,elements_partition,atoms_partition,partition_atoms_unique,partition_num,center_coordinate,saving_path=saving_path)
        
    return None











"""
========================
========================
DENSITY GRID COMPUTATION
========================
========================
"""




def calculate_grid(coordinates):
    """
    Calculates the grid for the calculation of the electronic density on a 3D real-space grid.
    The np.meshgrid() function is used for this.
    """

    x_min,x_max=np.min(coordinates[:,0])-additional_space,np.max(coordinates[:,0])+additional_space 
    y_min,y_max=np.min(coordinates[:,1])-additional_space,np.max(coordinates[:,1])+additional_space 
    z_min,z_max=np.min(coordinates[:,2])-additional_space,np.max(coordinates[:,2])+additional_space 
    x_pixels=int(np.floor((x_max-x_min)/pixel_size+1))
    y_pixels=int(np.floor((y_max-y_min)/pixel_size+1))
    z_pixels=int(np.floor((z_max-z_min)/pixel_size+1))
    x_max=x_min+(x_pixels-1)*pixel_size
    y_max=y_min+(y_pixels-1)*pixel_size
    z_max=z_min+(z_pixels-1)*pixel_size
    x,y,z=np.linspace(x_min,x_max,x_pixels,dtype=single),np.linspace(y_min,y_max,y_pixels,dtype=single),np.linspace(z_min,z_max,z_pixels,dtype=single)
    x,y,z=np.meshgrid(x,y,z,indexing='ij')

    return x,y,z,x_min,y_min,z_min


@njit
def wave_function_tables(x,y,z,x_min,y_min,z_min,gaussian_functions_coordinates,gaussian_functions_coefficients,gaussian_functions_exponents,coordinates,
                         gaussian_functions_index_list,atom_of_basisfunction,num_basis_functions):
    """
    Precomputes the wave functions needed for calculation the density of a Hartree-Fock calculation on a real-space grid.
    These wave functions are precomputed since they are used many times during the calculation of the individual electronic densities.
    """

    wave_function_grid_length=int((2.0*basis_function_space)/pixel_size+1)
    wave_function_grids=np.zeros((num_basis_functions,wave_function_grid_length,wave_function_grid_length,wave_function_grid_length),dtype=single)
    wave_function_points=np.zeros((num_basis_functions,3),dtype='int32')

    for i in range(num_basis_functions):
        center=coordinates[atom_of_basisfunction[i]]
        x_min_i=center[0]-basis_function_space
        y_min_i=center[1]-basis_function_space
        z_min_i=center[2]-basis_function_space
        x_point=int((x_min_i-x_min)/pixel_size)
        y_point=int((y_min_i-y_min)/pixel_size)
        z_point=int((z_min_i-z_min)/pixel_size)
        x_wave,y_wave,z_wave=x[x_point:x_point+wave_function_grid_length,y_point:y_point+wave_function_grid_length,z_point:z_point+wave_function_grid_length],\
                             y[x_point:x_point+wave_function_grid_length,y_point:y_point+wave_function_grid_length,z_point:z_point+wave_function_grid_length],\
                             z[x_point:x_point+wave_function_grid_length,y_point:y_point+wave_function_grid_length,z_point:z_point+wave_function_grid_length]
        wave_function_points[i,0],wave_function_points[i,1],wave_function_points[i,2]=x_point,y_point,z_point
        for gi in range(gaussian_functions_index_list[i],gaussian_functions_index_list[i+1]):
            x_wave_new=x_wave-gaussian_functions_coordinates[gi,0]
            y_wave_new=y_wave-gaussian_functions_coordinates[gi,1]
            z_wave_new=z_wave-gaussian_functions_coordinates[gi,2]
            wave_function_grids[i]+=gaussian_functions_coefficients[gi]*np.exp(-gaussian_functions_exponents[gi]*(x_wave_new*x_wave_new+y_wave_new*y_wave_new+z_wave_new*z_wave_new))
    wave_function_points_r=wave_function_points+wave_function_grid_length

    return wave_function_grids,wave_function_points,wave_function_points_r


@njit
def remove_density_overlap(ij_list_no_duplicates,atom_of_basisfunction,atoms_partition,partition_atoms_unique):
    """
    Removes density contributions that not included in the current partition. 
    This is done by checking if both wave functions of a denisty are located on atoms in the current partition.
    """

    relevant_densities=len(ij_list_no_duplicates)
    relevant_densities_no_overlap=np.zeros((relevant_densities,2),dtype='int32')
    no_overlap_count=0
    for d in range(relevant_densities):
        i,j=ij_list_no_duplicates[d]
        atom_i,atom_j=atom_of_basisfunction[i],atom_of_basisfunction[j]
        system_atom_i,system_atom_j=atoms_partition[atom_i],atoms_partition[atom_j]
        i_included,j_included=False,False
        if (system_atom_i in partition_atoms_unique): i_included=True
        if (system_atom_j in partition_atoms_unique): j_included=True
        
        if (i_included and j_included):
            relevant_densities_no_overlap[no_overlap_count,0],relevant_densities_no_overlap[no_overlap_count,1]=i,j
            no_overlap_count+=1
        elif ((i_included and not j_included) or (not i_included and j_included)):
            relevant_densities_no_overlap[no_overlap_count,0],relevant_densities_no_overlap[no_overlap_count,1]=i,j
            no_overlap_count+=1

    relevant_densities_no_overlap=relevant_densities_no_overlap[:no_overlap_count]

    return relevant_densities_no_overlap



@njit
def initialize_divide_conquer_HF_for_plot(total_coordinates,total_elements,partition_num,xyz):
    """
    Initializes a divide-and-conquer Hartree-Fock run for calculating the density on a grid.
    """
    
    parts_center_coordinates=xyz
    
    center_coordinate=parts_center_coordinates[partition_num]
    
    section_atoms,section_coordinates,section_elements=select_relevant_atoms(total_coordinates,total_elements,center_coordinate,0.5*partition_length+partition_cut_off+section_cut_off)
    
    partition_atoms,partition_coordinates,_=select_relevant_atoms(section_coordinates,section_elements,center_coordinate,0.5*partition_length)
    
    padded_partition_atoms,_,_,partition_unique\
        =partition_naive_neighbor_list(partition_atoms,partition_coordinates,section_coordinates,section_elements,partition_cut_off,parts_center_coordinates,partition_length,partition_num)

    bonds,_,_,bond_nums,_=calculate_bonds(section_coordinates,section_elements,cut=4.0,cut_H=2.6)
    atoms_final,coordinates_final,elements_final=avoid_bond_cutting(padded_partition_atoms,section_coordinates,section_elements,bonds,bond_nums)
    partition_atoms_unique=partition_unique
    
    atom_ids=section_atoms[atoms_final]

    return coordinates_final,elements_final,atoms_final,partition_atoms_unique,atom_ids



@njit
def calculate_density_grid_for_partitions(x,y,z,x_min,y_min,z_min,total_coordinates,total_elements,xyz,num_subsystems,
                                          hide_H_atoms=False,saving_path='Output_Data/Vault/Densities'):
    """
    The main functions that is called to compute a real-space grid of the electronic density after a large-scale Hartree-Fock calculation.
    """
    
    num_plot_threads=1

    x_len,y_len,z_len=x.shape[0],x.shape[1],x.shape[2]
    complete_density_grid=np.zeros((x_len,y_len,z_len),dtype=single)

    relevant_partitions=np.arange(num_subsystems)
    num_plots=len(relevant_partitions)

    id_cut=968136-1

    print('Plotting subsystems:')
    print(relevant_partitions)
    print()
    print()
    print('Current system')

    for t in range(num_plot_threads):
        
        for partition_num in relevant_partitions[t::num_plot_threads]:
            print(str(partition_num)+'/'+str(num_plots) +'-'+str(int(partition_num/num_plots*10000.0)/100)+'%')

            partition_coordinates,partition_elements,atoms_partition,partition_atoms_unique,atom_ids=initialize_divide_conquer_HF_for_plot(total_coordinates,total_elements,partition_num,xyz)
            
            if (np.min(atom_ids)>id_cut): continue


            num_atoms=len(partition_coordinates)
            num_basis_functions=calculate_num_basis_functions(partition_elements,num_atoms)
            
            num_gaussian_functions,_,gaussian_functions_index_list,atom_of_basisfunction,type_of_basis_function\
                            =calculate_num_gaussian_functions(partition_elements,num_atoms,num_basis_functions)
            gaussian_functions_coordinates,gaussian_functions_coefficients,gaussian_functions_exponents\
                            =calculate_gaussian_function_inputs(partition_elements,partition_coordinates,num_atoms,num_gaussian_functions)

            
            num_orbital_parts,orbital_parts_index_list=calculate_num_orbital_parts(partition_elements,num_atoms,num_basis_functions) 
            num_parts_gaussian_functions,orbital_parts_gaussian_index_list\
                            =calculate_gaussians_for_orbital_parts(partition_elements,num_atoms,num_orbital_parts)
            orbital_parts_coordinates,orbital_parts_coefficients,orbital_parts_exponents=calculate_orbital_parts_preprocessing(partition_elements,partition_coordinates,num_parts_gaussian_functions,num_atoms)
            
            ij_list_no_duplicates,_,_,_,_,_,_\
                            =calculate_relevant_densities(orbital_parts_coefficients,orbital_parts_exponents,orbital_parts_coordinates,
                                                        orbital_parts_index_list,orbital_parts_gaussian_index_list,atom_of_basisfunction,gaussian_functions_index_list,
                                                        partition_coordinates,num_gaussian_functions,num_basis_functions)



            relevant_densities_no_overlap=remove_density_overlap(ij_list_no_duplicates,atom_of_basisfunction,atoms_partition,partition_atoms_unique)

            relevant_densities=relevant_densities_no_overlap
            relevant_densities_values=np.load(saving_path+'/'+str(partition_num)+'_relevant_densities.npy')
        
            num_basis_functions=len(atom_of_basisfunction)   

            wave_function_grids,wave_function_points,wave_function_points_r=wave_function_tables(x,y,z,x_min,y_min,z_min,gaussian_functions_coordinates,gaussian_functions_coefficients,gaussian_functions_exponents,
                                                                                                partition_coordinates,gaussian_functions_index_list,atom_of_basisfunction,num_basis_functions)

            for d in range(len(relevant_densities)):
                i,j=int(relevant_densities[d,0]),int(relevant_densities[d,1])

                update_density=True
                if (atom_ids[atom_of_basisfunction[i]]>id_cut or atom_ids[atom_of_basisfunction[j]]>id_cut):
                    update_density=False
                if (hide_core_electrons):
                    if ((type_of_basis_function[i]==1 and partition_elements[atom_of_basisfunction[i]]!=1) or (type_of_basis_function[j]==1 and partition_elements[atom_of_basisfunction[j]]!=1)):
                        update_density=False
                    if ((type_of_basis_function[i]<=3 and partition_elements[atom_of_basisfunction[i]]>10) or (type_of_basis_function[j]<=3 and partition_elements[atom_of_basisfunction[j]]>10)):
                        update_density=False
                if (hide_H_atoms):
                    if (partition_elements[atom_of_basisfunction[i]]==1 or partition_elements[atom_of_basisfunction[j]]==1):
                        update_density=False
                
                if (update_density):
                    x_point_l=max(wave_function_points[i,0],wave_function_points[j,0])
                    y_point_l=max(wave_function_points[i,1],wave_function_points[j,1])
                    z_point_l=max(wave_function_points[i,2],wave_function_points[j,2])
                    x_point_r=min(wave_function_points_r[i,0],wave_function_points_r[j,0])
                    y_point_r=min(wave_function_points_r[i,1],wave_function_points_r[j,1])
                    z_point_r=min(wave_function_points_r[i,2],wave_function_points_r[j,2])
                    x_point_l_i,y_point_l_i,z_point_l_i=x_point_l-wave_function_points[i,0],y_point_l-wave_function_points[i,1],z_point_l-wave_function_points[i,2]
                    x_point_l_j,y_point_l_j,z_point_l_j=x_point_l-wave_function_points[j,0],y_point_l-wave_function_points[j,1],z_point_l-wave_function_points[j,2]
                    x_point_r_i,y_point_r_i,z_point_r_i=x_point_r-wave_function_points[i,0],y_point_r-wave_function_points[i,1],z_point_r-wave_function_points[i,2]
                    x_space=max(0,x_point_r_i-x_point_l_i)
                    y_space=max(0,y_point_r_i-y_point_l_i)
                    z_space=max(0,z_point_r_i-z_point_l_i)
                    current_density=np.multiply(wave_function_grids[i,x_point_l_i:x_point_l_i+x_space,y_point_l_i:y_point_l_i+y_space,z_point_l_i:z_point_l_i+z_space],
                                                wave_function_grids[j,x_point_l_j:x_point_l_j+x_space,y_point_l_j:y_point_l_j+y_space,z_point_l_j:z_point_l_j+z_space])
                if (update_density):
                    if (i!=j):
                        double_prefactor=2.0
                    else:
                        double_prefactor=1.0
                    complete_density_grid[x_point_l:x_point_r,y_point_l:y_point_r,z_point_l:z_point_r]+=relevant_densities_values[d]*double_prefactor*current_density

 

    return complete_density_grid





























"""
=====================================
=====================================
REAL-TIME TIME-DEPENDENT HARTREE-FOCK
=====================================
=====================================
"""





@njit
def electric_field_integral(gaussian_functions_coefficients_i,gaussian_functions_coefficients_j,gaussian_functions_exponents_i,gaussian_functions_exponents_j,
                            gaussian_functions_coordinates_i_x,gaussian_functions_coordinates_i_y,gaussian_functions_coordinates_i_z,
                            gaussian_functions_coordinates_j_x,gaussian_functions_coordinates_j_y,gaussian_functions_coordinates_j_z,
                            e_field_strength,e_field_origin_x,e_field_origin_y,e_field_origin_z,direction):
    """
    Calculates a single entry for the electric field matrix E.
    The computed integrals are <phi_i|d_alpha|phi_j> where d_alpha is one component of the dipole moment operator d=transpose(x,y,z)
    For example: we are computing <phi_i|x|phi_j> for the E_x matrix.
    """
    
    prefactor=gaussian_functions_coefficients_i*gaussian_functions_coefficients_j
    exp_sum=gaussian_functions_exponents_i+gaussian_functions_exponents_j
    exp_product=gaussian_functions_exponents_i*gaussian_functions_exponents_j
    product_sum_quotient=exp_product/exp_sum

    distance_x=gaussian_functions_coordinates_i_x-gaussian_functions_coordinates_j_x
    distance_y=gaussian_functions_coordinates_i_y-gaussian_functions_coordinates_j_y
    distance_z=gaussian_functions_coordinates_i_z-gaussian_functions_coordinates_j_z
    coordinate_distance=distance_x*distance_x+distance_y*distance_y+distance_z*distance_z

    pi_divided_by_sum=np.pi/exp_sum
    result_s=prefactor*pi_divided_by_sum*np.sqrt(pi_divided_by_sum)*np.exp(-product_sum_quotient*coordinate_distance)

    if (direction==0):
        correction=(gaussian_functions_exponents_i*gaussian_functions_coordinates_i_x+gaussian_functions_exponents_j*gaussian_functions_coordinates_j_x-exp_sum*e_field_origin_x)
    elif (direction==1):
        correction=(gaussian_functions_exponents_i*gaussian_functions_coordinates_i_y+gaussian_functions_exponents_j*gaussian_functions_coordinates_j_y-exp_sum*e_field_origin_y)
    elif (direction==2):
        correction=(gaussian_functions_exponents_i*gaussian_functions_coordinates_i_z+gaussian_functions_exponents_j*gaussian_functions_coordinates_j_z-exp_sum*e_field_origin_z)
    result_e=e_field_strength*result_s*correction/exp_sum
    
    return result_e


@njit
def calculate_electric_field_matrix(gaussian_functions_coefficients,gaussian_functions_exponents,gaussian_functions_coordinates,
                                    gaussians_for_densities,gaussians_for_densities_index_list,relevant_densities_no_duplicates,
                                    e_field_strength,e_field_origin_x,e_field_origin_y,e_field_origin_z,direction):
    """
    This function calculates the electric field matrix E which is needed for real-time time-dependent Hartree-Fock calculations.
    The individual entries of the matrix E are computed by calling the function electric_field_integral() for every relevant density.
    """

    electric_field_matrix=np.zeros((relevant_densities_no_duplicates),dtype=datatype)

    for d in range(relevant_densities_no_duplicates):
        for gd in range(gaussians_for_densities_index_list[d],gaussians_for_densities_index_list[d+1]):
            gi,gj=gaussians_for_densities[gd,0],gaussians_for_densities[gd,1]
            integral_value_e=electric_field_integral(gaussian_functions_coefficients[gi],gaussian_functions_coefficients[gj],gaussian_functions_exponents[gi],gaussian_functions_exponents[gj],
                                                     gaussian_functions_coordinates[gi,0],gaussian_functions_coordinates[gi,1],gaussian_functions_coordinates[gi,2],
                                                     gaussian_functions_coordinates[gj,0],gaussian_functions_coordinates[gj,1],gaussian_functions_coordinates[gj,2],
                                                     e_field_strength,e_field_origin_x,e_field_origin_y,e_field_origin_z,direction)
            electric_field_matrix[d]+=integral_value_e
    
    return electric_field_matrix



@njit(parallel=True,fastmath=True)
def calculate_complex_G(P,V_ee,ijkl_list,num_basis_functions,relevant_V_ee_elements):
    """
    Calculates the two-center part of the Fock matrix. This algorithm is modified for a complex matrix G. 
    The usual algorithm cannot be used for a calculation with a complex density matrix input since it relies on it being real symmetric.
    """

    num_parts=num_threads_G
    part_length=int(np.ceil(relevant_V_ee_elements/num_parts))
    G=np.zeros((num_parts,num_basis_functions,num_basis_functions),dtype='complex128')
    if (num_basis_functions==1): return np.sum(G,axis=0)
    
    for part in prange(num_parts):
        max_index=min((part+1)*part_length,relevant_V_ee_elements)
        ijkl_list_part=ijkl_list[part*part_length:max_index]
        V_ee_part=V_ee[part*part_length:max_index]
        for ee in range(max_index-part*part_length):
            ijkl_list_ee=ijkl_list_part[ee]
            i,j,k,l=ijkl_list_ee[0],ijkl_list_ee[1],ijkl_list_ee[2],ijkl_list_ee[3]
            V_ee_ee=V_ee_part[ee]
            P_kl_V=P[k,l]*V_ee_ee
            P_lk_V=P[l,k]*V_ee_ee
            P_ij_V=P[i,j]*V_ee_ee
            P_ji_V=P[j,i]*V_ee_ee

            if (k!=l):
                G[part,i,j]+=P_kl_V
                G[part,i,j]+=P_lk_V
                G[part,i,k]-=0.5*P[l,j]*V_ee_ee
            else:
                G[part,i,j]+=P_kl_V
            G[part,i,l]-=0.5*P[k,j]*V_ee_ee

            if (i!=j):
                if (k!=l):
                    G[part,j,i]+=P_kl_V
                    G[part,j,i]+=P_lk_V
                    G[part,j,k]-=0.5*P[l,i]*V_ee_ee
                else:
                    G[part,j,i]+=P_kl_V
                G[part,j,l]-=0.5*P[k,i]*V_ee_ee
                        
            b=not(i==k and j==l)
            if (b):
                if (i!=j):
                    G[part,k,l]+=P_ij_V
                    G[part,k,l]+=P_ji_V
                    G[part,k,i]-=0.5*P[j,l]*V_ee_ee
                else:
                    G[part,k,l]+=P_ij_V
                G[part,k,j]-=0.5*P[i,l]*V_ee_ee
                
            if (b and k!=l):
                if (i!=j):
                    G[part,l,k]+=P_ij_V
                    G[part,l,k]+=P_ji_V
                    G[part,l,i]-=0.5*P[j,k]*V_ee_ee
                else:
                    G[part,l,k]+=P_ij_V
                G[part,l,j]-=0.5*P[i,k]*V_ee_ee
            
    G=np.sum(G,axis=0)
    return G




def time_propagation(F_n_1_2_in,F_n_3_2_in,S,P,eigenorbitals,H_core,E,V_ee,ijkl_list,relevant_V_ee_elements,num_basis_functions,e_field_strengths,e_field_strengths_half,elements,
                     time_domain,time_steps,delta_t,update=100):
    """
    This function performs the propagtion in time for a real-time time-dependent Hartree-Fock calculation.
    The runtimes of the individual parts of the code are tracked with time.time() and returned after completion of the method in the console.
    """

    total_time=0.0
    time_s_matrix=0.0
    time_prep=0.0
    time_F_transform=0.0
    time_matrix_exp=0.0
    time_P_transform=0.0
    time_time_evolution=0.0
    time_P_transform_back=0.0
    time_G=0.0
    time_other=0.0

    time_start=time.time()
    
    time_1=time.time()
    dipole_moments=np.zeros((3,time_steps+1),dtype='complex128')
    consistency=np.zeros((3,time_steps+1),dtype='complex128')
    H_core=torch.from_numpy(H_core).to(torch.complex128)

    S=torch.from_numpy(S.astype('float64')).to(torch.float64)
    evals,evecs=torch.linalg.eigh(S)
    evpow_1=evals**(-1/2) 
    S_inverse_sqrt=torch.matmul(evecs,torch.matmul(torch.diag(evpow_1),torch.inverse(evecs))).to(torch.complex128)
    evpow_2=evals**(1/2) 
    S_sqrt=torch.matmul(evecs,torch.matmul(torch.diag(evpow_2),torch.inverse(evecs))).to(torch.complex128)
    time_2=time.time()
    time_s_matrix+=time_2-time_1
    
    for xyz in range(3):
        
        time_1=time.time()
        E_xyz=E[xyz]
        E_xyz=torch.from_numpy(E_xyz).to(torch.complex128)

        P_0=torch.from_numpy(P).to(torch.complex128).detach().clone()
        F_n_1_2=torch.from_numpy(F_n_1_2_in).to(torch.complex128).detach().clone()
        F_n_3_2=torch.from_numpy(F_n_3_2_in).to(torch.complex128).detach().clone()

        dipole_moments[xyz,0]=torch.sum(P_0*E_xyz).numpy()
        SPS=S_sqrt@(P_0@S_sqrt)
        consistency[xyz,0]=torch.sum(SPS*SPS).numpy()
        time_2=time.time()
        time_prep+=time_2-time_1

        for i in range(1,time_steps+1):

            time_1=time.time()
            relative_e_field_strength_1_2=e_field_strengths_half[i]
            F_1_4=1.75*F_n_1_2-0.75*F_n_3_2
            time_2=time.time()
            time_other+=time_2-time_1

            time_1=time.time()
            exp_matrix=(-0.5*delta_t*1j)*(S_inverse_sqrt@(F_1_4@S_inverse_sqrt))
            time_2=time.time()
            time_F_transform+=time_2-time_1

            time_1=time.time()
            U_1_2=torch.linalg.matrix_exp(exp_matrix)
            time_2=time.time()
            time_matrix_exp+=time_2-time_1

            time_1=time.time()
            P_0_transformed=S_sqrt@(P_0@S_sqrt)
            time_2=time.time()
            time_P_transform+=time_2-time_1

            time_1=time.time()
            P_1_2=U_1_2@(P_0_transformed@(torch.conj(torch.t(U_1_2))))
            time_2=time.time()
            time_time_evolution+=time_2-time_1

            time_1=time.time()
            P_1_2=S_inverse_sqrt@(P_1_2@S_inverse_sqrt)
            time_2=time.time()
            time_P_transform_back+=time_2-time_1

            time_1=time.time()
            G=calculate_complex_G(P_1_2.numpy(),V_ee,ijkl_list,num_basis_functions,relevant_V_ee_elements)
            time_2=time.time()
            time_G+=time_2-time_1

            time_1=time.time()
            F_1_2=H_core+torch.from_numpy(G).to(torch.complex128)+E_xyz*relative_e_field_strength_1_2
            time_2=time.time()
            time_other+=time_2-time_1



            time_1=time.time()
            exp_matrix=(-delta_t*1j)*(S_inverse_sqrt@(F_1_2@S_inverse_sqrt))
            time_2=time.time()
            time_F_transform+=time_2-time_1

            time_1=time.time()
            U_1=torch.linalg.matrix_exp(exp_matrix)
            time_2=time.time()
            time_matrix_exp+=time_2-time_1

            time_1=time.time()
            P_1=U_1@(P_0_transformed@(torch.conj(torch.t(U_1))))
            time_2=time.time()
            time_time_evolution+=time_2-time_1

            time_1=time.time()
            consistency[xyz,i]=torch.sum(P_1*P_1)
            time_2=time.time()
            time_other+=time_2-time_1

            time_1=time.time()
            P_1=S_inverse_sqrt@(P_1@S_inverse_sqrt)
            time_2=time.time()
            time_P_transform_back+=time_2-time_1

            time_1=time.time()
            dipole_moments[xyz,i]=(torch.sum(P_1*E_xyz)).numpy()
            P_0=P_1.detach().clone()
            F_n_3_2=F_n_1_2.detach().clone()
            F_n_1_2=F_1_2.detach().clone()
            time_2=time.time()
            time_other+=time_2-time_1
            
            
            np.save('file/to/output/dipole_moments',dipole_moments)


            if (i%update==0): print('Coordinate '+str(xyz+1)+' - Step '+str(i)+'/'+str(time_steps)+': '+str(np.round(i/time_steps*100.0,4))+'% - dipole moment: '+str(np.real(dipole_moments[xyz,i]-dipole_moments[xyz,0]))+' - numerical stability: '+str(np.real(consistency[xyz,i]-consistency[xyz,0])))

    

    
    dipole_moments[0]-=dipole_moments[0,0]
    dipole_moments[1]-=dipole_moments[1,0]
    dipole_moments[2]-=dipole_moments[2,0]

    time_stop=time.time()
    total_time=time_stop-time_start

    print('Time-propagtion times:')
    print('    |S matrix exponentiation: '+str(np.round(time_s_matrix,4))+' s')
    print('    |Preparation times: '+str(np.round(time_prep,4))+' s')
    print('    |Fock matrix transforms: '+str(np.round(time_F_transform,4))+' s')
    print('    |Matrix exponentiation: '+str(np.round(time_matrix_exp,4))+' s')
    print('    |Density matrix transforms: '+str(np.round(time_P_transform,4))+' s')
    print('    |Time evolution: '+str(np.round(time_time_evolution,4))+' s')
    print('    |Density matrix back-transforms: '+str(np.round(time_P_transform_back,4))+' s')
    print('    |G matrix computations: '+str(np.round(time_G,4))+' s')
    print('    |Additions, traces and copies: '+str(np.round(time_other,4))+' s')
    print('____________________________________________')
    print('Total time: '+str(np.round(total_time,4))+' s')

    return dipole_moments,consistency






def run_rthf(coordinates,elements,time_steps=10000,delta_t=0.1,pulse_standard_deviation=0.2,pulse_shift_factor=15,e_field_max=2.0e-5,update=100):
    """
    The main function to run a real-time time-dependent Hartree-Fock calculation.
    First a single Hartree-Fock run is done to calculate relevant matrices (e.g. the density matrix, overlap matrix, the electron rpulsion tensor, ...).
    Afterwards the E-field matrices are computed for the three spatial directions.
    Finally the propagation in time is done by calling the function time_propagtion(). 
    The outputs are stored in an array (rthf_outputs) and returned.
    """

    pulse_shift=pulse_shift_factor*pulse_standard_deviation

    time_domain=np.linspace(0,time_steps*delta_t,time_steps+1)

    relative_e_field_strengths=np.exp(-((time_domain-pulse_shift)**2)/(2*pulse_standard_deviation**2))*e_field_max
    relative_e_field_strengths_half=np.exp(-((time_domain-0.5*delta_t-pulse_shift)**2)/(2*pulse_standard_deviation**2))*e_field_max

    gaussian_functions_coefficients,gaussian_functions_exponents,gaussian_functions_coordinates,gaussians_for_densities,gaussians_for_densities_index_list,\
    F,S,P,eigenorbitals,H_core,ij_list_no_duplicates,relevant_densities_no_duplicates,V_ee,ijkl_list,relevant_V_ee_elements,num_basis_functions,center_of_mass,_,_,_\
                    =run_HF(coordinates,elements,rthf=True)
    
    F=F.astype('complex128')
    P=P.astype('complex128')
    H_core=H_core.astype('complex128')
    V_ee=V_ee.astype('complex128')

    e_field_origin_x,e_field_origin_y,e_field_origin_z=center_of_mass[0],center_of_mass[1],center_of_mass[2]
    E=np.zeros((3,num_basis_functions,num_basis_functions),dtype='complex128')
    for xyz in range(3):
        E[xyz]=sparse_to_dense(ij_list_no_duplicates,
                               calculate_electric_field_matrix(gaussian_functions_coefficients,gaussian_functions_exponents,gaussian_functions_coordinates,
                                                               gaussians_for_densities,gaussians_for_densities_index_list,relevant_densities_no_duplicates,
                                                               1.0,e_field_origin_x,e_field_origin_y,e_field_origin_z,xyz)*(-1), 
                               num_basis_functions)
        
    
    dipole_moments,consistency=time_propagation(F,F,S,P,eigenorbitals,H_core,E,V_ee,ijkl_list,relevant_V_ee_elements,num_basis_functions,relative_e_field_strengths,relative_e_field_strengths_half,elements,
                                    time_domain,time_steps,delta_t,update=update)
    
    rthf_outputs=np.zeros((8,time_steps+1),dtype='complex128')
    rthf_outputs[:3]=dipole_moments
    rthf_outputs[3]=time_domain
    rthf_outputs[4]=relative_e_field_strengths
    rthf_outputs[5:8]=consistency
    
    return rthf_outputs





























"""
=======================================
=======================================
ALPHA-FOLD CONFIDENCE SCORE PREDICTIONS
=======================================
=======================================
"""



def load_CA_coordinates_pdb(file_path,discard_hetatoms=False,file_type=2):
    """
    Loads in only the C-alpha atoms of a pdb file.
    Used for visualizing protein chains.
    """

    structure_elements=[]
    structure_coordinates=[]
    structure_proteins=[]
    structure_numbers=[]
    element_strings=['H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar']

    with open(file_path+'.txt','r') as file:
        reading_coords=False
        stop_reading=False

        count=0
        for line in file:
            words=line.split()

            if (words[0]=='ATOM' or words[0]=='HETATM'):
                reading_coords=True
            if (reading_coords and words[0]=='#'):
                break
            
            if (reading_coords):
                if (words[0]=='TER' or words[0]=='END' or words[0]=='IGN' or words[0]=='CONECT' or words[0]=='ANISOU'):
                    continue
                if ((words[0]=='HETATM' and discard_hetatoms)
                    or (words[0]=='ENDMDL')
                    or (words[0]=='MODEL' and words[1]=='2')):
                    stop_reading=True
                    break
                if ((words[3]=='WAT' or words[2]=='WAT') and discard_hetatoms):
                    stop_reading=True
                    break

                if (file_type==1):
                    count+=1
                    if (words[3]!='CA'): continue
                    structure_proteins.append(words[6])
                    structure_numbers.append(count)
                    structure_coordinates.append([words[10],words[11],words[12]])
                    for i in range(len(element_strings)):
                        if (words[2]==element_strings[i]):
                            structure_elements.append(i+1)
                            break
                elif (file_type==2):
                    count+=1
                    if (words[2]!='CA'): continue
                    structure_proteins.append(words[6])
                    structure_numbers.append(count)
                    if (words[3]=='WAT' or words[2]=='WAT'):
                        if (words[0]=='HETATM'):
                            structure_coordinates.append([words[5],words[6],words[7]])
                        else:
                            structure_coordinates.append([words[4],words[5],words[6]])
                    elif ((words[2]=='H1' or words[2]=='H2' or words[2]=='OH2') and count>10000):
                        if (len(words[3])>5):
                            structure_coordinates.append([words[4],words[5],words[6]])
                        else:
                            structure_coordinates.append([words[5],words[6],words[7]])
                        if (words[2]=='OH2'):
                            structure_elements.append(8)
                        else:
                            structure_elements.append(1)
                        continue
                    else:
                        if (len(words[2])<5):
                            structure_coordinates.append([words[6],words[7],words[8]])
                        else:
                            structure_coordinates.append([words[5],words[6],words[7]])
                    if (len(words[-1])>2):
                        structure_elements.append(1)
                    else:
                        for i in range(len(element_strings)):
                            if (words[-1]==element_strings[i]):
                                structure_elements.append(i+1)
                                break
            
            if (stop_reading): break

    structure_coordinates=np.array(structure_coordinates,dtype='float32')*angstrom_to_bohr
    structure_elements=np.array(structure_elements,dtype='int32')
    structure_numbers=np.array(structure_numbers,dtype='int32')

    return structure_coordinates,structure_elements,structure_proteins,structure_numbers







@njit
def naive_neighbor_list_for_unique_section(total_atoms_coordinates,unique_atoms_ids,cut_off,max_neighbors=1000):
    """
    A naive neighbourhood algorithm.
    """

    num_total_atoms=len(total_atoms_coordinates)
    num_unique_atoms=len(unique_atoms_ids)
    total_atoms_ids=np.arange(num_total_atoms)

    n_list=np.zeros(num_unique_atoms*max_neighbors,dtype='int32')
    n_list_length=0
    for i in unique_atoms_ids:
        for j in total_atoms_ids:
            coordinates_i=total_atoms_coordinates[i]
            coordinates_j=total_atoms_coordinates[j]
            dist_x=coordinates_i[0]-coordinates_j[0]
            if (np.abs(dist_x)>cut_off): continue
            dist_y=coordinates_i[1]-coordinates_j[1]
            if (np.abs(dist_y)>cut_off): continue
            dist_z=coordinates_i[2]-coordinates_j[2]
            if (np.abs(dist_z)>cut_off): continue
            dist=np.sqrt(dist_x*dist_x+dist_y*dist_y+dist_z*dist_z)
            if (dist>cut_off): continue
            n_list[n_list_length]=j
            n_list_length+=1
    
    n_list=np.unique(n_list[:n_list_length])
    return n_list



def run_AlphaFold_prediction(coordinates_without_water,elements_without_water,coordinates,elements,structure_numbers,bonds,bond_nums,amino_acids_per_cluster,saving_path):
    """
    The main function for running a calculation of atomic energies for a protein or protein complex.
    These energies can be used to evaluate protein structure predictions since they correlate with AlphaFold's pLDDT (predicted local distance difference test) score.
    """

    max_unique_atoms_per_cluster=1000
    num_atoms_without_water=len(coordinates_without_water)

    num_amino_acids=len(structure_numbers)
    number_of_clusters=int(np.ceil(num_amino_acids/amino_acids_per_cluster))
    cluster_borders=structure_numbers[np.linspace(0,num_amino_acids-1,number_of_clusters+1).astype('int32')-1]
    cluster_borders[0]=0
    cluster_borders[-1]=num_atoms_without_water

    cluster_unique_atoms=np.zeros((number_of_clusters,max_unique_atoms_per_cluster),dtype='int32')
    num_unique_coords=np.zeros(number_of_clusters,dtype='int32')
    max_atoms=0
    for i in range(number_of_clusters):
        atoms_of_this_cluster=cluster_borders[i+1]-cluster_borders[i]
        if (atoms_of_this_cluster>max_atoms): max_atoms=atoms_of_this_cluster
        cluster_unique_atoms[i,:atoms_of_this_cluster]=np.arange(cluster_borders[i],cluster_borders[i+1])
        num_unique_coords[i]=atoms_of_this_cluster
    cluster_unique_atoms=cluster_unique_atoms[:,:max_atoms]

    num_atoms_total=len(elements_without_water)

    energies_0_total=np.zeros(num_atoms_total)
    energies_converged_total=np.zeros(num_atoms_total)


    print('Number of clusters:',number_of_clusters)

    for current_cluster_num in range(number_of_clusters):
        print('============')
        print('Cluster',current_cluster_num)
        print('============')

        unique_atoms_ids=cluster_unique_atoms[current_cluster_num,:num_unique_coords[current_cluster_num]]
        print('Unique atoms in this cluster:',len(unique_atoms_ids))
        n_list=naive_neighbor_list_for_unique_section(coordinates,unique_atoms_ids,10*angstrom_to_bohr)
        print('Atoms after adding neighbors:',len(n_list))
        
        atoms_final,coordinates_final,elements_final=avoid_bond_cutting(n_list,coordinates,elements,bonds,bond_nums)
        print('Atoms after avoiding bond cutting:',len(atoms_final))
        print()
        
        final_coordinates_cluster,final_elements_cluster=coordinates_final,elements_final

        _,P,P_0,G,G_0,H_core,_,_,_,_,_,_,_,type_of_basis_function,num_basis_functions\
            =run_HF(final_coordinates_cluster,final_elements_cluster,enable_plotting=True)
        print()
            
        E_0=H_core+0.5*G_0
        E=H_core+0.5*G
        
        num_atoms=len(final_coordinates_cluster)
        _,basis_functions_index_list,_,_,type_of_basis_function=calculate_num_gaussian_functions(final_elements_cluster,num_atoms,num_basis_functions)
        
        energies_0=np.zeros(num_atoms)
        energies_converged=np.zeros(num_atoms)
        
        
        h_atom_count=0
        heavy_atom_count=0
        for atm in range(num_atoms):
            for i in range(basis_functions_index_list[atm],basis_functions_index_list[atm+1]):
                if (type_of_basis_function[i]==1 and final_elements_cluster[atm]>1): continue
                if (type_of_basis_function[i]<=3 and final_elements_cluster[atm]==16): continue
                energies_0[atm]+=np.sum(E_0[i]*P_0[i])/final_elements_cluster[atm]
                energies_converged[atm]+=np.sum(E[i]*P[i])/final_elements_cluster[atm]
            if (final_elements_cluster[atm]>1): 
                heavy_atom_count+=1
            else: 
                h_atom_count+=1
        
        
        for atm in range(num_atoms):
            atom_id=atoms_final[atm]
            if (atom_id in unique_atoms_ids):
                energies_0_total[atom_id]=energies_0[atm]
                energies_converged_total[atom_id]=energies_converged[atm]
                
        np.save(saving_path+'/energies_0',energies_0_total)
        np.save(saving_path+'/energies_converged',energies_converged_total)

    return None



















"""
====================
####### MAIN #######
====================

Select a calculation mode (explanation below) and follow the corresponding instructions. 
You only need to modify the section of the selected calculation mode.

Two general annotations:
    1. Replace any strings containing path/to/... with the actual directories!
    2. Load atomic coordinates and elements
        - via 'coordinates,elements,_=load_coordinates(path/to/coordinate/file)' for a .json file
        - via 'coordinates,elements=load_coordinates_pdb(path/to/coordinate/file)' for a .pdb (protein data base) file
        - via 'coordinates=np.load('path/to/coordinates.npy')' and 'elements=np.load('path/to/elements.npy')' for coordinates/elements stored in a numpy file 
          (recommended for very large systems with >1,000,000 atoms)


Recommended test: download the coordinate file for Beta-Carotene obtained at 
https://pubchem.ncbi.nlm.nih.gov/compound/Beta-Carotene#section=3D-Conformer
and run the program in mode='normal' with the file path changed to the directory where the file was saved.
The output then should be identical to the output displayed at the parameter section, subsection outputs (apart from the last 2/3 digits which can vary).
This only holds if the default settings are used.
The execution time will be ~1-3 minutes if the program was not loaded before, otherwise ~10-60 seconds depending on the computer.
Note: The first execution of NIMBLE can take around 1-2 minutes longer as normally due to imports and compilation of the jit-functions.



------------------------------------
Explanations for the different modes
------------------------------------


---normal---
A single Hartree-Fock calculation.
Load the coordinates of the atoms and elements as described above.
run_HF() is called afterwards and the calculation starts.



---large_scale---
For a divide-and-conquer Hartree-Fock calculation. For >1,000,000 atoms it is recommended to use numpy arrays in single precision (.astype('float32')) to store and load coordinates and elements 
since PDB files of these structures can have the size of multiple GB and are difficult to upload and read out.

Specify the number of subsystems and number of compute nodes for the calculation (it is recommended to run this mode only on computing clusters, if not choose num_nodes=1). 
The number of subsystems has to be computed before the actual calculation by calling
'center_coordinates=calculate_parts_center_coordinates(coordinates,partition_length,partition_cut_off)'. 
This can also be done on a normal computer. Select the given output (total) as the number of your subsystems.

Make sure that the cut-offs for divide-and-conquer calculations are selected accordingly in the variable declaration section at the beginning of the program.

The job array number is the number of the computation thread. We recommend using the job array option from SLURM and passing the job number as 'job_array_number=int(sys.argv[1])'.
If only one device is used, set 'job_array_number=0'

Specify a saving path with 'saving_path=...'.

initialize_and_run_HF() is called and the calculation starts.



---plotting---
For calculating the electronic density on a 3D real-space grid. This mode therefore visualizes the results of a large-scale calculation.

Make sure that the cut-offs for divide-and-conquer calculations AND the parameters for density plotting calculations are selected accordingly 
in the variable declaration section at the beginning of the program.

Specify the path where the numpy array for the 3D grid will be saved with 'path/to/density_grid.npy'

calculate_density_grid_for_partitions() is called and the calculation starts.



---time_dependent---
For running a real-time time-dependent Hartree-Fock calculation used for the calculation of absorption spectra.

Load the coordinates of the atoms and elements as described above.

Make sure that the configurations for real-time time-dependent Hartree-Fock calculations are selected accordingly 
in the variable declaration section at the beginning of the program.

Specify a saving path with 'saving_path=...'.

run_rthf() is called and the calculation starts.



---alpha_fold---
For running a calculation of atomic energies. These correlate strongly with AlphaFolds pLDDT (predicted local distance difference test) score
which means atomic energies can be used to evaluate predicted protein structures from AlphaFold.

Load the coordinates of the atoms and elements by specifying the file path. Here we assume a .pdb file is used.

Make sure that the configuration for Alpha-Fold prediction calculations is selected accordingly 
in the variable declaration section at the beginning of the program ('amino_acids_per_cluster=...').

Specify a saving path with 'saving_path=...'.

run_AlphaFold_prediction() is called and the calculation starts.


"""



mode='normal'

if (mode=='normal'):

    """
    Examples:
    Beta-carotene, Insulin (more time-consuming), DNA (more time-consuming)
    coordinates,elements,_=load_coordinates('path/to/coordinate/file') 
    coordinates,elements=load_coordinates_pdb('Insulin_Test')
    coordinates,elements=load_coordinates_pdb('DNA_Test',file_type=1)
    """
    coordinates,elements,_=load_coordinates('Beta_Carotene_Test')
    energy,E_nn,P,F,eigenorbitals,eigenenergies,gaussian_functions_coefficients,gaussian_functions_exponents,gaussian_functions_coordinates,\
        ij_list_no_duplicates,atom_of_basisfunction,gaussian_functions_index_list,type_of_basis_function,num_basis_functions\
        =run_HF(coordinates,elements,enable_plotting=True)


elif (mode=='large_scale'):

    coordinates=np.load('path/to/coordinates.npy')
    elements=np.load('path/to/elements.npy')

    num_jobs=10000
    num_nodes=10
    job_array_number=int(sys.argv[1])
    saving_path='path/to/density/files'

    initialize_and_run_HF(coordinates,elements,saving_path,num_jobs,num_nodes,job_array_number)


elif (mode=='plotting'):

    total_coordinates=np.load('path/to/coordinates.npy')
    total_elements=np.load('path/to/elements.npy')

    num_subsystems=10000

    x,y,z,x_min,y_min,z_min=calculate_grid(total_coordinates)
    xyz=calculate_parts_center_coordinates(total_coordinates,partition_length,partition_cut_off)

    density_grid=calculate_density_grid_for_partitions(x,y,z,x_min,y_min,z_min,total_coordinates,total_elements,xyz,num_subsystems,
                                                       hide_H_atoms=False,saving_path='path/to/density/files')
    np.save('path/to/density_grid.npy',density_grid.astype('float32'))


elif (mode=='time_dependent'):

    coordinates,elements=load_coordinates_pdb('path/to/coordinate/file')


    saving_path='path/to/RTHF/data'

    rthf_outputs=run_rthf(coordinates,elements,time_steps=time_steps,delta_t=delta_t,pulse_standard_deviation=pulse_standard_deviation,pulse_shift_factor=pulse_shift_factor,e_field_max=e_field_max,update=update)

    np.save(saving_path,rthf_outputs)


elif (mode=='alpha_fold'):

    alpha_fold_file_path='path/to/coordinate/file'
    structure_coordinates,structure_elements,structure_proteins,structure_numbers=load_CA_coordinates_pdb(alpha_fold_file_path,discard_hetatoms=False,file_type=2)
    coordinates_without_water,elements_without_water=load_coordinates_pdb(alpha_fold_file_path,discard_hetatoms=True,file_type=2)
    coordinates,elements=load_coordinates_pdb(alpha_fold_file_path,discard_hetatoms=False,file_type=2)

    bonds,bond_types,bond_distances,bond_nums,element_distances=calculate_bonds(coordinates,elements,cut=4.0,cut_H=2.6)

    saving_path='path/to/AlphaFold/data'

    run_AlphaFold_prediction(coordinates_without_water,elements_without_water,coordinates,elements,structure_numbers,bonds,bond_nums,amino_acids_per_cluster,saving_path)


else:
    print('Calculation mode not recognized - change it in section MAIN. Choose between normal, large_scale, plotting, time_dependent, alpha_fold.')


