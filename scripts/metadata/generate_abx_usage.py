#  Copyright© 2023 Merck Sharp & Dohme Corp. a subsidiary of Merck & Co., Inc., Rahway, NJ, USA.

#  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

# script to generate data table of antibiotics usage from visit information

import os
import numpy as np
import pandas as pd
import datetime 
import dateutil 
####################################################################################################

# set data path
data_path = '../../data/metadata/' 

# read participant and visit data
participants_df = pd.read_csv(os.path.join(data_path, 'participants.tsv'), sep='\t', index_col=0)
visits_df = pd.read_csv(os.path.join(data_path, 'visits.tsv'), sep='\t', index_col=0)

####################################################################################################
# build a table of all antibiotic usage recorded at a visit
# table will be line per antbiotic instance

antibiotics_df = pd.DataFrame(columns=['BabyN','AntibioticN','Name','Reason',
									   'Start_Date','End_Date','Duration_(days)'])

# select columns from visits table that are related to antibiotics use
ab_columns = ['Antibiotics #1', 'ab#1 Reason', 'ab#1 Date Start', 'ab#1 Date End', 
			  'Antibiotics #2', 'ab#2 Reason', 'ab#2 Date Start', 'ab#2 Date End', 
			  'Antibiotics #3', 'ab#3 Reason', 'ab#3 Date Start', 'ab#3 Date End', 
			  'Antibiotics #4', 'ab#4 Reason', 'ab#4 Date Start', 'ab#4 Date End']
sdf = visits_df[visits_df['Has the infant received antibiotics since the last visit?']=='Yes'][['BabyN']+ab_columns]

for irow, row in sdf.iterrows():
	for abn in [1,2,3,4]: # each row has four antibiotic slots
		if str(row['Antibiotics #'+str(abn)])!='nan':
			# pull information from table
			res = {'BabyN':row['BabyN'],
			       'Name':row['Antibiotics #'+str(abn)].strip(),
			       'Reason':row['ab#'+str(abn)+' Reason'],
			       'Start_Date':row['ab#'+str(abn)+' Date Start'],
			       'End_Date':row['ab#'+str(abn)+' Date End']}
			# add a number for this instance of ab in this child
			if row['BabyN'] not in antibiotics_df['BabyN'].tolist():
				res['AntibioticN'] = 1
			else:
				res['AntibioticN'] = antibiotics_df['BabyN'].value_counts()[row['BabyN']] + 1
			# save the dates in a standard format
			sd = res['Start_Date']; ed = res['End_Date']
			try:
				sd = dateutil.parser.parse(sd)
				res['Start_Date'] = datetime.datetime.strftime(sd,'%Y-%m-%d')
			except:
				pass
			try:
				ed = dateutil.parser.parse(ed)
				res['End_Date'] = datetime.datetime.strftime(ed,'%Y-%m-%d')				
			except:
				pass
			# calculate duration where possible:
			sd = res['Start_Date']; ed = res['End_Date']
			try:
				sd = dateutil.parser.parse(sd)
				ed = dateutil.parser.parse(ed)
				# calculate and store the duration in days
				res['Duration_(days)'] = (ed-sd).days
			except:
				res['Duration_(days)'] = 'Unknown'
			# add to dataframe
			antibiotics_df = antibiotics_df.append(res, ignore_index=True)

# set a primary key
antibiotics_df['PrimaryKey'] = antibiotics_df['BabyN']+'_Antibiotic'+antibiotics_df['AntibioticN'].astype(str)
antibiotics_df.set_index('PrimaryKey', inplace=True)

# manual correction of some entries

# Baby 123 has a stack of 'ongoing' antibiotics and finally (#5) an end date. 
# Remove entry #s 2-5 for this child and update entry #1 with the end date
antibiotics_df.loc['Baby123_Antibiotic1']['End_Date'] = antibiotics_df.loc['Baby123_Antibiotic5']['End_Date']
antibiotics_df.loc['Baby123_Antibiotic1']['Duration_(days)'] = antibiotics_df.loc['Baby123_Antibiotic5']['Duration_(days)']
antibiotics_df.drop(['Baby123_Antibiotic2','Baby123_Antibiotic3','Baby123_Antibiotic4','Baby123_Antibiotic5'], inplace=True)

# Baby 127 has duration of -356 days -- end date is 1/4/19 when it should be 1/4/20
antibiotics_df.loc['Baby127_Antibiotic5']['End_Date'] = '2020-01-04'
# calculate and store the duration in days
sd = dateutil.parser.parse(antibiotics_df.loc['Baby127_Antibiotic5']['Start_Date'])
ed = dateutil.parser.parse(antibiotics_df.loc['Baby127_Antibiotic5']['End_Date'])
antibiotics_df.loc['Baby127_Antibiotic5']['Duration_(days)'] = (ed-sd).days

# Baby 203 has duration of -355 days -- start date is a year later than visit date so correct
antibiotics_df.loc['Baby203_Antibiotic1']['Start_Date'] = '2018-12-31'
# calculate and store the duration in days
sd = dateutil.parser.parse(antibiotics_df.loc['Baby203_Antibiotic1']['Start_Date'])
ed = dateutil.parser.parse(antibiotics_df.loc['Baby203_Antibiotic1']['End_Date'])
antibiotics_df.loc['Baby203_Antibiotic1']['Duration_(days)'] = (ed-sd).days

####################################################################################################
# add start age and end age (and DOB for calculating these)
antibiotics_df['DateOfBirth'] = [dateutil.parser.parse(participants_df.loc[babyN]['Date of Birth']) for babyN in antibiotics_df.BabyN]
antibiotics_df['AgeAtStart'] = [(dateutil.parser.parse(row.Start_Date) - row.DateOfBirth).days if row.Start_Date!='Not Documented' else np.nan for irow, row in antibiotics_df.iterrows()]
antibiotics_df['AgeAtEnd'] = [(dateutil.parser.parse(row.End_Date) - row.DateOfBirth).days if row.End_Date!='Not Documented' else np.nan for irow, row in antibiotics_df.iterrows()]
####################################################################################################

####################################################################################################
# add the route of administration, based on the antibiotic and the reason (where necessary)

# read abx details
abx_details = pd.read_csv(os.path.join(data_path, 'antibiotic_details.csv'))

# add a column for route
antibiotics_df['Route'] = np.nan

# for each abx instance, decide on route
for irow, row in antibiotics_df.iterrows():
	if row.Name not in abx_details.Antibiotic.tolist():
		print(row.Name)
	else:
		if abx_details[abx_details.Antibiotic==row.Name].shape[0] != 1:
			print('More than one entry for abx ', row.Name)
		this_abx = abx_details[abx_details.Antibiotic==row.Name].iloc[0]
		if pd.isnull(this_abx['Route of administration']):
			# this is where the recorded antibiotic is unknown or is not an antibiotic (e.g. antiviral)
			# leave these entries as NAN in route
			pass
		elif this_abx['Route of administration'] != 'see reason column':
			# this is where the recorded antibiotic didn't have multiple reason/route pairs
			antibiotics_df.loc[irow,'Route'] = this_abx['Route of administration']
		elif this_abx['Route of administration'] == 'see reason column':
			# now we need to look at the reason for the antibiotic treatment
			for suffix in ['_1', '_2', '_3']:
				# there are three reason-route pair columns, try each in turn for a match
				if row.Reason == this_abx['Reason'+suffix]:
					antibiotics_df.loc[irow,'Route'] = this_abx['Route'+suffix]
####################################################################################################

####################################################################################################
# save to file
antibiotics_df.to_csv(os.path.join(data_path, 'antibiotic_usage.tsv'), sep='\t')
####################################################################################################