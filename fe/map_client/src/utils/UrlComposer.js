const configs = require('configurations')

class UrlComposer {
    static verticesMetadata(graphName) {
        return configs['endpoints']['base'] + configs['endpoints']['verticesMetadata'] + "/" + graphName
    }

    static graph(graphId) {
        let toParametriseUrlFragment = configs['endpoints']['graphById'];
        let parametrisedUrlFragment = toParametriseUrlFragment.replace(/{graphId}/g, graphId)
        return configs['endpoints']['base'] + parametrisedUrlFragment
    }

    static closestPoint(graphId, x, y) {
        let toParametriseUrlFragment = configs['endpoints']['closestPoint'];
        let parametrisedUrlFragment = toParametriseUrlFragment.replace(/{graphId}/g, String(graphId));
        parametrisedUrlFragment = parametrisedUrlFragment.replace(/{x}/g, x);
        parametrisedUrlFragment = parametrisedUrlFragment.replace(/{y}/g, y);
        console.log("parametrisedUrlFragment " , parametrisedUrlFragment)
        return configs['endpoints']['base'] + parametrisedUrlFragment
    }

    /**
     * Returns the URL to fetch tiles. The random int purpose is to force the broswer to NOT CACHE.
     * @param graphName
     * @returns {string}
     */
    static tileLayer(graphId, z, x, y) {
        let toParametriseUrlFragment = configs['endpoints']['tile'];
        let parametrisedUrlFragment = toParametriseUrlFragment.replace(/{graphId}/g, graphId)
        if(z !== undefined && x !== undefined && y !== undefined){
            parametrisedUrlFragment = parametrisedUrlFragment.replace(/{z}/g, z)
            parametrisedUrlFragment = parametrisedUrlFragment.replace(/{x}/g, x)
            parametrisedUrlFragment = parametrisedUrlFragment.replace(/{y}/g, y)
        }
        return configs['endpoints']['base'] + parametrisedUrlFragment
    }

    static matchingVertices(metadataObject, graphId) {
        let metaType = metadataObject['type'];
        let toParametriseUrlFragment = configs['endpoints']['matchingVertex'][metaType];
        let parametrisedUrlFragment = toParametriseUrlFragment.replace(/{value}/g, metadataObject['value'])
        return configs['endpoints']['base'] + parametrisedUrlFragment + '?graphId=' + graphId
    }

    static addVertexMetadata() {
        return configs['endpoints']['base'] + configs['endpoints']['addVertexMetadata'] ;
    }

    static graphs() {
        return configs['endpoints']['base'] + configs['endpoints']['availableGraphs'];
    }

    static autocompletionTerms(page) {
        let toParametriseUrlFragment = configs['endpoints']['autocompletionTerms'];
        let parametrisedUrlFragment = toParametriseUrlFragment.replace(/{page}/g, String(page));
        return configs['endpoints']['base'] + parametrisedUrlFragment
    }

    static user(userName){
        let toParametriseUrlFragment = configs['endpoints']['user']
        let parametrisedUrlFragment = toParametriseUrlFragment.replace(/{userName}/g, userName);
        return configs['endpoints']['base'] + parametrisedUrlFragment;
    }

    static recentMetadataSearches(){
        return configs['endpoints']['base'] + configs['endpoints']['recentMetadataSearches'];
    }

    static edgePlot(graphId, zoom_level) {
        let toParametriseUrlFragment = configs['endpoints']['edgePlot']
        let parametrisedUrlFragment = toParametriseUrlFragment.replace(/{graphId}/g, graphId);
        parametrisedUrlFragment = parametrisedUrlFragment.replace(/{z}/g, zoom_level);
        return configs['endpoints']['base'] +parametrisedUrlFragment;
    }
}

export default UrlComposer;