#!/usr/bin/env python3
"""
1. Read the data from pdb_cluster.csv
2. Iterate over the data
3. Extract frames from clusters into pdbs
4. Use as:
python extract_ligand_from_clusters_02.py pdb_test.csv -r Dir_Traj1_Metad_0.3.txt -f 300
"""

import argparse
import csv
import sys

from typing import List, Tuple
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

import pandas as pd
import warnings
from pathlib import Path

from numpy import arange

import numpy as np
import MDAnalysis as mda


def main(argv: List[str]):
    opts = parse_args(argv)
    data = pd.read_csv(opts.input, sep=";", comment="#")
    paths = pd.read_csv(opts.routes, sep=",", comment="#", quotechar="'")
    N = int(opts.frames) #Convertir a int
    print(paths["path"][7])
    # degree = int(opts.degree)
    sorted_data = data.sort_values(by="traj")
    print(sorted_data)
    trajs = pd.unique(sorted_data["traj"])
    replicas = pd.unique(sorted_data["replica"])
    clusters = pd.unique(sorted_data["cluster"])

    i = 0
    for replica in sorted_data.replica.unique():
        for traj in sorted_data[sorted_data.replica == replica].traj.unique():
            print("PRINT",sorted_data[sorted_data.replica == replica].traj.unique())
            print("LOAD",replica,traj,paths["path"][replica])
            u = mda.Universe("{}.pdb".format(traj),"{}".format(paths["path"][replica]))
            u_length = int(len(u.trajectory))
            #M = sorted_data["frame"][j]
            #print("MMMM",M)
            #C = (sorted_data.cluster)
            #C = pd.unique(sorted_data["cluster"])
            system_reduced = u.select_atoms("all")
            #system_reduced.write("{}_{}_{}.pdb".format(C,j,M),frames=u.trajectory[[M]])
            
            for row in sorted_data.iterrows():
                C = row[1]["cluster"]
                M = row[1]["frame"]
                for cluster in clusters:
                    if (
                        (traj == row[1]["traj"])
                        and (replica == row[1]["replica"])
                        and (cluster == row[1]["cluster"])
                    ):
                        fr_r=int(u_length-N+M)
                        print("WRITING",C,replica,M)
                        system_reduced.write("{}_{}_{}_{}.pdb".format(C,replica,traj,M),frames=u.trajectory[[fr_r]])
                    
                #system_reduced.write("{}_{}_{}_{}.pdb".format(C,j,k,M),frames=u.trajectory[[M]])
    #                #for ts in u.trajectory[0:-300:1]:
    #                #    print("FRAME",ts.frame)
            i += 1



def read_md(reference, traj, replica, frame):
    for i in range(1, 5):
        if traj == str("Traj{}_0.6".format(i)):
            reference = str("{}".format(traj))


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "input",
        help="Input File. Specify the input file to read the data.",
    )
    parser.add_argument(
        "-r",
        dest="routes",
        required=True,
        help="File with the true paths of replicas.",
    )
    parser.add_argument(
        "-f",
        dest="frames",
        required=True,
        help="Frames loaded, for instance, if were loaded the last 300 frames, -f = 300",
    )
    opts = parser.parse_args(argv)
    return opts


if __name__ == "__main__":
    main(sys.argv[1:])

