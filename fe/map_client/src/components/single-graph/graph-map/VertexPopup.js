import React, {Component} from 'react';
import SearchBar from "../search-bar/SearchBar";
import {Popup} from "react-leaflet";
import {func, string, array} from "prop-types";

class VertexPopup extends Component {
    constructor(props) {
        super(props);
        this.state = {
            selectedMetadata: []
        }
        this.addMetadataCallback = this.addMetadataCallback.bind(this)
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
                        selectedMetadataCallback={this.addMetadataCallback}
                        recentMetadataSearches={this.props.recentMetadataSearches}
                        placeholder={'ADD METADATA'}/>
                </>
            </Popup>
        );
    }

    getAddedMetadata() {
        let addition = {'type': ' ', 'label': ' '}
        if (this.state.selectedMetadata.length > 0) {
            for (const metadataObject of this.state.selectedMetadata) {
                addition[metadataObject['metadata_type']] += metadataObject['metadata_value'] + " ";
            }
        }
        return addition;
    }

    addMetadataCallback(currentSelection){
        this.props.selectionCallback(currentSelection[currentSelection.length - 1])
        this.setState({
            selectedMetadata: [...currentSelection]
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