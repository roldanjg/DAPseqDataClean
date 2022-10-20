#!/usr/bin/env Rscript

library(DMRcaller)

plotMethylationDataCoveragethree <- function(methylationData1,
                                        methylationData2 = NULL,
                                        methylationData3 = NULL,
                                        breaks,
                                        regions = NULL,
                                        conditionsNames = NULL,
                                        context = "CG",
                                        proportion = TRUE,
                                        labels=NULL,
                                        col=NULL,
                                        pch = c(1,0,16,1,0,16,1,0,16),
                                        lty = c(4,1,3,4,1,3,4,1,3),
                                        contextPerRow = FALSE) {
  .validateContext(context)
  .validateMethylationData(methylationData1, variableName="methylationData1")
  numberOfConditions <- 1
  if(!is.null(methylationData2)){
    .validateMethylationData(methylationData2, variableName="methylationData2")
    numberOfConditions <- 2
  }
  if(!is.null(methylationData3)){
    .validateMethylationData(methylationData3, variableName="methylationData3")
    numberOfConditions <- 3
  }
  if(is.null(conditionsNames) | length(conditionsNames) < numberOfConditions){
    conditionsNames <- paste("condition ",(1:numberOfConditions),sep="")
  }
  
  number_of_symbols <- numberOfConditions*length(context)
  
  if(!.isColor(col, minLength = number_of_symbols )){
    if(number_of_symbols <= 6){
      col <- c("#D55E00","#E69F00", "#0072B2", "#56B4E9", "#F0E442", "#009E73")
    } else if(number_of_symbols <= 8){
      col <- c("#D55E00","#E69F00", "#0072B2", "#D55E00","#E69F00", "#0072B2","#D55E00","#E69F00", "#0072B2")
    } else{
      col <- rainbow(number_of_symbols)
    }
  }
  
  .stopIfNotAll(c(!is.null(pch),
                  all(as.integer(pch) == pch),
                  all(pch >= 0),
                  length(pch) >= number_of_symbols),
                paste(" pch is a vector of positive integers of size ",number_of_symbols, sep=""))
  
  .stopIfNotAll(c(!is.null(lty),
                  all(as.integer(lty) == lty),
                  all(lty >= 0),
                  length(lty) >= number_of_symbols),
                paste(" lty is a vector of positive integers of size ",number_of_symbols, sep=""))
  
  
  if(!is.null(labels) & (length(labels) < length(coverage) | !is.character(labels))){
    labels <- LETTERS[1:length(coverage)]
  }
  
  
  
  par(mar=c(4, 4, 3, 1)+0.1)
  if(contextPerRow){
    par(mfrow = c(length(context),1))
  } else{
    par(mfrow = c(1,length(context)))
  }
  
  for(i in 1:length(context)){
    buffer_coverage <- matrix(0, nrow = length(breaks), ncol=numberOfConditions)
    buffer_coverage[,1] <- computeMethylationDataCoverage(methylationData1,
                                                          regions = regions,
                                                          context = context[i],
                                                          breaks=breaks,
                                                          proportion = proportion)
    
    if(numberOfConditions > 1){
      buffer_coverage[,2] <- computeMethylationDataCoverage(methylationData2,
                                                            regions = regions,
                                                            context = context[i],
                                                            breaks=breaks,
                                                            proportion = proportion)
      buffer_coverage[,3] <- computeMethylationDataCoverage(methylationData3,
                                                            regions = regions,
                                                            context = context[i],
                                                            breaks=breaks,
                                                            proportion = proportion)
    }
    colnames(buffer_coverage) <- conditionsNames
    
    symbols_ind <- (numberOfConditions*(i-1) + 1):(numberOfConditions*i)
    
    plot(breaks, buffer_coverage[, 1], type = "o", ylim = c(0,1), main = paste("Coverage in ",context[i]," context",sep=""),
         xlab="minimum number of reads", ylab="coverage", col=col[symbols_ind[1]], xaxt="n", yaxt="n",
         lty = lty[symbols_ind[1]], pch = pch[symbols_ind[1]])
    
    if(numberOfConditions > 1){
      lines(breaks, buffer_coverage[, 2], type = "o", col=col[symbols_ind[2]], lty = lty[symbols_ind[2]], pch = pch[symbols_ind[2]])
      lines(breaks, buffer_coverage[, 3], type = "o", col=col[symbols_ind[3]], lty = lty[symbols_ind[3]], pch = pch[symbols_ind[3]])
    }
    
    axis(1, at=breaks,labels=breaks, las=1)
    axis(2, at=seq(0,1,0.1),labels=seq(0,1,0.1), las=1)
    
    
    legend("topright", legend = colnames(buffer_coverage), lty = lty[symbols_ind], col = col[symbols_ind], pch = pch[symbols_ind], bty="n")
    
    
    mtext(labels[i], line = 0.7, adj = 0, cex=1.0);
    
  }

  invisible(NULL)
}

environment(plotMethylationDataCoveragethree) <- asNamespace('DMRcaller')


setwd("/home/joaquin/projects/methylation/data/DMRs/plots/coverageMethylation")
args <- commandArgs(trailingOnly = TRUE)
for (a in args) {
   print(a)
}
# installed.packages()[, c("Package", "LibPath")]
# sessionInfo()
rep1 <- readBismarkPool(args[4])
rep2 <- readBismarkPool(args[5])
rep3 <- readBismarkPool(args[6])
print('hola')
jpeg(filename = args[7],
     width = 10, height = 3, units = "in", res = 300,
     bg = "white")
print('hola1')
plotMethylationDataCoveragethree(rep1, rep2, rep3,
                            breaks = c(1, 5, 10, 15),
                            regions = NULL,
                            conditionsNames = c(args[1], args[2], args[3]),
                            context = c("CG", "CHH", "CHG"),
                            proportion = TRUE,
                            labels = LETTERS,
                            contextPerRow = FALSE)
print('hola3')
dev.off()
