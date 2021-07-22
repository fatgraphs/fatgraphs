import React, {Component} from 'react';
import SearchBar from "../search-bar/SearchBar";
import {Popup} from "react-leaflet";
import {func, string, array} from "prop-types";

class VertexPopup extends Component {
    constructor(props) {
        super(props);
        this.state = {
            recentlyAddedMetadata: []
        }
        this.vertexAddMetadataCallback = this.vertexAddMetadataCallback.bind(this)
    }

    render() {
        let addedMetadata = this.getAddedMetadata();
        return (
            <Popup>
                <>
                    <div><span>Types : </span> <span>{this.props.typesConcatenated + addedMetadata['type']}</span></div>
                    <div><span>Labels : </span> <span>{this.props.labelsConcatenated + addedMetadata['label']}</span></div>
                    <a href={'https://etherscan.io/address/' + this.props.eth}
                       target="_blank">{this.props.eth}</a>
                    <SearchBar
                        showSelected={false}
                        graphName={this.props.graphName}
                        graphId={this.props.graphId}
                        selectedMetadataCallback={this.vertexAddMetadataCallback}
                        recentMetadataSearches={this.props.recentMetadataSearches}
                        placeholder={'ADD METADATA'}/>
                </>
            </Popup>
        );
    }

    getAddedMetadata() {
        let addition = {'type': ' ', 'label': ' '}
        if (this.state.recentlyAddedMetadata.length > 0) {
            for (const metadataObject of this.state.recentlyAddedMetadata) {
                addition[metadataObject['type']] += metadataObject['value'] + " ";
            }
        }
        return addition;
    }

    vertexAddMetadataCallback(currentSelection){
        this.props.selectionCallback(currentSelection[currentSelection.length - 1])
        this.setState({
            recentlyAddedMetadata: [...currentSelection]
        })
    }
}

VertexPopup.propTypes = {
    eth: string.isRequired,
    selectionCallback: func.isRequired,
    typesConcatenated: string.isRequired,
    labelsConcatenated: string.isRequired,
    graphName: string.isRequired,
    recentMetadataSearches: array.isRequired
}

VertexPopup.defaultProps = {
    typesConcatenated: "",
    labelsConcatenated: "",
}

export default VertexPopup;