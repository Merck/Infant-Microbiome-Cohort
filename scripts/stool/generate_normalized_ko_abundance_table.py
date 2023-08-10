#  Copyright© 2023 Merck Sharp & Dohme Corp. a subsidiary of Merck & Co., Inc., Rahway, NJ, USA.

#  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

import pandas as pd

ko_abunds = pd.read_csv("../../data/stool/ko_abundance_table.tsv", sep='\t', index_col=0)
ko_abunds_rel = ko_abunds.div(ko_abunds.sum()) # convert to relative abundance
# ko_abunds_rel = ko_abunds_rel.loc[(ko_abunds_rel > 0).sum(axis=1) > 10] # remove KOs not seen in at least 10 samples
ko_abunds_rel.to_csv("../../data/stool/ko_abundance_table.rel.tsv", sep='\t')
