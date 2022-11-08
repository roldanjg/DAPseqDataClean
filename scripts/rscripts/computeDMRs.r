#!/usr/bin/env Rscript

library(DMRcaller)

setwd("/home/joaquin/projects/methylation/data/DMRs/DMRsData")

# ------------------------------------------------------------------------

data("syntheticDataReplicates")
# compute the DMRs in CG context with neighbourhood method
# creating condition vector
condition <- c("a", "a", "b", "b")
# computing DMRs using the neighbourhood method
DMRsReplicatesNeighbourhood <- computeDMRsReplicates(methylationData = methylationData,
condition = condition,
regions = NULL,
context = "CHH",
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
cores = 20)
write.table(
    x = DMRsReplicatesNeighbourhood,
    file = paste("hola", "_NoiseFilter_CG.tsv",sep=""),
    sep="\t", col.names = TRUE,
    row.names = FALSE,
    quote=FALSE )
# ------------------------------------------------------------------------
# args <- commandArgs(trailingOnly = TRUE)
# for (a in args) {
#    print(a)
# }
# # installed.packages()[, c("Package", "LibPath")]
# # sessionInfo()


# methylationMock <- readBismarkPool(c(args[1],args[2],args[3]))
# methylationCondition <- readBismarkPool(c(args[4],args[5],args[6]))


# DMRsNoiseFilterCG <- computeDMRs(methylationMock,
#                                  methylationCondition,
#                                  context = "CG", method = "noise_filter",
#                                  windowSize = 100, kernelFunction = "triangular",
#                                  test = "score", pValueThreshold = 0.01,
#                                  minCytosinesCount = 4, minProportionDifference = 0.2,
#                                  minGap = 200, minSize = 20, minReadsPerCytosine = 4,
#                                  cores = 10)
# write.table(
#     x = DMRsNoiseFilterCG,
#     file = paste(args[7], "_NoiseFilter_CG.tsv",sep=""),
#     sep="\t", col.names = TRUE,
#     row.names = FALSE,
#     quote=FALSE )
    
# DMRsNoiseFilterCHH <- computeDMRs(methylationMock,
#                                  methylationCondition,
#                                  context = "CHH", method = "noise_filter",
#                                  windowSize = 100, kernelFunction = "triangular",
#                                  test = "score", pValueThreshold = 0.01,
#                                  minCytosinesCount = 4, minProportionDifference = 0.2,
#                                  minGap = 200, minSize = 20, minReadsPerCytosine = 4,
#                                  cores = 10)
# write.table( 
#     x = DMRsNoiseFilterCHH,
#     file = paste(args[7], "_NoiseFilter_CHH.tsv",sep=""),
#     sep="\t", col.names = TRUE,
#     row.names = FALSE,
#     quote=FALSE )
# DMRsNoiseFilterCHG <- computeDMRs(methylationMock,
#                                  methylationCondition,
#                                  context = "CHG", method = "noise_filter",
#                                  windowSize = 100, kernelFunction = "triangular",
#                                  test = "score", pValueThreshold = 0.01,
#                                  minCytosinesCount = 4, minProportionDifference = 0.2,
#                                  minGap = 200, minSize = 20, minReadsPerCytosine = 4,
#                                  cores = 10)
# write.table(
#     x = DMRsNoiseFilterCHG,
#     file = paste(args[7], "_NoiseFilter_CHG.tsv",sep=""),
#     sep="\t", col.names = TRUE,
#     row.names = FALSE,
#     quote=FALSE )
