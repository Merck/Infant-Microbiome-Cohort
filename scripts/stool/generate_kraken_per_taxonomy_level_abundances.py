#  Copyright© 2023 Merck Sharp & Dohme Corp. a subsidiary of Merck & Co., Inc., Rahway, NJ, USA.

#  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

import pandas as pd

def summarize_to_level(abunds, level='g__'):
    """Summarize a Kraken data table to a single level of taxonomy based on taxa names"""
    abunds_level = abunds.loc[[i.split('|')[-1].startswith(level) for i in abunds.index]]
    return abunds_level

kraken_abunds = pd.read_csv('../../data/stool/kraken_abundance_table.tsv', sep='\t', index_col=0)
kraken_abunds.index = [i.replace("'", "_").replace('#', '_') for i in kraken_abunds.index]
kraken_abunds.columns = [i.split('.txt')[0] for i in kraken_abunds.columns]
kraken_abunds = kraken_abunds.loc[[i for i in kraken_abunds.index if i.startswith('d__Bacteria')]]

levels = [('d__', 'domain'), ('p__', 'phylum'), ('c__', 'class'), ('o__', 'order'), ('f__', 'family'), ('g__', 'genus'), ('s__', 'species')]
for level, taxa_level in levels:
    abunds_level = summarize_to_level(kraken_abunds, level=level)
    abunds_level.to_csv('../../data/stool/kraken_taxa_level_abunds/kraken_%s_abunds.tsv' % taxa_level, sep='\t')
