#!/usr/bin/env python3
"""
This script will extract pdb files from a clustering output from the modified tool:
https://github.com/HITS-MCM/MD-IFP/blob/master/IFP_generation_examples_TRAJ.ipynb
to write the pdb_cluster.csv file.
Modified version at http...
1. Read the data from pdb_cluster.csv
2. Iterate over the data
3. Extract frames from clusters into pdbs
4. Use as:
python extract_ligand_from_clusters_02.py pdb_test.csv -r Dir_Traj1_Metad_0.3.txt -f 300
"""

import argparse
import sys
from typing import List
import pandas as pd
import MDAnalysis as mda


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
        help="Frames specified in the modified IFP_generation_examples_TRAJ.ipynb tool.",
    )
    opts = parser.parse_args(argv)
    return opts


def main(argv: List[str]):
    opts = parse_args(argv)
    data = pd.read_csv(opts.input, sep=";", comment="#")
    paths = pd.read_csv(opts.routes, sep=",", comment="#", quotechar="'")
    N = int(opts.frames)  # Convertir a int
    print(paths["path"][7])
    sorted_data = data.sort_values(by="traj")
    print(sorted_data)
    clusters = pd.unique(sorted_data["cluster"])

    i = 0
    for replica in sorted_data.replica.unique():
        for traj in sorted_data[sorted_data.replica == replica].traj.unique():
            print("PRINT", sorted_data[sorted_data.replica == replica].traj.unique())
            print("LOAD", replica, traj, paths["path"][replica])
            u = mda.Universe("{}.pdb".format(traj), "{}".format(paths["path"][replica]))
            u_length = int(len(u.trajectory))
            system_reduced = u.select_atoms("all")

            for row in sorted_data.iterrows():
                C = row[1]["cluster"]
                M = row[1]["frame"]
                for cluster in clusters:
                    if (
                        (traj == row[1]["traj"])
                        and (replica == row[1]["replica"])
                        and (cluster == row[1]["cluster"])
                    ):
                        fr_r = int(u_length - N + M)
                        print("WRITING", C, replica, M)
                        system_reduced.write(
                            "{}_{}_{}_{}.pdb".format(C, replica, traj, M),
                            frames=u.trajectory[[fr_r]],
                        )
            i += 1


if __name__ == "__main__":
    main(sys.argv[1:])

