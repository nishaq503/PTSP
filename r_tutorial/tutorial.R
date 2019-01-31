library(ggplot2)

original_data <- read.csv(file="data/gapminder_data.csv", header=TRUE, sep=",", stringsAsFactors=FALSE)
original_data[sample(nrow(original_data), 5), ]
summary(original_data)
ggplot(data=original_data, aes(x=year, y=lifeExp, color=continent)) + geom_point()
original_data[original_data$lifeExp == min(original_data$lifeExp),]