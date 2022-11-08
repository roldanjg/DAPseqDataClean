#!/usr/bin/env Rscript



setwd("/home/joaquin/projects/methylation/scripts/rscripts")

library(ComplexHeatmap)
library(circlize)

ratios = as.matrix(read.table("M3_H7_Ratios.txt", header=TRUE, sep="\t",row.names = 1,as.is=TRUE))

col_fun = colorRamp2(c(-2, 0, 2), c("blue", "white", "red"))
set.seed(123)

jpeg(filename = "M3_H7_Ratios.jpg",
     width = 12, height = 12, units = "in", res = 150,
     bg = "white")

heatratio = Heatmap(ratios, row_km = 15,  col = col_fun, cluster_columns = FALSE,show_row_names = FALSE,column_split =  factor(rep(1:6, each = 3)),column_gap = unit(c(0,0,2,0,0), "mm"),cluster_column_slices = FALSE, border=TRUE)

ht = draw(heatratio)
rorder = row_order(ht)
#row_km_repeats = 1500,
dev.off()