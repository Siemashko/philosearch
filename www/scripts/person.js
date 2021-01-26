function getParams(url) {
    var params = {};
    var parser = document.createElement('a');
    parser.href = url;
    var query = parser.search.substring(1);
    var vars = query.split('&');
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        params[pair[0]] = decodeURIComponent(pair[1]);
    }
    return params;
}

async function initializePersonPage() {
    params = getParams(window.location.href);

    philosopherDetails = await getPhilosopherDetails(params.pid);
    console.log(philosopherDetails);
    details = document.getElementById("details");
    newline = document.createElement("br");
    var image = document.createElement("img");
    image.src = philosopherDetails.image.value;
    image.alt = philosopherDetails.name.value;
    image.width = 180;
    // searchResults.forEach(searchResult => addSearchResultToList(searchResult));
    // philosophersList.forEach(philosopherBrief => addPhilosopherBriefToList(philosopherBrief));
    details.append(image);
    details.append(newline);
    var name = document.createElement("h2");
    name.style = "float: right; padding: -5px";
    name.innerHTML = philosopherDetails.name.value;
    details.append(name);
    // details.append(newline);

    var other = document.createElement("h5");
    other.style = "float: right; text-align: right";
    var born;
    if (philosopherDetails.born && parseInt(philosopherDetails.born.value) < 0) {
        born = Math.abs(parseInt(philosopherDetails.born.value));
        bornYear = born + " BC";
    } else if (philosopherDetails.born) {
        bornYear = philosopherDetails.born.value;
    } else {
        bornYear = "unknown";
    }
    if (philosopherDetails.died && parseInt(philosopherDetails.died.value) < 0) {
        died = Math.abs(parseInt(philosopherDetails.died.value));
        diedYear = died + " BC"
    } else if (philosopherDetails.died) {
        diedYear = philosopherDetails.died.value;
    } else {
        diedYear = "present"
    }

    other.innerHTML = bornYear + " - " + diedYear;

    other.innerHTML += '</br><a href="' + philosopherDetails.era.value + '">' + philosopherDetails.era.value.substr(28).replaceAll("_", " ") + '<a/>';
    details.append(other);

    other.innerHTML += '</br></br><a href="' + philosopherDetails.dbpedia.value + '">' + "DBPedia" + '<a/>';
    other.innerHTML += '</br></br><a href="' + philosopherDetails.wikidata.value + '">' + "Wikidata" + '<a/>';

    section = document.getElementById("informations");

    var headerAbstract = document.createElement("h2");
    headerAbstract.innerHTML = "Description";
    section.append(headerAbstract);

    var abstract = document.createElement("p");
    abstract.innerHTML = philosopherDetails.abstract.value;
    section.append(abstract);
    var hrline = document.createElement("hr");
    hrline.style = '<hr style="width:50%;text-align:left;margin-left:0">';
    section.append(hrline);

    var headerMainThoughts = document.createElement("h2");
    headerMainThoughts.innerHTML = "Main thoughts";
    var thoughtsHTMLList = document.createElement("ul");
    for (var i = 0; i < philosopherDetails.thoughts.length; i++) {
        var thought = philosopherDetails.thoughts[i];
        var listElement = document.createElement("li")
        line = thought.line.value;
        reference = thought.reference.value;
        categories = thought.category;
        listElement.innerHTML = "Category: " + [...new Set(categories)].map(category => "<b>" + category.value + "</b>").join(", ") + ": ";
        listElement.innerHTML += line + "<br/>";
        listElement.innerHTML += "<i>" + reference + "</i><br/><br/><br/>";
        thoughtsHTMLList.append(listElement);
    }
    section.append(headerMainThoughts);
    section.append(thoughtsHTMLList);

    hrline = document.createElement("hr");
    hrline.style = '<hr style="width:50%;text-align:left;margin-left:0">';
    section.append(hrline);


    var headerNotableIdeas = document.createElement("h2");
    headerNotableIdeas.innerHTML = "Notable Ideas";
    var notableIdeasHTMLList = document.createElement("ul");
    for (var i = 0; i < philosopherDetails.notableIdeas.length; i++) {
        var notableIdea = philosopherDetails.notableIdeas[i];
        var listElement = document.createElement("li");
        listElement.innerHTML = '<a href="' + notableIdea.value + '">' + notableIdea.value.substr(28).replaceAll("_", " ") + "</a>";
        notableIdeasHTMLList.append(listElement);
    }
    section.append(headerNotableIdeas);
    section.append(notableIdeasHTMLList);

    hrline = document.createElement("hr");
    hrline.style = '<hr style="width:50%;text-align:left;margin-left:0">';
    section.append(hrline);

    var headerDisagreedWith = document.createElement("h2");
    headerDisagreedWith.innerHTML = "Disagreed with";
    var disagreedWithHTMLList = document.createElement("ul");
    for (var i = 0; i < philosopherDetails.disagreedWith.length; i++) {
        var disagreement = philosopherDetails.disagreedWith[i];
        var listElement = document.createElement("li");
        var value = '<a href="person.html?pid=' + disagreement.subjectN.value.substr(27) + '">' + disagreement.nameN.value + '</a>';
        listElement.innerHTML = value;
        disagreedWithHTMLList.append(listElement);
    }
    section.append(headerDisagreedWith);
    section.append(disagreedWithHTMLList);

    hrline = document.createElement("hr");
    hrline.style = '<hr style="width:50%;text-align:left;margin-left:0">';
    section.append(hrline);

    var headerAgreedWith = document.createElement("h2");
    headerAgreedWith.innerHTML = "Agreed with";
    var agreedWithHTMLList = document.createElement("ul");
    for (var i = 0; i < philosopherDetails.agreedWith.length; i++) {
        var agreement = philosopherDetails.agreedWith[i];
        var listElement = document.createElement("li");
        var value = '<a href="person.html?pid=' + agreement.subjectP.value.substr(27) + '">' + agreement.nameP.value + "</a>";
        listElement.innerHTML = value;
        agreedWithHTMLList.append(listElement);
    }
    section.append(headerAgreedWith);
    section.append(agreedWithHTMLList);

    hrline = document.createElement("hr");
    hrline.style = '<hr style="width:50%;text-align:left;margin-left:0">';
    section.append(hrline);
}

document.addEventListener("DOMContentLoaded", initializePersonPage);