#  Copyright© 2023 Merck Sharp & Dohme Corp. a subsidiary of Merck & Co., Inc., Rahway, NJ, USA.

#  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

import pandas as pd

# load data
meta = pd.read_csv('../../data/metadata/stool/stool_metadata.csv', index_col=0)

abx_class = pd.read_csv('../../data/metadata/antibiotic_details.csv', index_col=0)

abx = pd.read_csv('../../data/metadata/antibiotic_usage.tsv', sep='\t', index_col=0)

# clean up and get ages from babies
abx['BabyN'] = [int(i.split('Baby')[1]) for i in abx['BabyN']]
abx['cleaned_name'] = [abx_class.loc[i, 'Name for analysis'] for i in abx['Name']]
abx['route'] = [abx_class.loc[i, 'Route of administration'] for i in abx['Name']]
age_at_start = list() # get age of baby at start and end of abx
age_at_end = list()
for i, row in abx.iterrows():
    babyN = row['BabyN']
    baby_frame = meta.query('BabyN == @babyN')
    if len(baby_frame) == 0:
        age_at_start.append('???')
        age_at_end.append('???')
    else:
        dob =  pd.to_datetime(baby_frame.iloc[0]['DOB'])
        if row['Start_Date'] == 'Not Documented':
            age_at_start.append(pd.NA)
        else:
            age_at_start.append((pd.to_datetime(row['Start_Date']) - dob).days)
        if row['End_Date'] == 'Not Documented':
            age_at_end.append(pd.NA)
        else:
            age_at_end.append((pd.to_datetime(row['End_Date']) - dob).days)
abx['age_at_start'] = age_at_start
abx['age_at_end'] = age_at_end

# get data about abx usage relative to each sample
abx_rows = dict()
for baby, baby_frame in meta.groupby('BabyN'):  # for each baby
    baby_frame = baby_frame.sort_values('age_at_collection')
    baby_abx = abx.query('BabyN == @baby') # get abx baby was on
    routes_to_keep = ['oral', 'IV', 'IM']
    baby_abx = baby_abx.query("route in @routes_to_keep") # get oral/IV only TODO: separate oral and IV from topical
    never_abx = len(baby_abx) == 0  # no antibiotics so set all values to defaults
    for baby_sample, baby_row in baby_frame.iterrows():
        abx_rows[baby_sample] = dict()
        abx_rows[baby_sample]['never_abx'] = never_abx
        age_in_days = baby_row['age_at_collection']
        if never_abx:
            # abx_rows[baby_sample]['days_since_abx_start'] = age_in_days
            abx_rows[baby_sample]['days_since_abx_start'] = pd.NA
            # abx_rows[baby_sample]['days_since_abx_end'] = age_in_days
            abx_rows[baby_sample]['days_since_abx_end'] = pd.NA
            abx_rows[baby_sample]['on_abx'] = False
            abx_rows[baby_sample]['previous_abx'] = False
        else:
            # get information about most recent start
            previous_abx_start = baby_abx.query('age_at_start < @age_in_days')
            if len(previous_abx_start) == 0:
                # abx_rows[baby_sample]['days_since_abx_start'] = age_in_days
                abx_rows[baby_sample]['days_since_abx_start'] = pd.NA
                abx_rows[baby_sample]['on_abx'] = False
                abx_rows[baby_sample]['previous_abx'] = False
            else:
                abx_rows[baby_sample]['days_since_abx_start'] = age_in_days - previous_abx_start['age_at_start'].max()
                # check if currently on abx
                abx_rows[baby_sample]['on_abx'] = ((previous_abx_start['age_at_start'] <= age_in_days) & (previous_abx_start['age_at_end'] >= age_in_days)).any()
                abx_rows[baby_sample]['previous_abx'] = True
            # then do the same for abx end
            previous_abx_end = baby_abx.query('age_at_end < @age_in_days')
            if len(previous_abx_end) == 0:
                # abx_rows[baby_sample]['days_since_abx_end'] = age_in_days
                abx_rows[baby_sample]['days_since_abx_end'] = pd.NA
            else:
                abx_rows[baby_sample]['days_since_abx_end'] = age_in_days - previous_abx_end['age_at_end'].max()
per_sample_abx = pd.DataFrame(abx_rows).transpose()

per_sample_abx.to_csv('../../data/metadata/stool/stool_abx_usage.csv', index_label='SampleID')
