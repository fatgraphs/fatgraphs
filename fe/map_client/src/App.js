//import './App.css';
///import Mymap from "./components/graph-map/Mymap";
import React from 'react';
import Mymap from "./components/map-body/graph-map/Mymap";
import '../build/styles.css'
import GraphMapHeader from "./components/map-header/GraphMapHeader";
import GraphMapBody from "./components/map-body/GraphMapBody";
import GraphMapFooter from "./components/GraphMapFooter";

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"
                      integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A=="
                      crossOrigin=""/>
                <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"
                        integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA=="
                        crossOrigin=""></script>
            </header>
            <GraphMapHeader graph_name={'test medium graph'}/>
            <GraphMapBody/>
            <GraphMapFooter/>
        </div>
    );
}

export default App;
