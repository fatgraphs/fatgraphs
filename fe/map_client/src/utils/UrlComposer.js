const configs = require('configurations')

class UrlComposer {
    static verticesMetadata(graph_name){
        return configs['endpoints']['base'] + configs['endpoints']['vertices_metadata'] + "/" + graph_name
    }

    static graphMetadata(graph_name){
        return configs['endpoints']['base'] + configs['endpoints']['graph_metadata'] + "/" + graph_name
    }

    static proximityClick(graph_name, x, y){
        if(! typeof x === 'number' || Number.isInteger(x)){
            throw "You need to pass a float"
        }
        if(! typeof y === 'number' || Number.isInteger(y)){
            throw "You need to pass a float"
        }
        return configs['endpoints']['base'] + configs['endpoints']['proximity_click'] + "/" + graph_name + "/" + x + "/" + y
    }

    /**
     * Returns the URL to fetch tiles. The random int purpose is to force the broswer to NOT CACHE.
     * @param graph_name
     * @returns {string}
     */
    static tileLayerUrl(graph_name) {
        return configs['endpoints']['base'] +
            configs['endpoints']['tile'] + "/" +
            graph_name +
            '/{z}/{x}/{y}.png?{randint}'
    }
}

export default UrlComposer;