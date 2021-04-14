import React, {Component} from 'react';
import SingleGraphView from "../../../single-graph-view/SingleGraphView";
import {useHistory} from "react-router";

class GraphThumbnail extends Component {

    constructor(props) {
        super(props);
        this.state = {
            name: props.name,
            key: props.key,
            open: props.open,
        }
        this.handleClick = this.handleClick.bind(this)
    }

    render() {
        return <>
            <div key={this.state.key}
                 className={"m-2 p-1 border-4 border-black bg-gray-100 border-opacity-75 cursor-pointer hover:bg-gray-300"}
                 onClick={this.handleClick}>
                <p>{this.state.name}</p>
            </div>
        </>;
    }

    handleClick() {
        this.state.open(this.state.name)
    }
}

export default GraphThumbnail;