import React, {Component} from 'react';
import {faClipboard} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import s from './singleGraph.module.scss'
import {connect} from "react-redux";

class CopyGtmCommand extends Component {

    constructor(props) {
        super(props);
        this.copyGtmCommand = this.copyGtmCommand.bind(this)
        this.generateGtmCommand = this.generateGtmCommand.bind(this)
    }

    render() {
        return (

            <div className={s.copyGtmCommand}
                 onClick={this.copyGtmCommand}>
                <FontAwesomeIcon
                    className={'mr-2'}
                    icon={faClipboard}/>

                copy gtm command
            </div>

        );
    }

    copyGtmCommand() {
        let command = this.generateGtmCommand()
        navigator.clipboard.writeText(command);
    }

    generateGtmCommand() {
        let configs = this.props.graphConfiguration;
        let build = "./gtm.py" +
            " -n " + configs.graphName +
            " --csv " + configs.source +
            " --ts " + configs.tileSize +
            " -z " + configs.zoomLevels +
            " --min_t " + configs.minTransparency +
            " --max_t " + configs.maxTransparency +
            " --std " + configs.stdTransparencyAsPercentage +
            " --med_thick " + configs.medEdgeThickness +
            " --max_thick " + configs.maxEdgeThickness +
            " --med_size " + configs.medVertexSize +
            " --max_size " + configs.maxVertexSize +
            " --curvature " + configs.curvature +
            " --mean_t  " + configs.tileBasedMeanTransparency
        return build;
    }
}

const mapStateToPropsCopyCommands = (state) => {
    return {
        graphConfiguration: state.graph.graphConfiguration
    }
}

export default connect(mapStateToPropsCopyCommands, null)(CopyGtmCommand);