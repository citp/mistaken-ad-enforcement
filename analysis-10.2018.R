library(ggplot2)
library(binom)
library(gmodels)
library(texreg)
library(Hmisc)
library(xtable)

rm(list=ls())

cbbPalette <- c("#E69F00", "#000000", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")

###################################################
## Estimating Mistaken Enforcement of Election Advertising 
## Policies by Facebook and Google
## analysis by J. Nathan Matias and Austin Hounsel
## October 15, 2018
##
## Study pre-registration at: https://osf.io/4zudh/
###################################################

#############
## SETTINGS
#############
code.data.url = "github.com/citp/mistaken-ad-enforcement"

## LOAD PER-INVESTIGATOR DATASETS
filenames = c(
"ad.poster.1.data.csv",
"ad.poster.2.data.csv",
"ad.poster.3.data.csv",
"ad.poster.4.data.csv",
"ad.poster.5.data.csv",
"ad.poster.6.data.csv",
"ad.poster.27.data.csv")

advertising.results <- read.csv(paste("data/ad-results/",filenames[[1]], sep="/"))
for(i in seq(2, length(filenames))){
  print(filenames[[i]])
  df <- read.csv(paste("data/ad-results/",filenames[[i]], sep="/"))
  advertising.results <- rbind(advertising.results, df)
}

advertising.results$date <- as.Date(advertising.results$Date,"%m/%d/%Y")

## RETAIN ALL AD PLACEMENT ATTEMPTS FOR WHICH WE DO NOT HAVE EXPLICITLY LABELED MISSING RECORDS
advertising.results <- subset(advertising.results, Ad.Permitted..Y.N.!="NA")

## KEY DATES
first.date <- min(advertising.results$date)
last.date <- max(advertising.results$date)

## CREATE AD PLACEMENT DATAFRAME FROM THE CSV DATA
ad.placement.attempt = data.frame(
  poster.id = factor(advertising.results$Ad.Poster.ID),
  publication.status.permitted = advertising.results$Ad.Permitted..Y.N. != "N",
  ad.candidate.party = advertising.results$Left.or.right.leaning.,
  ad.general.issue = advertising.results$Product.or.Issue.reference. =="Issue",
  ad.candidate.support = advertising.results$Product.or.Issue.reference. == "Product",
  election = advertising.results$State.or.National.candidate.issue.,
  platform = advertising.results$Platform,
  date= advertising.results$date
)
ad.placement.attempt$ad.type <- "issue.mistake"
ad.placement.attempt$ad.type[ad.placement.attempt$ad.general.issue==FALSE] <- "candidate.mistake"
ad.placement.attempt$ad.type <- factor(ad.placement.attempt$ad.type)
ad.placement.attempt$election <- tolower(ad.placement.attempt$election)
ad.placement.attempt$election[ad.placement.attempt$election=="national"] <- "federal"
ad.placement.attempt$election <- factor(ad.placement.attempt$election)
ad.placement.attempt$persona <- "US"
ad.placement.attempt$persona[ad.placement.attempt$poster.id==6] <- "Non-US"
ad.placement.attempt$persona[ad.placement.attempt$poster.id==4] <- "Non-US"
ad.placement.attempt$persona[ad.placement.attempt$poster.id==27] <- "Non-US"
ad.placement.attempt$attempt.key <- paste(gsub("persona.", "",ad.placement.attempt$persona), 
                                          ad.placement.attempt$election, 
                                          ad.placement.attempt$ad.candidate.party, 
                                          ad.placement.attempt$ad.type, sep=" + ")


## SUMMARY TABLES
summary(factor(ad.placement.attempt$attempt.key))
ftable(xtabs(~ad.type+election+poster.id, data=ad.placement.attempt))

####################################################################
### PER-CHARACTERISTIC ANALYSIS
### NOTE: This code has changed slightly from the pre-analysis plan
###       since the code in the published plan failed to include 
###       the full set of characteristics being considered 
###       and since the original code included a study-wide N as 
###       denominator rather than a N for the subset in question
####################################################################

psp.results <- setNames(data.frame(matrix(ncol = 8, nrow = 0)), 
                        c("persona", "election", "advert", "key", 
                          "estimated.prob", 
                          "estimated.lower.conf", 
                          "estimated.upper.conf"))
for(platform_key in unique(ad.placement.attempt$platform)){
  for(persona_key in unique(ad.placement.attempt$persona)){
    for(election_key in unique(ad.placement.attempt$election)){
      for(party_key in unique(ad.placement.attempt$ad.candidate.party)){
        for(advert_key in unique(ad.placement.attempt$ad.type)){
          
          ad.placement.subset <- subset(ad.placement.attempt, 
                                          (persona == persona_key &
                                          election == election_key &
                                          ad.candidate.party == party_key &
                                          ad.type == advert_key &
                                          platform == platform_key))
          obs_count = nrow(ad.placement.subset)
          results <- data.frame(platform = platform_key,
                                persona=persona_key, 
                                election = election_key, 
                                party=party_key, 
                                advert=advert_key,
                                key = paste(gsub("persona.", "",persona_key), 
                                            election_key, party_key, 
                                            advert_key, sep=" + "),
                                observations = obs_count)
          estimate <- binom.confint(x = nrow(subset(ad.placement.subset, publication.status.permitted==1)), 
                                    n = obs_count,
                                    conf.level=0.95, methods="wilson")    
          results$estimated.prob <- estimate$mean
          results$estimated.lower.conf <- estimate$lower
          results$estimated.upper.conf <- estimate$upper
          psp.results <- rbind(psp.results, results)
        }
      }
    }
  }
}


## REMOVE NA RESULTS FOR AD TYPES THAT WERE NOT INCLUDED IN THE STUDY 
psp.results <- subset(psp.results, is.na(estimated.prob) != TRUE)
## GENERATE LaTeX table of results for report
psp.results$pct.published <- paste(sprintf("%0.1f", psp.results$estimated.prob*100), "%", sep="")
print(colnames(psp.results))
xtable(psp.results[,c("platform", "persona", "election", "party", "advert", "observations", "pct.published")])

## GENERATE PLOTS: 
## issue.mistake ads 
## (national parks and veteran's day parades)

advert_key = "issue.mistake"
sample.size <- sum(subset(psp.results, advert==advert_key)$observations)

ggplot(subset(psp.results, advert==advert_key), aes(factor(paste("  ", gsub(paste("\\+ ",advert_key,sep=""), "", key), sep="")), estimated.prob, color=factor(party))) +
  facet_grid( . ~ platform ) +
  geom_point(size=2) +
  geom_errorbar(ymax=subset(psp.results, advert==advert_key)$estimated.upper.conf, 
                ymin=subset(psp.results, advert==advert_key)$estimated.lower.conf,
                width=0.2) +
  scale_y_continuous(limits=c(0,1), breaks=seq(0,1,0.1), labels = scales::percent) +
  scale_color_manual(values=c(cbbPalette[[3]], cbbPalette[[7]]), name = "Issue", labels=c("National Parks\n(Democrat)", "Veterans Day\n(Republican)")) +
  theme_bw(base_size = 12, base_family = "Helvetica") +
  labs(y="", x="") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
        axis.title.y = element_blank(),
        axis.title.x = element_text(hjust=0, size=1,lineheight = 0.9)
  ) +
  coord_flip()  +
  ggtitle("Veterans Day & National Park Ad Publication Rates") +
  ggsave("figures/issue_mistake_results.png", width=10, height=2)


## candidate mistake ads
## (products that share a name with a candidate)

advert_key = "candidate.mistake"
sample.size <- sum(subset(psp.results, advert==advert_key)$observations)

ggplot(subset(psp.results, advert==advert_key), aes(factor(gsub(paste("\\+ ",advert_key,sep=""), "", key)), estimated.prob, color=factor(party))) +
  facet_grid( . ~ platform ) +
  geom_point(size=2) +
  geom_errorbar(ymax=subset(psp.results, advert==advert_key)$estimated.upper.conf, 
                ymin=subset(psp.results, advert==advert_key)$estimated.lower.conf,
                width=0.2) +
  scale_y_continuous(limits=c(0,1), breaks=seq(0,1,0.1), labels = scales::percent) +
  scale_color_manual(values=c(cbbPalette[[3]], cbbPalette[[7]]), name = "Mistaken Party", labels=c("Democrat", "Republican      ")) +
  theme_bw(base_size = 12, base_family = "Helvetica") +
  labs(y=paste("Estimated chance of publication ",
               "for a given ad combination",
               "(ad poster, election, leaning).\n",
               "Total ad placements: ", sum(psp.results$obs), " ads placed by ", length(unique(ad.placement.attempt$poster.id)), " people from ", first.date, " to ", last.date, ".",  
               "\nProduct ads are music albums that share a word with a candidate name.\n",
               "Veterans Day & National Park ads are about events and places that could be be mistaken by platform policy enforcers \nas election-related ads 'of national importance.'",
               "\n95% confidence intervals use the Wilson method. Code & data at: ",  code.data.url,
               "\n", "Data and analysis by J. Nathan Matias and Austin Hounsel of Princeton University\n",
               "with Melissa Hopkins, Ben Werdmuller, Jason Griffey, Chris Peterson, Scott Hale, and Nick Feamster", sep="")) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
        axis.title.y = element_blank(),
        axis.title.x = element_text(hjust=0, size=10,lineheight = 0.9)
  ) +
  coord_flip() +
  ggtitle("Ad Publication Rates for Products that Share a Name with a Candidate") +
  ggsave("figures/candidate_mistake_results.png", width=10, height=4)

####################################################################
### EXPLORATORY ANALYSES
### In these analyses, we search for differences in mistaken enforcement
### between different kinds of ads using logistic regression models
####################################################################

## COMPARING ISSUE MISTAKES AND AND CANDIDATE MISTAKES WITHIN FACEBOOK
summary(issue.candidate.lm <- glm(publication.status.permitted ~ ad.general.issue, data=subset(ad.placement.attempt, platform=="Facebook"), family=binomial))

issue.candidate.lm.sim = data.frame(ad.general.issue = c(TRUE,FALSE), ad.legend=c("Parks & Veterans Day\n(Issues)", "Products\n(Candidates)"))
issue.candidate.lm.sim.fit <- predict(issue.candidate.lm, issue.candidate.lm.sim, type="link", se.fit=TRUE)

issue.candidate.lm.sim$fit <- issue.candidate.lm.sim.fit$fit
issue.candidate.lm.sim$fit.upr <- issue.candidate.lm.sim.fit$fit + 1.96 * issue.candidate.lm.sim.fit$se.fit
issue.candidate.lm.sim$fit.lwr <- issue.candidate.lm.sim.fit$fit - 1.96 * issue.candidate.lm.sim.fit$se.fit
issue.candidate.lm.sim$prob.fit <- exp(issue.candidate.lm.sim.fit$fit)/(1+exp(issue.candidate.lm.sim.fit$fit))
issue.candidate.lm.sim$prob.upr <- exp(issue.candidate.lm.sim$fit.upr)/(1+exp(issue.candidate.lm.sim$fit.upr))
issue.candidate.lm.sim$prob.lwr <- exp(issue.candidate.lm.sim$fit.lwr)/(1+exp(issue.candidate.lm.sim$fit.lwr))

ggplot(issue.candidate.lm.sim, aes(ad.general.issue, prob.fit, color=ad.legend)) +
  geom_point(size=2) +
  geom_text(aes(y=issue.candidate.lm.sim$prob.fit), 
            label=paste(round(100*issue.candidate.lm.sim$prob.fit, 0), "%", sep=""),
            show.legend = FALSE,
            nudge_x=-0.17,nudge_y=-0.02) +
  geom_errorbar(ymax=issue.candidate.lm.sim$prob.upr, ymin=issue.candidate.lm.sim$prob.lwr, width=0.2) +
  scale_x_discrete(labels = issue.candidate.lm.sim$ad.legend) +
  scale_y_continuous(limits=c(0,1), breaks=seq(0,1,0.1), labels = scales::percent) +
  scale_color_manual(values=c(cbbPalette[[2]], cbbPalette[[4]]), name = "Ad Type") +
  theme_bw(base_size = 12, base_family = "Helvetica") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
        axis.title.y = element_blank(),
        axis.title.x = element_text(hjust=0, size=10,lineheight = 0.9),
        axis.text.y=element_blank()
  ) +
  coord_flip() +
  ggtitle("Facebook permitted fewer non-election ads about parks and holidays than non-election ads about products") +
  labs(y=paste("Estimated Facebook publication rate for non-election advertisements ",
               "comparing Park & Parade ads (issue mistake) \nto Product ads (candidate mistake).",
               "Total ad placements: ", nrow(subset(ad.placement.attempt, platform=="Facebook")), " ads placed by ", 
               length(unique(subset(ad.placement.attempt, platform=="Facebook")$poster.id)), " people from ", first.date, " to ", last.date, ". \n",  
               "Product ads are music albums that share a word with a candidate name. ",
               "Park & Veterans Day ads are about events & places \n",
               "that could be be mistaken by platform policy enforcers as election-related ads 'of national importance.'",
               "\nResults from a logistic regression (p=", 
               round(summary(issue.candidate.lm)$coefficients['ad.general.issueTRUE',][['Pr(>|z|)']], 3),
               "). Code & data at: ",  code.data.url,
               "\n", "Data and analysis by J. Nathan Matias and Austin Hounsel of Princeton University\n",
               "with Melissa Hopkins, Ben Werdmuller, Jason Griffey, Chris Peterson, Scott Hale, and Nick Feamster", sep="")) +
  ggsave("figures/issue_vs_candidate_mistakes.png", width=10, height=4)
  

## FACEBOOK: DIFFERENCES BETWEEN ENFORCEMENT OF MISTAKEN ADS BY POLITICAL LEANINGS
summary(issue.political.leaning.lm <- glm(publication.status.permitted ~ ad.candidate.party, data=subset(ad.placement.attempt, platform=="Facebook"), family=binomial))

## FACEBOOK:  DIFFERENCES BETWEEN STATE VS FEDERAL
summary(state.federal.lm <- glm(publication.status.permitted ~ election , data=subset(ad.placement.attempt, platform=="Facebook"), family=binomial))


## FACEBOOK:  DIFFERENCES BETWEEN US AND Non-US
summary(persona.lm <- glm(publication.status.permitted ~ persona , data=subset(ad.placement.attempt, platform=="Facebook"), family=binomial))


## OUTPUT TABLE FOR FACEBOOK MODELS
screenreg(list(issue.candidate.lm, issue.political.leaning.lm, state.federal.lm, persona.lm),
          custom.coef.names = c("(Intercept)", "Ad Type (Park \\& Parade)", "Leaning (Republican)", "Location (State)", "Ad Poster (US)"),
          custom.model.names = c("Ad Type", "Leaning", "Location", "Poster Location"))

texreg(list(issue.candidate.lm, issue.political.leaning.lm, state.federal.lm, persona.lm),
          custom.coef.names = c("(Intercept)", "Ad Type (Park \\& Parade)", "Leaning (Republican)", "Location (State)", "Ad Poster (US)"),
          custom.model.names = c("Ad Type", "Leaning", "Location", "Poster Location"))


####################################################################
### OUTPUT RESULTS
####################################################################
rm(filenames)
save.image("data/ad.placement.attempts.10.15.2018.RData")

