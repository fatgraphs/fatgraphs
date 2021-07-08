import React from 'react';
import './GraphMap.css';
import L from 'leaflet';
import UrlComposer from "../../../utils/UrlComposer";
import {fetchClosestPoint} from "../../../API_layer";
import ClickClosestVertex from "./ClickClosestVertex";
import {to_graph_coordinate} from "../../../utils/CoordinatesUtil";
import SelectedVertices from "./SelectedVertices";

let configs = require('../../../../../../configurations.json');


class GraphMap extends React.Component {

    constructor(props) {
        super(props);
        this.clickClosestVertex = undefined;
        this.selectedVertices = undefined;
        this.state = {
            center: 'world',
            myMap: null,
            closest_vertex: undefined,
            zoom: 0
        }
        this.bindOnClickCallback = this.bindOnClickCallback.bind(this)
        this.bindOnZoomCallback = this.bindOnZoomCallback.bind(this)
    }

    render() {
        return <div>
            <div>
                <div>Zoom level: {this.state.zoom}</div>
                <div id="mapid" className={'z-10'}/>
            </div>
        </div>
    }

    componentDidUpdate() {
        this.clickClosestVertex.update(this.state.zoom, this.state.closest_vertex)
        this.selectedVertices.update(this.state.zoom, this.props.selected_tags)
    }

    componentDidMount() {

        // uncomment if we need to bound the map
        // let corner1 = L.latLng(0, 0);
        // let corner2 = L.latLng(- configs['tile_size'], configs['tile_size']);
        // let bounds = L.latLngBounds(corner1, corner2); // stops panning (scrolling around)  maxBounds: bounds

        const myMap = this.bindLeafletMapToHtml();

        this.clickClosestVertex = new ClickClosestVertex(myMap, this.props.graph_metadata)
        this.selectedVertices = new SelectedVertices(myMap, this.props.graph_metadata)

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

            let coord = click_event.latlng;
            let lat = coord.lat;
            let lng = coord.lng;
            // console.log("you clicked the map at latitude: " + lat + " and longitude: " + lng);
            let pos = to_graph_coordinate([lat, lng], this.props.graph_metadata)

            fetchClosestPoint(this.props.graph_name, pos).then(closest_vertex => {
                this.setState({closest_vertex: closest_vertex})
                this.props.set_displayed_address(closest_vertex['eth'])
            })

        }.bind(this));
    }
}

GraphMap.propTypes = {};
GraphMap.defaultProps = {};

export default GraphMap;