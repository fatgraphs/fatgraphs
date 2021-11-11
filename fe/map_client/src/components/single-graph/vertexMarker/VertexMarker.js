import React, {Component} from 'react';
import {generateLargeRandom} from "../../../utils/Utils";
import VertexPopup from "./VertexPopup";
import {Marker} from "react-leaflet";
import {fetchEdges} from "../../../APILayer";
import {toMapCoordinate} from "../../../utils/CoordinatesUtil";
import L from "leaflet";
import {updatePersistOnNewClick} from "../../../redux/markersSlice";
import {connect} from "react-redux";

const configs = require('../../../../../../configurations.json');


class VertexMarker extends Component {

    constructor() {
        super();
        this.state = {
            edges: []
        }
        this.receiveNotification = this.receiveNotification.bind(this)
        this.udpdateEdges = this.udpdateEdges.bind(this)
    }

    async componentDidMount() {
        await this.udpdateEdges();
    }

    async udpdateEdges() {
        if (this.props.fetchEdges) {
            let paths = []
            let edges = await fetchEdges(this.props.graphId, this.props.vertexObject['vertex'])
            for (const edge of edges) {
                let srcPos = toMapCoordinate(edge['src']['pos'], this.props.graphConfiguration)
                let targetPos = toMapCoordinate(edge['trg']['pos'], this.props.graphConfiguration)

                let deltaX = srcPos[0] - targetPos[0]
                let deltaY = srcPos[1] - targetPos[1]
                let edgeLength = Math.sqrt(deltaX ** 2 + deltaY ** 2)
                let curvature = edgeLength * configs['edge_curvature'] * 0.75

                let signY = deltaX < 0 ? -1 : 1
                let signX = deltaY < 0 ? 1 : -1

                let path = L.curve(
                    ['M', [srcPos[0], srcPos[1]],
                        'C', [srcPos[0] - (deltaX / 4) + curvature * signX, srcPos[1] - deltaY / 4 + curvature * signY],
                        [srcPos[0] - deltaX / 4 * 3 + curvature * signX, srcPos[1] - deltaY / 4 * 3 + curvature * signY],
                        [targetPos[0], targetPos[1]]],
                    {
                        color: this.props.vertexObject.vertex === edge['src'].vertex ? configs['out_edge_color'] : configs['in_edge_color'],
                        weight: 3,
                        lineCap: 'round',
                        dashArray: '10',
                        animate: {duration: 5000 * (2 ** this.props.zoom), iterations: Infinity}
                    }
                ).addTo(this.props.mapRef);

                paths.push(path)

            }
            this.setState({edges: paths})
        }
    }

    render() {
        if (this.props.vertexObject !== undefined) {
            return (
                <Marker key={generateLargeRandom()}
                        position={this.props.vertexObject['pos']}
                        eventHandlers={{
                            // bug prevention: double-clicking a marker should be equivalent to click it once
                            dblclick: (e) => {
                                e.stopPropagation();
                            },
                        }}
                >
                    <VertexPopup
                        vertexObject={this.props.vertexObject}
                        graphName={this.props.graphName}
                        graphId={this.props.graphId}
                        recentMetadataSearches={this.props.recentMetadataSearches}
                        autocompletionTerms={this.props.autocompletionTerms}
                        checkboxCallback={this.receiveNotification}
                        ticked={this.props.ticked}
                    />
                </Marker>
            )
        } else {
            return <></>
        }
    }

    componentWillUnmount() {
        this.state.edges.forEach(e => {
            this.props.mapRef.removeLayer(e);
        })
    }

    receiveNotification(event) {
        this.props.updatePersistOnNewClick(
            {
                isChecked: event.target.checked,
                vertex: this.props.vertexObject.vertex
            })
    }


}


export default connect(null, {updatePersistOnNewClick})(VertexMarker);