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
            <div className={s.fillable}>
                <Widget>
                    <div className={s.overFlow}>
                        {this.props.children}
                    </div>
                </Widget>
            </div>
        );
    }
}

export default Fillable;
