import React, {Component} from 'react';
import {withRouter} from "react-router-dom";
import {fetchAutocompletionTerms,fetchEdges, fetchGraph, fetchMatchingVertices} from "../../APILayer";
import _ from 'underscore';
import {MyContext} from "../../Context";
import GraphMap from "./GraphMap";
import SidePanel from "./SidePanel";
import GraphTitle from "./GraphTitle";
import CopyGtmCommand from "./CopyGtmCommand";
import s from './singleGraph.module.scss';
import TagListGraph from "../tagList/tagListGraph";
import {toMapCoordinate} from "../../utils/CoordinatesUtil"; import Fillable from "../../reactBlueTemplate/src/pages/tables/static/Fillable"; import UrlComposer from "../../utils/UrlComposer"; import {IconsLegend} from "./IconsLegend";
import EdgePlots from "./EdgePlots";
import LoadingComponent from "../LoadingComponent";
import {getQueryParam, updateQueryParam} from "../../utils/Utils";

class SingleGraphView extends Component {

    static contextType = MyContext

    constructor(props) {
        super(props);
        this.state = {
            graphMetadata: undefined,
            selectedTags: [],
            recentMetadataSearches: [],
            metadataObjects: [],
            mapMarkers: [],
            clearSignal: false
        }
        this.receiveClearAck = this.receiveClearAck.bind(this)
        this.receiveSelectedTags = this.receiveSelectedTags.bind(this)
        this.receiveSingleVertexSearch = this.receiveSingleVertexSearch.bind(this)
    }

    async componentDidMount() {

        let graphMetadata = await fetchGraph(this.props.match.params.graphId);
        let autocompletionTerms = await fetchAutocompletionTerms(this.props.match.params.graphId);
        this.setState({
            graphMetadata: graphMetadata,
            autocompletionTerms: autocompletionTerms,
            recentMetadataSearches: []
        })

        // TODO: MOVE TO graph map?
        function processUrlVertexIfPresent() {
            if (!!getQueryParam(this.props, 'vertex')) {
                this.setState({
                    selectedTags: [
                        ...this.state.selectedTags,
                        {
                            type: 'eth',
                            value: getQueryParam(this.props, 'vertex'),
                            fetchEdges: true,
                            flyTo: true
                        }
                    ]
                })
            }
        }
        processUrlVertexIfPresent.call(this);
    }

    async componentDidUpdate(prevProps, prevState) {

        if (_.isEqual(this.state.selectedTags, prevState.selectedTags)) {
            return
        }

        let markers = await this.getVerticesMatchingTags(this.state.selectedTags);

        markers.forEach(m => {
            m['removeOnNewClick'] = false
            m['refetch'] = 0
        })

        this.setState({mapMarkers: markers})
    }

    render() {
        if (this.state.graphMetadata === undefined) {
            return <LoadingComponent/>
        } else {
            return (
                <div className={s.singleGraphGrid}>

                    <GraphTitle
                        graphMetadata={this.state.graphMetadata}/>

                    <TagListGraph
                        autocompletionTerms={this.state.autocompletionTerms}
                        sendSelectedTags={this.receiveSelectedTags}
                        sendSingleVertexSearch={this.receiveSingleVertexSearch}
                        receiveClearSignal={this.state.clearSignal}
                        sendClearAck={this.receiveClearAck}
                        />


                    <CopyGtmCommand
                        graphMetadata={this.state.graphMetadata}/>


                    <div>
                        <SidePanel
                            selectedVertices={this.state.selectedTags}/>
                        <div className={'mt-2'}>
                            <Fillable>
                                <IconsLegend></IconsLegend>
                            </Fillable>
                        </div>
                    </div>

                    <GraphMap
                        autocompletionTerms={this.state.autocompletionTerms}
                        graphMetadata={this.state.graphMetadata}
                        graphId={this.props.match.params.graphId}
                        graphName={this.props.match.params.graphName}
                        markersFromParent={this.state.mapMarkers}
                        recentMetadataSearches={this.state.recentMetadataSearches}
                        afterFlyToLast={() => this.setState({isFlyToLastVertex: false})}
                        clearParent={() => {
                            this.setState({
                                mapMarkers: [],
                                clearSignal: true
                            })
                        }}
                        filterOutFromParent={(vertex) => {
                            let selectedVertices = this.state.mapMarkers.filter(v => v.vertex !== vertex);
                            this.setState({mapMarkers: selectedVertices})
                        }}
                    />

                    <EdgePlots
                        zoomLevels={this.state.graphMetadata['zoomLevels']}/>
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
        const types = [... new Set(groupedByEth[vertex].map(obj => obj.types).flat())]
        const labels = [... new Set(groupedByEth[vertex].map(obj => obj.labels).flat())]
        const {pos, size, fetchEdges, flyTo} = groupedByEth[vertex][0]
        const mapCoordinate = toMapCoordinate(pos, this.state.graphMetadata)

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

    receiveClearAck(){
        this.setState({
            clearSignal: false
        })
    }

    receiveSelectedTags(currentSelection){
        this.setState({selectedTags: currentSelection})
    }

    receiveSingleVertexSearch(vertex){
        updateQueryParam(this.props, {vertex: vertex})
    }
}

export default withRouter(SingleGraphView);
