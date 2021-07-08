import React, {Component} from 'react'
import './assets/main.css';
import Gallery from "./components/gallery/GraphGallery";

import {HashRouter, Route, Switch} from "react-router-dom";
import About from "./components/about/About";
import MainNavBar from "./components/MainNavBar";
import SingleGraphView from "./components/single-graph/SingleGraphView";
import {fetchAutocompletionTerms} from "./API_layer";
import {MyContext} from "./Context";

class App extends Component {

    constructor() {
        super();
        this.state = {
            autocomplete: {}
        }
    }

    async componentDidMount() {
        document.title = "Token GraphGallery.js"
        let autocomplete_response = await fetchAutocompletionTerms();
        console.log('autocomplete')
        console.log(autocomplete_response)
        this.setState({
            autocomplete: autocomplete_response['response']
        })
    }

    render() {
        return (
            <HashRouter>
                <MainNavBar/>

                <MyContext.Provider value={{autocomplete: this.state.autocomplete}}>
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
                </MyContext.Provider>

            </HashRouter>
        );
    }
}

export default App;