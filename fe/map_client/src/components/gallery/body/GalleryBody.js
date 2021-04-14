import React, {Component} from 'react';
import GraphThumbnail from "./graph-thumbnail/GraphThumbnail";
import {Route, Switch, withRouter} from "react-router-dom";
import SingleGraphView from "../../single-graph-view/SingleGraphView";

class GalleryBody extends Component {

    constructor(props) {
        super(props);
        this.state = {
            available_graphs: props.available_graphs,
        }
        this.openGraph = this.openGraph.bind(this);
    }

    openGraph(name){
        const { match, location, history } = this.props;
        history.push("/graph/" + name);
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
}

export default withRouter(GalleryBody);