original_data <- read.csv(file="data/gapminder_data.csv", header=TRUE, sep=",", stringsAsFactors=FALSE)
original_data[sample(nrow(original_data), 5), ]
