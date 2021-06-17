import React, {Component} from 'react';
import Header from "./header/Header";
import {withRouter} from "react-router-dom";
import SidePanel from "./SidePanel";
import GraphMap from "./GraphMap";
import {fetchGraphMetadata, fetchVerticesMetadata} from "../../API_layer";
import SearchBar from "./search-bar/SearchBar";

class SingleGraphView extends Component {

    constructor(props) {
        super(props);
        this.state = {
            vertices_metadata: undefined,
            graph_metadata: undefined,
            is_marker_visible: false,
            address_displayed_currently: undefined,
            selected_tags: []
        }
        this.toggle_markers = this.toggle_markers.bind(this)
        this.set_displayed_address = this.set_displayed_address.bind(this)
        this.set_selected_tags = this.set_selected_tags.bind(this)
    }

    render() {
        if (this.state.vertices_metadata === undefined || this.state.graph_metadata === undefined) {
            return <div>Loading . . . </div>
        } else {
            return (
                <div className={'flex flex-col p-2'}>
                    <SearchBar
                        graph_name={this.props.match.params.graph_name}
                        selection_updated_callback={this.set_selected_tags}
                        vertices_metadata={this.state.vertices_metadata}/>
                    <Header graph_metadata={this.state.graph_metadata}/>
                    <div className={'flex flex-col lg:flex-row'}>
                        <GraphMap graph_metadata={this.state.graph_metadata}
                                  vertices_metadata={this.state.vertices_metadata}
                                  graph_name={this.props.match.params.graph_name}
                                  is_marker_visible={this.state.is_marker_visible}
                                  set_displayed_address={this.set_displayed_address}
                                  selected_tags={this.state.selected_tags}/>
                        <SidePanel
                            address_displayed_currently={this.state.address_displayed_currently}/>
                    </div>
                </div>
            );
        }
    }

    async componentDidMount() {
        let graphMetadata = await fetchGraphMetadata(this.props.match.params.graph_name);
        let verticesMetadata_response = await fetchVerticesMetadata(this.props.match.params.graph_name);
        this.setState({graph_metadata: graphMetadata})
        this.setState({vertices_metadata: verticesMetadata_response['response']})
    }

    toggle_markers() {
        this.setState({is_marker_visible: !this.state['is_marker_visible']})
    }

    set_displayed_address(address) {
        this.setState({address_displayed_currently: address})
    }

    set_selected_tags(selected_tags) {
        this.setState({selected_tags: selected_tags})
    }
}

export default withRouter(SingleGraphView);