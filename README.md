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

## References

1. Hrebík, D. et al. **Structure and genome ejection mechanism of Staphylococcus aureus phage P68.** Sci. Adv. 5, eaaw7414 (2019).

1. Jumper, J. et al. **Highly accurate protein structure prediction with AlphaFold.** Nature 596, 583–589 (2021).

1. Thota, N. A., Li, X. H., Bingman, C. & Sundaralingam, M. **High-resolution refinement of the hexagonal A-DNA octamer d (GTGTACAC) at 1.4 Å.** Biol. Crystallogr. 49, 282–291 (1993).

1. Masliah, G., René, B., Zargarian, L., Fermandjian, S. & Mauffret, O. **Identification of intrinsic dynamics in a DNA sequence preferentially cleaved by topoisomerase II enzyme.** J. Mol. Biol. 381, 692–706 (2008).

1. Schäfer, M., Sheldrick, G. M., Bahner, I. & Lackner, H. **Crystal structures of actinomycin D and actinomycin Z3.** Angew. Chem. Int. Ed. 37, 2381–2384 (1998).

1. Hou, M. H., Robinson, H., Gao, Y. G. & Wang, A. H. J. **Crystal structure of actinomycin D bound to the CTG triplet repeat sequences linked to neurological diseases.** Nucleic Acids Res. 30, 4910–4917 (2002).

1. Van Der Spoel, D. et al. **GROMACS: fast, flexible, and free.** J. Comput. Chem. 26, 1701–1718 (2005).

1. Case, D. A. et al. **The Amber biomolecular simulation programs.** J. Comput. Chem. 26, 1668–1688 (2005).

1. Vanommeslaeghe, K. et al. **CHARMM general force field: a force field for drug-like molecules compatible with the CHARMM all-atom additive biological force fields.** J. Comput. Chem. 31, 671–690 (2010).

1. Senn, H. M. & Thiel, W. **QM/MM methods for biomolecular systems.** Angew. Chem. Int. Ed. 48, 1198–1229 (2009).

1. Dauber-Osguthorpe, P. & Hagler, A. T. **Biomolecular force fields: where have we been, where are we now, where do we need to go and how do we get there?** J. Comput. Aided Mol. Des. 33, 133–203 (2019).

1. Soler, J. M. et al. **The SIESTA method for ab initio order-N materials simulation.** J. Phys.: Condens. Matter 14, 2745 (2002).

1. Neese, F. **The ORCA program system. Wiley Interdiscip.** Rev. Comput. Mol. Sci. 2, 73–78 (2012).

1. Schade, R. et al. **Towards electronic structure-based ab-initio molecular dynamics simulations with hundreds of millions of atoms.** Parallel Comput. 111, 102920 (2022).

1. Stocks, R. et al. **Breaking the million-electron and 1 EFLOP/s barriers: biomolecular-Scale ab initio molecular dynamics using MP2 potentials.** In SC24: International Conference for High Performance Computing, Networking, Storage and Analysis 1–12 (IEEE, 2024).

1. Andermatt, S., Cha, J., Schiffmann, F. & VandeVondele, J. **Combining linear-scaling DFT with subsystem DFT in Born–Oppenheimer and Ehrenfest molecular dynamics simulations: From molecules to a virus in solution.** J. Chem. Theory Comput. 12, 3214–3227 (2016).

1. Mohr, S. et al. **Accurate and efficient linear scaling DFT calculations with universal applicability.** Phys. Chem. Chem. Phys. 17, 31360–31370 (2015).

1. de Luzuriaga, I. O. et al. **Semi-empirical and linear-scaling DFT methods to characterize duplex DNA and G-quadruplexes in the presence of interacting small molecules.** Phys. Chem. Chem. Phys. 24, 11510–11519 (2022).

1. Gundelach, L., Fox, T., Tautermann, C. S. & Skylaris, C. K. **Protein-ligand free energies of binding from full-protein DFT calculations: convergence and choice of exchange–correlation functional.** Phys. Chem. Chem. Phys. 23, 9381–9393 (2021).

1. He, X. & Merz, K. M. Jr **Divide and conquer Hartree–Fock calculations on proteins.** J. Chem. theory Comput. 6, 405–411 (2010).

1. Guidon, M., Hutter, J. & VandeVondele, J. **Robust periodic Hartree–Fock exchange for large-scale simulations using Gaussian basis sets.** J. Chem. theory Comput. 5, 3010–3021 (2009).

1. Cole, D. J. & Hine, N. D. **Applications of large-scale density functional theory in biology.** J. Phys. Condens. Matter 28, 393001 (2016).
   
1. Fedorov, D. G. & Kitaura, K. **Extending the power of quantum chemistry to large systems with the fragment molecular orbital method.** J. Phys. Chem. A 111, 6904–6914 (2007).

1. Shimojo, F., Kalia, R. K., Nakano, A. & Vashishta, P. **Divide-and-conquer density functional theory on hierarchical real-space grids: parallel implementation and applications.** Phys. Rev. B 77, 085103 (2008).

1. Schwegler, E. & Challacombe, M. **Linear scaling computation of the Hartree–Fock exchange matrix.** J. Chem. Phys. 105, 2726–2734 (1996).

1. Ochsenfeld, C., White, C. A. & Head-Gordon, M. **Linear and sublinear scaling formation of Hartree–Fock-type exchange matrices.** J. Chem. Phys. 109, 1663–1669 (1998).

1. Vashishta, P., Kalia, R. K. & Nakano, A. **Multimillion atom simulations of dynamics of oxidation of an aluminum nanoparticle and nanoindentation on ceramics.** J. Phys. Chem. B 110, 3727–3733 (2006).

1. Ordejón, P., Artacho, E. & Soler, J. M. **Self-consistent order-N density-functional calculations for very large systems.** Phys. Rev. B 53, R10441 (1996).

1. Fonseca Guerra, C., Snijders, J. G., Te Velde, G. T. & Baerends, E. J. **Towards an order-N DFT method.** Theor. Chem. Acc. 99, 391–403 (1998).

1. Goletto, L., Kjønstad, E. F., Folkestad, S. D., Høyvik, I. M. & Koch, H. **Linear-scaling implementation of multilevel Hartree–Fock theory.** J. Chem. Theory Comput. 17, 7416–7427 (2021).

1. Nakata, A. et al. **Large scale and linear scaling DFT with the CONQUEST code.** J. Chem. Phys. 152, 164112 (2020).

1. Bowler, D. R. & Miyazaki, T. **Calculations for millions of atoms with density functional theory: linear scaling shows its potential.** J. Phys. Condens. Matter 22, 074207 (2010).

1. Varnay, I., Truffault, V., Kessler, H. & Coles, M., **Solution structure of Ph1500: a homohexameric protein centered on a 12-bladed beta-propeller** https://doi.org/10.2210/pdb2M3X/pdb (2013).

1. Meng, E. C. et al. **UCSF ChimeraX: tools for structure building and analysis.** Protein Sci. 32, e4792 (2023).

1. Strout, D. L. & Scuseria, G. E. **A quantitative study of the scaling properties of the Hartree–Fock method.** J. Chem. Phys. 102, 8448–8452 (1995).

1. Royant, A. et al. **X-ray structure of sensory rhodopsin II at 2.1-Å resolution.** Proc. Natl. Acad. Sci. 98, 10131–10136 (2001).

1. Whitten, J. L. **Gaussian lobe function expansions of Hartree–Fock solutions for the first-row atoms and ethylene.** J. Chem. Phys. 44, 359–364 (1966).

1. Tan, J. et al. **Structural basis of the bacterial flagellar motor rotational switching.** Cell Res. 34, 788–801 (2024).

1. Guerra, P. et al. **Symmetry disruption commits vault particles to disassembly.** Sci. Adv. 8, eabj7795 (2022).

1. Müller, C., Sharma, M. & Sierka, M. **Real-time time-dependent density functional theory using density fitting and the continuous fast multipole method.** J. Comput. Chem. 41, 2573–2582 (2020).

1. Liu, Y. et al. **Ultra-fast computation of excited-states spectra for large systems: ultraviolet and fluorescence spectra of proteins.** Interdiscip. Sci. Comput. Life Sci. 13, 140–146 (2021).

1. Miao, L. et al. **The anti-quorum sensing activity and bioactive substance of a marine derived Streptomyces.** Biotechnol. Biotechnol. Equip. 31, 1007–1015 (2017).

1. Ozdemir, A., Sarioglu, O. F. & Tekinay, T. **Spectroscopic evaluation of DNA–borate interactions.** Biol. trace Elem. Res. 168, 508–515 (2015).

1. Toader, A. M., Dascalu, I. & Enache, M. **Effect of SDS Micelles on Actinomycin D-DNA Complexes.** Acta Chim. Slov. 69, 331–335 (2022).

1. David, A., Islam, S., Tankhilevich, E. & Sternberg, M. J. **The AlphaFold database of protein structures: a biologist’s guide.** J. Mol. Biol. 434, 167336 (2022).

1. Dill, K. A., Ozkan, S. B., Shell, M. S. & Weikl, T. R. **The protein folding problem.** Annu. Rev. Biophys. 37, 289–316 (2008).

1. Berman, H. M. et al. **The protein data bank.** Nucleic Acids Res. 28, 235–242 (2000).

1. Ruff, K. M. & Pappu, R. V. **AlphaFold and implications for intrinsically disordered proteins.** J. Mol. Biol. 433, 167208 (2021).

1. Koch, D. et al. **The analysis of electron densities: from basics to emergent applications.** Chem. Rev. 124, 12661–12737 (2024).


 

Felder, C. E., Prilusky, J., Silman, I. & Sussman, J. L. A server and database for dipole moments of proteins. Nucleic acids Res. 35, 512–521 (2007).


 

Kulik, M. & Dominiak, P. M. Electron density is not spherical: the many applications of the transferable aspherical atom model. Comput. Struct. Biotechnol. J. 20, 6237–6243 (2022).


Rackers, J. A., Tecot, L., Geiger, M. & Smidt, T. E. A recipe for cracking the quantum scaling limit with machine learned electron densities. Mach. Learn. Sci. Technol. 4, 015027 (2023).


Liu, X., Patel, A. & Chow, E. A new scalable parallel algorithm for Fock matrix construction. In Proc. IEEE 28th International Parallel and Distributed Processing Symposium 902–914 (IEEE, 2014).

Umeda, H. et al. Parallel Fock matrix construction with distributed shared memory model for the FMO-MO method. J. Comput. Chem. 31, 2381–2388 (2010).


 

Chow, E., Liu, X., Smelyanskiy, M. & Hammond, J. R. Parallel scalability of Hartree–Fock calculations. J. Chem. Phys. 142, 104103 (2015).

Petke, J. D., Whitten, J. L. & Douglas, A. W. Gaussian lobe function expansions of Hartree–Fock solutions for the second-row atoms. J. Chem. Phys. 51, 256–262 (1969).


 

Helgaker, T. & Taylor, P. R. Gaussian basis sets and molecular integrals. Modern Electronic Structure Theory: Part II 725–856 (World Scientific, 1995).

Gill, P. M. Molecular integrals over gaussian basis functions. In Advances in Quantum Chemistry Vol. 25, 141–205 (Academic Press, 1994).

Dupuis, M., Rys, J. & King, H. F. Evaluation of molecular integrals over Gaussian basis functions. J. Chem. Phys. 65, 111–116 (1976).



Pople, J. A. & Hehre, W. J. Computation of electron repulsion integrals involving contracted Gaussian basis functions. J. Comput. Phys. 27, 161–168 (1978).


 

Yasuda, K. Two-electron integral evaluation on the graphics processor unit. J. Comput. Chem. 29, 334–342 (2008).


 

Pritchard, B. P., Altarawy, D., Didier, B., Gibson, T. D. & Windus, T. L. New basis set exchange: an open, up-to-date resource for the molecular sciences community. J. Chem. Inf. Model. 59, 4814–4820 (2019).


 

Virtanen, P. et al. SciPy 1.0: fundamental algorithms for scientific computing in Python. Nat. methods 17, 261–272 (2020).


 

Abramowitz, M. & Stegun, I. A. (eds) Handbook of Mathematical Functions with Formulas, Graphs, and Mathematical Tables Vol. 55 (US Government Printing Office, 1968).

Neese, F., Wennmohs, F., Becker, U. & Riplinger, C. The ORCA quantum chemistry program package. J. Chem. Phys. 152, 224108 (2020).

Neese, F. Software update: the ORCA program system, version 4.0. Wiley Interdiscip. Rev. Comput. Mol. Sci. 8, e1327 (2018).

 

Neese, F. Software update: the ORCA program system—Version 5.0. Wiley Interdiscip. Rev. Comput. Mol. Sci. 12, e1606 (2022).


 

Neese, F. The SHARK integral generation and digestion system. J. Comput. Chem. 44, 381–396 (2023).

r
 

Neese, F. Approximate second-order SCF convergence for spin unrestricted wavefunctions. Chem. Phys. Lett. 325, 93–98 (2000).


 

Humphrey, W., Dalke, A. & Schulten, K. VMD: visual molecular dynamics. J. Mol. Graph. 14, 33–38 (1996).



Wu, X., Xie, X. & Troisi, A. Calibration of several first excited state properties for organic molecules through systematic comparison of TDDFT with experimental spectra. J. Mater. Chem. C. 12, 18886–18892 (2024).


 

Jacquemin, D., Perpete, E. A., Scuseria, G. E., Ciofini, I. & Adamo, C. TD-DFT performance for the visible absorption spectra of organic dyes: conventional versus long-range hybrids. J. Chem. theory Comput. 4, 123–135 (2008).


 

Savitzky, A. & Golay, M. J. Smoothing and differentiation of data by simplified least squares procedures. Anal. Chem. 36, 1627–1639 (1964).


 

Pettersen, E. F. et al. UCSF Chimera—a visualization system for exploratory research and analysis. J. Comput. Chem. 25, 1605–1612 (2004).


 

Van Rossum, G. & Drake Jr F. L. Python Tutorial Vol. 620 (Centrum voor Wiskunde en Informatica, 1995).

Lam, S. K., Pitrou, A. & Seibert, S. Numba: A llvm-based python jit compiler. In Proc. Second Workshop on the LLVM Compiler Infrastructure in HPC 1–6 (ACM, 2015).

Harris et al. Array programming with NumPy. Nature 585, 357–362 (2020).


 

Paszke, A. et al. Pytorch: An imperativestyle, high-performance deep learning library. Advances in Neural Information Processing Systems 32 (NeurIPS, 2019).

Hunter, J. D. Matplotlib: A 2D graphics environment. Comput. Sci. Eng. 9, 90–95 (2007).



Royant, A. et al. Sensory rhodopsin II https://doi.org/10.2210/pdb1H68/pdb (2001).

Dominik, H., Karel, S., Fuzik, T. & Plevka, P. Structure of native bacteriophage P68 https://doi.org/10.2210/pdb6Q3G/pdb (2018).

Schafer, M., Sheldrick, G. M., Bahner, I. & Lackner, H. Crystal structure of Actinomycin D https://doi.org/10.2210/pdb1A7Y/pdb (1998).

Thota, N., Li, X. H., Bingman, C. A. & Sundaralingam, M. High resolution refinement of the hexagonal A-DNA octamer D(GTGTACAC) at 1.4 Angstroms resolution https://doi.org/10.2210/pdb1D79/pdb (1992).

Masliah, G. & Mauffret, O. NMR Structure of a 21 bp DNA duplex preferentially cleaved by Human Topoisomerase II https://doi.org/10.2210/pdb2JYK/pdb (2007).

Hou, M.-H., Robinson, H., Gao, Y.-G. & Wang, A. H.-J. Actinomycin D binding to ATGCTGCAT https://doi.org/10.2210/pdb1MNV/pdb (2002).

Tan, J. X., Zhang, L., Zhou, Y. & Zhu, Y. Q. Cryo-EM structure of the membrane-anchored part of the flagellar motor-hook complex in the CW state https://doi.org/10.2210/pdb8WL2/pdb (2023).

Guerra, P. et al. Vault structure in primmed conformation https://doi.org/10.2210/pdb7PKR/pdb (2021).

Pettersen, E. F. et al. UCSF ChimeraX: structure visualization for researchers, educators, and developers. Protein Sci. 30, 70–82 (2021).

Goddard, T. D. et al. UCSF ChimeraX: meeting modern challenges in visualization and analysis. Protein Sci. 27, 14–25 (2018).


 

Sehnal, D. et al. Mol* Viewer: modern web app for 3D visualization and analysis of large biomolecular structures. Nucleic Acids Res. 49, 431–437 (2021).


 

Pugliese, L., Coda, A., Malcovati, M. & Bolognesi, M. Three-dimensional structure of the tetragonal crystal form of egg-white avidin in its functional complex with biotin at 2.7 Å resolution. J. Mol. Biol. 231, 698–710 (1993).


 

Pugliese, L., Coda, A., Malcovati, M. & Bolognesi, M. Three-dimensional structure of the tetragonal crystal form of egg-white avidin in its functional complex with biotin at 2.7 Angstroms resolution https://doi.org/10.2210/pdb1AVD/pdb (1993).

Wilson, K. P. et al. Comparative X-ray structures of the major binding protein for the immunosuppressant FK506 (tacrolimus) in unliganded form and in complex with FK506 and rapamycin. Biol. Crystallogr. 51, 511–521 (1995).


 

Wilson, K. P., Sintchak, M. D., Thomson, J. A. & Navia, M. A. Atomic structure of FKBP12-FK506, an immunophilin immunosuppressant complex https://doi.org/10.2210/pdb1FKJ/pdb (1995).

General, I. J., Dragomirova, R. & Meirovitch, H. Absolute free energy of binding of avidin/biotin, revisited. J. Phys. Chem. B 116, 6628–6636 (2012).


 

Rivera, A. & Heitman, J. Natural product ligands of FKBP12: immunosuppressive antifungal agents FK506, rapamycin, and beyond. PLoS Pathog. 19, e1011056 (2023).


  
