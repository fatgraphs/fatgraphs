import UrlComposer from "./utils/UrlComposer";

const configs = require("configurations")

// Interaction with the server happens via methods defined here

export function fetchClosestPoint(graph_name, graph_coordinate) {

    let url = UrlComposer.proximityClick(graph_name, graph_coordinate[0], graph_coordinate[1]);
    return fetch(url)
        .then(response =>
            response.json())
        .then(data => {
            return data
        })
}

export function fetchGraphs() {
    let url = configs['endpoints']['base'] + configs['endpoints']['available_graphs'];
    return fetch(url)
        .then(response =>
            response.json())
        .then(data => {
            return data
        })
}

export function fetchEdgePlots(graph_name, max_zoom) {
    let fetches = []
    for (let zoom_level = 0; zoom_level < max_zoom; zoom_level++) {
        let name_zoom = "/" + graph_name + "/" + zoom_level + "?" + Math.floor(Math.random() * 2000) + 1;
        let url = configs['endpoints']['base'] + configs['endpoints']['edge_distributions'] + name_zoom;
        fetches.push(fetch(url)
            .then(response => {
                return response.blob();
            })
            .then(data => {
                return {
                    zl: zoom_level,
                    data: data
                };
            }));
    }
    return Promise.all(fetches);
}


export function fetchGraphMetadata(graph_name) {
    let url = UrlComposer.graphMetadata(graph_name);
    return fetch(url)
        .then(response =>
            response.json())
        .then(data => {
            return data
        })
}

export function fetchAutocompletionTerms() {
    let url = configs['endpoints']['base'] + configs['endpoints']['autocompletion_terms']
    return fetch(url)
        .then(response =>
            response.json())
        .then(data => {
            return data
        })

}

export function post_recent_tag(tag_object) {
    let url = configs['endpoints']['base'] + configs['endpoints']['user_recent_tags'];
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(tag_object)
    })
        .then(response =>
            response.json())
        .then(data => {
            console.log(data)
            return data
        })

}

export function fetch_recent_tags(){
    let url = configs['endpoints']['base'] + configs['endpoints']['user_recent_tags'];
    return fetch(url)
        .then(response =>
            response.json())
        .then(data => {
            return data
        })
}

export function fetch_matching_vertices(graph_name, tag_object){
    let url = UrlComposer.matching_vertices(graph_name, tag_object);
    return fetch(url)
        .then(response => {
            console.log(response)
            return response.json()
        })
        .then(data => {
            console.log(data)
            return data
        })
}