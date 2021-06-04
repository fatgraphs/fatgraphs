import React, {Component} from 'react';
import {fetchEdgePlots} from "../../../API_layer";
import {string, number} from "prop-types";

class EdgeTransparencyPlots extends Component {

    constructor(props) {
        super(props);
        this.state = {
            plots: []
        }
    }

    async componentDidMount() {
        let plots = await fetchEdgePlots(this.props.graph_name, this.props.zoom_levels);
        this.setState({"plots": plots})
    }

    render() {
        return this.state.plots.length > 0 ?
            <div className={'flex flex-row flex-wrap'}>
                {this.state.plots
                    .sort((a, b) => a.zl > b.zl ? 1 : -1)
                    .map((img, i) => <img
                        key={i}
                        width={'500rem'}
                        src={URL.createObjectURL(img.data)}/>
                    )}
            </div> :
            <div>Loading . . .</div>
    }
}

EdgeTransparencyPlots.propTypes = {
    graph_name: string.isRequired,
    zoom_levels: number.isRequired
}

export default EdgeTransparencyPlots;