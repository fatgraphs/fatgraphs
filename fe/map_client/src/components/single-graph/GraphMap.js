import React from 'react';
import L from 'leaflet';
import UrlComposer from "../../utils/UrlComposer";
import {fetchClosestPoint} from "../../APILayer";
import {toGraphCoordinate, toMapCoordinate} from "../../utils/CoordinatesUtil";
import {MapContainer, Marker, TileLayer} from 'react-leaflet'
import {generateLargeRandom, hashVertexToInt} from "../../utils/Utils";
import s from './singleGraph.module.scss'
import "./circleMarker.scss"; import VertexPopup from "./VertexPopup"; import VertexMarker from "./VertexMarker";
import '@elfalem/leaflet-curve'
import Fullscreen from 'react-leaflet-fullscreen-plugin';
import {withRouter} from "react-router-dom";

import './clearMapMarkers'

let configs = require('../../../../../configurations.json');

class GraphMap extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            mapRef: undefined,
            zoom: 0,
            selectedVertices : []
        }
        this.bindOnClickCallback = this.bindOnClickCallback.bind(this)
        this.bindOnZoomCallback = this.bindOnZoomCallback.bind(this)
        this.bindOnZoomCallback = this.bindOnZoomCallback.bind(this)
        this.mapCreationCallback = this.mapCreationCallback.bind(this)
        this.clearMapMarkersCallback = this.clearMapMarkersCallback.bind(this)
        this.checkboxCallback = this.checkboxCallback.bind(this)
        this.doFlyToVertexLogic = this.doFlyToVertexLogic.bind(this)
    }

    async componentDidUpdate(prevProps, prevState, snapshot) {
        this.doFlyToVertexLogic();
    }

    doFlyToVertexLogic() {
        if (this.props.isFlyToLastVertex && this.props.markersFromParent.length > 0){
            this.state.map_ref.flyTo(
                this.props.markersFromParent[this.props.markersFromParent.length - 1].pos,
                this.props.graphMetadata['zoomLevels'] - 1)
        this.props.afterFlyToLast()
        }
    }

    render() {
        const {match, location, history} = this.props;
        const tileUrl = UrlComposer.tileLayer(this.props.graphId);
        const position = [this.props.graphMetadata.tileSize / -2.0,
            this.props.graphMetadata.tileSize / 2.0]


        let allMarkers = [...this.state.selectedVertices, ...this.props.markersFromParent]

        allMarkers = [...new Map(allMarkers.map(item =>
            [item['vertex'], item])).values()];


        return <MapContainer
            whenCreated={this.mapCreationCallback}
            className={s.myMap}
            center={position}
            zoom={0}
            scrollWheelZoom={true}
            noWrap={true}
            crs={L.CRS.Simple}>
            <TileLayer
                attribution='tokengallery 2.0'
                url={tileUrl}
                randint={generateLargeRandom()}
                maxZoom={this.props.graphMetadata['zoomLevels'] - 1}
                tileSize={this.props.graphMetadata.tileSize}
            />
            <Fullscreen {...{position: 'topright'}} />

            {allMarkers.map(
                (e, i) => {

                    console.log(e)

                return  <VertexMarker
                    key={hashVertexToInt(e.vertex) + e.refetch}
                    fetchEdges={e.fetchEdges}
                    zoom={this.state.zoom}
                    mapRef={this.state.map_ref}
                    graphMetadata={this.props.graphMetadata}
                    vertexObject={e}
                    autocompletionTerms={this.props.autocompletionTerms}
                    graphName={this.props.graphName}
                    graphId={this.props.graphId}
                    checkboxCallback={this.checkboxCallback}
                    ticked={ !e.removeOnNewClick}>
                    >
                </VertexMarker>
                })
            }
        </MapContainer>
    }

    mapCreationCallback(map) {
        this.centerView(map);
        this.bindOnZoomCallback(map);
        this.bindOnClickCallback(map);
        this.setState({
            map_ref: map
        })
        L.control.clearMapMarkersControl({callback: this.clearMapMarkersCallback }).addTo(map);
    }

    centerView(map) {
        map.setView(
            [this.props.graphMetadata.tileSize / -2.0,
                this.props.graphMetadata.tileSize / 2.0],
            configs['initialZoom'])
    }

    bindOnZoomCallback(map) {
        map.on('zoom', function () {
            this.setState({
                zoom: map.getZoom()
            })
        }.bind(this))
    }

    bindOnClickCallback(mapRef) {

        function getGraphPosFromMapClick(clickEvent, graphMetadata){
            return toGraphCoordinate([
                clickEvent.latlng.lat,
                clickEvent.latlng.lng],
                graphMetadata)
        }

        mapRef.on('click', async function (clickEvent) {
            let graphPosClicked = getGraphPosFromMapClick(clickEvent, this.props.graphMetadata)
            let vertex = await this.fetchClosestVertex(graphPosClicked);
            this.updateDisplayedVertices(vertex);
        }.bind(this));

    }

    async fetchClosestVertex(pos) {
        let closestVertex = await fetchClosestPoint(this.props.graphId, pos)
        closestVertex['pos'] = toMapCoordinate(closestVertex['pos'], this.props.graphMetadata);
        closestVertex['refetch'] = 0;
        closestVertex['removeOnNewClick'] = true;
        closestVertex['fetchEdges'] = true;
        return closestVertex;
    }

     updateDisplayedVertices(newVertex) {
	    this.props.history.push({search: '?vertex=' + newVertex['vertex']})
        let refetchCount = this.state.selectedVertices
            .filter(v => v.vertex === newVertex.vertex)
            .forEach(v => newVertex['refetch'] = v['refetch'] + 1);

        this.setState({selectedVertices: [
            ...this.state.selectedVertices.filter(v => ! v.removeOnNewClick),
         newVertex]})

    }

    clearMapMarkersCallback(){
        this.setState({selectedVertices: []})
        this.props.clearParent()
    }

    checkboxCallback(vertexObject, ticked){

        vertexObject.removeOnNewClick = ! ticked

        if(! ticked){
            let selectedVertices = this.state.selectedVertices.filter(v => v.vertex !== vertexObject.vertex);
            this.props.filterOutFromParent(vertexObject.vertex)
            console.log("vertices without selected: ", selectedVertices)
            this.setState({
                selectedVertices: selectedVertices
            })
        }
    }


}

GraphMap
    .propTypes = {};
GraphMap
    .defaultProps = {};

export default withRouter(GraphMap);
