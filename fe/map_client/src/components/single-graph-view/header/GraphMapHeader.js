import React, {Component} from 'react';
import DescriptionTable from "../../description-table/DescriptionTable";
import {faClipboard} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {withRouter} from "react-router-dom";
import GraphHeaderNavigationBar from "./graphHeaderNavigationBar/GraphHeaderNavigationBar";

class GraphMapHeader extends Component {

    constructor(props) {
        super(props);
        console.log(this.props.graph_metadata);
        this.state = {
            nodes: this.props.graph_metadata.vertices,
            edges: this.props.graph_metadata.edges,
            median_distance: this.props.graph_metadata.median_pixel_distance
        }
        this.copyGtmCommand = this.copyGtmCommand.bind(this)
        this.generateGtmCommand = this.generateGtmCommand.bind(this)
    }

    render() {
        return (
            <div className={'border-2 flex-1'}>
                <div className={'relative flex flex-row items-center'}>
                    <h3 className={'text-2xl'}>Graph summary </h3>
                    <div className={'hover:cursor-pointer active:text-2xl'}
                         onClick={this.copyGtmCommand}>
                        <p className={'absolute inset-y-0 right-0 mr-2'}>copy gtm command <FontAwesomeIcon icon={faClipboard}/>
                        </p>
                    </div>
                </div>
                <GraphHeaderNavigationBar graph_metadata={this.props.graph_metadata}/>
            </div>
        );
    }

    copyGtmCommand() {
        let command = this.generateGtmCommand()
        navigator.clipboard.writeText(command);
    }

    generateGtmCommand() {
        let build = "./gtm.py" +
            " -n " + this.props.graph_metadata.graph_name +
            " --csv " + this.props.graph_metadata.source +
            " --ts " + this.props.graph_metadata.tile_size +
            " -z " + this.props.graph_metadata.zoom_levels +
            " --min_t " + this.props.graph_metadata.min_transparency +
            " --max_t " + this.props.graph_metadata.max_transparency +
            " --std " + this.props.graph_metadata.std_transparency_as_percentage +
            " --med_thick " + this.props.graph_metadata.med_edge_thickness +
            " --max_thick " + this.props.graph_metadata.max_edge_thickness +
            " --med_size " + this.props.graph_metadata.med_vertex_size +
            " --max_size " + this.props.graph_metadata.max_vertex_size +
            " --curvature " + this.props.graph_metadata.curvature +
            " --mean_t  " + this.props.graph_metadata.tile_based_mean_transparency
        return build;
    }
}

export default withRouter(GraphMapHeader);