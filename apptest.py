import streamlit as st
import luna
luna.version

from luna.mol.entry import MolEntry, MolFileEntry, ChainEntry

csv1 = st.file_uploader("Upload your Interaction Matrix of 1st Complex", type="txt")
input_file = "./inputs/MolEntries.txt"
entries = list(MolFileEntry.from_file(input_file, pdb_id="D4", mol_file="./inputs/ligands.mol2", mol_obj_type="openbabel"))

for e in entries:
    print(e)
print()

entries[0].mol_obj.as_rdkit()

opts = {}

opts['entries'] = entries  # The list of entries to calculate 
opts['working_path'] = "./outputs/luna_results"  # Where project results will be saved
opts['pdb_path'] = "./inputs"  # Path containing local PDB files or to where the PDB files will be downloaded. PDB filenames must match that defined for the entries.

opts['overwrite_path'] = False  # Allows script to overwrite directory - can remove files from previous project.

opts['add_h'] = True  # Define if you need to add Hydrogens or not.
opts['ph'] = 7.4  # Controls the pH and how the hydrogens are going to be added - default 7.4. It doesn't modify the protonation of molecular files defined by a MolEntry object.

# Whether or not to fix atomic charges, valence, and bond types for small molecules and residues at PDB files. 
# Only molecules at PDB files are validated because they don't contain charge, valence, and bond types. That causes molecules to be sometimes incorrectly perceived.
#
# This procedure is only applied for molecules at PDB files. Therefore, molecules from external files (MolEntry objects) won't be modified.
#
opts['amend_mol'] = True

#opts['mol_obj_type'] = 'rdkit'  # What type of mol object, options are 'rdkit' and 'openbabel' - default rdkit
opts['calc_ifp'] = False  # Whether or not to calculate interaction fingerprints

# Define how many processors to use. 
# If you set it to -1, LUNA will use all available CPUs -1. 
# If you set it to None, LUNA will be run serially.
opts['nproc'] = -1

opts['binding_mode_filter'] = None  # Provide a BindingModeFilter object that specifies how to filter binding modes.

opts['logging_enabled'] = True  # Enable logger
opts['verbosity'] = 2  # How verbose is the logger

from luna.interaction.config import DefaultInteractionConfig

inter_config = DefaultInteractionConfig()
inter_config["max_da_dist_hb_inter"] = 4.0
inter_config['inter_conf'] = inter_config

from luna.interaction.filter import InteractionFilter

pli_filter = InteractionFilter.new_pli_filter(ignore_self_inter = False) # protein-ligand interactions, including intra-molecular interactions
ppi_filter = InteractionFilter.new_ppi_filter() # protein-protein interactions
pni_filter = InteractionFilter.new_pni_filter() # protein-nucleotide interactions

from luna.interaction.calc import InteractionCalculator

custom_filter = InteractionFilter.new_pli_filter() # protein-ligand interactions
inter_calc = InteractionCalculator(inter_filter=custom_filter, add_proximal=False)
opts['inter_calc'] = inter_calc

proj_obj = luna.projects.LocalProject(**opts)
proj_obj.run()

entry_result = proj_obj.get_entry_results(entries[0])

from luna.analysis.residues import generate_residue_matrix
residue_matrix = generate_residue_matrix(proj_obj.interactions_mngrs, by_interaction=False)
residue_matrix

residue_matrix = generate_residue_matrix(proj_obj.interactions_mngrs, by_interaction=True)
residue_matrix.to_csv('test1.csv')
residue_matrix