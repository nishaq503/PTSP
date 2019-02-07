#install.packages("ape")
#install.packages("phangorn")
#install.packages("seqinr")
#install.packages("dplyr")

library(ape)
library(phangorn)
library(seqinr)

mammals <- read.dna("data/TNKS.dna")
mammals_phydat <- phyDat(mammals)

mt <- modelTest(mammals_phydat)

library(dplyr)
arrange(mt, AIC)[1, 1]

dna_d <- dist.ml(mammals_phydat, model = "JC69")

mammals_UPGMA <- upgma(dna_d)

plot(mammals_UPGMA)


mammals_NJ <- NJ(dna_d)

plot(mammals_NJ)


parsimony(mammals_UPGMA, mammals_phydat)
parsimony(mammals_NJ, mammals_phydat)

mammals_optimal_pars <- optim.parsimony(mammals_NJ, mammals_phydat)

plot(mammals_optimal_pars)


fit <- pml(mammals_NJ, mammals_phydat)
fitJC <- optim.pml(fit, model = "JC")

plot(fitJC)


bs <- bootstrap.pml(fitJC, bs = 100, multicore = TRUE, optNni = TRUE)

plotBS(bs, p = 50, type = "p")
