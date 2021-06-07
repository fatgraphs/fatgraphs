import React, {Component} from 'react';
import DescriptionTable from "../../../generic_components/DescriptionTable";
import {faClipboard} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
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
            <div className={'border-2 flex-1'}>
                <h3 className={'text-2xl'}>{this.props.graph_metadata.graph_name}</h3>
                <CopyGtmCommand graph_metadata={this.props.graph_metadata}/>
                <GraphNavBar graph_metadata={this.props.graph_metadata}/>
            </div>
        );
    }

}

export default withRouter(GraphMapHeader);