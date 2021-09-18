import React, {Component} from 'react'
import Gallery from "./components/gallery/GraphGallery";
import {HashRouter, Route, Switch} from "react-router-dom";
import About from "./components/about/About";
import SingleGraphView from "./components/single-graph/SingleGraphView";
import {fetchAutocompletionTerms} from "./APILayer";
import {MyContext} from "./Context";
import NavBar from "./components/navbar/NavBar";

import './reactBlueTemplate/src/styles/theme.scss';
import './main.css'

class App extends Component {

    constructor() {
        super();
        this.state = {
            autocompleteTerms: []
        }
    }

    async componentDidMount() {
        document.title = "Token GraphGallery.js"
    }

    render() {
        return (
            <HashRouter>
                <NavBar/>

                <MyContext.Provider>
                    <Switch>
                        <Route exact path="/" component={Gallery}>
                        </Route>

                        <Route path="/map" component={About}>
                        </Route>

                        <Route path="/graph/:graphName/:graphId">
                            <SingleGraphView/>
                        </Route>


                        <Route path="*">
                            <div>
                                <p className={'text-6xl'}>404</p>
                            </div>
                        </Route>
                    </Switch>
                </MyContext.Provider>

            </HashRouter>
        );
    }
}

export default App;