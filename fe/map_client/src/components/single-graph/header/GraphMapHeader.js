import React, {Component} from 'react';
import {withRouter} from "react-router-dom";
import GraphNavBar from "./GraphNavBar";
import CopyGtmCommand from "./CopyGtmCommand";

class GraphMapHeader extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <>

                 <div className={'flex flex-row flex-wrap p-2'}>
                    <h3 className={'text-2xl'}>{this.props.graphMetadata.graphName}</h3>
                    <CopyGtmCommand graphMetadata={this.props.graphMetadata}/>
                </div>
                <div className={'flex flex-row flex-wrap p-2'}>
                    <GraphNavBar graphMetadata={this.props.graphMetadata}/>
                </div>
            </>
        );
    }

}

export default withRouter(GraphMapHeader);