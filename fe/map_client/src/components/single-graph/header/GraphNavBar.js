import React, {Component} from 'react';
import {Link, Route, Switch, withRouter} from "react-router-dom";
import DescriptionTable from "../../../generic_components/DescriptionTable";
import EdgeTransparencyPlots from "./EdgeTransparencyPlots";

class GraphNavBar extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        let keys = Object.getOwnPropertyNames(this.props.graph_metadata);
        let values = Object.values(this.props.graph_metadata).map((e) => String(e))
        return (
        <div>
            <nav>
                <ul className={'flex flex-row'}>
                    <li className={'border-black border-2 mr-2'}>
                        <Link to={`${this.props.match.url}/graph-metadata`}>
                            Graph metadata
                        </Link>
                    </li>
                    <li className={'border-black border-2 mr-2'}>
                        <Link to={`${this.props.match.url}/edge-length-distribution`}>
                            Edge length Distribution
                        </Link>
                    </li>
                </ul>
            </nav>

            <Switch>
                <Route path={`${this.props.match.path}/graph-metadata`}>
                    <DescriptionTable
                        keys={keys}
                        values={values}
                    />
                </Route>
                <Route path={`${this.props.match.path}/edge-length-distribution`}>
                   <EdgeTransparencyPlots graph_name={this.props.graph_metadata.graph_name}
                                          zoom_levels={this.props.graph_metadata.zoom_levels}
                   />
                </Route>
            </Switch>
        </div>
        );
    }
}

export default withRouter(GraphNavBar);