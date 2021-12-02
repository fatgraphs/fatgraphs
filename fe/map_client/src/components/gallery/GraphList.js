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
        this.applyFilter = this.applyFilter.bind(this);
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
        let filteredGraphs = this.applyFilter();

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

    applyFilter() {
        let byname = this.props.filter.searchTerms.length > 0
            ? this.props.availableGraphs.filter(
            (graph) => this.props.filter.searchTerms.some(
                (filterTerm) => {
                    console.log(graph)
                    return graph.graphName.toLowerCase().includes(filterTerm)
                })
            )
            : this.props.availableGraphs
        let byvertex = byname.filter(g => g.vertices >= this.props.filter.vertices[0] && g.vertices <= this.props.filter.vertices[1])
        let byedge = byvertex.filter(g => g.edges >= this.props.filter.edges[0] && g.edges <= this.props.filter.edges[1])
        return byedge;
    }
}

GraphList.propType = {
    filter: PropTypes.object
}

export default withRouter(GraphList);
