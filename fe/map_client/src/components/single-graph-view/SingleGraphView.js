import React, {Component} from 'react';
import UrlComposer from "../../UrlComposer";
import GraphMapHeader from "./header/GraphMapHeader";
import GraphMapBody from "./body/GraphMapBody";
import {withRouter} from "react-router-dom";
import InfoPanel from "./body/info-panel/InfoPanel";

class SingleGraphView extends Component {

    constructor(props) {
        super(props);
        const graph_name = this.props.match.params.graph_name;
        this.state = {
            graph_name: graph_name,
            vertices_metadata: undefined,
            graph_metadata: undefined
        }
    }

    render() {
        if (this.state.vertices_metadata === undefined || this.state.graph_metadata === undefined) {
            return <div>Loading . . . </div>
        } else {
            return (
                <div className={'flex flex-col p-2'}>
                    <GraphMapHeader graph_metadata={this.state.graph_metadata}/>
                    <div className={'flex flex-col lg:flex-row'}>
                        <GraphMapBody graph_metadata={this.state.graph_metadata}
                                      vertices_metadata={this.state.vertices_metadata}
                                      graph_name={this.state.graph_name}/>
                        <InfoPanel/>
                    </div>
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

export default withRouter(SingleGraphView);