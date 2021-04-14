import React from 'react';
import './assets/main.css';
import Gallery from "./components/gallery/gallery";

import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link, HashRouter
} from "react-router-dom";
import About from "./components/about/About";
import NavigationBar from "./components/navigationBar/NavigationBar";
import SingleGraphView from "./components/single-graph-view/SingleGraphView";
import GraphThumbnail from "./components/gallery/body/graph-thumbnail/GraphThumbnail";

export default function App() {

    return (<HashRouter>

        <NavigationBar></NavigationBar>


        <Switch>

            <Route exact path="/" component={Gallery}>
            </Route>

            <Route path="/about" component={About}>
            </Route>

            <Route path="/graph/:graph_name">
                <SingleGraphView/>
            </Route>


            <Route path="*">
                <div>
                    <p className={'text-6xl'}>404</p>
                </div>
            </Route>

        </Switch>

    </HashRouter>);
}