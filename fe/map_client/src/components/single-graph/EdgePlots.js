import React, {Component} from 'react';
import s from "./singleGraph.module.scss";
import Fillable from "../../reactBlueTemplate/src/pages/tables/static/Fillable";
import UrlComposer from "../../utils/UrlComposer";
import {withRouter} from "react-router-dom";

class EdgePlots extends Component {

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
            <Fillable>
                {this.state.edgePlotUrls.map((url, i) => <img
                    key={i*63 + 1}
                    className={s.plot}
                    src={url}/>
               )}
            </Fillable>
        );
    }
}

export default withRouter(EdgePlots);