import React, {Component} from 'react';
import {faClipboard} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

class CopyGtmCommand extends Component {

    constructor(props) {
        super(props);
        this.copyGtmCommand = this.copyGtmCommand.bind(this)
        this.generateGtmCommand = this.generateGtmCommand.bind(this)
    }

    render() {
        return (

            <div className={'hover:cursor-pointer active:text-2xl ml-2'}
                 onClick={this.copyGtmCommand}>
                <p className={'mr-2'}>copy gtm command <FontAwesomeIcon
                    icon={faClipboard}/>
                </p>
            </div>

        );
    }

    copyGtmCommand() {
        let command = this.generateGtmCommand()
        navigator.clipboard.writeText(command);
    }

    generateGtmCommand() {
        let build = "./gtm.py" +
            " -n " + this.props.graphMetadata.graphName +
            " --csv " + this.props.graphMetadata.source +
            " --ts " + this.props.graphMetadata.tileSize +
            " -z " + this.props.graphMetadata.zoomLevels +
            " --min_t " + this.props.graphMetadata.minTransparency +
            " --max_t " + this.props.graphMetadata.maxTransparency +
            " --std " + this.props.graphMetadata.stdTransparencyAsPercentage +
            " --med_thick " + this.props.graphMetadata.medEdgeThickness +
            " --max_thick " + this.props.graphMetadata.maxEdgeThickness +
            " --med_size " + this.props.graphMetadata.medVertexSize +
            " --max_size " + this.props.graphMetadata.maxVertexSize +
            " --curvature " + this.props.graphMetadata.curvature +
            " --mean_t  " + this.props.graphMetadata.tileBasedMeanTransparency +
            " --labels " + this.props.graphMetadata.labels
        return build;
    }
}

export default CopyGtmCommand;