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

let configs = require('../../../../../configurations.json');

class GraphMap extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            zoom: 0,
            center: 'world',
            myMap: null,
            markers: [],
            closest: undefined,
            closest_marker : undefined
        }
        this.draw_markers = this.draw_markers.bind(this)
        this.make_popup = this.make_popup.bind(this)
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
        this.update_markers();
    }

    update_markers() {

        if(this.state.closest !== undefined && this.state.closest_marker === undefined){
            let graphCoordinate = [Number.parseFloat(this.state.closest['x']), Number.parseFloat(this.state.closest['y'])];
            let pos = convert_graph_coordinate_to_map(
                graphCoordinate,
                this.props.graph_metadata['min'],
                this.props.graph_metadata['max'],
                this.props.graph_metadata['tile_size']);

            console.log(">><>>>>")
            console.log(pos)

            let myIcon = L.divIcon({className: 'proximity-marker'});
            let marker = L.marker(pos, {icon: myIcon});

            marker.bindPopup(this.make_popup('Closest point', this.state.closest['eth'])).openPopup();

            this.setState({closest_marker: marker})
            marker.addTo(this.state.myMap);
        }

        if (Object.keys(this.props.vertices_metadata).length === 0) {
            return
        }

        if (this.props.is_marker_visible && this.state.markers.length === 0) {
            this.draw_markers(this.state.myMap);
        }

        if (!this.props.is_marker_visible && this.state.markers.length > 0) {
            for (const i in this.state.markers) {
                this.state.myMap.removeLayer(this.state.markers[i])
            }
            this.setState({markers: []})
        }
    }

    componentDidMount() {

        // uncomment if we need to bound the map
        // let corner1 = L.latLng(0, 0);
        // let corner2 = L.latLng(- configs['tile_size'], configs['tile_size']);
        // let bounds = L.latLngBounds(corner1, corner2); // stops panning (scrolling around)  maxBounds: bounds

        const myMap = this.bindLeafletMapToHtml();

        this.centerView(myMap);

        this.addTileLayerToMap(myMap);

        this.bindOnZoomCallback(myMap);

        myMap.on('click', function (e) {
            let coord = e.latlng;
            let lat = coord.lat;
            let lng = coord.lng;
            // console.log("you clicked the map at latitude: " + lat + " and longitude: " + lng);
            let graph_coordinate = convert_map_coordinate_to_graph(
                [lat, lng],
                this.props.graph_metadata['min'],
                this.props.graph_metadata['max'],
                this.props.graph_metadata['tile_size']);

            if(this.state.closest_marker !== undefined){
                this.state.myMap.removeLayer(this.state.closest_marker)
            }

            fetchClosestPoint(this.props.graph_name, graph_coordinate).then(e => {
                this.setState({
                    closest: e,
                    closest_marker: undefined
                })
            })

        }.bind(this));

        this.setState({myMap: myMap})


    }

    centerView(myMap) {
        myMap.setView(
            [this.props.graph_metadata.tile_size / -2.0,
                this.props.graph_metadata.tile_size / 2.0],
            configs['initial_zoom'])
    }

    bindOnZoomCallback(myMap) {
        console.log(this)
        myMap.on('zoom', function () {
            this.setState({zoom: myMap.getZoom()})
        }.bind(this))
    }

    addTileLayerToMap(myMap) {
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

    bindLeafletMapToHtml() {
        const myMap = L.map('mapid', {
            noWrap: true,
            crs: L.CRS.Simple,
        });
        return myMap;
    }

    make_popup(title, address) {
        let link_etherscan = `<div>
                                <h3>${title}</h3>
                                <a href="https://etherscan.io/address/${address}"
                                    target="_blank">${address}</a>
                            </div>`
        let popup = L.popup()
            .setContent(link_etherscan)
        return popup
    }

    draw_markers(myMap) {


        let markers = []

        // console.log(this.props.vertices_metadata)
        // let d = {"(442, 442)": ["okkkkk"]}
        for (let p in this.props.vertices_metadata) {
            // console.log(">>>>>>>>>>>>>>")
            let pos = convert_graph_coordinate_to_map(
                parseTuple(p),
                this.props.graph_metadata['min'],
                this.props.graph_metadata['max'],
                this.props.graph_metadata['tile_size']);

            let myIcon = L.divIcon({className: 'my-div-icon'});
            let marker = L.marker(pos, {icon: myIcon});
            // marker.on('click', this.props.set_displayed_address(this.props.vertices_metadata[p]))
            markers.push(marker)
            // console.log(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            // console.log(this.props.vertices_metadata[p][1])
            marker.bindPopup(this.make_popup(this.props.vertices_metadata[p][0], this.props.vertices_metadata[p][1])).openPopup();
        }

        for (const marker in markers) {
            // console.log(markers[marker])
            markers[marker].addTo(myMap);
        }
        this.setState({markers: markers})
    }
}

GraphMap.propTypes = {};

GraphMap.defaultProps = {};

export default GraphMap;