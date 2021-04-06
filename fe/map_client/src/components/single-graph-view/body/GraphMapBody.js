import React from "react";
import Mymap from "./graph-map/Mymap";

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
        return <div>
            <Mymap graph_metadata={this.state.graph_metadata}
                   vertices_metadata={this.state.vertices_metadata}
                   is_marker_visible={this.state.is_marker_visible}
                   graph_name={this.props.graph_name}/>
            {/*<InfoPanel/>*/}
        </div>
    }
}

export default GraphMapBody