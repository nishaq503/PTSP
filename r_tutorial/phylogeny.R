#install.packages("ape")
#install.packages("phangorn")
#install.packages("seqinr")

library(ape)
library(phangorn)
library(seqinr)

mammals <- read.dna("data/TNKS.dna")
mammals_phydat <- phyDat(mammals)
