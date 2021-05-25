import React from 'react';
import './Mymap.css';
import L from 'leaflet';

let configs = require('../../../../../../../configurations');

class Mymap extends React.Component {

    constructor (props) {
        super(props);
        this.state={
            zoom:0,
            center:'world',
            myMap: null,
            markers: []
        }
        this.draw_markers = this.draw_markers.bind(this)
    }

    render() {

        return <div>
            <div >
                <div>Zoom level: {this.state.zoom}</div>
                <div id="mapid"/>
            </div>

            {/*<ToggleBar className={'border flex-6'}*/}
            {/*    call_back={this.toggle_markers}*/}
            {/*/>*/}

            </div>
    }

    componentDidUpdate() {
        console.log(this.state.markers)

        if(this.props.is_marker_visible && this.state.markers.length === 0){
            this.draw_markers(this.state.myMap);
        }

        if(! this.props.is_marker_visible && this.state.markers.length > 0){
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
        const myMap = L.map('mapid' , {
            noWrap: true,
            crs: L.CRS.Simple,
        }).setView([this.props.graph_metadata.tile_size / -2.0, this.props.graph_metadata.tile_size / 2.0], initial_zoom);

        this.setState({myMap: myMap})

        // TODO: create API file for all calls to server and add the tile call
        const layer = L.tileLayer(configs['endpoints']['base'] +  configs['endpoints']['tile'] + "/" + this.props.graph_name + '/{z}/{x}/{y}.png?{randint}', {
            randint: Math.floor( Math.random() * 200000 ) + 1,
            maxZoom: this.props.graph_metadata['zoom_levels'] - 1,
            attribution: 'tokengallery 2.0',
            tileSize: this.props.graph_metadata.tile_size,
            detectRetina: true
        }).addTo(myMap);

        myMap.on('zoom', function () {
            this.setState({zoom: myMap.getZoom()})
        }.bind(this))
    }

    draw_markers(myMap) {

        let popup = L.popup()
            .setContent('<p>Hello world!<br />This is a nice popup.</p>')

        let markers = []

        // console.log(this.props.vertices_metadata)
        let d = { "(442, 442)": ["okkkkk"]}
        for (let p in this.props.vertices_metadata) {
            // console.log(">>>>>>>>>>>>>>")
            let pos = convert_graph_coordinate_to_map(
                parseTuple(p),
                this.props.graph_metadata['min'],
                this.props.graph_metadata['max'],
                this.props.graph_metadata['tile_size']);

            let myIcon = L.divIcon({className: 'my-div-icon'});
            let marker = L.marker(pos, {icon: myIcon});
            markers.push(marker)
            // marker.bindPopup(popup).openPopup()
            //         .addTo(myMap);
        }
        console.log("okkkkkkkk >>>>>>>>>>")
        // this.setState({markers: markers})
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

// TODO: move somewhere else

/**
 * Given a graph coordinate (as generated by force atlas 2) it returns the
 * corresponding coordinate on the map.
 *
 * @param graph_coordinate
 * @param g_min: this should be the smallest number appearing either as x or y among all
 * the coordinates of the graph
 * @param g_max same as g_min but the largest number
 * @param tile_size tile size used when generating the graph tiles
 */
function convert_graph_coordinate_to_map(graph_coordinate, g_min, g_max, tile_size){
    console.log("graph_coordinate" + graph_coordinate)
    // console.log(g_min)
    // console.log(g_max)
    let graph_side = g_max - g_min
    console.log("graph sixe: " + graph_side)
    let map_x = (graph_coordinate[0] + Math.abs(g_min)) * tile_size / graph_side
    let map_y = (graph_coordinate[1] + Math.abs(g_min)) * tile_size / graph_side
    // console.log(">>>>>>>>>>>>>>")
    console.log([- map_y, map_x])
    return [- map_y, map_x]
}

function parseTuple(t) {
    return JSON.parse("[" + t.replace(/\(/g, "[").replace(/\)/g, "]") + "]")[0];
}