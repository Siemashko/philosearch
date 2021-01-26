from flask import Flask, request
from flask_cors import CORS
import re
from datetime import datetime
import os
import json
import random
import rdflib
import pickle
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://127.0.0.1:3030/Philosophers")

app = Flask(__name__)
CORS(app)

def aggregate_results(results):
    result_dict = {}
    for res in results:
        name = res["name"]["value"]
        if name not in result_dict:
            result_dict[name] = {
                "name": res["name"],
                "philosopher": res["subject"],
                "dbpedia_philosopher": res["dbpedia_subject"],
                "sortby": res["sortby"],
                "born": res["born"],
                "died": res["died"] if "died" in res else None,
                "era" : res["era"],
                "notableIdeas": [res["notableIdea"]]
            }
        else:
            result_dict[name]["notableIdeas"].append(res["notableIdea"])
    return result_dict

def aggregate_philosopher(info_results,
                          image_results,
                          notable_works_results,
                          notable_ideas_results,
                          thoughts_results,
                          agreed_with_results,
                          disagreed_with_results):

    result_dict = {
        "dbpedia": info_results[0]["dbpedia_subject"],
        "wikidata": image_results[0]["wikidata_subject"],
        "image": image_results[0]["image"],
        "name": info_results[0]["name"],
        "born": info_results[0]["born"],
        "died": info_results[0]["died"] if "died" in info_results[0] else None,
        "abstract": info_results[0]["abstract"],
        "era": info_results[0]["era"],
        "notableWorks": notable_works_results[0]["notableWorks"] if len(notable_works_results) > 0 else None,
        "notableIdeas": [], "thoughts": {}, "agreedWith": [], "disagreedWith": []}

    for row in notable_ideas_results:
        result_dict["notableIdeas"].append(row["notableIdea"])

    for row in thoughts_results:
        if row["thought"]["value"] in result_dict["thoughts"]:
            result_dict["thoughts"][row["thought"]["value"]]["category"].append(row["category"])
        else:
            result_dict["thoughts"][row["thought"]["value"]] = row
            result_dict["thoughts"][row["thought"]["value"]]["category"] = [row["category"]]
    result_dict["thoughts"] = list(result_dict["thoughts"].values())

    for row in agreed_with_results:
        result_dict["agreedWith"].append(row)

    for row in disagreed_with_results:
        result_dict["disagreedWith"].append(row)

    return result_dict

def get_image_results(philosopher_id):
    sparql_image_query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        prefix p: <http://philo.search/person/>
        prefix r: <http://philo.search/property/>
        SELECT DISTINCT ?name ?image ?wikidata_subject
           WHERE {
              p:""" + philosopher_id + """ r:name ?name .

              SERVICE <https://query.wikidata.org/sparql> {
                ?wikidata_subject rdfs:label ?name ;
                                  wdt:P18 ?image .
              }
          }
    """
    print(sparql_image_query)
    sparql.setQuery(sparql_image_query)
    sparql.setReturnFormat(JSON)
    image_results = sparql.query().convert()
    return image_results["results"]["bindings"]

def get_info_results(philosopher_id):
    sparql_info_query = """
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX dbp: <http://dbpedia.org/property/>
        prefix p: <http://philo.search/person/>
        prefix r: <http://philo.search/property/>
        SELECT DISTINCT ?name ?born ?died
                        ?dbpedia_subject ?abstract ?era 
           WHERE {
              p:""" + philosopher_id + """ r:name ?name ;
                       r:born ?born ;

              OPTIONAL {p:""" + philosopher_id + """ r:died ?died}

              SERVICE <http://dbpedia.org/sparql> {
                ?dbpedia_subject dbp:name ?name ;
                                 dbo:abstract ?abstract ;
                                 dbo:era ?era .
                FILTER (LANGMATCHES(LANG(?abstract), "en") && LANGMATCHES(LANG(?name), "en"))
              }
          }
        """
    sparql.setQuery(sparql_info_query)
    sparql.setReturnFormat(JSON)
    info_results = sparql.query().convert()
    return info_results["results"]["bindings"]

def get_notable_works_results(philosopher_id):
    sparql_notable_works_query = """
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX dbr: <http://dbpedia.org/resource/>
            PREFIX dbp: <http://dbpedia.org/property/>
            prefix p: <http://philo.search/person/>
            prefix r: <http://philo.search/property/>
            SELECT DISTINCT ?name ?notableWorks
               WHERE {
                  p:""" + philosopher_id + """ r:name ?name ;
                  SERVICE <http://dbpedia.org/sparql> {
                    ?dbpedia_subject dbp:name ?name ;
                                     dbp:notableWorks ?notableWorks .
                  }
              }
            """
    sparql.setQuery(sparql_notable_works_query)
    sparql.setReturnFormat(JSON)
    notable_works_results = sparql.query().convert()
    return notable_works_results["results"]["bindings"]

def get_notable_ideas_results(philosopher_id):
    sparql_notable_ideas_query = """
                PREFIX dbo: <http://dbpedia.org/ontology/>
                PREFIX dbr: <http://dbpedia.org/resource/>
                PREFIX dbp: <http://dbpedia.org/property/>
                prefix r: <http://philo.search/property/>
                prefix p: <http://philo.search/person/>
                SELECT DISTINCT ?name ?notableIdea
                   WHERE {
                      p:""" + philosopher_id + """ r:name ?name ;
                      SERVICE <http://dbpedia.org/sparql> {
                        ?dbpedia_subject dbp:name ?name ;
                                         dbo:notableIdea ?notableIdea .
                      }
                  }
                """
    sparql.setQuery(sparql_notable_ideas_query)
    sparql.setReturnFormat(JSON)
    notable_ideas_results = sparql.query().convert()
    return notable_ideas_results["results"]["bindings"]

def get_thoughts_results(philosopher_id):
    sparql_thoughts_query = """
                PREFIX dbo: <http://dbpedia.org/ontology/>
                PREFIX dbr: <http://dbpedia.org/resource/>
                PREFIX dbp: <http://dbpedia.org/property/>
                prefix r: <http://philo.search/property/>
                prefix p: <http://philo.search/person/>
                SELECT DISTINCT ?name ?thought ?line ?reference ?category
                   WHERE {
                      p:""" + philosopher_id + """ r:name ?name ;
                                                   r:said ?thought .

                      ?thought r:value ?line ;
                               r:reference ?reference ;
                               r:category ?category .
                  }
                """
    sparql.setQuery(sparql_thoughts_query)
    sparql.setReturnFormat(JSON)
    thoughts_results = sparql.query().convert()
    return thoughts_results["results"]["bindings"]

def get_agreed_with_results(philosopher_id):
    sparql_agreed_with_query = """
                PREFIX dbo: <http://dbpedia.org/ontology/>
                PREFIX dbr: <http://dbpedia.org/resource/>
                PREFIX dbp: <http://dbpedia.org/property/>
                prefix r: <http://philo.search/property/>
                prefix p: <http://philo.search/person/>
                SELECT DISTINCT ?name ?subjectP ?nameP
                   WHERE {
                      p:""" + philosopher_id + """ r:name ?name ;
                               r:said ?thought .
        
                      ?thought r:agreedWith ?thoughtP .
        
                      ?subjectP r:said ?thoughtP ;
                                r:name ?nameP ;
        
                  }
        """
    sparql.setQuery(sparql_agreed_with_query)
    sparql.setReturnFormat(JSON)
    agreed_with_results = sparql.query().convert()
    return agreed_with_results["results"]["bindings"]

def get_disagreed_with_results(philosopher_id):
    sparql_disagreed_with_query = """
                PREFIX dbo: <http://dbpedia.org/ontology/>
                PREFIX dbr: <http://dbpedia.org/resource/>
                PREFIX dbp: <http://dbpedia.org/property/>
                prefix r: <http://philo.search/property/>
                prefix p: <http://philo.search/person/>
                SELECT DISTINCT ?name ?subjectN ?nameN
                   WHERE {
                      p:""" + philosopher_id + """ r:name ?name ;
                               r:said ?thought .
        
                      ?thought r:disagreedWith ?thoughtN .
        
                      ?subjectN r:said ?thoughtN ;
                                r:name ?nameN ;
        
                  }
        """
    sparql.setQuery(sparql_disagreed_with_query)
    sparql.setReturnFormat(JSON)
    disagreed_with_results = sparql.query().convert()
    return disagreed_with_results["results"]["bindings"]

@app.route("/search")
def query_database():
    def convert_rules_to_filters(rules):
        filters = []
        for rule in rules:
            if re.match("agreed with \w*", rule):
                value = rule[12:]
                filters.append(f'CONTAINS(LCASE(?nameP), "{value}")')
            elif re.match("disagreed with \w*", rule):
                value = rule[15:]
                filters.append(f'CONTAINS(LCASE(?nameN), "{value}")')
            elif re.match("talked about \w*", rule):
                value = rule[13:]
                filters.append(f'CONTAINS(LCASE(?line), "{value}")')
            elif re.match("interested in \w*", rule):
                value = rule[14:]
                filters.append(f'CONTAINS(LCASE(?category), "{value}")')
            elif re.match("lived before \w* bc", rule):
                value = int(rule[13:-3])
                filters.append(f'?born <= {-value}')
            elif re.match("lived after \w* bc", rule):
                value = int(rule[12:-3])
                filters.append(f'?born >= {-value}')
            elif re.match("lived before \w*", rule):
                value = int(rule[13:])
                filters.append(f'?born <= {value}')
            elif re.match("lived after \w*", rule):
                value = int(rule[12:])
                filters.append(f'?born >= {value}')
            else:
                value = rule
                filters.append(f'CONTAINS(LCASE(?name), "{value}")')
        filters = "FILTER (" + " && ".join(filters) + ")"
        return filters
    if request.args.get("query") is not None:
        query = request.args.get("query")[1:-1].lower()
    else:
        query = ""
    rules = re.split("\s*;\s*", query)

    query_identifier = str(sorted(rules))
    filename = f"search_results/{datetime.now().replace(microsecond=0).isoformat()}&{random.randint(10,99)}&{query_identifier}.json"
    previous_results = os.listdir("search_results")
    matching = [match for match in previous_results if match.split("&")[2] == query_identifier + ".json"]
    if len(matching) > 0:
        filename = f"search_results/{matching[0]}"
        with open(filename, "br") as file:
            results = pickle.load(file)
    else:
        filters = convert_rules_to_filters(rules)
        sparql_query = """
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX dbp: <http://dbpedia.org/property/>
        prefix r: <http://philo.search/property/>
        SELECT DISTINCT ?subject ?sortby ?name ?born ?died ?era ?notableIdea ?dbpedia_subject
           WHERE {
              ?subject r:name ?name ;
                       r:born ?born ;
                       r:sortby ?sortby ;
                       r:said ?thought .
                       
              OPTIONAL {?subject r:died ?died}
                       
              ?thought r:value ?line ;
                       r:agreedWith ?thoughtP ;
                       r:disagreedWith ?thoughtN ;
                       r:category ?category .
              
              ?subjectP r:said ?thoughtP ;
                        r:name ?nameP .
              ?subjectN r:said ?thoughtN ;
                        r:name ?nameN .
                        
              SERVICE <http://dbpedia.org/sparql> {
                ?dbpedia_subject dbp:name ?name ;
                                 dbo:era ?era ;
                                 dbo:notableIdea ?notableIdea . 
              }
              """ + filters + "\n}"
        print(sparql_query)
        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
    with open(filename, "bw") as file:
        pickle.dump(results, file)
    qres = results["results"]["bindings"]

    return json.dumps(sorted(list(aggregate_results(qres).values()), key=lambda x: x["sortby"]["value"]))

@app.route("/search_results")
def get_search_result_list():
    def build_query_from_rules(rules):
        parsed_rules = eval(rules)
        return "; ".join(parsed_rules)
    contains = request.args.get("contains")
    result = [{"timestamp": res.split("&")[0],
               "queryId": res.split("&")[0]+"&"+res.split("&")[1],
               "query": build_query_from_rules(res.split("&")[2][:-5])} for res in os.listdir("search_results") if contains in build_query_from_rules(res.split("&")[2][:-5])]

    return json.dumps(sorted(result, key=lambda x: x["timestamp"], reverse=True))

@app.route("/philosophers")
def get_philosophers():
    return query_database()

@app.route("/philosophers/<philosopher_id>")
def get_philosopher(philosopher_id):
    info_results = get_info_results(philosopher_id)
    image_results = get_image_results(philosopher_id)
    notable_works_results = get_notable_works_results(philosopher_id)
    notable_ideas_results = get_notable_ideas_results(philosopher_id)
    thoughts_results = get_thoughts_results(philosopher_id)
    agreed_with_results = get_agreed_with_results(philosopher_id)
    disagreed_with_results = get_disagreed_with_results(philosopher_id)

    result = aggregate_philosopher(info_results,
                                   image_results,
                                   notable_works_results,
                                   notable_ideas_results,
                                   thoughts_results,
                                   agreed_with_results,
                                   disagreed_with_results)

    return json.dumps(result)