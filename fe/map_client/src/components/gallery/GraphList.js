import React from "react";

import s from "./Static.module.scss";
import {fetchGraphs} from "../../APILayer";
import {Card, CardBody, CardImg, CardTitle} from "reactstrap";
import UrlComposer from "../../utils/UrlComposer";
import {withRouter} from "react-router-dom";
import * as PropTypes from "prop-types";

class GraphList extends React.Component {
    constructor(props) {
        super(props);
    }

    parseDate(date) {
        this.dateSet = date.toDateString().split(" ");

        return `${date.toLocaleString("en-us", {month: "long"})} ${
            this.dateSet[2]
        }, ${this.dateSet[3]}`;
    }

    openGraph(graph) {
        this.props.history.push("/graph/" + graph.graphName + '/' + graph.id);
    }

    render() {
        let filteredGraphs = this.props.filterTerms.length > 0
            ? this.props.availableGraphs.filter(
                (grap) => this.props.filterTerms.some(
                    (filterTerm) => {
                        return grap.graphName.toLowerCase().includes(filterTerm)
                    })
            )
            : this.props.availableGraphs

        return (
            <div className={s.root}>

                <h2 className="page-title">
                    Explore <span className="fw-semi-bold">graphs</span>
                </h2>

                <div className={s.myGrid}>
                    {filteredGraphs.map((row, i) => {
                            let imageUrl = UrlComposer.tileLayer(row.id, 0, 0, 0);
                            imageUrl = imageUrl.replace(/{randint}/g, 43);

                            return <Card
                                key={i*23 + 1}
                                className={s.myCard}
                                         onClick={() => {
                                             this.openGraph(row)
                                         }}>
                                <CardImg top width="100%" src={imageUrl} alt="Card image cap"/>
                                <CardBody>
                                    <CardTitle tag="h4" className={`mb-0`}>{row.graphName}</CardTitle>
                                </CardBody>
                            </Card>
                        }
                    )}
                </div>
            </div>
        );
    }
}

GraphList.propType = {
    filterTerms: PropTypes.array
}

export default withRouter(GraphList);
