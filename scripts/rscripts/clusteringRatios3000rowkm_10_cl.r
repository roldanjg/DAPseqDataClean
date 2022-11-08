#!/usr/bin/env Rscript



setwd("/home/joaquin/projects/methylation/scripts/rscripts")

library(ComplexHeatmap)
library(circlize)

ratios = as.matrix(read.table("M3_H7_Ratios.txt", header=TRUE, sep="\t",row.names = 1,as.is=TRUE))

col_fun = colorRamp2(c(-2, 0, 2), c("blue", "white", "red"))
set.seed(123)

jpeg(filename = "M3_H7_Ratios.3000rowkm_10_cl.jpg",
     width = 12, height = 12, units = "in", res = 300,
     bg = "white")

heatratio = Heatmap(ratios, row_km = 10,  col = col_fun,row_km_repeats = 3000, cluster_columns = FALSE,show_row_names = FALSE,column_split =  factor(rep(1:6, each = 3)),column_gap = unit(c(0,0,2,0,0), "mm"),cluster_column_slices = FALSE, border=TRUE)

ht = draw(heatratio)
rorder = row_order(ht)
#,
dev.off()
write.table(rorder[["1"]], file = "clus01.3000rowkm_10_cl.txt")
write.table(rorder[["2"]], file = "clus02.3000rowkm_10_cl.txt")
write.table(rorder[["3"]], file = "clus03.3000rowkm_10_cl.txt")
write.table(rorder[["4"]], file = "clus04.3000rowkm_10_cl.txt")
write.table(rorder[["5"]], file = "clus05.3000rowkm_10_cl.txt")
write.table(rorder[["6"]], file = "clus06.3000rowkm_10_cl.txt")
write.table(rorder[["7"]], file = "clus07.3000rowkm_10_cl.txt")
write.table(rorder[["8"]], file = "clus08.3000rowkm_10_cl.txt")
write.table(rorder[["9"]], file = "clus09.3000rowkm_10_cl.txt")
write.table(rorder[["10"]], file = "clus10.3000rowkm_10_cl.txt")