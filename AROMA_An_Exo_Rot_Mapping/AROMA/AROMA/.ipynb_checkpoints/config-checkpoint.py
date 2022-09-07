# config.py

from pathlib import Path  # pathlib is seriously awesome!

data_dir = Path('/Users/fuda/Documents/GitHub/aroma/AROMA_An_Exo_Rot_Mapping/data/')
print('data_dir : '+data_dir)

data_path = Path('/Users/fuda/Documents/GitHub/aroma/AROMA_An_Exo_Rot_Mapping/data/processed/luhman_16ab_sector36-37.txt')  # use feather files if possible!!!
print('data_path : '+data_path)

plot_dir = Path('/Users/fuda/Documents/GitHub/aroma/AROMA_An_Exo_Rot_Mapping/plots/')
print('plot_dir : '+plot_dir)

fitting_dir =  Path('/Users/fuda/Documents/GitHub/aroma/AROMA_An_Exo_Rot_Mapping/notebooks/periodSineFit_metadata/')
print('fit_dir : '+fitting_dir)

