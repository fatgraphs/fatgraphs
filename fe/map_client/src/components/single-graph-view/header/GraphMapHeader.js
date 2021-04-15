import React, {Component} from 'react';
import DescriptionTable from "../../description-table/DescriptionTable";
import {faClipboard} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

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
        let ownPropertyNames = Object.getOwnPropertyNames(this.props.graph_metadata);
        let ownPropertyValues = Object.values(this.props.graph_metadata).map((e) => String(e))
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

                <DescriptionTable
                    keys={ownPropertyNames}
                    values={ownPropertyValues}>
                </DescriptionTable>
            </div>
        );
    }

    copyGtmCommand() {
        let command = this.generateGtmCommand()
        navigator.clipboard.writeText(command);
    }

    generateGtmCommand() {
        let build = "./gtm.py" + " --csv " + this.props.graph_metadata.source +
            " --ts " + this.props.graph_metadata.tile_size + " -z " + this.props.graph_metadata.zoom_levels +
            " --min_t " + this.props.graph_metadata.min_transparency + " --max_t " + this.props.graph_metadata.max_transparency +
            " --std " + this.props.graph_metadata.std_transparency_as_percentage + " --max_thick " + this.props.graph_metadata.max_edge_thickness +
            " --min_thick " + this.props.graph_metadata.min_edge_thickness + " --target_median " + this.props.graph_metadata.target_median +
            " --target_max " + this.props.graph_metadata.target_max + " --edge_curvature " + this.props.graph_metadata.edge_curvature
        return build;
    }
}

export default GraphMapHeader;