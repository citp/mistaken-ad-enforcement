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
        return self.country.permitrate * self.election.permitrate * \
            self.party.permitrate * self.ad_type.permitrate


class Simulation:
    

    def __init__(self, observations, countries, elections, parties, ad_types, title):
        self.observations = observations
        self.countries = countries
        self.elections = elections
        self.parties = parties
        self.ad_types = ad_types
        self.title = title

        
    def get_permitted(self, persona):
        permitted = np.random.binomial(1,persona.get_permitrate(), size=self.observations)
        return permitted

    
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
            writer.writerow(["Label","Characteristic", "Permitrate"])
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
    nonally = Characteristic("persona.NonAlly", 0.25)
    
    ## AD TYPE 
    nonpolitical_issue = Characteristic("non-political issue", 0.95)   
    political_issue = Characteristic("political issue", 0.75)

    ## ELECTION
    state = Characteristic("state", 0.9)
    fed = Characteristic("federal", 0.75)

    ## PARTY
    republican = Characteristic("republican", 1.0)
    democrat = Characteristic("democrat", 1.0)

    ## CONSTRUCT GROUPS FROM PERSONA, AD TYPE, ELECTION, PARTY
    countries = [us, nonally]
    elections = [fed, state]
    parties   = [republican, democrat]
    ad_types = [political_issue, nonpolitical_issue]

    title = "Simulation of ads being permitted with expected probabilities"
    simulation = Simulation(observations, countries, elections, parties, ad_types, title)
    simulation.write_ground_truth("csv/simulation-simple-truth.csv")
    simulation.write_simulation("csv/simulation-simple.csv")
