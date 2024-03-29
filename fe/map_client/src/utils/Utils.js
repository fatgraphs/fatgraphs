import React from "react";
import qs from "query-string";

export function symmetricDifference(a, b) {
    /**
     * Given 2 js lists returns the set difference
     * @type {Set<any>}
     * @private
     */
    let setA = new Set(a)
    let setB = new Set(b)
    let _difference = new Set(setA)
    for (let elem of setB) {
        if (_difference.has(elem)) {
            _difference.delete(elem)
        } else {
            _difference.add(elem)
        }
    }
    return _difference
}

export function generateLargeRandom() {
    return Math.floor(Math.random() * 200000) + 1;
}

export function truncateEth(string, _len){
    if (! string) {
        return ""
    }
    let len = _len | 4;

    let prefix = string.slice(0, len)
    if  (string.slice(0,2).toLowerCase() === '0x'){
        prefix = string.slice(0, len + 2)
    }
    let suffix = string.slice(string.length - len, string.length)
    return prefix + '...' + suffix;
}


export function hashVertexToInt(vertex){
    let byteArray = new TextEncoder().encode(vertex);
    return byteArray.reduceRight((a, b)=>a+b)
}

export function updateBrowserUrlQueryParam(props, newQueryParam, push = true) {

    // when  navigating back we don't want to push  the same path, even without this check react-router won't allow us to
    // push an existing path; I want to prevent warning messages on the console
    let isPathAlreadyPushed = true;
    for (const key of Object.keys(newQueryParam)) {
        isPathAlreadyPushed &= newQueryParam[key] === getQueryParam(props, key)
    }

    if(isPathAlreadyPushed){
        return;
    }

    console.log(`${push ? 'pushing' : 'replacing'} url xyz to history: `, newQueryParam)
    const queryParams = qs.parse(props.location.search);
    const newQueries = {...queryParams, ...newQueryParam};
    if (push) {
        props.history.push({search: qs.stringify(newQueries)})
    } else {
        // doesn't create a new state (back-arrow will ignore it)
        props.history.replace({search: qs.stringify(newQueries)})
    }
}

export function getQueryParam(props, queryParam) {
    return new URLSearchParams(props.location.search).get(queryParam);
}

export function areAlmostIdentical(urlNow, oldUrl) {
    return Math.abs(urlNow['x'] - oldUrl['x']) <= 1
        && Math.abs(urlNow['y'] - oldUrl['y']) <= 1
        && urlNow['z'] === oldUrl['z'];
}