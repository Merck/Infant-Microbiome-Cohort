#  Copyright© 2023 Merck Sharp & Dohme Corp. a subsidiary of Merck & Co., Inc., Rahway, NJ, USA.

#  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

# Script to generate vaccine response outcome data table for use in analyses
# - outlier removal
# - min-max normalisation
# - comparison to protective threshold (for DTaP/Hib antigens) and categorisation as normal or low vaccine responder
# Input: raw antibody titers: titers.tsv
# Output: vaccine response tables at year 1 and year 2: vaccine_response_y1.tsv and vaccine_response_y2.tsv

import os
import numpy as np
import pandas as pd
from scipy import stats

# set data path
data_path = '../../data/vaccine_response/' 

# read antibody titer information
titers = pd.read_csv(os.path.join(data_path, 'titers.tsv'), sep='\t', index_col=0)

# set up for output data table
all_babyNs = sorted(titers.BabyN.unique().tolist())
all_ags = titers.Antigen.unique().tolist()
dtaphib_ags = [x for x in all_ags if not x.startswith('PCV')]

# BUILD OUTPUT DATA FRAMES 

# (1) pivot long titres dataframe to take values for each antigen
outcomes_y1 = titers[titers.Category=='1y']\
                .pivot(index='BabyN',columns='Antigen',values='Value')\
                .reindex(columns=all_ags)
outcomes_y2 = titers[titers.Category=='2y']\
                .pivot(index='BabyN',columns='Antigen',values='Value')\
                .reindex(columns=all_ags)

# (2) remove outliers -- more than 3sd from mean (as used by Tom in previous analysis)
sdm = 3 # sd multiplier
# replace y1 outliers
abs_z = np.abs(stats.zscore(outcomes_y1, nan_policy='omit')) # column-wise z-values, ignoring nans
outcomes_y1.mask(abs_z>sdm, inplace=True)
# replace y2 outliers
abs_z = np.abs(stats.zscore(outcomes_y2, nan_policy='omit')) # column-wise z-values, ignoring nans
outcomes_y2.mask(abs_z>sdm, inplace=True)

# (3) min-max normalisation on each column
for ag in outcomes_y1.columns:
    outcomes_y1[ag+'_mmNorm'] = (outcomes_y1[ag] - outcomes_y1[ag].min())/(outcomes_y1[ag].max()-outcomes_y1[ag].min())
for ag in outcomes_y2.columns:
    outcomes_y2[ag+'_mmNorm'] = (outcomes_y2[ag] - outcomes_y2[ag].min())/(outcomes_y2[ag].max()-outcomes_y2[ag].min())

# (4) median normalised titres for each individual
# cross vaccine
outcomes_y1['median_mmNorm'] = outcomes_y1[[c for c in outcomes_y1.columns if c.endswith('_mmNorm')]].median(axis=1)
outcomes_y2['median_mmNorm'] = outcomes_y2[[c for c in outcomes_y2.columns if c.endswith('_mmNorm')]].median(axis=1)
# DTaP/Hib
outcomes_y1['median_mmNorm_DTAPHib'] = outcomes_y1[[c for c in outcomes_y1.columns if (c.endswith('_mmNorm') and c.startswith(tuple(dtaphib_ags)))]].median(axis=1)
outcomes_y2['median_mmNorm_DTAPHib'] = outcomes_y2[[c for c in outcomes_y2.columns if (c.endswith('_mmNorm') and c.startswith(tuple(dtaphib_ags)))]].median(axis=1)
# PCV
outcomes_y1['median_mmNorm_PCV'] = outcomes_y1[[c for c in outcomes_y1.columns if (c.endswith('_mmNorm') and c.startswith('PCV'))]].median(axis=1)
outcomes_y2['median_mmNorm_PCV'] = outcomes_y2[[c for c in outcomes_y2.columns if (c.endswith('_mmNorm') and c.startswith('PCV'))]].median(axis=1)

# (5) record whether 6 dtap/hib ags are above or below protective thresholds
protective_thresholds = {'Dip':0.1,
                         'TET':0.1,
                         'PRP (Hib)':0.15,
                         'PT':8,
                         'PRN':8,
                         'FHA':8}
for ag in dtaphib_ags:
    outcomes_y1[ag+'_protected'] = outcomes_y1[ag] > protective_thresholds[ag]
    outcomes_y2[ag+'_protected'] = outcomes_y2[ag] > protective_thresholds[ag]

# (6) record low or normal vaccine response 
#  low = 4 or more below protective threshold
#     (= 2 or fewer above protective threshold)
outcomes_y1['VR_group'] = (outcomes_y1[[c for c in outcomes_y1.columns if c.endswith('_protected')]] \
                            .sum(axis=1) <= 2) \
                            .replace({True:'LVR', False:'NVR'})
outcomes_y2['VR_group'] = (outcomes_y2[[c for c in outcomes_y1.columns if c.endswith('_protected')]] \
                            .sum(axis=1) <= 2) \
                            .replace({True:'LVR', False:'NVR'})

# save to file
outcomes_y1.to_csv(os.path.join(data_path, 'vaccine_response_y1.tsv'), sep='\t')
outcomes_y2.to_csv(os.path.join(data_path, 'vaccine_response_y2.tsv'), sep='\t')
