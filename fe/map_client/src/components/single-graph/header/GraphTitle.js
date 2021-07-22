import React, {Component} from 'react';
import {withRouter} from "react-router-dom";

class GraphTitle extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className={this.props.className }>
                Graph name:
                <h3 className={'text-2xl'}>{this.props.graphMetadata.graphName}</h3>
            </div>
        );
    }

}

export default withRouter(GraphTitle)