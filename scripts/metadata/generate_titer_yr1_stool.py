#  Copyright© 2023 Merck Sharp & Dohme Corp. a subsidiary of Merck & Co., Inc., Rahway, NJ, USA.

#  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

import pandas as pd

# read in data
meta = pd.read_csv('../../data/metadata/stool/stool_metadata.csv', index_col=0)
titer_data = pd.read_csv('../../data/vaccine_response/vaccine_response_y1.tsv', sep='\t', index_col=0)
titer_data.index = [int(i.split('Baby')[-1]) for i in titer_data.index]

# get per sample titer levels
stool_titer_data = pd.DataFrame({sample: titer_data.loc[row['BabyN']] for sample, row in meta.iterrows() if row['BabyN'] in titer_data.index}).transpose()
stool_titer_data.to_csv('../../data/metadata/stool/stool_titers_yr1.csv', index_label='SampleID')
