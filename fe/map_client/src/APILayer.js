import UrlComposer from "./utils/UrlComposer";
import Graph from "./model/graph";

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

export function fetchClosestPoint(graphId, graphCoordinate) {
    let url = UrlComposer.closestPoint(graphId, graphCoordinate[0], graphCoordinate[1]);
    return doRequest(url, {});
}

export async function fetchGraphs() {
    let url = UrlComposer.graphs()
    let response = await doRequest(url, {});
    return response.map(raw => new Graph(raw))
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


export function fetchGraph(graphId) {
    let url = UrlComposer.graph(graphId);
    return doRequest(url, {});
}

export function fetchAutocompletionTerms(page) {
    let url = UrlComposer.autocompletionTerms(page)
    return doRequest(url, {});
}

export function postRecentMetadataSearches(metadataObject) {
    let url = UrlComposer.recentMetadataSearches()
    let init = {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(metadataObject)
    };
    return doRequest(url, init);
}

export function fetchUser(userName) {
    let url = UrlComposer.user(userName)
    return doRequest(url, {});
}

export function fetchMatchingVertices(graphId, metadataObject) {
    let url = UrlComposer.matchingVertices(metadataObject, graphId);
    return doRequest(url);
}

export function postVertexMetadata(eth, metadataObject) {
    let url = UrlComposer.addVertexMetadata();
    let type = metadataObject['type'];
    let value = metadataObject['value'];
    let init = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "eth": eth,
            "type": type === 'type' ? value : '',
            "label": type === 'label' ? value : '',
            "description": ""
        })
    }
    return doRequest(url, init);
}

export function fetchRecentMetadata() {
    let url = UrlComposer.recentMetadataSearches();
    return doRequest(url, {});
}