import React from 'react';
import L from 'leaflet';
import UrlComposer from "../../utils/UrlComposer";
import {fetchClosestPoint,fetchEdges, postVertexMetadata} from "../../APILayer";
import {toGraphCoordinate, toMapCoordinate} from "../../utils/CoordinatesUtil";
import {MapContainer, Marker, TileLayer} from 'react-leaflet'
import {generateLargeRandom} from "../../utils/Utils";
import s from './singleGraph.module.scss'
import "./circleMarker.scss"; import VertexPopup from "./VertexPopup"; import VertexMarker from "./VertexMarker";
import '@elfalem/leaflet-curve'
import Fullscreen from 'react-leaflet-fullscreen-plugin';

let configs = require('../../../../../configurations.json');

class GraphMap extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            mapRef: undefined,
            closestVertex: undefined,
            zoom: 0,
            paths: []
        }
        this.bindOnClickCallback = this.bindOnClickCallback.bind(this)
        this.bindOnZoomCallback = this.bindOnZoomCallback.bind(this)
        this.bindOnZoomCallback = this.bindOnZoomCallback.bind(this)
        this.mapCreationCallback = this.mapCreationCallback.bind(this)

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
        let edges = await fetchEdges(this.props.graphId, closestVertex['vertex'])

        for (const path of this.state.paths) {
          this.state.map_ref.removeLayer(path)
        }

        closestVertex['pos'] = toMapCoordinate(closestVertex['pos'], this.props.graphMetadata);

        let paths = []

        console.log("edges >>>> ", edges)
        for (const edge of edges) {
            let srcPos = toMapCoordinate(edge['src']['pos'], this.props.graphMetadata)
            let targetPos = toMapCoordinate(edge['trg']['pos'], this.props.graphMetadata)


            let deltaX = srcPos[0] - targetPos[0]
            let deltaY = srcPos[1] - targetPos[1]
            let edgeLength = Math.sqrt(deltaX**2 + deltaY**2)
            let curvature = edgeLength * configs['edge_curvature'] * 0.75

          let signY = deltaX < 0 ? -1 : 1
          let signX = deltaY < 0 ? 1: -1
           let path = L.curve(
           ['M',[srcPos[0], srcPos[1]],
            'C',[srcPos[0] - (deltaX/4) + curvature * signX, srcPos[1] - deltaY/4  + curvature * signY],
                [srcPos[0] - deltaX/4*3 + curvature * signX, srcPos[1] - deltaY/4*3 + curvature * signY],
                [targetPos[0], targetPos[1]]],
                {weight: 3, lineCap: 'round', dashArray: '10', animate: {duration: 5000 * (2**this.state.zoom), iterations: Infinity}}
            ).addTo(this.state.map_ref);
           //  let isThisSrc = edge['src']['vertex'] === closestVertex['vertex']
           //  let otherPos = toMapCoordinate(edge[isThisSrc ? 'trg' : 'src']['pos'], this.props.graphMetadata)
           //  console.log(otherPos)
           //
           //  let deltaX = thisPos[0] - otherPos[0]
           //  let deltaY = thisPos[1] - otherPos[1]
           //  let edgeLength = Math.sqrt(deltaX**2 + deltaY**2)
           //  let curvature = edgeLength * configs['edge_curvature'] * 1.1
           //  curvature = isThisSrc ? curvature : curvature * -1
           //
           //
           // let odl = {color:'red', weight:1, animate: 1}
           // let tempSize =  Math.log(edge['amount'] + 1) / 10
           // console.log(">>>>>>> tempSize ", tempSize)
           // let path = L.curve(
           // ['M',[thisPos[0], thisPos[1]],
           //  'C',[thisPos[0] - (deltaX/4) + curvature, thisPos[1] - (deltaY/4)  + curvature],
           //      [thisPos[0] - (deltaX/4)*3  + curvature, thisPos[1] - (deltaY/4)*3  + curvature],
           //      [otherPos[0], otherPos[1]]],
           //      {weight: tempSize, lineCap: 'round', dashArray: '5', animate: {duration: 3000, iterations: Infinity}}
           //  ).addTo(this.state.map_ref);




            paths.push(path)

        }

        this.setState({closestVertex: closestVertex, paths: paths})
        this.props.setDisplayedAddress(closestVertex)
    }




}

GraphMap
    .propTypes = {};
GraphMap
    .defaultProps = {};

export default GraphMap;
