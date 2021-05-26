import React, {Component} from 'react';
import UrlComposer from "../../UrlComposer";
import GraphMapHeader from "./header/GraphMapHeader";
import {withRouter} from "react-router-dom";
import InfoPanel from "./body/info-panel/InfoPanel";
import Mymap from "./body/graph-map/Mymap";

class SingleGraphView extends Component {

    constructor(props) {
        super(props);
        this.state = {
            vertices_metadata: undefined,
            graph_metadata: undefined,
            is_marker_visible: false,
            address_displayed_currently: undefined
        }
        this.toggle_markers = this.toggle_markers.bind(this)
        this.set_displayed_address = this.set_displayed_address.bind(this)
    }

    render() {
        if (this.state.vertices_metadata === undefined || this.state.graph_metadata === undefined) {
            return <div>Loading . . . </div>
        } else {
            return (
                <div className={'flex flex-col p-2'}>
                    <GraphMapHeader graph_metadata={this.state.graph_metadata}/>
                    <div className={'flex flex-col lg:flex-row'}>
                        <Mymap graph_metadata={this.state.graph_metadata}
                               vertices_metadata={this.state.vertices_metadata}
                               graph_name={this.props.match.params.graph_name}
                               is_marker_visible={this.state.is_marker_visible}
                               set_displayed_address={this.set_displayed_address}/>
                        <InfoPanel toggle={[this.toggle_markers]}
                                   address_displayed_currently={this.state.address_displayed_currently}/>
                    </div>
                </div>
            );
        }
    }

    componentDidMount() {
        fetch(UrlComposer.verticesMetadata(this.props.match.params.graph_name))
            .then(response =>
                response.json())
            .then(data => {
                this.setState({"vertices_metadata": data})
            })

        fetch(UrlComposer.graphMetadata(this.props.match.params.graph_name))
            .then(response =>
                response.json())
            .then(data => {
                this.setState({"graph_metadata": data})
            })
    }

    toggle_markers() {
        this.setState({is_marker_visible: !this.state['is_marker_visible']})
        console.log(this.state)
    }

    set_displayed_address(address) {

        function on_marker_click_callback() {
            this.setState({address_displayed_currently: address})
        }

        on_marker_click_callback = on_marker_click_callback.bind(this)
        return on_marker_click_callback
    }
}

export default withRouter(SingleGraphView);