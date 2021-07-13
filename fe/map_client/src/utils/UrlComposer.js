const configs = require('configurations')

class UrlComposer {
    static verticesMetadata(graphName){
        return configs['endpoints']['base'] + configs['endpoints']['verticesMetadata'] + "/" + graphName
    }

    static graphMetadata(graphName){
        return configs['endpoints']['base'] + configs['endpoints']['graphMetadata'] + "/" + graphName
    }

    static proximityClick(graphName, x, y){
        if(! typeof x === 'number' || Number.isInteger(x)){
            throw "You need to pass a float"
        }
        if(! typeof y === 'number' || Number.isInteger(y)){
            throw "You need to pass a float"
        }
        return configs['endpoints']['base'] + configs['endpoints']['proximityClick'] + "/" + graphName + "/" + x + "/" + y
    }

    /**
     * Returns the URL to fetch tiles. The random int purpose is to force the broswer to NOT CACHE.
     * @param graphName
     * @returns {string}
     */
    static tileLayerUrl(graphName) {
        return configs['endpoints']['base'] +
            configs['endpoints']['tile'] + "/" +
            graphName +
            '/{z}/{x}/{y}.png?{randint}'
    }

    static matchingVertices(graphName, metadataObject) {
        return configs['endpoints']['base'] +
            configs['endpoints']['matchingVertex'] + "/" +
            graphName + "/" +
            metadataObject['metadata_type'] + "/" +
            metadataObject['metadata_value'];
    }

    static addVertexMetadata(eth, metadataValue, metadataType) {
        return configs['endpoints']['base'] +
            configs['endpoints']['addVertexMetadata'] + "/" +
            eth + "/" +
            metadataValue + "/" +
            metadataType;
    }
}

export default UrlComposer;