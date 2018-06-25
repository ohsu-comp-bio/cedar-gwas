### R plugin to run linear model with gamma link function #########################################
library(BoutrosLab.plotting.general)
library(mada)
Rplink <- function(PHENO,GENO,CLUSTER,COVAR) {
	f1 <- function(s) {
		# calculate 
		r <- get.correlation.p.and.corr(PHENO, s, method = 'spearman');
                # get confidence intervals
                if(is.na(r[1])) {
                        results <- c(r,NA,NA)
                } else {
                        CI <- CIrho(r[1], length(PHENO));
                        # merge and return
                        results <- c(r, unlist(CI[,2:3]))
                }
		c( length(results), results);
	}
	apply( GENO, 2, f1);
}
