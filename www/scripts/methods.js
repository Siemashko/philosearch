async function reloadSearchHistory(contains = "") {
    searchResults = await getSearchResults(contains);
    document.getElementById("search_history").innerHTML = "";
    searchResults.forEach(searchResult => addSearchResultToList(searchResult));
}

async function reloadPhilosophersList() {
    if (philosophersList.length === 0) {
        philosophersList = await findAllPhilosophers();
    }
    document.getElementById("philosophers").innerHTML = "";
    philosophersList.forEach(philosopherBrief => addPhilosopherBriefToList(philosopherBrief));
}

async function initializeApplication() {
    reloadSearchHistory();
    reloadPhilosophersList();
}

async function reloadSearchHistoryDelayed() {
    clearTimeout(delayTimer);
    delayTimer = setTimeout(function() {
        searchInput = document.getElementById("search_input");
        reloadSearchHistory(searchInput.value);
    }, 500);
}

function addSearchResultToList(searchResult) {
    if (searchResult.query.length === 0) {
        return
    }
    var searchResultList = document.getElementById("search_history");
    var listElement = document.createElement("li");
    listElement.id = searchResult.queryId;
    listElement.innerHTML = "<a>" + searchResult.timestamp + "</br>" + searchResult.query + "</a>";
    listElement.addEventListener("click", insertSearchResultQuery);
    searchResultList.append(listElement);
}

function insertSearchResultQuery(e) {
    value = e.target.innerHTML;
    query = value.substr(23);
    console.log(query);
    searchInput = document.getElementById("search_input");
    searchInput.value = query;
}

function parseEra(era) {
    return era.substr(28).replaceAll("_", " ");
}

function addPhilosopherBriefToList(philosopherBrief) {
    var philosophersHTMLList = document.getElementById("philosophers");
    var listElement = document.createElement("li");
    listElement.id = philosopherBrief.philosopher.value;
    pid = philosopherBrief.philosopher.value.substr(27);
    listElement.innerHTML = '<a href="person.html?pid=' + philosopherBrief.philosopher.value.substr(27) + '">' + philosopherBrief.name.value + "</br>" + parseEra(philosopherBrief.era.value) + "</a>";
    // listElement.addEventListener("click", runQuery);
    philosophersHTMLList.append(listElement);
}

async function runQuery(e) {
    console.log("click");
    searchInput = document.getElementById("search_input");
    loader = document.getElementById("loader");
    loader.style.visibility = "visible";
    philosophersList = await runSearchQuery('"' + searchInput.value + '"');
    loader.style.visibility = "hidden";
    initializeApplication();
}

document.addEventListener("DOMContentLoaded", initializeApplication);

document.addEventListener("DOMContentLoaded", function() {
    var searchInput = document.getElementById("search_input");

    // Execute a function when the user releases a key on the keyboard
    searchInput.addEventListener("keyup", function(event) {
        // Number 13 is the "Enter" key on the keyboard
        if (event.keyCode === 13) {
            // Trigger the button element with a click
            document.getElementById("search_button").click();
        }
    });
});