let configs = require('configurations');

class UrlComposer {
    static verticesMetadata(graphName){
        return configs['endpoints']['base'] + configs['endpoints']['vertices_metadata'] + "/" + graphName
    }

    static graphMetadata(graphName){
        return configs['endpoints']['base'] + configs['endpoints']['graph_metadata'] + "/" + graphName
    }
}

export default UrlComposer;