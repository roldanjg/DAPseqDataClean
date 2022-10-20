#!/usr/bin/env Rscript
# computeDMRsReplicates(
#    methylationData, condition = NULL, regions = NULL,
#    context = "CG", method = "neighbourhood", binSize = 100,
#    test = "betareg", pseudocountM = 1, pseudocountN = 2,
#    pValueThreshold = 0.01, minCytosinesCount = 4,
#    minProportionDifference = 0.4, minGap = 200, minSize = 50,
#    minReadsPerCytosine = 4, cores = 1
#    )
library(DMRcaller)
#
# setwd("/home/joaquin/projects/methylation/data/DMRs")
args = commandArgs(trailingOnly=TRUE)
for (a in args) {
   print(a)
}
 methylation_data_tratement <- readBismarkPool(
   c("rep1._CX_report.txt",
    "rep2._CX_report.txt",
     "rep3._CX_report.txt",
     "rep4._CX_report.txt"
     ))
methylation_data_tratement <- as.list(methylation_data_tratement, use.names = TRUE)

# head(methylation_data_tratement[[1]], 20)
# ind is the number of replicates -1

# methylationDataRep <- joinReplicates(methylation_data_tratement[[1]], methylation_data_tratement[[2]]) # nolint

print(arg)
for (h in as.list(methylation_data_tratement, use.names = TRUE)) {
   print(h)
# methylationDataRep<-joinReplicates(methylationDataRep, methylation_data_tratement[h])
}
head(methylationDataRep,20)

#
# joined_data <- joinReplicates(methylation_data_tratement)
# head(joined_data, 20)
# condition_names <- c("1Mock", "1Mock", "1Mock", "1ACC", "1ACC", "1ACC")

# # chr_local <- GRanges(seqnames = Rle("Chr3"))

# CG_DMRS <-   computeDMRsReplicates(
#    methylation_data_tratement, condition = condition_names, regions = NULL,
#    context = "CG", method = "neighbourhood", binSize = 100,
#    test = "betareg", pseudocountM = 1, pseudocountN = 2,
#    pValueThreshold = 0.01, minCytosinesCount = 4,
#    minProportionDifference = 0.4, minGap = 200, minSize = 50,
#    minReadsPerCytosine = 4, cores = 1
#    )
# head(CG_DMRS, 20)










# methylationData <- readBismark("1ACCrep1_CX_report.txt.gz")
# head(methylationData)
# methylationDataMet13 <- readBismark("1Mockrep1_CX_report.txt.gz")
# methylationDataList <- GRangesList("WT" = methylationDataWT,
# "met1-3" = methylationDataMet13)

#     "1ACCrep1_CX_report.txt.gz"   "1ACCrep2_CX_report.txt.gz"  
#   "1ACCrep3_CX_report.txt.gz"   "1JArep1_CX_report.txt.gz"   
#   "1JArep2_CX_report.txt.gz"    "1JArep3_CX_report.txt.gz"   
#   "1Mockrep1_CX_report.txt.gz"  "1Mockrep2_CX_report.txt.gz" 
#   "1Mockrep3_CX_report.txt.gz"  "24ACCrep1_CX_report.txt.gz" 
#  "24ACCrep2_CX_report.txt.gz"  "24ACCrep3_CX_report.txt.gz" 
#  "24JArep1_CX_report.txt.gz"   "24JArep2_CX_report.txt.gz"  
#  "24JArep3_CX_report.txt.gz"   "24Mockrep1_CX_report.txt.gz"
#  "24Mockrep2_CX_report.txt.gz" "24Mockrep3_CX_report.txt.gz"
#  "6ACCrep1_CX_report.txt.gz"   "6ACCrep2_CX_report.txt.gz"  
#  "6ACCrep3_CX_report.txt.gz"   "6JArep1_CX_report.txt.gz"   
#  "6JArep2_CX_report.txt.gz"    "6JArep3_CX_report.txt.gz"   
#  "6Mockrep1_CX_report.txt.gz"  "6Mockrep2_CX_report.txt.gz" 
#  "6Mockrep3_CX_report.txt.gz" 

# data(GEs)
# #select the genes
# genes <- GEs[which(GEs$type == "gene")]
# # compute the DMRs in CG context over genes
# DMRsGenesCG <- filterDMRs(methylationDataList[["WT"]],
# methylationDataList[["met1-3"]],
# potentialDMRs = genes[overlapsAny(genes, chr_local)],
# context = "CG",
# test = "score",
# pValueThreshold = 0.01,
# minCytosinesCount = 4,
# minProportionDifference = 0.4,
# minReadsPerCytosine = 3,
# cores = 1)

# list.files(path = ".", pattern = NULL, all.files = FALSE,
#     full.names = FALSE)
## Not run:
# # load the methylation data
# data(methylationDataList)
# # Joins the wildtype and the mutant in a single object
# methylationDataList[["WT"]],
# methylationDataList[["met1-3"]], FALSE)

# head(methylationDataList[["WT"]], 20)