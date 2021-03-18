import React from 'react';
import './Mymap.css';
import L from 'leaflet';
import { INITIAL_ZOOM, MAX_ZOOM_IN }  from './constants'

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
        return <div className="Mymap" class={'center'} >
            <div>Zoom level: {this.state.zoom}</div>
            <div id="mapid"></div>

        </div>;
    }

    componentDidMount() {

        let corner1 = L.latLng(50, -50);
        let corner2 = L.latLng(5.1, -5.1);
        let bounds = L.latLngBounds(corner1, corner2); // stops panning (scrolling around)  maxBounds: bounds

        const myMap = L.map('mapid' , {
            noWrap: true,
            crs: L.CRS.Simple,
            center: L.latLng(50.0, 50.0),

        }).setView([-1000, 1000], INITIAL_ZOOM);

        this.setState({myMap: myMap})

        const layer = L.tileLayer('http://127.0.0.1:5000/base_url/tms/1.0.0/test-graph/{z}/{x}/{y}.png', {
            maxZoom: MAX_ZOOM_IN,
            attribution: 'tokengallery 2.0',
            tileSize: 2000
        }).addTo(myMap);

        L.marker([-256, 256]).addTo(myMap);

        myMap.on('zoom', function () {
            console.log("on zoom callback")
            this.setState({zoom: myMap.getZoom()})
        }.bind(this))
    }
}

Mymap.propTypes = {};

Mymap.defaultProps = {};

export default Mymap;


