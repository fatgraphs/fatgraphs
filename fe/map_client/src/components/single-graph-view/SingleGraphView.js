import React, {Component} from 'react';
import UrlComposer from "../../UrlComposer";

class SingleGraphView extends Component {

    constructor(props) {
        super(props);
        this.state = {
            graph_name: props.graph_name,
            vertices_metadata: undefined,
            graph_metadata: undefined
        }
    }

    render() {
        console.log(this.state)
        if (this.state.vertices_metadata === undefined || this.state.graph_metadata === undefined) {
            return <div>Loading . . . </div>
        } else {
            return (
                <div>
                    {/*<GraphMapHeader graph_metadata={this.state.graph_metadata}/>*/}
                    {/*<GraphMapBody graph_metadata={this.state.graph_metadata} vertices_metadata={this.state.vertices_metadata}/>*/}
                    {/*<GraphMapFooter/>*/}
                </div>
            );
        }
    }

    componentDidMount() {
        fetch(UrlComposer.verticesMetadata(this.state.graph_name))
        .then(response =>
            response.json())
        .then(data => {
            this.setState({"vertices_metadata": data})
        })

        fetch(UrlComposer.graphMetadata(this.state.graph_name))
        .then(response =>
            response.json())
        .then(data => {
            this.setState({"graph_metadata": data})
        })
    }
}

export default SingleGraphView;