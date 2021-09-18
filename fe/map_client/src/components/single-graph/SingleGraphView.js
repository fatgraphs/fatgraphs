import React, {Component} from 'react';
import {withRouter} from "react-router-dom";
import {fetchAutocompletionTerms, fetchGraph, fetchMatchingVertices} from "../../APILayer";
import _ from 'underscore';
import {MyContext} from "../../Context";
import GraphMap from "./GraphMap";
import SidePanel from "./SidePanel";
import GraphTitle from "./GraphTitle";
import CopyGtmCommand from "./CopyGtmCommand";
import s from './singleGraph.module.scss';
import TagListGraph from "../tagList/tagListGraph";
import {toMapCoordinate} from "../../utils/CoordinatesUtil"; import Fillable from "../../reactBlueTemplate/src/pages/tables/static/Fillable"; import UrlComposer from "../../utils/UrlComposer"; import {IconsLegend} from "./IconsLegend";

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
        let autocompletionTerms = await fetchAutocompletionTerms(this.props.match.params.graphId);
        this.setState({
            graphMetadata: graphMetadata,
            autocompletionTerms: autocompletionTerms,
            recentMetadataSearches: []
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

            let plot_urls = []
            for(let z = 0; z < this.state.graphMetadata['zoomLevels']; z++){
                plot_urls.push(UrlComposer.edgePlot(this.props.match.params.graphId, z))
            }

            return (
                <div className={s.singleGraphGrid}>

                    <GraphTitle
                        graphMetadata={this.state.graphMetadata}/>

                    <TagListGraph
                        autocompletionTerms={this.state.autocompletionTerms}
                        onChange={(currentSelection) => this.setState({selectedMetadata: currentSelection})}/>


                    <CopyGtmCommand
                        graphMetadata={this.state.graphMetadata}/>


                    <div>
                        <SidePanel
                            closestVertex={this.state.closestVertex}
                            selectedVertices={this.state.markersSelectedMetadata}/>
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
                        setDisplayedAddress={this.setClosestVertex}
                        selectedMetadataMarkers={this.state.markersSelectedMetadata}
                        recentMetadataSearches={this.state.recentMetadataSearches}/>

                    <Fillable>
                        {plot_urls.map(url => <img src={url}/>)}
                    </Fillable>
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
        let groupedByEth = _.groupBy(verticesMatchingMetadata, 'vertex');

        let markers = []
        for (const vertex in groupedByEth) {
            this.populateMarkers(groupedByEth, vertex, markers);
        }
        return markers
    }

    populateMarkers(groupedByEth, vertex, markers) {
        const types = groupedByEth[vertex].map(obj => obj.types).flat()
        const labels = groupedByEth[vertex].map(obj => obj.labels).flat()
        const {pos, size} = groupedByEth[vertex][0]
        let mapCoordinate = toMapCoordinate(pos, this.state.graphMetadata)

        markers.push({
            types: types,
            labels: labels,
            pos: mapCoordinate,
            size: size,
            vertex: vertex
        })
        // this.setState({markersSelectedMetadata: markers})

    }

}

export default withRouter(SingleGraphView);