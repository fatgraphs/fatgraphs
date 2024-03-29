import React, {Component} from 'react';
import {
    fetchAutocompletionTerms,
    fetchEdges,
    fetchGraph, fetchGraphConfiguration,
    fetchMatchingVertices,
} from "../../APILayer";
import _ from 'underscore';
import {MyContext} from "../../Context";
import GraphMap from "./GraphMap";
import SidePanel from "./SidePanel";
import GraphTitle from "./GraphTitle";
import s from './singleGraph.module.scss';
import TagListGraph from "../tagList/tagListGraph";
import {toMapCoordinate} from "../../utils/CoordinatesUtil";
import LeftPanel from "./LeftPanel";
import LoadingComponent from "../LoadingComponent";
import {updateBrowserUrlQueryParam} from "../../utils/Utils";
import {graphSelected} from "../../redux/selectedGraphSlice";
import {connect} from "react-redux";

const configs = require('configurations')

class SingleGraphView extends Component {

    static contextType = MyContext

    constructor(props) {
        super(props);
        this.state = {
            graph: undefined,
            graphConfiguration: undefined,
            metadataObjects: []
        }
        this.receiveSingleVertexSearch = this.receiveSingleVertexSearch.bind(this)
    }

    async componentDidMount() {

        let graphConfiguration = await fetchGraphConfiguration(this.props.match.params.graphId);
        let graph = await fetchGraph(this.props.match.params.graphId);

        this.props.graphSelected({
            graphId: this.props.match.params.graphId,
            graph: graph,
            graphConfiguration: graphConfiguration
        })

        let autocompletionTerms = await fetchAutocompletionTerms(this.props.match.params.graphId);

        this.setState({
            graphConfiguration: graphConfiguration,
            autocompletionTerms: autocompletionTerms,
            graph: graph
        })
    }


    render() {
        if (this.state.graphConfiguration === undefined) {
            return <LoadingComponent/>
        } else {
            return (
                <div className={s.singleGraphGrid}>

                    <GraphTitle/>

                    <TagListGraph
                        autocompletionTerms={this.state.autocompletionTerms}
                        sendSingleVertexSearch={this.receiveSingleVertexSearch} // TODO remove
                        receiveClearSignal={this.state.clearSignal}
                    />



                    <div>
                        <div className={s.leftPanel}>
                            <LeftPanel/>
                        </div>
                    </div>

                    <GraphMap
                        autocompletionTerms={this.state.autocompletionTerms}
                    />

                   
                </div>
            );
        }
    }

    async getVerticesMatchingTags(metadataObjects) {

        async function fetchVertices() {
            let verticesMatchingMetadata = []
            for (const metadataObject of metadataObjects) {
                let response = await fetchMatchingVertices(this.props.match.params.graphId, metadataObject);
                response.forEach(v => v['fetchEdges'] = metadataObject['fetchEdges'])
                response.forEach(v => v['flyTo'] = metadataObject['flyTo'])
                verticesMatchingMetadata.push(...response)
            }
            return verticesMatchingMetadata;
        }

        let verticesMatchingMetadata = await fetchVertices.call(this);

        // the same eth may have multiple types and labels
        let groupedByEth = _.groupBy(verticesMatchingMetadata, 'vertex');

        let markers = []
        for (const vertex in groupedByEth) {
            markers.push(this.convertToMarker(groupedByEth, vertex));
        }

        return markers
    }

    convertToMarker(groupedByEth, vertex) {
        const types = [...new Set(groupedByEth[vertex].map(obj => obj.types).flat())]
        const labels = [...new Set(groupedByEth[vertex].map(obj => obj.labels).flat())]
        const {pos, size, fetchEdges, flyTo} = groupedByEth[vertex][0]
        const mapCoordinate = toMapCoordinate(pos, this.state.graphConfiguration)

        return {
            types: types,
            labels: labels,
            pos: mapCoordinate,
            size: size,
            vertex: vertex,
            fetchEdges: fetchEdges,
            flyTo: flyTo
        }
    }

    receiveSingleVertexSearch(vertex) {
        updateBrowserUrlQueryParam(this.props, {vertex: vertex})
    }
}

export default connect(null, {graphSelected})(SingleGraphView);
