import React, {Component} from 'react';
import {fetchGraphs} from "../../API_layer";
import HeaderGraphGallery from "./HeaderGraphGallery";
import BodyGraphGallery from "./BodyGraphGallery";

class Gallery extends Component {

    /**
     * A gallery of available graphs that can be clicked and visualised.
     */

    constructor(props) {
        super(props);
        this.state = {
            available_graphs: undefined,
        }
    }

    async componentDidMount() {
        let graphs = await fetchGraphs()
        this.setState({available_graphs: graphs})
    }


    render() {
        return this.state.available_graphs ?
            <div>
                <HeaderGraphGallery/>
                <BodyGraphGallery available_graphs={this.state.available_graphs}
                             className={"flex-1"}/>
            </div> :
            <div>Loading . . .</div>
    }
}

export default Gallery;