#  Copyright© 2023 Merck Sharp & Dohme Corp. a subsidiary of Merck & Co., Inc., Rahway, NJ, USA.

#  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

library(vegan)

# Script for filtering are rarefying nasal 16S OTU table, generates table to use across notebooks

abunds = read.table('../../data/nasal/otu_table.tsv', header=T, row.names=2)
drops <- c("label", "numOtus")
abunds = abunds[ , !(names(abunds) %in% drops)]

abunds_gt10 = abunds[colSums(abunds) >= 10]
abunds_gt10_min10K = abunds_gt10[rowSums(abunds_gt10) >= 10000,]

abunds_gt10_rar10K = rrarefy(abunds_gt10_min10K, 10000)
abunds_gt10_rar10K = abunds_gt10_rar10K[,colSums(abunds_gt10_rar10K) > 0]

write.table(abunds_gt10_rar10K, '../../data/nasal/otu_table.gt10_rar10K.tsv', sep='\t', quote=F)
