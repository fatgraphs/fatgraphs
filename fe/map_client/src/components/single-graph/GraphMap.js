import React from 'react';
import L from 'leaflet';
import UrlComposer from "../../utils/UrlComposer";
import {fetchClosestPoint} from "../../APILayer";
import {toGraphCoordinate, toMapCoordinate} from "../../utils/CoordinatesUtil";
import {MapContainer, Marker, TileLayer} from 'react-leaflet'
import {generateLargeRandom, hashVertexToInt, updateQueryParam} from "../../utils/Utils";
import s from './singleGraph.module.scss'
import "./circleMarker.scss";
import VertexPopup from "./vertexMarker/VertexPopup";
import VertexMarker from "./vertexMarker/VertexMarker";
import '@elfalem/leaflet-curve'
import Fullscreen from 'react-leaflet-fullscreen-plugin';
import {withRouter} from "react-router-dom";

import makeCustomControl from "./customMapControl/customMapControl";

let configs = require('../../../../../configurations.json');

class GraphMap extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            mapRef: undefined,
            zoom: 0,
            selectedVertices: [],
            lastFlyLocation: undefined,
            persistAllClicks: false
        }
        this.mapCreationCallback = this.mapCreationCallback.bind(this)
        this.bindOnClickCallback = this.bindOnClickCallback.bind(this)
        this.bindOnZoomCallback = this.bindOnZoomCallback.bind(this)
        this.bindOnPanCallback = this.bindOnPanCallback.bind(this)
        this.clearMapMarkersCallback = this.clearMapMarkersCallback.bind(this)
        this.checkboxCallback = this.checkboxCallback.bind(this)
        this.persistAllClicksCallback = this.persistAllClicksCallback.bind(this)
        this.removeLatMarker = this.removeLatMarker.bind(this)
        // this.doFlyToVertexLogic = this.doFlyToVertexLogic.bind(this)
    }

    async componentDidUpdate(prevProps, prevState, snapshot) {
        if (this.props.markersFromParent.length > 0) {
            let flyTarget = this.props.markersFromParent.filter(m => m.flyTo)[0];
            if (flyTarget !== undefined && flyTarget.vertex !== this.state.lastFlyLocation) {
                this.state.map_ref.flyTo(
                    flyTarget.pos,
                    this.props.graphMetadata['zoomLevels'] - 1)
                this.setState({
                    lastFlyLocation: flyTarget.vertex
                })
            }

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

                    return <VertexMarker
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
                        ticked={!e.removeOnNewClick}>
                        >
                    </VertexMarker>
                })
            }
        </MapContainer>
    }


    mapCreationCallback(map) {
        this.bindOnZoomCallback(map);
        this.bindOnClickCallback(map);
        this.bindOnPanCallback(map);
        this.addClearEdgesControl(map);
        this.addPersistAllClicksControl(map);
        this.addUndoControl(map);

        this.setState({
            map_ref: map
        })

        function setInitialMapView() {
            let urlZoom = new URLSearchParams(this.props.location.search).get('z') || 0;
            let urlLat = new URLSearchParams(this.props.location.search).get('lat') || -configs['tile_size'] / 2;
            let urlLng = new URLSearchParams(this.props.location.search).get('lng') || configs['tile_size'] / 2;
            map.setView([urlLat, urlLng], urlZoom)
            updateQueryParam(this.props, {
                z: urlZoom,
                lat: urlLat,
                lng: urlLng
            })
        }

        setInitialMapView.call(this);
    }

    addPersistAllClicksControl(map) {
        makeCustomControl(this.persistAllClicksCallback,
            `<a href="#" role="button" title="Clear edges" aria-label="Clear edges">P</a>`,
            'topright'
        ).addTo(map);
    }

    addClearEdgesControl(map) {
        makeCustomControl(this.clearMapMarkersCallback,
            `<a href="#" role="button" title="Clear edges" aria-label="Clear edges">✗</a>`,
            'topright'
        ).addTo(map);
    }

    addUndoControl(map) {
        makeCustomControl(this.removeLatMarker,
            `<a href="#" role="button" title="Undo last selection" aria-label="Undo last selection">←</a>`,
            'topright'
        ).addTo(map);
    }

    bindOnZoomCallback(map) {
        let zoomCallback = function () {
            // updateQueryParam(this.props, {z:map.getZoom()})
            this.setState({
                zoom: map.getZoom()
            })
        }.bind(this);
        map.on('zoom', zoomCallback)
    }

    bindOnClickCallback(mapRef) {

        function getGraphPosFromMapClick(clickEvent, graphMetadata) {
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

    bindOnPanCallback(mapRef) {
        let panCallback = function () {
            let currentLocation = mapRef.getCenter();
            let temp = () => {
                updateQueryParam(this.props, {
                    lat: Math.round(currentLocation.lat),
                    lng: Math.round(currentLocation.lng)
                })
            }
            temp.bind(this)
            setTimeout(temp, 0)
        }.bind(this);
        mapRef.on('moveend', panCallback);
    }

    async fetchClosestVertex(pos) {
        let closestVertex = await fetchClosestPoint(this.props.graphId, pos)
        closestVertex['pos'] = toMapCoordinate(closestVertex['pos'], this.props.graphMetadata);
        closestVertex['refetch'] = 0;
        closestVertex['removeOnNewClick'] = !this.state.persistAllClicks;
        closestVertex['fetchEdges'] = true;
        return closestVertex;
    }

    updateDisplayedVertices(newVertex) {
        updateQueryParam(this.props, {vertex: newVertex['vertex']})
        let refetchCount = this.state.selectedVertices
            .filter(v => v.vertex === newVertex.vertex)
            .forEach(v => newVertex['refetch'] = v['refetch'] + 1);

        this.setState({
            selectedVertices: [
                ...this.state.selectedVertices.filter(v => !v.removeOnNewClick),
                newVertex]
        })

    }

    clearMapMarkersCallback() {
        this.setState({selectedVertices: []})
        this.props.clearParent()
        this.props.history.push({search: ''})
    }

    persistAllClicksCallback() {
        this.setState({
            persistAllClicks: !this.state.persistAllClicks
        })
    }

    checkboxCallback(vertexObject, ticked) {

        vertexObject.removeOnNewClick = !ticked

        if (!ticked) {
            let selectedVertices = this.state.selectedVertices.filter(v => v.vertex !== vertexObject.vertex);
            this.props.filterOutFromParent(vertexObject.vertex)
            console.log("vertices without selected: ", selectedVertices)
            this.setState({
                selectedVertices: selectedVertices
            })
        }
    }

    removeLatMarker() {
        this.setState({
            selectedVertices: this.state.selectedVertices.slice(0, this.state.selectedVertices.length - 1)
        })
    }


}

GraphMap
    .propTypes = {};
GraphMap
    .defaultProps = {};

export default withRouter(GraphMap);
