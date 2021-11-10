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
    static deleteVertexMetadata(vertex, metadataObject) {
        let toParametriseUrlFragment = configs['endpoints']['deleteVertexMetadata'] ;

        let parametrisedUrlFragment = toParametriseUrlFragment.replace(/{vertex}/g, String(vertex));
        parametrisedUrlFragment = parametrisedUrlFragment.replace(/{type}/g, String(metadataObject['type']));
        parametrisedUrlFragment = parametrisedUrlFragment.replace(/{value}/g, String(metadataObject['value']));

        return configs['endpoints']['base'] + parametrisedUrlFragment;
    }

    static graphs(galleryType) {
        let toParametriseUrlFragment = configs['endpoints']['availableGraphs'];
        let parametrisedUrlFragment = toParametriseUrlFragment.replace(/{galleryType}/g, String(galleryType));
        return configs['endpoints']['base'] + parametrisedUrlFragment
    }

    static autocompletionTerms(graphId) {
        let toParametriseUrlFragment = configs['endpoints']['autocompletionTerms'];
        let parametrisedUrlFragment = toParametriseUrlFragment.replace(/{graphId}/g, String(graphId));
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

    static edges(graphId, vertex){
        let toParametriseUrlFragment = configs['endpoints']['edges']
        let parametrisedUrlFragment = toParametriseUrlFragment.replace(/{graphId}/g, graphId);
        parametrisedUrlFragment = parametrisedUrlFragment.replace(/{vertex}/g, vertex);
        return configs['endpoints']['base'] + parametrisedUrlFragment;
    }

    static getGalleryCategories() {
        return configs['endpoints']['base'] + configs['endpoints']['galleryCategories'];
    }

    static graphConfiguration(graphId){
        let toParametriseUrlFragment = configs['endpoints']['graphConfiguration'];
        let parametrisedUrlFragment = toParametriseUrlFragment.replace(/{graphId}/g, String(graphId));
        return configs['endpoints']['base'] + parametrisedUrlFragment
    }
}

export default UrlComposer;