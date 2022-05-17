# Understanding the differences of Danusertib’s Residence Time in Aurora Kinases A/B: Dissociation Paths and Key Residues Identified Using Conventional and Enhanced Molecular Dynamics Simulations.

## Initial structures

In this repository are available the initial structures of [Aurora A](Aurora_A_Danusertib.pdb) and [Aurora B](Aurora_B_Danusertib.pdb) in complex with Danusertib ligand in PDB format. 

## Instructions and scripts to extract cluster structures from WT-MetaD trajectories. 



1. The fingerprints must be previously calculated using the [PL IFP Traj tool](https://github.com/HITS-MCM/MD-IFP/blob/master/IFP_generation_examples_TRAJ.ipynb) script.  [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3981155.svg)](https://doi.org/10.5281/zenodo.3981155).

a ``routes.csv`` file should be prepared with the output paths of the processed trajectories as the example [routes.csv](routes.csv).

**Note:** To obtain the paths, use the [PL IFP Traj tool](https://github.com/HITS-MCM/MD-IFP/blob/master/IFP_generation_examples_TRAJ.ipynb) script. In the cell where the paths are read, the "trajectory" number and the path will be printed. Note that this is the order of the replicas to be used as it depends on the order in which the files are read in the analysis. Not always the "trajectory" 1 will correspond to the WT-MetaD replica1. 

Save the information in the [routes.csv](routes.csv) file with the following structure:

```
trajectory,path
0,'/path_to_output/Traj4_0.3/rep01/ramd_trj_fixed.xtc'
1,'/path_to_output/Traj4_0.3/rep010/ramd_trj_fixed.xtc'
2,'/path_to_output/Traj4_0.3/rep011/ramd_trj_fixed.xtc'
3,'/path_to_output/Traj4_0.3/rep012/ramd_trj_fixed.xtc'
...
```

2. The clusters will be obtained using the [PL IFP Analysis tool](https://github.com/HITS-MCM/MD-IFP/blob/master/IFP_generation_examples_Analysis.ipynb), however, the [PL IFP Analysis tool](https://github.com/HITS-MCM/MD-IFP/blob/master/IFP_generation_examples_Analysis.ipynb) script should be modified, and a cell should be added at the end with the following code: 

```
ifp_dataframe = df_ext[["time", "label", "Traj", "Repl"]]
ifp_dataframe.rename(columns={"time": "frame", "label": "cluster", "Traj": "traj", "Repl": "replica"}, inplace=True,)
ifp_dataframe.to_csv("IFP_data.csv")
```

These lines will write the [IFP_data.csv](IFP_data.csv) file with the following information:

```
,frame,cluster,traj,replica
0,0,2,15,Traj4_0.3
1,3,2,15,Traj4_0.3
...
```

Then the [extract_frames.py](extract_frames.py) script should be used to extract the structures in PDB files using [MDAnalysis](https://github.com/MDAnalysis/mdanalysis).

Use it as: 
``python extract_frames.py IPF_data.csv -r routes.csv -f 300``

The input file is the IFP_data.csv. For the -r or --routes option is passed the [routes.csv](routes.csv) file and the -f or --frames option is passed the number of frames with which the fingerprints analysis was performed.

end

