import React from 'react';
import L from 'leaflet';
import UrlComposer from "../../utils/UrlComposer";
import {fetchClosestPoint, postVertexMetadata} from "../../APILayer";
import {toGraphCoordinate, toMapCoordinate} from "../../utils/CoordinatesUtil";
import {MapContainer, Marker, TileLayer} from 'react-leaflet'
import {generateLargeRandom} from "../../utils/Utils";
import s from './singleGraph.module.scss'
import "./circleMarker.scss"; import VertexPopup from "./VertexPopup"; import VertexMarker from "./VertexMarker";

let configs = require('../../../../../configurations.json');

class GraphMap extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            mapRef: undefined,
            closestVertex: undefined,
            zoom: 0
        }
        this.bindOnClickCallback = this.bindOnClickCallback.bind(this)
        this.bindOnZoomCallback = this.bindOnZoomCallback.bind(this)
        this.bindOnZoomCallback = this.bindOnZoomCallback.bind(this)
        this.mapCreationCallback = this.mapCreationCallback.bind(this)

    }


    async componentDidUpdate(prevProps, prevState, snapshot) {
        // ttis.state.selected;etadata

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

            <VertexMarker
                markerObject={this.state.closestVertex}
                autocompletionTerms={this.props.autocompletionTerms}
                graphName={this.props.graphName}
                graphId={this.props.graphId}>
            </VertexMarker>

            {this.props.selectedMetadataMarkers.map(
                (e, i) => {
                return  <VertexMarker
                    key={i}
                    markerObject={e}
                    autocompletionTerms={this.props.autocompletionTerms}
                    graphName={this.props.graphName}
                    graphId={this.props.graphId}>
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
        closestVertex['pos'] = toMapCoordinate(closestVertex['pos'], this.props.graphMetadata)
        this.setState({closestVertex: closestVertex})
        this.props.setDisplayedAddress(closestVertex)
    }




}

GraphMap
    .propTypes = {};
GraphMap
    .defaultProps = {};

export default GraphMap;