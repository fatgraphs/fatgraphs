import React, {Component} from 'react';
import {connect} from "react-redux";
import {changeUrl, urlChanged} from "../redux/urlSlice";
import {getQueryParam, updateQueryParam} from "../utils/Utils";
import {withRouter} from "react-router-dom";
import _ from 'underscore';
import {fetchVertices} from "../redux/markersSlice";

class UrlManager extends Component {
    constructor() {
        super();
        this.state = {
            lastQueryParams: {}
        }
    }

    render() {
        return (
            <></>
        );
    }

    componentDidMount() {
        window.onhashchange = function (e) {
            if (!_.isEqual(this.getCurrentQueryParams(), this.props.queryParams)) {
                // console.log("onhashchange")
                // console.log("this.getCurrentQueryParams()", this.getCurrentQueryParams())
                // console.log("this.props.queryParams", this.props.queryParams)
                this.props.changeUrl(this.getCurrentQueryParams())
            }
        }.bind(this)

        if (this.getCurrentQueryParams()['vertex']) {
            console.log("url manager mounted, fetching existing vertex", this.getCurrentQueryParams())
            this.props.fetchVertices(
                {
                    graphId: this.props.graphId,
                    fetchEdges: true,
                    flyTo: true,
                    persistOnNewClick: true,
                    graphMetadata: this.props.graphMetadata,
                    metadataObject: {
                        type: 'vertex',
                        value: this.getCurrentQueryParams().vertex
                    }
                }
            )
        }
        console.log("on mount setting default for qps")
        if (Object.keys(this.getCurrentQueryParams()).length === 0) {
            updateQueryParam(this.props, {
                x: - 128,
                y: 128,
                z: 0,
            })
        }

    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        let update = {}
        if (prevProps.queryParams.vertex !== this.props.queryParams.vertex) {
            if (!this.props.verticesSelected
                .map(v => v.vertex)
                .includes(this.props.queryParams.vertex)) {

                this.props.fetchVertices(
                    {
                        graphId: this.props.graphId,
                        fetchEdges: true,
                        flyTo: false,
                        persistOnNewClick: false,
                        graphMetadata: this.props.graphMetadata,
                        metadataObject: {
                            type: 'vertex',
                            value: this.props.queryParams.vertex
                        }
                    }
                )

            }
            update['vertex'] = this.props.queryParams.vertex
        }
        if (prevProps.queryParams.x !== this.props.queryParams.x) {
            update['x'] = this.props.queryParams.x
        }
        if (prevProps.queryParams.y !== this.props.queryParams.y) {
            update['y'] = this.props.queryParams.y
        }
        if (prevProps.queryParams.z !== this.props.queryParams.z) {
            update['z'] = this.props.queryParams.z
        }
        if (!_.isEqual(update, {})) {
            console.log("updating qps: ", update)
            updateQueryParam(this.props, update)
        }
    }

    getCurrentQueryParams() {
        let result = {}

        for (const queryParam of ['x', 'y', 'z', 'vertex']) {
            getQueryParam(this.props, queryParam) ?
            result[queryParam] = getQueryParam(this.props, queryParam) : false;
        }

        return result;
    }
}

const mapUrlToProps = (state) => {
    return {
        queryParams: state.url,
        graphId: state.graph.graphId,
        graphMetadata: state.graph.graphMetadata,
        verticesSelected: state.marker.vertices
    }
};

export default withRouter(connect(mapUrlToProps, {changeUrl, fetchVertices})(UrlManager));