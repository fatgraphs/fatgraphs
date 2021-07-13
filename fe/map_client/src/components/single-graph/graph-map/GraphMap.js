import React from 'react';
import L from 'leaflet';
import UrlComposer from "../../../utils/UrlComposer";
import {fetchMatchingVertices, fetchClosestPoint, postVertexMetadata} from "../../../APILayer";
import {toGraphCoordinate, toMapCoordinate} from "../../../utils/CoordinatesUtil";
import {MapContainer, Marker, TileLayer} from 'react-leaflet'
import {generateLargeRandom} from "../../../utils/Utils";
import {getCircleIcon, getTextLabelIcon, getVertexPopup} from "./VisualElements";
import _ from "underscore";

let configs = require('../../../../../../configurations.json');

class GraphMap extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            mapRef: undefined,
            selectedMetadata: [],
            closestVertex: undefined,
            zoom: 0
        }
        this.bindOnClickCallback = this.bindOnClickCallback.bind(this)
        this.bindOnZoomCallback = this.bindOnZoomCallback.bind(this)
        this.bindOnZoomCallback = this.bindOnZoomCallback.bind(this)
        this.mapCreationCallback = this.mapCreationCallback.bind(this)
    }


    async componentDidUpdate(prevProps, prevState, snapshot) {
        if (_.isEqual(this.props.selectedMetadata, prevProps.selectedMetadata)) {
            return
        }
        let selectedMetadata = await this.getVerticesMatchingMetadata(this.props.selectedMetadata);
        this.setState({selectedMetadata: selectedMetadata})

    }

    render() {
        const tileUrl = UrlComposer.tileLayerUrl(this.props.graphName);
        const position = [this.props.graphMetadata.tileSize / -2.0,
            this.props.graphMetadata.tileSize / 2.0]


        return <MapContainer
            whenCreated={this.mapCreationCallback}
            className={'h-96 bg-black z-10'}
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
            {this.generateCircleWithPopup(this.state.closestVertex, this.state.zoom)}
            {this.state.selectedMetadata.map((e, i) => {
                return this.generateTextLabel(e, this.state.zoom)
            })
            }
        </MapContainer>
    }

    async getVerticesMatchingMetadata(metadataObjects) {
        let verticesMatchingMetadata = []
        for (const metadataObject of metadataObjects) {
            let response = await fetchMatchingVertices(this.props.graphMetadata.graphName, metadataObject);
            verticesMatchingMetadata.push(...response['response'])
        }

        // the same eth may have multiple types and labels
        let groupedByEth = _.groupBy(verticesMatchingMetadata, 'eth');

        let markers = []

        for (const eth in groupedByEth) {

            const types = groupedByEth[eth].map(obj => obj.type)
            const labels = groupedByEth[eth].map(obj => obj.label)
            const {pos, size} = groupedByEth[eth][0]
            let mapCoordinate = toMapCoordinate(pos, this.props.graphMetadata)

            markers.push({
                types: types,
                labels: labels,
                pos: mapCoordinate,
                size: size,
                eth: eth
            })
        }
        return markers;
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

    addTileToMap(mapRef) {
        const tileUrl = UrlComposer.tileLayerUrl(this.props.graphName);
        const layer = L.tileLayer(
            tileUrl,
            {
                randint: Math.floor(Math.random() * 200000) + 1,
                maxZoom: this.props.graphMetadata['zoomLevels'] - 1,
                attribution: 'tokengallery 2.0',
                tileSize: this.props.graphMetadata.tileSize,
                detectRetina: true
            }).addTo(mapRef);
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
            // console.log("coord ", coord)
            let lat = coord.lat;
            let lng = coord.lng;
            let pos = toGraphCoordinate([lat, lng], this.props.graphMetadata)
            console.log('pos ', pos)
            this.fetchClosestAndUpdate(pos);

        }.bind(this));
    }


    fetchClosestAndUpdate(pos) {
        console.log('pos ', pos)
        fetchClosestPoint(this.props.graphName, pos).then(closestVertex => {
            closestVertex['pos'] = toMapCoordinate(closestVertex['pos'], this.props.graphMetadata)
            this.setState({closestVertex: closestVertex})
            this.props.setDisplayedAddress(closestVertex['eth'])
        })
    }

    generateCircleWithPopup(markerObject, zoom) {
        if (markerObject !== undefined) {
            let {types, labels, pos, size, eth} = markerObject
            let iconSize = size * (2 ** zoom);
            let icon = getCircleIcon('rounded-full border-green-500 bg-green-100 bg-opacity-70 border-2', [iconSize, iconSize])
            let labelsString = labels === null ? 'NA' : labels.join(', ');
            let typesString = types === null ? 'NA' : types.join(', ');

            let popup = getVertexPopup(typesString, labelsString, eth, this.props.graphName, this.addSingleMetadataToVertex(eth), this.props.recentMetadataSearches);

            return (
                <Marker key={generateLargeRandom()}
                        position={pos}
                        icon={icon}
                >
                    {popup}
                </Marker>
            );

        } else {
            return <></>
        }
    }


    generateTextLabel(markerObject, zoom) {
        if (markerObject !== undefined) {
            let {types, labels, pos, size, eth} = markerObject
            let icon = getTextLabelIcon(eth, pos, labels, types)
            let labelsString = labels === null ? 'NA' : labels.join(', ');
            let typesString = types === null ? 'NA' : types.join(', ');

            let popup = getVertexPopup(typesString, labelsString, eth, this.props.graphName, this.addSingleMetadataToVertex(eth), this.props.recentMetadataSearches);
            return (
                <Marker key={generateLargeRandom()}
                        position={pos}
                        icon={icon}>
                    {popup}
                </Marker>
            );

        } else {
            return <></>
        }

    }

    addSingleMetadataToVertex(eth) {
        return async function (e) {
            await postVertexMetadata(eth, e['metadata_value'], e['metadata_type'])
        }.bind(this)
    }


}

GraphMap
    .propTypes = {};
GraphMap
    .defaultProps = {};

export default GraphMap;