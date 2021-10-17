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

export function updateQueryParam(props, newQueryParam){
    console.log("newQueryParam ", newQueryParam)
    const queryParams = qs.parse(props.location.search);
    console.log("queryParams ", queryParams)
    const newQueries = { ...queryParams, ...newQueryParam};
    props.history.push({ search: qs.stringify(newQueries) })
}