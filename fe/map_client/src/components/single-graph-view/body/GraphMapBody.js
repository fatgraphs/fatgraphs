import React from "react";
import Mymap from "./graph-map/Mymap";
import InfoPanel from "./info-panel/InfoPanel";
import ToggleBar from "./toggle-bar/ToggleBar";

class GraphMapBody extends React.Component {

    constructor(props) {
        super(props);
        console.log("constructor called")
        this.state = {
            vertices_metadata: props.vertices_metadata,
            graph_metadata: props.graph_metadata,
            is_marker_visible: true
        }
    }
    render() {
        console.log(this.state.is_marker_visible)
        return <div className={'flex justify-between'}>
            <Mymap graph_metadata={this.state.graph_metadata}
                   vertices_metadata={this.state.vertices_metadata}
                   is_marker_visible={this.state.is_marker_visible}
            />
            <InfoPanel/>
        </div>
    }
}

export default GraphMapBody