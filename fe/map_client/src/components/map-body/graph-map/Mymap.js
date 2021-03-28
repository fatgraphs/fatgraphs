import React from 'react';
import './Mymap.css';
import L from 'leaflet';
import { INITIAL_ZOOM }  from '../../../configurations'

let configs = require('configurations');

class Mymap extends React.Component {

    constructor (props) {
        super(props);
        this.state={
            zoom:INITIAL_ZOOM,
            center:'world',
            myMap: null
        }
    }

    render() {
        return <div className={'border flex-1'}>
            <div>Zoom level: {this.state.zoom}</div>
            <div id="mapid"/>

        </div>;
    }

    componentDidMount() {

        let corner1 = L.latLng(0, 0);
        let corner2 = L.latLng(- configs['tile_size'], configs['tile_size']);
        let bounds = L.latLngBounds(corner1, corner2); // stops panning (scrolling around)  maxBounds: bounds

        const myMap = L.map('mapid' , {
            noWrap: true,
            crs: L.CRS.Simple,
            maxBounds: bounds,
            maxBoundsViscosity: 0.9
        }).setView([configs['tile_size'] / -2, configs['tile_size'] / 2], INITIAL_ZOOM);

        this.setState({myMap: myMap})

        const layer = L.tileLayer(configs['endpoints']['base'] + configs['endpoints']['tile'] + '/{z}/{x}/{y}.png', {
            maxZoom: configs['zoom_levels'] - 1,
            attribution: 'tokengallery 2.0',
            tileSize: configs['tile_size']
        }).addTo(myMap);

        fetch(configs['endpoints']['base'] + configs['endpoints']['interest_points'])
            .then(response =>
                response.json())
            .then(data => console.log(data));

        // L.marker([0, 500]).addTo(myMap);
        // L.marker([0, 0]).addTo(myMap);

        myMap.on('zoom', function () {
            console.log("on zoom callback")
            this.setState({zoom: myMap.getZoom()})
        }.bind(this))
    }
}

Mymap.propTypes = {};

Mymap.defaultProps = {};

export default Mymap;

// TODO: move somewhere else

/**
 *
 * @param graph_coordinate
 * @param map_side the length of the tile (a tile is a square). The coordinate system of a tile is: (0,0) is top-left,
 * (-map-side, +map_side) is bottom-right
 * @param half_graph_side (half the length of the square that encapsulates the graph; this coordinate system
 * has (0,0)  in the middle
 */
function convert_graph_coordinate_to_map(graph_coordinate, map_side, half_graph_side){
    let map_x = (graph_coordinate[0] * (- map_side / 2 * half_graph_side)) - map_side / 2
    let map_y = (graph_coordinate[1] * (- map_side / 2 * half_graph_side)) - map_side / 2
    return (map_x, map_y)
}