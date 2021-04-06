import React, {Component} from 'react';
import UrlComposer from "../../UrlComposer";
import GraphMapFooter from "./footer/GraphMapFooter";
import GraphMapHeader from "./header/GraphMapHeader";
import GraphMapBody from "./body/GraphMapBody";

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
                <div className={'flex flex-row'}>
                    <GraphMapHeader graph_metadata={this.state.graph_metadata}/>
                    <GraphMapBody graph_metadata={this.state.graph_metadata}
                                  vertices_metadata={this.state.vertices_metadata}
                                  graph_name={this.state.graph_name}/>
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