import React from "react";

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

