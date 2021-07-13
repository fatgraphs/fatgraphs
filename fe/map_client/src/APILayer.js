import UrlComposer from "./utils/UrlComposer";

const configs = require("configurations")

// Interaction with the server happens via methods defined here

function doRequest(url, options) {
    return fetch(url, options)
        .then(response =>
            response.json())
        .then(data => {
            return data
        })
}

export function fetchClosestPoint(graphName, graphCoordinate) {
    let url = UrlComposer.proximityClick(graphName, graphCoordinate[0], graphCoordinate[1]);
    return doRequest(url, {});
}

export function fetchGraphs() {
    let url = configs['endpoints']['base'] + configs['endpoints']['availableGraphs'];
   return doRequest(url, {});
}

export function fetchEdgePlots(graphName, maxZoom) {
    let fetches = []
    for (let zoomLevel = 0; zoomLevel < maxZoom; zoomLevel++) {
        let nameZoom = "/" + graphName + "/" + zoomLevel + "?" + Math.floor(Math.random() * 2000) + 1;
        let url = configs['endpoints']['base'] + configs['endpoints']['edgeDistributions'] + nameZoom;
        fetches.push(fetch(url)
            .then(response => {
                return response.blob();
            })
            .then(data => {
                return {
                    zl: zoomLevel,
                    data: data
                };
            }));
    }
    return Promise.all(fetches);
}


export function fetchGraphMetadata(graphName) {
    let url = UrlComposer.graphMetadata(graphName);
    return doRequest(url, {});
}

export function fetchAutocompletionTerms() {
    let url = configs['endpoints']['base'] + configs['endpoints']['autocompletionTerms']
    return doRequest(url, {});
}

export function postRecentMetadata(metadataObject) {
    let url = configs['endpoints']['base'] + configs['endpoints']['userRecentMetadataSearches'];
    let init = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(metadataObject)
    };
    return doRequest(url, init);
}

export function fetchRecentMetadataSearches(){
    let url = configs['endpoints']['base'] + configs['endpoints']['userRecentMetadataSearches'];
    return doRequest(url, {});
}

export function fetchMatchingVertices(graphName, metadataObject){
    let url = UrlComposer.matchingVertices(graphName, metadataObject);
    return doRequest(url, {});
}

export function postVertexMetadata(eth, metadataValue, metadataType){
    let url = UrlComposer.addVertexMetadata(eth, metadataValue, metadataType);
    return doRequest(url, {});
}