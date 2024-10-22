import ROOT as rt
import numpy as np

# Load the ROOT file
root_filename = "/user/tridevme/SPEBT/mcsim/macro/SPEBT.Singles_merged.root"
root_file = rt.TFile(root_filename)

# Load the tree from the ROOT file
tree_name = "tree"
tree = root_file.Get(tree_name)

# Check if the tree was successfully loaded
if not tree:
    print(f"Error: Tree '{tree_name}' not found in the file.")
    root_file.Close()
    exit()

# Prepare arrays to hold the system matrix data
source_pos_x = []
source_pos_y = []
source_pos_z = []
detector_ids = []

# Iterate over the entries in the tree and collect data
n_entries = tree.GetEntries()
for entry in range(n_entries):
    tree.GetEntry(entry)

    source_pos_x.append(tree.sourcePosX)
    source_pos_y.append(tree.sourcePosY)
    source_pos_z.append(tree.sourcePosZ)
    
    # Combine detector info: use IDs like rsectorID, moduleID, submoduleID, crystalID, and layerID
    detector_ids.append((tree.rsectorID, tree.moduleID, tree.submoduleID, tree.crystalID, tree.layerID))

# Convert lists to NumPy arrays
source_pos_x = np.array(source_pos_x)
source_pos_y = np.array(source_pos_y)
source_pos_z = np.array(source_pos_z)
detector_ids = np.array(detector_ids)

# You can now use source positions and detector IDs to build the system matrix
# Example: system matrix as a 2D array (detectors by sources)
# For simplicity, we'll concatenate the source positions into a single array
sources = np.vstack((source_pos_x, source_pos_y, source_pos_z)).T

# Create the system matrix (number of detectors x number of sources)
system_matrix = np.zeros((detector_ids.shape[0], sources.shape[0]))

# Fill the system matrix with dummy values (you can use a real metric here)
for i in range(detector_ids.shape[0]):
    # Use some metric to fill in the system matrix
    system_matrix[i] = np.linalg.norm(sources - sources[i], axis=1)  # Example using Euclidean distance

print("System matrix generated.")
root_file.Close()
