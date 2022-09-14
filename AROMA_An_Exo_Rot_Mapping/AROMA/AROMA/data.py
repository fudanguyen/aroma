# data.py
# Clean and write out light curve data

import pandas as pd
import numpy as np

## SECTOR 36 Light Curve
lc36_path = "~/Documents/GitHub/aroma/AROMA_An_Exo_Rot_Mapping/data/raw/luhman16_extended_mission/hlsp_pathos_tess_lightcurve_tic-0936441397-s036_tess_v1_llc.txt"

## SECTOR 37 Light Curve
lc37_path = "~/Documents/GitHub/aroma/AROMA_An_Exo_Rot_Mapping/data/raw/luhman16_extended_mission/hlsp_pathos_tess_lightcurve_tic-0936441397-s037_tess_v1_llc.txt"

headerstring = "TIME TIMECORR PSF_FLUX_RAW PSF_FLUX_COR AP1_FLUX_RAW AP1_FLUX_COR AP2_FLUX_RAW AP2_FLUX_COR AP3_FLUX_RAW AP3_FLUX_COR AP4_FLUX_RAW AP4_FLUX_COR SKY_LOCAL X_POSITION Y_POSITION DQUALITY"
headers = headerstring.split()

lc36_data_raw = pd.read_csv(lc36_path, names=headers, skiprows=26, sep='\s+')
lc37_data_raw = pd.read_csv(lc37_path, names=headers, skiprows=26, sep='\s+')

# Light curve cleaning
sky36_threshold = lc36_data_raw.SKY_LOCAL.mean() + 4*lc36_data_raw.SKY_LOCAL.std()
sky36_noise = 250 #(e s^-1)
lc36_data = lc36_data_raw.query("DQUALITY == 0 & PSF_FLUX_COR>%f & PSF_FLUX_COR<=%f"%(sky36_noise, sky36_threshold))


# sky37_threshold = lc37_data_raw.SKY_LOCAL.mean() + 4*lc37_data_raw.SKY_LOCAL.std()
sky37_noise = 200 #(e s^-1)
lc37_data = lc37_data_raw.query("DQUALITY == 0 & PSF_FLUX_COR>%f & PSF_FLUX_COR<=%f"%(sky36_noise, sky36_threshold))
# use sky threshold of sector 36

outpath = "~/Documents/GitHub/aroma/AROMA_An_Exo_Rot_Mapping/data/processed/"
lc_out_path = "luhman_16ab_sector36-37.txt"

lc36_data['PSF_MEAN'] = lc36_data.PSF_FLUX_COR.mean()
lc37_data['PSF_MEAN'] = lc37_data.PSF_FLUX_COR.mean()
lc36_data['AP1_MEAN'] = lc36_data.AP1_FLUX_COR.mean()
lc37_data['AP1_MEAN'] = lc37_data.AP1_FLUX_COR.mean()
frames = [lc36_data[['TIME', 'PSF_FLUX_RAW', 'PSF_MEAN', 'PSF_FLUX_COR', 'AP1_FLUX_COR', 'AP1_MEAN', 'SKY_LOCAL', 'X_POSITION', 'Y_POSITION']],
          lc37_data[['TIME', 'PSF_FLUX_RAW', 'PSF_MEAN','PSF_FLUX_COR', 'AP1_FLUX_COR', 'AP1_MEAN', 'SKY_LOCAL', 'X_POSITION', 'Y_POSITION']]]
lc3637 = pd.concat(frames)
lc3637.to_csv(outpath+lc_out_path, sep='\t', index=False)