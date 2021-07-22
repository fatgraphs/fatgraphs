import React, {Component} from 'react';
import GraphThumbnail from "./Thumbnail";
import {withRouter} from "react-router-dom";

class BodyGraphGallery extends Component {

    constructor(props) {
        super(props);
        this.openGraph = this.openGraph.bind(this);
    }

    render() {
        return <div className={'grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 lg:grid-cols-6 xl:grid-cols-7 2xl:grid-cols-9'}>
            {this.props.availableGraphs.map((value, index) => {
                return <GraphThumbnail graph={value}
                                       key={index}
                                       open={this.openGraph}/>
            })}
        </div>

    }

    openGraph(graph) {
        const {match, location, history} = this.props;
        history.push("/graph/" + graph['graphName'] + '/' + graph['id']);
    }
}

export default withRouter(BodyGraphGallery);
