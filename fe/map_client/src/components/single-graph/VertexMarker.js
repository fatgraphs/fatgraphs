import React, { Component } from 'react'; import {generateLargeRandom} from "../../utils/Utils";
import VertexPopup from "./VertexPopup";
import {Marker} from "react-leaflet";
import {postVertexMetadata} from "../../APILayer";

class VertexMarker extends Component {

 render() {
      if (this.props.markerObject !== undefined) {
        return (

            <Marker key={generateLargeRandom()}
                    position={this.props.markerObject['pos']}
            >
                <VertexPopup
                    types={this.props.markerObject['types']}
                    labels={this.props.markerObject['labels']}
                    vertex={this.props.markerObject['vertex']}
                    graphName={this.props.graphName}
                    graphId={this.props.graphId}
                    recentMetadataSearches={this.props.recentMetadataSearches}
                    autocompletionTerms={this.props.autocompletionTerms}
                />
            </Marker>)
      } else {
        return <></>
      }
  }
}


export default VertexMarker;