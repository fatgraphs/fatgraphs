import React, {Component} from 'react';
import {fetchGraphs} from "../../APILayer";
import HeaderGraphGallery from "./HeaderGraphGallery";
import BodyGraphGallery from "./BodyGraphGallery";
import {MyContext} from "../../Context";

class Gallery extends Component {

    /**
     * A gallery of available graphs that can be clicked and visualised.
     */

    static contextType = MyContext

    constructor(props) {
        super(props);
        this.state = {
            availableGraphs: undefined,
        }
    }

    async componentDidMount() {
        let graphs = await fetchGraphs('default_user')
        this.setState({
            availableGraphs: graphs,
        })
    }


    render() {
        return this.state.availableGraphs ?
            <>
                <HeaderGraphGallery/>
                <BodyGraphGallery availableGraphs={this.state.availableGraphs}
                                  autocompletion={this.state.autocompletion}
                                  className={"flex-1"}/>
            </> :
            <div>Loading . . .</div>
    }
}

export default Gallery;

