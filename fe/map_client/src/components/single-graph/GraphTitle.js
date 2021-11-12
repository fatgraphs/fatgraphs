import React, {Component} from 'react';
import {withRouter} from "react-router-dom";
import {connect} from "react-redux";

class GraphTitle extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className={this.props.className }>
                Graph name:
                <h3 className={'text-2xl'}>{this.props.graphName}</h3>
            </div>
        );
    }

}

let mapStateToPropsGraphTitle = state => {
    return {
        graphName: state.graph.graph.graphName
    }
}

export default withRouter(connect(mapStateToPropsGraphTitle, null)(GraphTitle))