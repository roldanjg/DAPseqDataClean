#!/usr/bin/env Rscript

library(DMRcaller)

setwd("/home/joaquin/projects/methylation/data/DMRs/DMRsData")
args <- commandArgs(trailingOnly = TRUE)
for (a in args) {
   print(a)
}

list_of_names <- c(args[1],args[2],args[3],c(args[4],args[5],args[6]))

leftSide <- readBismark(list_of_names[[1]])
rightSide <- readBismark(list_of_names[[2]])
leftSide<-joinReplicates(leftSide, rightSide)

for (h in 3:6) {
  print(h)
  head(leftSide)
  rightSide <- readBismark(list_of_names[[h]])
  leftSide<-joinReplicates(leftSide, rightSide)
}
head(leftSide)

condition <- c("a", "a","a", "b", "b","b")

DMRsReplicatesNeighbourhood <- computeDMRsReplicates(methylationData = leftSide,
                                                     condition = condition,
                                                     regions = NULL,
                                                     context = "CG",
                                                     method = "neighbourhood",
                                                     test = "betareg",
                                                     pseudocountM = 1,
                                                     pseudocountN = 2,
                                                     pValueThreshold = 0.01,
                                                     minCytosinesCount = 4,
                                                     minProportionDifference = 0.4,
                                                     minGap = 200,
                                                     minSize = 50,
                                                     minReadsPerCytosine = 4,
                                                     cores = 1)

head(DMRsReplicatesNeighbourhood)

write.table(
    x = DMRsReplicatesNeighbourhood,
    file = paste(args[7], "testreplicates.tsv",sep=""),
    sep="\t", col.names = TRUE,
    row.names = FALSE,
    quote = FALSE)
