import React, {Component} from 'react'
import Gallery from "./components/gallery/GraphGallery";
import {HashRouter, Route, Switch, Redirect} from "react-router-dom";
import About from "./components/about/About";
import SingleGraphView from "./components/single-graph/SingleGraphView";
import NavBar from "./components/navbar/NavBar";
import './reactBlueTemplate/src/styles/theme.scss';
import './main.css'
import {fetchCategories} from "./redux/galleryCategoriesSlice";
import {connect} from "react-redux";

class App extends Component {

    constructor() {
        super();
        this.state = {
            autocompleteTerms: []
        }
    }

    async componentDidMount() {
        document.title = "Token GraphGallery.js"
        this.props.fetchCategories()
    }

    render() {
        return (
            <HashRouter>
                <NavBar/>
                <Switch>

                    <Route path="/about" component={About}>
                    </Route>

                    <Route path="/graph/:graphName/:graphId" component={SingleGraphView}>
                    </Route>

                    <Route path={'/gallery/:galleryType'}>
                        <Gallery/>
                    </Route>

                    <Route path="/">
                        <Redirect to="/gallery/default"/>
                    </Route>

                    <Route path="*">
                        <div>
                            <p className={'text-6xl'}>404</p>
                        </div>
                    </Route>
                </Switch>
            </HashRouter>
        );
    }
}

export default connect(null, {fetchCategories})(App);