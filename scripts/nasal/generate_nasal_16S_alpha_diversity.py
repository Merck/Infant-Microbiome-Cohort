#  Copyright© 2023 Merck Sharp & Dohme Corp. a subsidiary of Merck & Co., Inc., Rahway, NJ, USA.

#  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

import pandas as pd
from skbio.diversity.alpha import shannon, simpson_e, observed_otus

# Script to generate alpha diversity metrics of nasal 16S samples

counts = pd.read_csv('../../data/nasal/otu_table.gt10_rar10K.tsv', sep='\t', index_col=0).transpose()

alpha_div = pd.concat([counts.apply(shannon).rename('shannon_div'),
                       counts.apply(simpson_e).rename('simpson_e_div'),
                       counts.apply(observed_otus).rename('n_otus_div')], axis=1)

alpha_div.to_csv('../../data/nasal/otu_alpha_diversity.csv', index_label='SampleID')
