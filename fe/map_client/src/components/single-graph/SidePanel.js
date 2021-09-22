import * as React from "react";
import Fillable from "../../reactBlueTemplate/src/pages/tables/static/Fillable"; import {Table} from "reactstrap"; import {truncateEth} from "../../utils/Utils";

class SidePanel extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {



        return <Fillable>
            <h3>Single Vertex </h3>
            <Table className="my-table-hover">
                <thead>
                <tr>
                    <th>Eth</th>
                    <th>Types</th>
                    <th>Labels</th>
                </tr>
                </thead>
                {/* eslint-disable */}
                <tbody>
                <tr>

                    <td>{truncateEth(this.props.closestVertex?.eth)}</td>
                    <td>{this.props.closestVertex?.types.filter((t) => !!t && t.length > 0).join(', ')}</td>
                    <td>{this.props.closestVertex?.labels.filter((t) => !!t && t.length > 0).join(', ')}</td>

                </tr>

                </tbody>
                {/* eslint-enable */}
            </Table>

            <h3>
                Search Bar Hits
            </h3>
            <Table className="my-table-hover">
                <thead>
                <tr>
                    <th>Eth</th>
                    <th>Types</th>
                    <th>Labels</th>
                </tr>
                </thead>
                {/* eslint-disable */}
                <tbody>
                <tr>

                </tr>

                </tbody>
                {/* eslint-enable */}
            </Table>

        </Fillable>
    }

}

export default SidePanel