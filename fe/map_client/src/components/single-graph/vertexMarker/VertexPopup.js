import React, {Component} from 'react';
import {Popup} from "react-leaflet";
import {array, object, string} from "prop-types";
import './leafletPopup.scss'
import {deleteVertexMetadata, postVertexMetadata} from "../../../APILayer";
import '../clearMapControl/clearMapMarkersControl.css'
import PopupCheckbox from "./PopupCheckbox";
import {truncateEth} from "../../../utils/Utils";
import TagListVertex from "../../tagList/tagListVertex";

class VertexPopup extends Component {

    constructor(props) {
        super(props);
        this.state = {
            currentInput: '',
            showAutocompletion: false,
            selfTicked: false
        }
    }

    componentDidMount() {
        console.log("popup mounted ")
    }

    render() {

        let uniqueLabels = new Set(this.props.vertexObject['labels']);
        let uniqueTypes = new Set(this.props.vertexObject['types']);

        uniqueLabels = [...uniqueLabels]
            .filter(e => e && e.length > 0)
            .map((ul) => {
                return {
                    type: 'label',
                    value: ul
                }
            })

        uniqueTypes = [...uniqueTypes]
            .filter(e => e && e.length > 0)
            .map((ul) => {
                return {
                    type: 'type',
                    value: ul
                }
            })

        return (
            <Popup
                ref={popupEl => this.assignPopupProperties(popupEl)}
            >
                <>
                    <span>Look vertex up: </span>
                    <a href={'https://etherscan.io/address/' + this.props.vertexObject['vertex']}
                       target="_blank">{truncateEth(this.props.vertexObject['vertex'])}</a>

                    <TagListVertex
                        autocompletionTerms={this.props.autocompletionTerms}
                        addTag={(metadataObject) => {
                            console.log("sendSelectedTags ", metadataObject)
                            postVertexMetadata(this.props.vertexObject['vertex'], metadataObject)

                        }}
                        deleteTag={(metadataObject) => {
                            console.log("removing ", metadataObject)
                            deleteVertexMetadata(this.props.vertexObject['vertex'], metadataObject)
                        }}
                        metadataObjects={[...uniqueLabels, ...uniqueTypes]}
                    />

                    <PopupCheckbox
                        checkboxCallback={this.props.checkboxCallback}
                        ticked={this.props.ticked}/>
                </>
            </Popup>
        );
    }

    assignPopupProperties(popup) {
        if(popup && popup.options){
            popup.options.autoClose = false;
            popup.options.closeOnClick = false;
        }
    }

}

VertexPopup.propTypes = {
    vertexObject: object.isRequired,
    typesConcatenated: string.isRequired,
    labelsConcatenated: string.isRequired,
    graphName: string.isRequired
}

VertexPopup.defaultProps = {
    typesConcatenated: "",
    labelsConcatenated: "",
}

export default VertexPopup;