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

class SingleGraphView extends Component {

    static contextType = MyContext

    constructor(props) {
        super(props);
        this.state = {
            graphMetadata: undefined,
            selectedMetadata: [],
            recentMetadataSearches: [],
            metadataObjects: [],
            markersSelectedMetadata: [],
            isFlyToLastVertex: false,
            clearSignal: false
        }
        this.receiveClearAck = this.receiveClearAck.bind(this)
    }

    async componentDidMount() {

        let graphMetadata = await fetchGraph(this.props.match.params.graphId);
        let autocompletionTerms = await fetchAutocompletionTerms(this.props.match.params.graphId);
        this.setState({
            graphMetadata: graphMetadata,
            autocompletionTerms: autocompletionTerms,
            recentMetadataSearches: []
        })

        function processUrlVertexIfPresent() {
            let newUrlVertex = new URLSearchParams(this.props.location.search).get('vertex');
            if (!!newUrlVertex) {
                this.setState({
                    isFlyToLastVertex: true,
                    selectedMetadata: [
                        ...this.state.selectedMetadata,
                        {
                            type: 'eth',
                            value: newUrlVertex,
                            fetchEdges: true
                        }
                    ]
                })
            }
        }

        processUrlVertexIfPresent.call(this);

    }

    async componentDidUpdate(prevProps, prevState) {


        if (_.isEqual(this.state.selectedMetadata, prevState.selectedMetadata)) {
            return
        }
        let fecthEdgesOfThose = this.state.selectedMetadata
            .filter(m => m.fetchEdges && m.type === 'eth')
            .map(m => m.value);
        console.log("fecthEdgesOfThose ", fecthEdgesOfThose)

        let markers = await this.getVerticesMatchingMetadata(this.state.selectedMetadata);


        markers.forEach(m => {
            console.log("m.vertex: ", m.vertex)
            m['removeOnNewClick'] = false
            m['refetch'] = 0
            m['fetchEdges'] =  fecthEdgesOfThose.includes(m.vertex)
        })



        this.setState({markersSelectedMetadata: markers})
    }

    render() {
        if (this.state.graphMetadata === undefined) {
            return <div>Loading . . . </div>
        } else {

            let plot_urls = []
            for(let z = 0; z < this.state.graphMetadata['zoomLevels']; z++){
                plot_urls.push(UrlComposer.edgePlot(this.props.match.params.graphId, z))
            }

	    const urlVertex = new URLSearchParams(this.props.location.search).get("vertex");

            return (
                <div className={s.singleGraphGrid}>

                    <GraphTitle
                        graphMetadata={this.state.graphMetadata}/>

                    <TagListGraph
                        autocompletionTerms={this.state.autocompletionTerms}
                        onChange={(currentSelection) => this.setState({selectedMetadata: currentSelection})}
                        onSpecificVertexSearch={(vertex) => {
                            this.props.history.push({
                                search: '?vertex=' + vertex
                            })
                            this.setState({
                                isFlyToLastVertex: true
                            })
                        }}
                        receiveClearSignal={this.state.clearSignal}
                        sendClearAck={this.receiveClearAck}
                        />


                    <CopyGtmCommand
                        graphMetadata={this.state.graphMetadata}/>


                    <div>
                        <SidePanel
                            selectedVertices={this.state.selectedMetadata}/>
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
                        markersFromParent={this.state.markersSelectedMetadata}
                        recentMetadataSearches={this.state.recentMetadataSearches}
			            isFlyToLastVertex={this.state.isFlyToLastVertex}
                        afterFlyToLast={() => this.setState({isFlyToLastVertex: false})}
                        clearParent={() => {
                            this.setState({
                                markersSelectedMetadata: [],
                                clearSignal: true
                            })
                        }}
                        filterOutFromParent={(vertex) => {
                            let selectedVertices = this.state.markersSelectedMetadata.filter(v => v.vertex !== vertex);
                            this.setState({markersSelectedMetadata: selectedVertices})
                        }}
                    />

                    <Fillable>
                        {plot_urls.map((url, i) => <img
                            key={i*63 + 1}
                            className={s.plot}
                            src={url}/>
                       )}
                    </Fillable>
                </div>
            );
        }
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
    }

    receiveClearAck(){
        this.setState({
            clearSignal: false
        })
    }
}

export default withRouter(SingleGraphView);
