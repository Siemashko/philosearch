class PhilosopherBrief {
    constructor(name, philosopher, dbpedia_philosopher, sortby, born, died, era, notableIdeas) {
        this.name = name;
        this.philosopher = philosopher;
        this.dbpedia_philosopher = dbpedia_philosopher;
        this.sortby = sortby;
        this.born = born;
        this.died = died;
        this.era = era;
        this.notableIdeas = notableIdeas;
    }
}

class PhilosopherDetails {
    constructor(dbpedia, wikidata, image, name, born, died, abstract, era, notableWorks, notableIdeas, thoughts, agreedWith, disagreedWith) {
        this.dbpedia = dbpedia;
        this.wikidata = wikidata;
        this.image = image;
        this.name = name;
        this.born = born;
        this.died = died;
        this.abstract = abstract;
        this.era = era;
        this.notableWorks = notableWorks;
        this.notableIdeas = notableIdeas;
        this.thoughts = thoughts;
        this.agreedWith = agreedWith;
        this.disagreedWith = disagreedWith;
    }
}

class SearchResults {
    constructor(timestamp, queryId, query) {
        this.timestamp = timestamp;
        this.queryId = queryId;
        this.query = query;
    }
}