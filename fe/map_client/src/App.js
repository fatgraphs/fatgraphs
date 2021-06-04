import React, {useEffect} from 'react'
import './assets/main.css';
import Gallery from "./components/gallery/GraphGallery";

import {HashRouter, Route, Switch} from "react-router-dom";
import About from "./components/about/About";
import MainNavBar from "./components/MainNavBar";
import SingleGraphView from "./components/single-graph/SingleGraphView";

export default function App() {

    useEffect(() => {
        document.title = "Token GraphGallery.js"
    }, [])

    return (<HashRouter>

        <MainNavBar></MainNavBar>


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