import React from 'react';
import './GraphMap.css';
import L from 'leaflet';
import {
    convert_graph_coordinate_to_map,
    convert_map_coordinate_to_graph,
    parseTuple
} from "../../utils/CoordinatesUtil";
import UrlComposer from "../../utils/UrlComposer";
import {fetchClosestPoint} from "../../API_layer";
import {symmetricDifference} from "../../utils/Utils";

let configs = require('../../../../../configurations.json');


class GraphMap extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            zoom: 0,
            center: 'world',
            myMap: null,
            markers_labels: {},
            closest_vertex: {},
        }
        this.draw_markers_labelled_vertices = this.draw_markers_labelled_vertices.bind(this)
        this.make_vertex_popup = this.make_vertex_popup.bind(this)
        this.draw_marker_closest_vertex = this.draw_marker_closest_vertex.bind(this)
        this.to_map_coordinate = this.to_map_coordinate.bind(this)
        this.to_graph_coordinate = this.to_graph_coordinate.bind(this)
        this.bindOnClickCallback = this.bindOnClickCallback.bind(this)
        this.bindOnZoomCallback = this.bindOnZoomCallback.bind(this)
        this.removeMarker = this.removeMarker.bind(this)
    }

    render() {

        return <div>
            <div>
                <div>Zoom level: {this.state.zoom}</div>
                <div id="mapid"/>
            </div>
        </div>
    }

    componentDidUpdate() {

        this.draw_marker_closest_vertex();

        if (this.props.vertices_metadata.length > 0) {
            this.draw_markers_labelled_vertices(this.state.myMap);
        }
    }

    componentDidMount() {

        // uncomment if we need to bound the map
        // let corner1 = L.latLng(0, 0);
        // let corner2 = L.latLng(- configs['tile_size'], configs['tile_size']);
        // let bounds = L.latLngBounds(corner1, corner2); // stops panning (scrolling around)  maxBounds: bounds

        const myMap = this.bindLeafletMapToHtml();

        this.centerView(myMap);

        this.addTileToMap(myMap);

        this.bindOnZoomCallback(myMap);

        this.bindOnClickCallback(myMap);

        this.setState({myMap: myMap})
    }

    bindLeafletMapToHtml() {
        const myMap = L.map('mapid', {
            noWrap: true,
            crs: L.CRS.Simple,
        });
        return myMap;
    }

    centerView(myMap) {
        myMap.setView(
            [this.props.graph_metadata.tile_size / -2.0,
                this.props.graph_metadata.tile_size / 2.0],
            configs['initial_zoom'])
    }

    addTileToMap(myMap) {
        const tile_url = UrlComposer.tileLayerUrl(this.props.graph_name);
        const layer = L.tileLayer(
            tile_url,
            {
                randint: Math.floor(Math.random() * 200000) + 1,
                maxZoom: this.props.graph_metadata['zoom_levels'] - 1,
                attribution: 'tokengallery 2.0',
                tileSize: this.props.graph_metadata.tile_size,
                detectRetina: true
            }).addTo(myMap);
    }


    bindOnZoomCallback(myMap) {
        myMap.on('zoom', function () {
            this.setState({
                zoom: myMap.getZoom()
            })
        }.bind(this))
    }

    bindOnClickCallback(myMap) {
        myMap.on('click', function (click_event) {

            if (Object.keys(this.state.closest_vertex).length !== 0) {
                this.removeMarker(this.state.closest_vertex['marker'])
            }

            let coord = click_event.latlng;
            let lat = coord.lat;
            let lng = coord.lng;
            // console.log("you clicked the map at latitude: " + lat + " and longitude: " + lng);
            let pos = this.to_graph_coordinate([lat, lng])


            fetchClosestPoint(this.props.graph_name, pos).then(closest_vertex => {

                this.props.set_displayed_address(closest_vertex['eth'])

                this.setState({
                    closest_vertex: {
                        x: closest_vertex['x'],
                        y: closest_vertex['y'],
                        eth: closest_vertex['eth'],
                        size: closest_vertex['size'],
                        marker: undefined
                    }
                })
            })

        }.bind(this));
    }

    removeMarker(marker) {
        this.state.myMap.removeLayer(marker)
    }

    make_vertex_popup(title, address) {
        let link_etherscan = `<div>
                                <h3>${title}</h3>
                                <a href="https://etherscan.io/address/${address}"
                                    target="_blank">${address}</a>
                            </div>`
        let popup = L.popup()
            .setContent(link_etherscan)
        return popup
    }

    draw_markers_labelled_vertices(myMap) {


        let markers_labels = {}

        let selected_types = this.props.vertices_metadata
            .filter(rec => this.props.selected_tags.includes(rec['type']))

        let new_marker_positions = selected_types.map(st => st['pos'])
        let old_marker_positions = Object.keys(this.state.markers_labels)
        let delta = symmetricDifference(new_marker_positions, old_marker_positions)


        if (delta.size === 0) {
            return
        }

        for (const pos of old_marker_positions) {

            this.removeMarker(this.state.markers_labels[pos]['marker'])
            this.removeMarker(this.state.markers_labels[pos]['label'])
        }

        for (let i in selected_types) {
            const {pos, type, eth, size} = selected_types[i]

            let map_coordinate = this.to_map_coordinate(pos)

            let label = this.draw_label(type, map_coordinate);

            let marker = this.make_marker_with_popup('labelled-vertex-marker',
                map_coordinate,
                type,
                eth,
                [size * 2 * (2 ** this.state.zoom),
                    size * 2 * (2 ** this.state.zoom)
                ])

            markers_labels[pos] = {marker: marker, label: label}
            marker.addTo(myMap)
        }

        this.setState({
            markers_labels: markers_labels
        })

    }

    draw_marker_closest_vertex() {

        if (Object.keys(this.state.closest_vertex).length === 0) {
            return
        }
        if(this.state.closest_vertex['marker'] !== undefined && this.state.zoom == this.state.closest_vertex.zoom){
            return
        }

        if(this.state.closest_vertex['marker'] !== undefined){
            this.removeMarker(this.state.closest_vertex['marker'])
        }

        let graphCoordinate = [Number.parseFloat(this.state.closest_vertex['x']), Number.parseFloat(this.state.closest_vertex['y'])];
        let pos = this.to_map_coordinate(graphCoordinate)


        let marker2 = this.make_marker_with_popup('proximity-marker',
            pos,
            "Eth: ",
            this.state.closest_vertex['eth'],
            [this.state.closest_vertex['size'] * (2 ** this.state.zoom),
                this.state.closest_vertex['size'] * (2 ** this.state.zoom)
            ])

        marker2.addTo(this.state.myMap);

        this.setState(oldState => {
            oldState.closest_vertex['marker'] = marker2
            oldState.closest_vertex['zoom'] = this.state.zoom
            return {
                closest_vertex: oldState.closest_vertex
            }
        })
    }


    draw_label(text, pos) {
        let icon = L.divIcon({
            html: `<div class="label-container">
                        <span class="label-vertex">${text}</span>
                    </div>`,
            className: 'label-container'
        });
        let marker = L.marker(pos, {icon: icon});
        marker.addTo(this.state.myMap);
        return marker
    }

    make_marker_with_popup(className, pos, title, eth_addresss, iconSize) {

        let myIcon = L.divIcon({className: className, iconSize: iconSize});
        let marker = L.marker(pos, {icon: myIcon});


        marker.bindPopup(this.make_vertex_popup(
            title,
            eth_addresss)).openPopup();
        return marker
    }

    to_map_coordinate(coordinate) {
        let graph_coord = coordinate;
        if (!Array.isArray(coordinate)) {
            graph_coord = parseTuple(coordinate)
        }
        let pos = convert_graph_coordinate_to_map(
            graph_coord,
            this.props.graph_metadata['min'],
            this.props.graph_metadata['max'],
            this.props.graph_metadata['tile_size']);
        return pos;
    }

    to_graph_coordinate(coordinate) {
        let map_coord = coordinate;
        if (!Array.isArray(coordinate)) {
            map_coord = parseTuple(coordinate)
        }
        let pos = convert_map_coordinate_to_graph(
            map_coord,
            this.props.graph_metadata['min'],
            this.props.graph_metadata['max'],
            this.props.graph_metadata['tile_size']);
        return pos;
    }
}

GraphMap.propTypes = {};

GraphMap.defaultProps = {};

export default GraphMap;