import json
import rdflib
import sys

def extractPhilosopherInfo(pd, output=sys.stdout):
    people = pd["people"]
    for p in people:
        id = p["id"]
        name = p["name"]
        time = p["time"]
        if time[-2:]=="BC":
            if time=="5th century BC":
                born = 500
                died = 401
            else:
                born, died = time[:-3].split("–")
            born, died = -int(born), -int(died)
        else:
            dates = time.split("–")
            if len(dates) > 1:
                born, died = dates[0], dates[1]
            else:
                born, died = dates[0], None
        # loc = p["loc"]
        sortby = p["sortby"]
        rdf_id = f"p:p{id}"
        info_rdf_record = f"{rdf_id} a schema:Person .\n"
        info_rdf_record += f"{rdf_id} r:name \"{name}\"@en .\n"
        info_rdf_record += f"{rdf_id} r:born {born} .\n"
        if died is not None:
            info_rdf_record += f"{rdf_id} r:died {died} .\n"
        info_rdf_record += f"{rdf_id} r:sortby \"{sortby}\"@en .\n"
        print(info_rdf_record, file=output)

def extractThoughts(pd, output=sys.stdout):
    cat_dictionary = {
        "on": "Ontology",
        "ep": "Epistemology",
        "et": "Ethics",
        "ae": "Aesthetics",
        "po": "Political Philosophy",
        "th": "Theology"
    }
    thoughts = pd["records"]
    for t in thoughts:
        id = t["id"]
        pid = t["person"]
        order = t["order"]
        line = t["line"]
        line = line.replace("\"", "\\\"")
        reference = t["reference"]
        reference = reference.replace("\"", "\\\"")
        cats = t["cats"]
        rdf_id = f"t:t{id}"
        thought_rdf_record = f"p:p{pid} r:said {rdf_id} .\n"
        thought_rdf_record += f"{rdf_id} r:value \"{line}\"@en .\n"
        thought_rdf_record += f"{rdf_id} r:reference \"{reference}\"@en .\n"
        thought_rdf_record += f"{rdf_id} r:order \"{order}\"@en .\n"
        for c in cats:
            thought_rdf_record += f"{rdf_id} r:category \"{cat_dictionary[c]}\"@en .\n"
        print(thought_rdf_record, file=output)

def extractRelations(pd, output=sys.stdout):
    relations = pd["links"]
    for r in relations:
        p0 = r["l0"]
        p1 = r["l1"]
        type = r["type"]
        if type=="p":
            relations_rdf_record = f"t:t{p0} r:agreedWith t:t{p1} .\nt:t{p1} r:agreedWith t:t{p0} ."
        else:
            relations_rdf_record = f"t:t{p0} r:disagreedWith t:t{p1} .\nt:t{p1} r:disagreedWith t:t{p0} ."
        print(relations_rdf_record, file=output)

with open("philosophers.json", "r") as input:
    philosophers = json.load(input)

print(philosophers.keys())


file_head = \
"""@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix schema: <http://schema.org/> .

@prefix p: <http://philo.search/person/> .
@prefix r: <http://philo.search/property/> .
@prefix t: <http://philo.search/thought/> .
"""
with open("philosophers.ttl", "w") as output:
    print(file_head, file=output)
    extractPhilosopherInfo(philosophers, output=output)
    extractThoughts(philosophers, output=output)
    extractRelations(philosophers, output=output)