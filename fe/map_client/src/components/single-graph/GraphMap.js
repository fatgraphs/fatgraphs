import React from 'react';
import L from 'leaflet';
import UrlComposer from "../../utils/UrlComposer";
import {fetchClosestPoint} from "../../APILayer";
import {toGraphCoordinate, toMapCoordinate} from "../../utils/CoordinatesUtil";
import {MapContainer, Marker, TileLayer} from 'react-leaflet'
import {generateLargeRandom} from "../../utils/Utils";
import s from './singleGraph.module.scss'
import "./circleMarker.scss"; import VertexPopup from "./VertexPopup"; import VertexMarker from "./VertexMarker";
import '@elfalem/leaflet-curve'
import Fullscreen from 'react-leaflet-fullscreen-plugin';

import './testCustomControl'

let configs = require('../../../../../configurations.json');

class GraphMap extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            mapRef: undefined,
            closestVertex: undefined,
            zoom: 0,
            showEdgeOverlay: false,
            selectedVertices : []
        }
        this.bindOnClickCallback = this.bindOnClickCallback.bind(this)
        this.bindOnZoomCallback = this.bindOnZoomCallback.bind(this)
        this.bindOnZoomCallback = this.bindOnZoomCallback.bind(this)
        this.mapCreationCallback = this.mapCreationCallback.bind(this)
        this.toggleEdgeLayoutView = this.toggleEdgeLayoutView.bind(this)
        this.checkboxCallback = this.checkboxCallback.bind(this)
    }

    async componentDidUpdate(prevProps, prevState, snapshot) {
        if(this.props.selectedMetadataMarkers !== undefined
            && this.props.flyToLast
            && this.props.selectedMetadataMarkers.length > 0){
                this.state.map_ref.flyTo(this.props.selectedMetadataMarkers[this.props.selectedMetadataMarkers.length - 1].pos,
                this.props.graphMetadata['zoomLevels'] - 1)
                this.props.afterFlyToLast()
        }

    }

    render() {
        const tileUrl = UrlComposer.tileLayer(this.props.graphId);
        const position = [this.props.graphMetadata.tileSize / -2.0,
            this.props.graphMetadata.tileSize / 2.0]


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

            {/* last clicked vertex */}

            {/* vertices with edges persisted using checkbox*/}
            {this.state.selectedVertices.map(
                (e, i) => {
                    console.log("e of selectedVertices: ", e)
                return  <VertexMarker
                    key={(i+1)*99}
                    fetchEdges={this.state.showEdgeOverlay}
                    zoom={this.state.zoom}
                    mapRef={this.state.map_ref}
                    graphMetadata={this.props.graphMetadata}
                    vertexObject={e}
                    autocompletionTerms={this.props.autocompletionTerms}
                    graphName={this.props.graphName}
                    graphId={this.props.graphId}
                    checkboxCallback={this.checkboxCallback}
                    ticked>
                </VertexMarker>
                })
            }

            {/* vertices selected with search bar*/}
            {this.props.selectedMetadataMarkers.map(
                (e, i) => {
                return  <VertexMarker
                    key={i}
                    fetchEdges={false}
                    vertexObject={e}
                    autocompletionTerms={this.props.autocompletionTerms}
                    graphName={this.props.graphName}
                    graphId={this.props.graphId} >
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
        L.control.testControl({ position: 'bottomleft', callback: this.toggleEdgeLayoutView }).addTo(map);
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
        mapRef.on('click', function (clickEvent) {
            let coord = clickEvent.latlng;
            let lat = coord.lat;
            let lng = coord.lng;
            let pos = toGraphCoordinate([lat, lng], this.props.graphMetadata)
            this.fetchClosestAndUpdate(pos);
        }.bind(this));
    }


    async fetchClosestAndUpdate(pos) {
        let closestVertex = await fetchClosestPoint(this.props.graphId, pos)

        closestVertex['pos'] = toMapCoordinate(closestVertex['pos'], this.props.graphMetadata);

        this.setState({selectedVertices: [
            ...this.state.selectedVertices.filter(v => v.persist),
         closestVertex]})

        this.props.setDisplayedAddress(closestVertex)
    }

    toggleEdgeLayoutView(){
        this.setState({showEdgeOverlay: ! this.state.showEdgeOverlay})
    }

    checkboxCallback(vertexObject, ticked){
        
        if(this.state.selectedVertices.some(v => v.vertex === vertexObject.vertex)){
            console.log("removing persisted markers")
            this.setState({
                selectedVertices: this.state.selectedVertices.filter(v => v.vertex !== vertexObject.vertex)
            })
            
        } else {
            this.setState({
                selectedVertices: [...this.state.selectedVertices, vertexObject]
            })
        }
    }


}

GraphMap
    .propTypes = {};
GraphMap
    .defaultProps = {};

export default GraphMap;
