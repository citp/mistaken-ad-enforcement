library(binom)
library(gplots)
library(ggplot2)
library(Rmisc)
library(texreg)


set.seed(23453987)
filename = "simulation-simple"


### LOAD GROUND TRUTH
ground_truth <- read.csv(file=paste("csv/", filename, "-truth.csv", sep=""), header=TRUE,
                         sep=",", stringsAsFactors=FALSE)

ground_truth$Characteristic <- factor(ground_truth$Characteristic, levels=
                                        c("federal", "state",
                                          "republican", "democrat", 
                                          "persona.Ally", "persona.NonAlly", "persona.US",  
                                          "candidate", "candidate.position", "issue"))
## ggplot(ground_truth, aes(Blockrate, Characteristic)) +
##   geom_point(color="darkorange2", size=4) +
##   facet_grid(Label ~., scales="free", switch="both") +
##   theme_bw(base_size = 12, base_family = "Helvetica") +
##   theme(
##     axis.title.y=element_blank(),axis.ticks=element_blank(),
##     strip.text.y = element_text(face="bold"),
##   ) +
##   scale_x_continuous(limits=c(0,1), breaks=seq(0,1,0.1)) +
##   labs(x="Rate of Publication") +
##   ggtitle("Base Rates For Simulating The Chance of an Ad Being Published") +
##   ggsave(paste("../paper/images/", filename, "-baserates.png", sep=""), width=200, height=105, units="mm")


# Load simulated research result
simulation <- read.csv(file=paste("csv/", filename, ".csv", sep=""), header=TRUE,
                       sep=",", stringsAsFactors=FALSE)


simulate.results <- function(simulation.df, sample.size){
  group.results <- setNames(data.frame(matrix(ncol = 8, nrow = 0)), 
                            c("persona", "election", "advert", "key", 
                              "estimated.prob", "estimated.lower.conf", "estimated.upper.conf",
                              "ground.truth"))
  for(persona_key in unique(simulation.df$persona)){
    for(election_key in unique(simulation.df$election)){
      for(party_key in unique(simulation.df$party)){
        for(advert_key in unique(simulation.df$ad_type)){
          combination.pop <- subset(simulation.df, 
                                    persona==persona_key & 
                                    election == election_key & 
                                    party == party_key &
                                    ad_type == advert_key)
          combination <- combination.pop[sample(1:nrow(combination.pop), sample.size, replace=FALSE),]
          
          obs_count = nrow(combination)
          results <- data.frame(persona=persona_key, election = election_key, party=party_key, advert=advert_key,
                                key = paste(gsub("persona.", "",persona_key), election_key, party_key, advert_key, sep=" + "),
                                observations = obs_count)
          estimate <- binom.confint(x = nrow(subset(combination, permitted==1)), n = obs_count,
                        conf.level=0.95, methods="wilson")    
          results$estimated.prob <- estimate$mean
          results$estimated.lower.conf <- estimate$lower
          results$estimated.upper.conf <- estimate$upper
          results$ground.truth <- mean(combination$groundtruth)
          group.results <- rbind(group.results, results)
        }
      }
    }
  }
  group.results
}

### SIMULATE A SAMPLE SIZE OF FIVE
sample.size = 5
psp.results.5 <- simulate.results(simulation, sample.size)

ggplot(psp.results.5, aes(factor(key), estimated.prob)) +
  geom_point(size=2) +
  geom_point(color="darkorange2", y=psp.results.5$ground.truth, shape=4, size=2) +
  geom_errorbar(ymax=psp.results.5$estimated.upper.conf, 
                ymin=psp.results.5$estimated.lower.conf,
                width=0.5) +
  scale_y_continuous(limits=c(0,1), breaks=seq(0,1,0.1)) +
  theme_bw(base_size = 12, base_family = "Helvetica") +
  labs(y=paste("Estimated chance of publication for a given ad combination (persona, election, advert).\n",
               "True block rates (the orange X) have been simulated. Total ad placements: ", sum(psp.results.5$obs), "\n",
               "Attempted ad placements per combination: ",sample.size, sep="")) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1),
        axis.title.y = element_blank(),
        axis.title.x = element_text(hjust=0, size=10,lineheight = 0.9)
        ) +   
  coord_flip() +
  ggtitle("Estimated Ad Publication Rates from Simulated Data") +
  ggsave(paste("../paper/images/", filename, "-estimated-rates-n-5.png", sep=""), width=250, height=150, units="mm")


### SIMULATE A SAMPLE SIZE OF 10
sample.size = 10
psp.results <- simulate.results(simulation, sample.size)

ggplot(psp.results, aes(factor(key), estimated.prob)) +
  geom_point(size=2) +
  geom_point(color="darkorange2", y=psp.results$ground.truth, shape=4, size=2) +
  geom_errorbar(ymax=psp.results$estimated.upper.conf, 
                ymin=psp.results$estimated.lower.conf,
                width=0.5) +
  scale_y_continuous(limits=c(0,1), breaks=seq(0,1,0.1)) +
  theme_bw(base_size = 12, base_family = "Helvetica") +
  labs(y=paste("Estimated chance of publication for a given ad combination (persona, election, advert).\n",
               "True block rates (the orange X) have been simulated. Total ad placements: ", sum(psp.results$obs), "\n",
               "Attempted ad placements per combination: ",sample.size, sep="")) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1),
        axis.title.y = element_blank(),
        axis.title.x = element_text(hjust=0, size=10,lineheight = 0.9)
  ) +   
  coord_flip() +
  ggtitle("Estimated Ad Publication Rates from Simulated Data") +
  ggsave(paste("../paper/images/", filename, "-estimated-rates-n-10.png", sep=""), width=250, height=150, units="mm")

### SIMULATE A SAMPLE SIZE OF 20
sample.size = 20
psp.results <- simulate.results(simulation, sample.size)

ggplot(psp.results, aes(factor(key), estimated.prob)) +
  geom_point(size=2) +
  geom_point(color="darkorange2", y=psp.results$ground.truth, shape=4, size=2) +
  geom_errorbar(ymax=psp.results$estimated.upper.conf, 
                ymin=psp.results$estimated.lower.conf,
                width=0.5) +
  scale_y_continuous(limits=c(0,1), breaks=seq(0,1,0.1)) +
  theme_bw(base_size = 12, base_family = "Helvetica") +
  labs(y=paste("Estimated chance of publication for a given ad combination (persona, election, advert).\n",
               "True block rates (the orange X) have been simulated. Total ad placements: ", sum(psp.results$obs), "\n",
               "Attempted ad placements per combination: ",sample.size, sep="")) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1),
        axis.title.y = element_blank(),
        axis.title.x = element_text(hjust=0, size=10,lineheight = 0.9)
  ) +   
  coord_flip() +
  ggtitle("Estimated Ad Publication Rates from Simulated Data") +
  ggsave(paste("../paper/images/", filename, "-estimated-rates-n-20.png", sep=""), width=250, height=150, units="mm")

### SIMULATE A SAMPLE SIZE OF 50
sample.size = 50
psp.results <- simulate.results(simulation, sample.size)

ggplot(psp.results, aes(factor(key), estimated.prob)) +
  geom_point(size=2) +
  geom_point(color="darkorange2", y=psp.results$ground.truth, shape=4, size=2) +
  geom_errorbar(ymax=psp.results$estimated.upper.conf, 
                ymin=psp.results$estimated.lower.conf,
                width=0.5) +
  scale_y_continuous(limits=c(0,1), breaks=seq(0,1,0.1)) +
  theme_bw(base_size = 12, base_family = "Helvetica") +
  labs(y=paste("Estimated chance of publication for a given ad combination (persona, election, advert).\n",
               "True block rates (the orange X) have been simulated. Total ad placements: ", sum(psp.results$obs), "\n",
               "Attempted ad placements per combination: ",sample.size, sep="")) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1),
        axis.title.y = element_blank(),
        axis.title.x = element_text(hjust=0, size=10,lineheight = 0.9)
  ) +   
  coord_flip() +
  ggtitle("Estimated Ad Publication Rates from Simulated Data") +
  ggsave(paste("../paper/images/", filename, "-estimated-rates-n-50.png", sep=""), width=250, height=150, units="mm")







### NOW ESTIMATE THE RELATIONSHIP BETWEEN PERSONA AND AD PUBLICATION

## strat.sample <- stratified(simulation, c("persona", "election", "party", "ad_type"), size=5)
## strat.sample$persona <- factor(strat.sample$persona, levels=c("persona.US", "persona.Ally", "persona.NonAlly"))
## summary(persona.model <- glm(permitted ~ persona, data=strat.sample, family=binomial(link='logit')))

## texreg(persona.model)
