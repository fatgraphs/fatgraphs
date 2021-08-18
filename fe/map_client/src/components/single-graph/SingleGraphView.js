import React, {Component} from 'react';
import {withRouter} from "react-router-dom";
import {fetchGraph, fetchMatchingVertices, fetchRecentMetadata} from "../../APILayer";
import _ from 'underscore';
import {MyContext} from "../../Context";
import GraphMap from "./GraphMap";
import SidePanel from "./SidePanel";
import GraphTitle from "./GraphTitle";
import CopyGtmCommand from "./CopyGtmCommand";
import s from './singleGraph.module.scss';
import TagListGraph from "../tagList/tagListGraph";
import {toMapCoordinate} from "../../utils/CoordinatesUtil";

class SingleGraphView extends Component {

    static contextType = MyContext

    constructor(props) {
        super(props);
        this.state = {
            graphMetadata: undefined,
            isMarkerVisible: false,
            closestVertex: undefined,
            selectedMetadata: [],
            recentMetadataSearches: [],
            metadataObjects: [],
            markersSelectedMetadata: []
        }
        this.setClosestVertex = this.setClosestVertex.bind(this)
    }

    async componentDidMount() {
        let graphMetadata = await fetchGraph(this.props.match.params.graphId);
        let recentMetadata = await fetchRecentMetadata();
        this.setState({
            graphMetadata: graphMetadata,
            recentMetadataSearches: recentMetadata
        })
    }

    async componentDidUpdate(prevProps, prevState) {
        // let recentMetadataSearches = await fetchRecentMetadata('default_user');
        // if (_.isEqual(this.state.recentMetadataSearches, recentMetadataSearches)) {
        //     return
        // }
        // this.setState({recentMetadataSearches: recentMetadataSearches})
        if (_.isEqual(this.state.selectedMetadata, prevState.selectedMetadata)) {
            return
        }
        let markers = await this.getVerticesMatchingMetadata(this.state.selectedMetadata);
        this.setState({markersSelectedMetadata: markers})
    }

    // className={'grid grid-rows-tokenGraphLayout grid-cols-tokenGraphLayout grid-cols-3 gap-1 p-4 h-full'}>

    render() {
        if (this.state.graphMetadata === undefined) {
            return <div>Loading . . . </div>
        } else {
            return (
                <div className={s.singleGraphGrid}>

                    <GraphTitle
                        graphMetadata={this.state.graphMetadata}/>

                    <TagListGraph
                        onChange={(currentSelection) => this.setState({selectedMetadata: currentSelection})}/>


                    <CopyGtmCommand
                        graphMetadata={this.state.graphMetadata}/>


                    <div>
                        <SidePanel
                            closestVertex={this.state.closestVertex}
                            selectedVertices={this.state.markersSelectedMetadata}/>
                    </div>

                    <GraphMap
                        graphMetadata={this.state.graphMetadata}
                        graphId={this.props.match.params.graphId}
                        graphName={this.props.match.params.graphName}
                        setDisplayedAddress={this.setClosestVertex}
                        selectedMetadataMarkers={this.state.markersSelectedMetadata}
                        recentMetadataSearches={this.state.recentMetadataSearches}/>

                    <SidePanel/>
                </div>
            );
        }
    }

    setClosestVertex(address) {
        this.setState({closestVertex: address})
    }

    async getVerticesMatchingMetadata(metadataObjects) {
        let verticesMatchingMetadata = []
        for (const metadataObject of metadataObjects) {
            let response = await fetchMatchingVertices(this.props.match.params.graphId, metadataObject);
            verticesMatchingMetadata.push(...response)
        }

        // the same eth may have multiple types and labels
        let groupedByEth = _.groupBy(verticesMatchingMetadata, 'eth');

        let markers = []
        for (const eth in groupedByEth) {
            this.populateMarkers(groupedByEth, eth, markers);
        }
        return markers
    }

    populateMarkers(groupedByEth, eth, markers) {
        const types = groupedByEth[eth].map(obj => obj.types).flat()
        const labels = groupedByEth[eth].map(obj => obj.labels).flat()
        const {pos, size} = groupedByEth[eth][0]
        let mapCoordinate = toMapCoordinate(pos, this.state.graphMetadata)

        markers.push({
            types: types,
            labels: labels,
            pos: mapCoordinate,
            size: size,
            eth: eth
        })
        // this.setState({markersSelectedMetadata: markers})

    }

}

export default withRouter(SingleGraphView);