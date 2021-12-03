import React, {Component} from 'react';
import {connect} from "react-redux";
import {changeUrl, urlChanged} from "../redux/urlSlice";
import {areAlmostIdentical, getQueryParam, updateBrowserUrlQueryParam} from "../utils/Utils";
import {withRouter} from "react-router-dom";
import _ from 'underscore';
import {fetchVertices, removeVertices} from "../redux/selectedVerticesSlice";

class UrlManager extends Component {
    /**
     * The main use-case for this class is enable a 2-way binding between the tuple {x, y, z, selectedVertex} as it
     * appears encoded in the URL (e.g. http://...?vertex=0x678b89fde5b6ebddbb050e2c87d6084bc5b25e32&x=-128&y=128&z=0)
     * and how it appears in the application UI (i.e. the map being panned at a certain location, with a certain zoom...)
     *
     * It uses the redux store
     */
    constructor() {
        super();
        this.state = {
            lastQueryParams: {}
        }
        this.browserUrlChangeCallback = this.browserUrlChangeCallback.bind(this);
        this.setDefaultQueryParamsIfEmpty = this.setDefaultQueryParamsIfEmpty.bind(this);
        this.fetchUrlEncodedVertexAtStartup = this.fetchUrlEncodedVertexAtStartup.bind(this);
        this.fetchUrlEncodedVertexAtRunTime = this.fetchUrlEncodedVertexAtRunTime.bind(this);
    }

    render() {
        return <></>
    }

    componentDidMount() {
        window.onhashchange = this.browserUrlChangeCallback
        this.fetchUrlEncodedVertexAtStartup();
        this.setDefaultQueryParamsIfEmpty();
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        let update = {}
        this.runVertexUpdateLogic(prevProps, update);
        if (prevProps.stateUrl.x !== this.props.stateUrl.x) {
            update['x'] = this.props.stateUrl.x
        }
        if (prevProps.stateUrl.y !== this.props.stateUrl.y) {
            update['y'] = this.props.stateUrl.y
        }
        if (prevProps.stateUrl.z !== this.props.stateUrl.z) {
            update['z'] = this.props.stateUrl.z
        }
        if (!_.isEqual(update, {})) {
            updateBrowserUrlQueryParam(this.props, update)
        }
    }

    runVertexUpdateLogic(prevProps, update) {
        if (prevProps.stateUrl.vertex !== this.props.stateUrl.vertex) {
            update['vertex'] = this.props.stateUrl.vertex

            let isUrlVertexAlreadySelected = this.props.verticesSelected
                .map(v => v.vertex)
                .includes(this.props.stateUrl.vertex);

            if (!isUrlVertexAlreadySelected) {

                // before fetching and showing a new vertex on the map, ensure that the removal logic runs to ensure
                // that those not supposed to be persisted are removed.
                this.props.removeVertices({})

                this.fetchUrlEncodedVertexAtRunTime();

            }
        }
    }

    fetchUrlEncodedVertexAtStartup() {
        // e.g. for use case when we send a url to a colleague with a vertex encoded in it
        if (this.getCurrentQueryParams()['vertex'] !== undefined) {

            this.props.fetchVertices(
                {
                    graphId: this.props.graphId,
                    fetchEdges: true,
                    flyTo: true,
                    persistOnNewClick: true,
                    graphConfiguration: this.props.graphConfiguration,
                    metadataObject: {
                        type: 'vertex',
                        value: this.getCurrentQueryParams().vertex
                    }
                }
            )
        }
    }

    setDefaultQueryParamsIfEmpty() {
        let isEmptyQueryParams = Object.values(this.getCurrentQueryParams()).every(e => !e);
        if (isEmptyQueryParams) {
            updateBrowserUrlQueryParam(this.props, {
                x: '-128',
                y: '128',
                z: '0',
            }, false)
        }
    }

    fetchUrlEncodedVertexAtRunTime() {
        this.props.fetchVertices(
            {
                graphId: this.props.graphId,
                fetchEdges: true,
                flyTo: false,
                persistOnNewClick: false,
                graphConfiguration: this.props.graphConfiguration,
                metadataObject: {
                    type: 'vertex',
                    value: this.props.stateUrl.vertex
                }
            }
        )
    }

    getCurrentQueryParams() {
        let result = {}

        for (const queryParam of ['x', 'y', 'z', 'vertex']) {
            // getQueryParam(this.props, queryParam) ?
            result[queryParam] = getQueryParam(this.props, queryParam) || '';
        }

        // console.log("qp got from props of urlManager: ", result)

        return result;
    }

    browserUrlChangeCallback(e) {
        console.log("areAlmostIdentical(this.getCurrentQueryParams(), this.props.stateUrl) ", areAlmostIdentical(this.getCurrentQueryParams(), this.props.stateUrl));
        if (!areAlmostIdentical(this.getCurrentQueryParams(), this.props.stateUrl)
            || this.props.stateUrl['vertex'] !== this.getCurrentQueryParams()['vertex']) {
            this.props.removeVertices({})
            this.props.changeUrl(this.getCurrentQueryParams())
        }
    }
}

const mapUrlToProps = (state) => {
    return {
        stateUrl: state.url,
        graphId: state.graph.graphId,
        graphConfiguration: state.graph.graphConfiguration,
        verticesSelected: state.marker.vertices
    }
};

export default withRouter(connect(mapUrlToProps, {changeUrl, fetchVertices, removeVertices})(UrlManager));