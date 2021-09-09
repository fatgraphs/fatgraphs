import React from "react";
import {Col, Row, Table,} from "reactstrap";

import Widget from "../../../components/Widget";
import s from "./Static.module.scss";
import {truncateEth} from "../../../../../utils/Utils";

class Static extends React.Component {
    constructor(props) {
        super(props);

        this.state = {};
    }


    render() {
        return (
            <div className={s.root}>

                <Row>

                    <Col lg={12} md={12} sm={12}>
                        <Widget>


                            <div className={s.overFlow}>
                                <h3>
                                    Single Vertex
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

                                        <td>{truncateEth(this.props.closestVertex?.eth)}</td>
                                        <td>{this.props.closestVertex?.types.filter((t) => t.length > 0).join(', ')}</td>
                                        <td>{this.props.closestVertex?.labels.filter((t) => t.length > 0).join(', ')}</td>

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

                            </div>
                        </Widget>
                    </Col>
                </Row>
            </div>
        );
    }
}

export default Static;
