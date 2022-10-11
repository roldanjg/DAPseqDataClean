computeDMRsReplicates(
   methylationData, condition = NULL, regions = NULL,
   context = "CG", method = "neighbourhood", binSize = 100,
   test = "betareg", pseudocountM = 1, pseudocountN = 2,
   pValueThreshold = 0.01, minCytosinesCount = 4,
   minProportionDifference = 0.4, minGap = 200, minSize = 50,
   minReadsPerCytosine = 4, cores = 1
   )