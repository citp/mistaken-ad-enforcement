# Estimating Publication Rates of Non-Election ads by Facebook and Google
by [Austin Hounsel](https://www.cs.princeton.edu/~ahounsel/), [J. Nathan Matias](https://natematias.com) ([@natematias](https://twitter.com/natematias)), Ben Werdmuller, Jason Griffey, Melissa Hopkins, Chris Peterson, Scott A. Hale, and Nick Feamster

_Please direct any questions about this research to Austin Hounsel (ahounsel@princeton.edu) and J. Nathan Matias (jmatias@princeton.edu)._

## Project Summary
Technology companies including Facebook and Google have created policies governing the kinds of advertisements they prohibit during the 2018 U.S. election. All enforcement systems make mistakes, and companies have been criticized for prohibiting ads that are unrelated to the election, including ads for public gatherings and for products that share names with candidates. Companies have also been accused of political bias in these enforcement mistakes. Both companies publish transparency databases that cannot be used to estimate enforcement rates, since they do not include information about advertisements that were prohibited and never published.

In this study, we ask how common these mistakes are and what kinds of ads are mistakenly prohibited by Facebook and Google. Over 23 days, 7 U.S. citizens living inside and outside the United States attempted to publish 477 non-election advertisements that varied in the type of ad, its potentially-mistaken political leaning, and its geographic targeting to a federal or state election voter population. Google did not prohibit any of the ads posted. Facebook prohibited 4.2% of the submitted ads.

![Comparing Facebook and Google's publication rates of advertisements for veterans day, parks, and products](https://s3.amazonaws.com/ftt-uploads/wp-content/uploads/2018/11/02071710/advertising-analysis-full-results-allpersonas-10.24.2018.png)

We found systematic evidence that Facebook’s policy enforcers are more likely to prohibit some kinds of non-election ads than others. Advertisements for national parks and veteran’s day celebrations were more commonly prohibited by Facebook than product ads. Within our sample size, we failed to find any differences of mistaken enforcement by Facebook in the leaning of the ad, the US/Non-US location of the submitter, or state/federal election targeting.

* Full report: [Estimating Publication Rates of Non-Election Ads by Facebook and Google](estimating-publication-rates-of-non-election-ads.pdf) (Nov 1, 2018)
* Atlantic Article: [We Tested Facebook’s Ad Screeners and Some Were Too Strict](https://www.theatlantic.com/technology/archive/2018/11/do-big-social-media-platforms-have-effective-ad-policies/574609/) (Nov 2, 2018)
* Pre-Analysis plan: [Estimating Mistaken Enforcement of Tech Platform Political Advertising Policies](https://osf.io/4zudh/) (Sep 17, 2018)

## About This Project
This project was developed by Austin Hounsel, J. Nathan Matias, and Nick Feamster at the Princeton University [Center for Information Technology Policy](https://citp.princeton.edu). It was also Austin's class project in [SOC412: Designing Field Experiments at Scale](http://natematias.com/courses/soc412/).

### Research Methods
Overall, our research method involved creating software to auto-generate ads that consistently tested enforcement rates for different kinds of ad posters, different kinds of ads, and different kinds of ad targeting. The software then directed our team of 7 researchers and U.S. citizens to publish the ad to Google and Facebook and record how the platform responded. We then analyzed the results in the full report and Atlantic article.

Full research methods are described in the [report with our results](estimating-publication-rates-of-non-election-ads.pdf). Before we collected any data, we also [pre-registered our analyses]((https://osf.io/4zudh/)) on the Open Science Framework. Because some of our research questions focused on political bias, we wanted to protect the trustworthiness of our research; by pre-registering our analysis, we protect ourselves from any question that we consciously or unconsciously altered our analysis approach after seeing the data. With the exception of fixing a bug, which we note in our [analysis source code](analysis-10.2018.R), we fully followed the procedure that we pre-registered.

Because we believe the ad-creation software represents a novel contribution to computer science, we are waiting to release more information about the software until after the work has academic received peer review.

### Research Ethics
For legal and ethical reasons, we did not place any ads that explicitly (or implicitly) endorsed a political candidate. The lead researchers on this study are employed by Princeton University, which holds a 501(c)(3) non-profit status. According to federal law, 501(c)(3)s are forbidden from participating in electioneering, which includes placing advertisements that advocate for a candidate. Instead, we focused this research on advertising that is completely unrelated to the election.

We designed this study through repeated and iterative discussions within our team and with outside advisors about the ethics of this research and the potential risks to participants. By choosing to test ads that do not engage in campaigning, and by balancing the number of ads that could be mistakenly construed as right or left leaning, we minimized the risk to voters and to elections (see Scott Desposato's [writing on this topic](http://www.desposato.org/ethicsfieldexperiments.pdf)).

We have also have followed standard practices in academic research ethics to minimize the risk from our research and to protect the privacy of those involved---storing all data securely, anonymizing the data, and minimizing the number of people who were exposed to the ads.

By investigating the rate at which non-election ads are prohibited, we are studying the performance of a platform’s enforcement systems on average. Policy enforcement mistakes could result from many factors, including the details of a company’s policies, the quality of training, the behavior of automated filter software, and perhaps differences in the judgment of individual workers. Because this study cannot distinguish between those factors, and because we evaluate the system as a whole rather than evaluating individuals, **these findings should never be interpreted as a reflection upon any individual worker enacting policy for these companies.**

## Files in this repository
This repository includes everything needed to re-analyze our results, including:

* **analysis-10.2018.R**: R code used to estimate results, create figures, and create the data file used to generate the report
* **main.Rtex**: Rtex file used to generate the report, showing the formulas used to calculate all quantitative claims
* **ref.bib**: BibTex file containing our full bibliography
* **figures/**: folder containing all figures used in the report, including some generated by analysis-10.2018.R
* **figures-from-article**: archive of figures used in the Atlantic article
* **estimating-publication-rates-of-non-election-ads.pdf** the full report
* **data/**: data recorded by our ad posters, and used by the analysis code to generate the result. For a codebook, please contact the authors.

## About The Team
* [J. Nathan Matias](https://natematias.com) researches social technology at the Princeton University Center for Information Technology Policy, the Psychology department, and the MIT Media Lab. He is also founder of [CivilServant](http://civilservant.io), which organizes citizen behavioral science for a world where digital power is guided by evidence and accountable to the public.
* [Austin Hounsel](https://www.cs.princeton.edu/~ahounsel/) is a computer science Ph.D. student at Princeton University and the Center for Information Technology Policy. He studies Internet censorship and automated content moderation.
* Melissa Hopkins is a law student at the George Washington University Law School.
* [Chris Peterson](http://www.cpeterson.org/) is a research affiliate at the MIT Center for Civic Media and a member of the Board of Directors of the National Coalition Against Censorship.
* [Jason Griffey](http://jasongriffey.net/) is a librarian, technologist, speaker, consultant and Affiliate at metaLAB at Harvard University. His work focuses on emerging technologies and their near-future effect on communities and civic institutions, especially libraries.
* [Ben Werdmuller](https://werd.io/) advises and builds ventures at the intersection of media and technology. He was formerly the Director of Investments in San Francisco for Matter Ventures.
* [Scott A. Hale](http://www.scotthale.net/blog/) develops and applies new computational methods to the study of human behavior as a Senior Data Scientist and Research Fellow at the Oxford Internet Institute.
* [Nick Feamster](https://www.cs.princeton.edu/~feamster/) is a professor of computer science and deputy director of the Princeton University Center for Information Technology Policy.

## Acknowledgments
We are grateful to [Molly Sauter](https://oddletters.com/), who provided logistical support to this study, and to [Jon Penney](https://www.dal.ca/faculty/law/faculty-staff/our-faculty/jon-penney.html), who provided helpful advice and feedback.

## License
We are making the source code, data, figures, and reports available under a [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/) license. 

You are free to share and adapt these materials if you give appropriate credit, link to the license, and indicate if changes were made, but not in any way that suggests that we endorse you or your use. You must also distribute your contributions under the same license as the original. Creative Commons have published [full details of the Attribution-ShareAlike 4.0 International license](https://creativecommons.org/licenses/by-sa/4.0/legalcode).
