import React, {Component} from 'react';
import {withRouter} from "react-router-dom";
import GraphNavBar from "./GraphNavBar";
import CopyGtmCommand from "./CopyGtmCommand";

class GraphMapHeader extends Component {

    constructor(props) {
        super(props);
        console.log(this.props.graph_metadata);
    }

    render() {
        return (
            <div>
                <h3 className={'text-2xl'}>{this.props.graph_metadata.graph_name}</h3>
                <div className={'flex flex-row flex-wrap p-2'}>
                    <GraphNavBar graph_metadata={this.props.graph_metadata}/>
                    <CopyGtmCommand graph_metadata={this.props.graph_metadata}/>
                </div>
            </div>

        );
    }

}

export default withRouter(GraphMapHeader);