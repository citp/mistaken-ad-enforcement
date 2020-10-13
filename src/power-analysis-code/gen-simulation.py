import csv
import numpy as np
import random

random.seed(93744)


class Characteristic:

    
    def __init__(self, name, permitrate):
        self.name = name
        self.permitrate = permitrate


    def __str__(self):
        return self.name


class Persona:

    
    def __init__(self, country, election, party, ad_type):
        self.country = country
        self.election = election
        self.party = party
        self.ad_type = ad_type

    def get_permitrate(self):
        return self.country.permitrate * self.election.permitrate * self.party.permitrate * self.ad_type.permitrate 


class Simulation:
    

    def __init__(self, observations, countries, elections, parties, ad_types, title):
        self.observations = observations
        self.countries = countries
        self.elections = elections
        self.parties = parties
        self.ad_types = ad_types
        self.title = title

        
    def get_permitted(self, persona):
        return np.random.binomial(1,persona.get_permitrate(), size=self.observations)


#    def get_emoji(self, characteristic):
#        name = characteristic.name
#        if name == "AllyPersona":
#            return "arrow_up"
#        elif name == "Nonally":
#            return "arrow_down"
#        elif name == "AllyCurrency":
#            return "arrow_right"
#        elif name == "NonAllyCurrency":
#            return "arrow_left"
#        elif name == "Federal":
#            return "x"
#        elif name == "State":
#            return "o"

    
    def write_simulation(self, filepath):
        id = 1
        with open(filepath, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(["persona.id", "persona", "election", "party", "ad_type",
                             "permitted", "total.observations", "groundtruth", "title"])
            for country in self.countries:
                for election in self.elections:
                    for party in self.parties:
                        for ad_type in self.ad_types:
                            persona = Persona(country, election, party, ad_type)
                            for attempt_result in self.get_permitted(persona):
                            #permitted = self.get_permitted(persona)
                                writer.writerow([id, country.name, election.name,  
                                                 party.name, ad_type.name, attempt_result,
                                                 self.observations, persona.get_permitrate(), title])
                            id += 1

    def write_ground_truth(self, filepath):
        with open(filepath, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(["Label","Characteristic", "Blockrate"])
            for country in self.countries:
                writer.writerow(["Country", country.name, country.permitrate])
            for party in self.parties:
                writer.writerow(["Party",party.name, party.permitrate])
            for election in self.elections:
                writer.writerow(["Election",election.name, election.permitrate])
            for ad_type in self.ad_types:
                writer.writerow(["Ad Type",ad_type.name, ad_type.permitrate])


if __name__ == "__main__":
    observations = 100

    # PERSONA COUNTRY
    us = Characteristic("persona.US", 0.95)
    ally = Characteristic("persona.Ally", 0.1)
    nonally = Characteristic("persona.NonAlly", 0.1)
    
    ## AD TYPE
    general_issue = Characteristic("issue", 1.0)
    candidate_support = Characteristic("candidate", 0.8)
    candidate_issue = Characteristic("candidate.position", 0.8)

    ## ELECTION
    fed = Characteristic("federal", 0.9)
    state = Characteristic("state", 1.0)

    ## PARTY
    republican = Characteristic("republican", 1.0)
    democrat = Characteristic("democrat", 1.0)

    ## CONSTRUCT GROUPS FROM PERSONA, AD TYPE, ELECTION, PARTY
    countries = [us, ally, nonally]
    elections = [fed, state]
    parties   = [republican, democrat]
    ad_types = [general_issue, candidate_support, candidate_issue]

    title = "Simulation of ads being permitted with expected probabilities"
    simulation = Simulation(observations, countries, elections, parties, ad_types, title)
    simulation.write_ground_truth("simulation-largesample-truth.csv")
    simulation.write_simulation("simulation-largesample.csv")
