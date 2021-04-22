import React, {Component} from 'react';
import {Link, Route, Switch, withRouter} from "react-router-dom";
import DescriptionTable from "../../../description-table/DescriptionTable";
import EdgeDistributionViewer from "../../../gaussian-distributions/EdgeDistributionViewer";

class GraphHeaderNavigationBar extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        let ownPropertyNames = Object.getOwnPropertyNames(this.props.graph_metadata);
        let ownPropertyValues = Object.values(this.props.graph_metadata).map((e) => String(e))
        return (
        <div>
            <nav>
                <ul className={'flex flex-row'}>
                    <li className={'ml-2 border'}>
                        <Link to={`${this.props.match.url}/graph-metadata`}>Graph metadata</Link>
                    </li>
                    <li className={'ml-2 border'}>
                        <Link to={`${this.props.match.url}/edge-length-distribution`}>Edge length Distribution</Link>
                    </li>
                </ul>
            </nav>

            <Switch>
                <Route path={`${this.props.match.path}/graph-metadata`}>
                    <DescriptionTable
                        keys={ownPropertyNames}
                        values={ownPropertyValues}>
                    </DescriptionTable>
                </Route>
                <Route path={`${this.props.match.path}/edge-length-distribution`}>
                   <EdgeDistributionViewer graph_name={this.props.graph_metadata.graph_name} zoom_levels={this.props.graph_metadata.zoom_levels}/>
                </Route>
            </Switch>
        </div>
        );
    }
}

export default withRouter(GraphHeaderNavigationBar);