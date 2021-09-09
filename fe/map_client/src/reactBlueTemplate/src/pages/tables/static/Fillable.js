import React from "react";
import {Col, Row} from "reactstrap";

import Widget from "../../../components/Widget";
import s from "./Static.module.scss";

class Fillable extends React.Component {
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
                                {this.props.children}
                            </div>
                        </Widget>
                    </Col>
                </Row>
            </div>
        );
    }
}

export default Fillable;
