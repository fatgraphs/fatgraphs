import React, {Component} from 'react';
import {withRouter} from "react-router-dom";
import {fetchGraphMetadata, fetchRecentMetadataSearches} from "../../APILayer";
import _ from 'underscore';
import SearchBar from "./search-bar/SearchBar";
import {MyContext} from "../../Context";
import GraphMap from "./graph-map/GraphMap";
import SidePanel from "./SidePanel";
import GraphMapHeader from "./header/GraphTitle";
import CopyGtmCommand from "./header/CopyGtmCommand";
import CenteredElement from "../../generic_components/CenteredElement";

class SingleGraphView extends Component {

    static contextType = MyContext

    constructor(props) {
        super(props);
        this.state = {
            graphMetadata: undefined,
            isMarkerVisible: false,
            addressDisplayedCurrently: undefined,
            selectedMetadata: [],
            recentMetadataSearches: []
        }
        this.setDisplayedAddress = this.setDisplayedAddress.bind(this)
    }

    async componentDidMount() {
        let graphMetadata = await fetchGraphMetadata(this.props.match.params.graphName);
        let recentMetadataSearches = await fetchRecentMetadataSearches();
        this.setState({
            graphMetadata: graphMetadata,
            recentMetadataSearches: recentMetadataSearches['response']
        })
    }

    async componentDidUpdate() {
        let recentMetadataSearches = await fetchRecentMetadataSearches();
        if (_.isEqual(this.state.recentMetadataSearches, recentMetadataSearches['response'])) {
            return
        }
        this.setState({recentMetadataSearches: recentMetadataSearches['response']})
    }

    render() {
        if (this.state.graphMetadata === undefined) {
            return <div>Loading . . . </div>
        } else {
            return (
                <div
                    className={'grid grid-rows-tokenGraphLayout grid-cols-tokenGraphLayout grid-cols-3 gap-1 p-4 h-full'}>

                    <CenteredElement>
                        Graph name:
                        <GraphMapHeader
                            className={'col-span-1 row-span-1'}
                            graphMetadata={this.state.graphMetadata}/>
                    </CenteredElement>

                    <SearchBar
                        className={'col-span-1 row-span-1'}
                        graphName={this.props.match.params.graphName}
                        selectedMetadataCallback={(selectedMetadata) => this.setState({selectedMetadata: selectedMetadata})}
                        recentMetadataSearches={this.state.recentMetadataSearches}
                        placeholder={'SEARCH BY NODE TYPE/LABEL'}/>

                    <CenteredElement>
                        <CopyGtmCommand
                            className={'col-span-1 row-span-1'}
                            graphMetadata={this.state.graphMetadata}/>
                    </CenteredElement>

                    <SidePanel
                        className={'col-span-1 row-span-1'}
                        addressDisplayedCurrently={this.state.addressDisplayedCurrently}/>

                    <GraphMap
                        className={'col-span-1 row-span-1'}
                        graphMetadata={this.state.graphMetadata}
                        graphName={this.props.match.params.graphName}
                        setDisplayedAddress={this.setDisplayedAddress}
                        selectedMetadata={this.state.selectedMetadata}
                        recentMetadataSearches={this.state.recentMetadataSearches}/>

                    <SidePanel
                        className={'col-span-1 row-span-1'}
                        addressDisplayedCurrently={this.state.addressDisplayedCurrently}/>
                </div>
            );
        }
    }

    setDisplayedAddress(address) {
        this.setState({addressDisplayedCurrently: address})
    }
}

export default withRouter(SingleGraphView);