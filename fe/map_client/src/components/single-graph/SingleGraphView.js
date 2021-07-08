import React, {Component} from 'react';
import Header from "./header/Header";
import {withRouter} from "react-router-dom";
import SidePanel from "./SidePanel";
import GraphMap from "./graph-map/GraphMap";
import {fetch_recent_tags, fetchGraphMetadata} from "../../API_layer";
import SearchBar from "./search-bar/SearchBar";
import _ from 'underscore';

class SingleGraphView extends Component {

    constructor(props) {
        super(props);
        this.state = {
            graph_metadata: undefined,
            is_marker_visible: false,
            address_displayed_currently: undefined,
            selected_tags: [],
            recentTags: []
        }
        this.toggle_markers = this.toggle_markers.bind(this)
        this.set_displayed_address = this.set_displayed_address.bind(this)
        this.set_selected_tags = this.set_selected_tags.bind(this)
    }

    async componentDidMount() {
        let graphMetadata = await fetchGraphMetadata(this.props.match.params.graph_name);
        let recentTags = await fetch_recent_tags();
        this.setState({
            graph_metadata: graphMetadata,
            recentTags: recentTags['response']
        })
    }

    async componentDidUpdate() {
        let recentTags = await fetch_recent_tags();
        if (_.isEqual(this.state.recentTags, recentTags['response'])) {
            return
        }
        this.setState({recentTags: recentTags['response']})
    }

    render() {
        if (this.state.graph_metadata === undefined) {
            return <div>Loading . . . </div>
        } else {
            return (
                <div className={'flex flex-col p-2'}>
                    <SearchBar
                        graph_name={this.props.match.params.graph_name}
                        set_selected_tags={this.set_selected_tags}
                        vertices_metadata={this.state.vertices_metadata}
                        recentTags={this.state.recentTags}/>
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

    toggle_markers() {
        this.setState({is_marker_visible: !this.state['is_marker_visible']})
    }

    set_displayed_address(address) {
        this.setState({address_displayed_currently: address})
    }

    async set_selected_tags(selected_tags) {
        this.setState({selected_tags: selected_tags})
    }
}

export default withRouter(SingleGraphView);