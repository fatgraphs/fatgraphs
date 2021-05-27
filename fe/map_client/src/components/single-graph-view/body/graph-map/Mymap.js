import React from 'react';
import './Mymap.css';
import L from 'leaflet';
import {
    convert_graph_coordinate_to_map,
    convert_map_coordinate_to_graph,
    parseTuple
} from "../../../../utils/CoordinatesUtil";
let configs = require('../../../../../../../configurations');

class Mymap extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            zoom: 0,
            center: 'world',
            myMap: null,
            markers: []
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

            {/*<ToggleBar className={'border flex-6'}*/}
            {/*    call_back={this.toggle_markers}*/}
            {/*/>*/}

        </div>
    }

    componentDidUpdate() {
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

        let initial_zoom = 0;
        const myMap = L.map('mapid', {
            noWrap: true,
            crs: L.CRS.Simple,
        }).setView([this.props.graph_metadata.tile_size / -2.0, this.props.graph_metadata.tile_size / 2.0], initial_zoom);

        this.setState({myMap: myMap})

        // TODO: create API file for all calls to server and add the tile call
        const layer = L.tileLayer(configs['endpoints']['base'] + configs['endpoints']['tile'] + "/" + this.props.graph_name + '/{z}/{x}/{y}.png?{randint}', {
            randint: Math.floor(Math.random() * 200000) + 1,
            maxZoom: this.props.graph_metadata['zoom_levels'] - 1,
            attribution: 'tokengallery 2.0',
            tileSize: this.props.graph_metadata.tile_size,
            detectRetina: true
        }).addTo(myMap);

        myMap.on('zoom', function () {
            this.setState({zoom: myMap.getZoom()})
        }.bind(this))
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
            console.log(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            console.log(this.props.vertices_metadata[p][1])
            marker.bindPopup(this.make_popup(this.props.vertices_metadata[p][0], this.props.vertices_metadata[p][1])).openPopup();
        }

        for (const marker in markers) {
            // console.log(markers[marker])
            markers[marker].addTo(myMap);
        }
        this.setState({markers: markers})
    }
}

Mymap.propTypes = {};

Mymap.defaultProps = {};

export default Mymap;