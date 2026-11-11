# NIMBLE: Nearsighted Integral-Optimized Matrix-Based Large-Scale Electronic Structure Prediction


```
===========================================
NIMBLE - a large-scale Hartree-Fock program
===========================================
Nearsighted Integral-Optimized Matrix-Based Large-Scale Electronic Structure Prediction
=           =                  =      =     =           =
=======================================================================================
```

## A quantum-mechanical framework for million-atom scale biological systems

L. Wieners, M.E. Garcia, **A quantum-mechanical framework for million-atom scale biological systems**, [Commun Chem 9, 170 (2026)](https://doi.org/10.1038/s42004-026-02038-y)


## Abstract

Quantum-mechanical simulations provide the most fundamental description of matter, yet their computational cost commonly limits applications to systems containing at most thousands of atoms. Here, we present an all-electron quantum-mechanical framework focused on very fast calculations up to the multimillion-atom regime which is achieved by scaling down the accuracy of the framework while still maintaining agreement with experimental results. By combining algorithmically optimised Hartree-Fock with divide-and-conquer, using a minimal basis set and truncating long-range interactions, our approach efficiently handles million-atom structures while remaining accessible for smaller computation clusters and saving energy due to fast run times. We demonstrate this approach on very large biological systems, including a bacteriophage in water, totalling over 150 million electrons, representing, to our knowledge, the largest Hartree-Fock calculation performed to date. Our framework allows computing spectral data for DNA and drugs and enables protein structure assessments in strong agreement with structure evaluations by AlphaFold.


## This Hartree-Fock program is focused on fast calculations for large systems.

The key priciples:
+ Nearsightedness: Based on this principle by Walter Kohn, irrelevant and long-range interactions can be ignored.
+ Integral-Optimized: The integral calculation algorithm can ignore integrals with only small contributions to the result.
+ Matrix-Based: A matrix formalism can be derived which enables an electron repulsion integral scheme which is highly parallelizable.
+ Large-Scale Systems: Sparse formalisms and memory constraints allow fast calculations for systems with multiple of hundereds of atoms.

The key features:
+ electronic structure calculations for large-scale systems with >1,000,000 atoms
+ very fast calculations for systems with a few hundred to a few thousand atoms
+ subsystem/clustering approach for linear scalability
+ visualization of electonic densities
+ UV/Vis spectra for systems containing hundreds or thousands of atoms

To run this program:
1. Read the program configurations below the variable selections and change variables according to your needs. The default values will work fine in most cases.
2. Read the section ---MAIN--- at the very end of the program and follow the instructions there.

```
Author/Contact information:
Luc Wieners
Institute of Physics, University of Kassel, Heinrich-Plett-Straße 40, 34132 Kassel, Germany
lucwieners@physik.uni-kassel.de
```
