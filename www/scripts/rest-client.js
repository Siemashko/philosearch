async function findAllPhilosophers() {
    const responseJson = await fetch(restServiceUrl + "/philosophers").then(response => response.json());
    return [...new Set(responseJson.map(philosopherBrief => Object.assign(new PhilosopherBrief, philosopherBrief)))];
}

async function runSearchQuery(query) {
    const responseJson = await fetch(restServiceUrl + "/search?query=" + query).then(response => response.json());
    return [...new Set(responseJson.map(philosopherBrief => Object.assign(new PhilosopherBrief, philosopherBrief)))];
}

async function getPhilosopherDetails(philosopherId) {
    const responseJson = await fetch(restServiceUrl + "/philosophers/" + philosopherId).then(response => response.json());
    return Object.assign(new PhilosopherDetails, responseJson);
}

async function getSearchResults(contains) {
    const responseJson = await fetch(restServiceUrl + "/search_results?contains=" + contains).then(response => response.json());
    return [...new Set(responseJson.map(searchResults => Object.assign(new SearchResults, searchResults)))];
}