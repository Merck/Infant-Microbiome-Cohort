#  Copyright© 2023 Merck Sharp & Dohme Corp. a subsidiary of Merck & Co., Inc., Rahway, NJ, USA.

#  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

import pandas as pd
from skbio.diversity.alpha import shannon, simpson_e, observed_otus

# read in genus level data
kraken_genus_abunds = pd.read_csv('../../data/stool/kraken_taxa_level_abunds/kraken_genus_abunds.tsv', sep='\t', index_col=0)
kraken_genus_abunds = kraken_genus_abunds.loc[[i for i in kraken_genus_abunds.index if i.startswith('d__Bacteria')]] # filter to only bacteria

# read in species level data
kraken_species_abunds = pd.read_csv('../../data/stool/kraken_taxa_level_abunds/kraken_species_abunds.tsv', sep='\t', index_col=0)
kraken_species_abunds = kraken_species_abunds.loc[[i for i in kraken_species_abunds.index if i.startswith('d__Bacteria')]] # filter to only bacteria

# calculate diversities and make table
diversity_metrics = pd.concat((kraken_genus_abunds.apply(shannon).rename('genus_shannon'),
                               kraken_genus_abunds.apply(simpson_e).rename('genus_evenness'),
                               kraken_genus_abunds.apply(observed_otus).rename('genus_richness'),
                               kraken_species_abunds.apply(shannon).rename('species_shannon'),
                               kraken_species_abunds.apply(simpson_e).rename('species_evenness'),
                               kraken_species_abunds.apply(observed_otus).rename('species_richness')), axis=1)

# write table to file
diversity_metrics.to_csv('../../data/stool/kraken_alpha_diversity.csv', index_label='SampleID')
