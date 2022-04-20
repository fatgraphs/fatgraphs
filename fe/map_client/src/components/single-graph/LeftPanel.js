import React, {Component} from 'react';
import s from "./singleGraph.module.scss";
import Fillable from "../../reactBlueTemplate/pages/tables/static/Fillable";
import UrlComposer from "../../utils/UrlComposer";
import {withRouter} from "react-router-dom";
import {connect} from "react-redux";
import {Table} from "reactstrap";
import {IconsLegend} from "./IconsLegend";
import CopyGtmCommand from "./CopyGtmCommand";

import {truncateEth} from "../../utils/Utils";

const configs = require('configurations')

class LeftPanel extends Component {

    constructor(props) {
        super(props);
        this.state = {
            edgePlotUrls: []
        }
    }

    componentDidMount() {
        let edgePlotUrls = []
        for(let z = 0; z < this.props.zoomLevels; z++){
            edgePlotUrls.push(UrlComposer.edgePlot(this.props.match.params.graphId, z))
        }
        this.setState({edgePlotUrls: edgePlotUrls})
    }

    render() {
        return (
            <>
            <Fillable>
                <Table className="my-table-hover">
                    <h3>Graph summary</h3>
                    {/* eslint-disable */}
                    <tbody>
                    <tr>
                        <td>Vertex count</td>
                        <td>{this.props.vertices}</td>
                    </tr>

                    <tr>
                        <td>Edge count</td>
                        <td>{this.props.edges}</td>
                    </tr>
                    </tbody>
                    {/* eslint-enable */}
                </Table>
            </Fillable>

            <Fillable>
                <div>
                    <h3>Graph description</h3>

                    <div
                        dangerouslySetInnerHTML={{__html: this.props.description}}>
                    </div>
                </div>
            </Fillable>

                {configs['debug_mode'] === 'true' ?
                <><Fillable>
                <div>
                    <h3>Debug Info</h3>
                    <CopyGtmCommand/>
                    <div style={{marginTop: '1rem'}}>
                        <h4>Edge Plots</h4>

                        {this.state.edgePlotUrls.map((url, i) => <img
                            key={i * 63 + 1}
                            className={s.plot}
                            src={url}/>
                        )}
                    </div>
                </div>
                </Fillable>
                </> :
                <div></div>}
            <Fillable>
                <div>
                    <h3>Legend</h3>
                    <IconsLegend></IconsLegend>
                </div>
                
            </Fillable>
            </>
        );
    }
}

let mapStateToPropsLeftPanel = state => {
    return {
        zoomLevels: state.graph.graphConfiguration.zoomLevels,
        vertices: state.graph.graph.vertices,
        edges: state.graph.graph.edges,
        description: state.graph.graph.description,
    }
}

export default withRouter(connect(mapStateToPropsLeftPanel, null)(LeftPanel));