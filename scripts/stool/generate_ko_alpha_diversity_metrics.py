#  Copyright© 2023 Merck Sharp & Dohme Corp. a subsidiary of Merck & Co., Inc., Rahway, NJ, USA.

#  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

import pandas as pd
from skbio.diversity.alpha import shannon, simpson_e, observed_otus

# read in ko data
ko_abunds = pd.read_csv('../../data/stool/ko_abundance_table.rel.tsv', sep='\t', index_col=0)
ko_abunds.index = [i.replace("'", "_").replace('#', '_') for i in ko_abunds.index]
ko_abunds.columns = [i.split('.txt')[0] for i in ko_abunds.columns]

# filter based on abundance, without this filter we get one sample with 8K KO (compared to 5K average)
ko_abunds_gt20 = ko_abunds.loc[(ko_abunds > 0).sum(axis=1) > ko_abunds.shape[1]*.1]

# calculate diversities and make table
diversity_metrics = pd.concat((ko_abunds_gt20.apply(shannon).rename('ko_shannon'),
                               ko_abunds_gt20.apply(simpson_e).rename('ko_evenness'),
                               ko_abunds_gt20.apply(observed_otus).rename('ko_richness')), axis=1)

# write table to file
diversity_metrics.to_csv('../../data/stool/ko_alpha_diversity.csv', index_label='SampleID')
