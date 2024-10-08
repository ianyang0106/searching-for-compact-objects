from astropy.io import fits
import pandas as pd
import numpy as np
import pickle
from tqdm import tqdm

#Select sources from low resolution
path_lrs_c = 'C:/Users/ianyang/Desktop/compact_search/LAMOST data/dr9_v2.0_LRS_catalogue.fits'
path_lrs_mec = "C:/Users/ianyang/Desktop/compact_search/LAMOST data/dr9_v2.0_LRS_mec.fits"
hdu_lc = fits.open(path_lrs_c)
data_lc = hdu_lc[1].data
df_lc = pd.DataFrame(data_lc)

#Select sources with mean SNR>10
tqdm.pandas(desc="Calculating Mean SNR")
msnr=(df_lc.snru+df_lc['snrg']+df_lc['snrr']+df_lc['snri']+df_lc['snrz'])/5  #mean snr
df_lc['msnr'] = msnr
filtered_df_lc = df_lc[df_lc['msnr']>10]
print(filtered_df_lc)

#select sources with more than one uid
df_lc = df_lc[df_lc.duplicated(subset='uid', keep=False)]
df_lc = df_lc.reset_index(drop=True)
value_columns = ['obsid', 'gp_id', 'designation', 'obsdate', 'lmjd', 'mjd',
       'planid', 'spid', 'fiberid', 'ra_obs', 'dec_obs', 'snru', 'snrg',
       'snrr', 'snri', 'snrz', 'class', 'subclass', 'z', 'z_err', 'ps_id',
       'mag_ps_g', 'mag_ps_r', 'mag_ps_i', 'mag_ps_z', 'mag_ps_y',
       'gaia_source_id', 'gaia_g_mean_mag', 'fibertype', 'offsets',
       'offsets_v', 'ra', 'dec', 'fibermask', 'with_norm_flux', 'msnr']
#Select repeated sources by uid and reset index
# dfnew_lc =filtered_df_lc.groupby('uid').filter(lambda x: len(x) > 1)

dfnew_lc = filtered_df_lc.groupby('uid').filter(lambda x: x['uid'].size > 1)
#one uid corresponds to a list
new_df= dfnew_lc.groupby('uid').agg({col: lambda x: list(x) for col in value_columns}).reset_index()

# #Store as pkl
new_df.to_pickle('dr9lrsgeneral_obssnr_select.pkl')
# data1= pd.read_pickle('dr9lrsgeneral_obssnr_select.pkl')