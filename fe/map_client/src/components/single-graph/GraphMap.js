import React from 'react';
import L from 'leaflet';
import UrlComposer from "../../utils/UrlComposer";
import {toGraphCoordinate} from "../../utils/CoordinatesUtil";
import {MapContainer, TileLayer} from 'react-leaflet'
import {generateLargeRandom, hashVertexToInt} from "../../utils/Utils";
import s from './singleGraph.module.scss'
import "./circleMarker.scss";
import VertexMarker from "./vertexMarker/VertexMarker";
import '@elfalem/leaflet-curve'
import Fullscreen from 'react-leaflet-fullscreen-plugin';

import makeCustomControl from "./customMapControl/customMapControl";
import {func} from "prop-types";
import {connect} from "react-redux";

import {clear, fetchClosestVertex, pop, removeVertices, togglePersistClick, updateFlyTo} from "../../redux/markersSlice";
import {changeUrl} from "../../redux/urlSlice";
import {graphMounted} from "../../redux/selectedGraphSlice";
import _ from 'underscore';
import UrlManager from "../urlManager";

let configs = require('../../../../../configurations.json');

class GraphMap extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            mapRef: undefined,
            renderingCommitted: false
        }
        this.mapCreationCallback = this.mapCreationCallback.bind(this)
        this.bindOnClickCallback = this.bindOnClickCallback.bind(this)
        this.bindOnZoomCallback = this.bindOnZoomCallback.bind(this)
        this.bindOnPanCallback = this.bindOnPanCallback.bind(this)
        this.clearMapMarkersCallback = this.clearMapMarkersCallback.bind(this)
    }

    componentDidMount() {
        this.props.commitRendering()
        this.setState({
            renderingCommitted: true
        })
    }

    componentWillUnmount() {
        this.props.clear()
    }

    async componentDidUpdate(prevProps, prevState, snapshot) {

        let lastVertexMarker = this.props.verticesFromStore[this.props.verticesFromStore.length - 1];
        if (lastVertexMarker && lastVertexMarker.flyTo) {
            this.state.mapRef.flyTo(
                lastVertexMarker.pos,
                this.props.graphConfiguration['zoomLevels'] - 1
            )
            this.props.updateFlyTo(lastVertexMarker)
        }

        if (this.state.mapRef && ! _.isEqual(prevProps.url, this.props.url)) {
            this.state.mapRef.setView([this.props.url.x, this.props.url.y], this.props.url.z);
        }
    }

    render() {
        const tileUrl = UrlComposer.tileLayer(this.props.graphId);
        const position = [this.props.graphConfiguration.tileSize / -2.0,
            this.props.graphConfiguration.tileSize / 2.0]

        return <MapContainer
            whenCreated={this.mapCreationCallback}
            className={s.myMap}
            center={position}
            zoom={0}
            scrollWheelZoom={true}
            closePopupOnClick={false}
            noWrap={true}
            crs={L.CRS.Simple}>
            <TileLayer
                attribution='tokengallery 2.0'
                url={tileUrl}
                randint={generateLargeRandom()}
                maxZoom={this.props.graphConfiguration['zoomLevels'] - 1}
                tileSize={this.props.graphConfiguration.tileSize}
            />
            <Fullscreen {...{position: 'topright'}} />

            {this.props.verticesFromStore.map(
                (e, i) => {

                    return <VertexMarker
                        key={hashVertexToInt(e.vertex)}
                        fetchEdges={e.fetchEdges}
                        zoom={this.state.mapRef.getZoom()}
                        mapRef={this.state.mapRef}
                        graphConfiguration={this.props.graphConfiguration}
                        vertexObject={e}
                        autocompletionTerms={this.props.autocompletionTerms}
                        graphName={this.props.graphName}
                        graphId={this.props.graphId}
                        ticked={e.persistOnNewClick}>
                    </VertexMarker>
                })
            }
             <UrlManager/>
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
            mapRef: map
        })

        map.toJSON = () => ({hidden: 'to help redux devtools :)'})
        this.props.graphMounted({
            graphMapRef: map
        })
    }

    addPersistAllClicksControl(map) {
        makeCustomControl(this.props.togglePersistClick,
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
        makeCustomControl(this.props.pop,
            `<a href="#" role="button" title="Undo last selection" aria-label="Undo last selection">←</a>`,
            'topright'
        ).addTo(map);
    }

    bindOnZoomCallback(map) {
        let zoomCallback = function () {
            this.props.changeUrl({z: map.getZoom()})
        }.bind(this);
        map.on('zoom', zoomCallback)
    }

    bindOnClickCallback(mapRef) {

        function getGraphPosFromMapClick(clickEvent, graphConfiguration) {
            return toGraphCoordinate([
                    clickEvent.latlng.lat,
                    clickEvent.latlng.lng],
                graphConfiguration)
        }

        mapRef.on('click', async function (clickEvent) {
            let graphPosClicked = getGraphPosFromMapClick(clickEvent, this.props.graphConfiguration)
            this.props.fetchClosestVertex(
                {
                    graphId: this.props.graphId,
                    pos: graphPosClicked,
                    graphConfiguration: this.props.graphConfiguration,
                    flyTo: false
                })

            this.props.removeVertices(
                {
                    persistOnNewClick: false
                }
            )
        }.bind(this));

    }

    bindOnPanCallback(mapRef) {
        let panCallback = function () {
            let currentLocation = mapRef.getCenter();

            // URL update is delayed to allow the map to autopan when a popup is opened
            clearTimeout(this.state.timeout)
            let timeout = setTimeout(() => {
                this.props.changeUrl({
                y: String(Math.round(currentLocation.lng)),
                x: String(Math.round(currentLocation.lat)),
                z: String(mapRef.getZoom())
            })
            }, 300);
            this.setState({
                timeout: timeout
            })
        }.bind(this);

        mapRef.on('moveend', panCallback);
    }

    clearMapMarkersCallback() {
        this.props.clear()
    }
}

GraphMap
    .propTypes = {
    clearSearches: func.isRequired
};
GraphMap
    .defaultProps = {};

let mapStateToProps = (store) => {
    return {
        verticesFromStore: store.marker.vertices,
        persistAllClicks: store.marker.isPersistClick,
        url: store.url
    }
};

export default connect(mapStateToProps, {
    togglePersistClick,
    clear,
    pop,
    removeVertices,
    updateFlyTo,
    fetchClosestVertex,
    changeUrl,
    graphMounted
})(GraphMap);