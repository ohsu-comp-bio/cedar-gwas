#!/usr/bin/env Rscript

require(ggplot2)
require(argparse)

parser = ArgumentParser(description="Generate Manhattan Plots")
parser$add_argument('--project', type="character")
parser$add_argument('--phenotype', type="character")
parser$add_argument('--chromosome', type="character")
parser$add_argument('--file', type="character")
args = parser$parse_args()

file <- read.table(args$file, header=TRUE, sep="\t")
value <- file[-log10(file$P) > 8,]
out <- paste(args$project,args$phenotype,args$chromosome,sep="_")

#if(nrow(value) > 3) {
    ggplot(file, aes(x=BP, y=-log10(P))) +
        geom_point(alpha=0.8, size=1.3, color="#2b8cbe") +
        theme_bw() +
        theme(
            legend.position="none",
            panel.border = element_blank(),
            panel.grid.major.x = element_blank(),
            panel.grid.minor.x = element_blank()
        )
    ggsave(file=paste(out,"png",sep="."))
#}
