export function symmetricDifference(setA, setB) {
    /**
     * Given 2 js lists returns the set difference
     * @type {Set<any>}
     * @private
     */
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