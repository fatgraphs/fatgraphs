import React, {Component} from 'react';
import GraphThumbnail from "./Thumbnail";
import {withRouter} from "react-router-dom";

class BodyGraphGallery extends Component {

    constructor(props) {
        super(props);
        this.state = {
            available_graphs: props.available_graphs,
        }
        this.openGraph = this.openGraph.bind(this);
    }

    render() {
        return <div className={'flex flex-wrap'}>
            {this.state.available_graphs.map((value, index) => {
                return <GraphThumbnail name={value}
                                       key={index}
                                       open={this.openGraph}/>
            })}
        </div>

    }

    openGraph(name) {
        const {match, location, history} = this.props;
        history.push("/graph/" + name);
    }
}

export default withRouter(BodyGraphGallery);