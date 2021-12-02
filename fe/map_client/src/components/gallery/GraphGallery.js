import React, {Component} from 'react';
import {fetchGraphs} from "../../APILayer";
import {MyContext} from "../../Context";
import GraphList from "./GraphList";
import TagListGallery from "../tagList/tagListGallery";
import {withRouter} from "react-router-dom";
import LoadingComponent from "../LoadingComponent";
import './graphGalleryContainer.scss';
import Sliders from "./Sliders";

class Gallery extends Component {

    /**
     * A gallery of available graphs that can be clicked and visualised.
     */

    static contextType = MyContext

    constructor(props) {
        super(props);
        this.state = {
            availableGraphs: undefined,
            graphFilteringObject: {
                searchTerms: [],
                edges: [],
                vertices: []
            }
        }
    }

    async componentDidMount() {

        let graphs = await fetchGraphs(this.props.match.params.galleryCategory)
        this.setState({
            availableGraphs: graphs
        })
    }

    async componentDidUpdate(prevProps) {

        if (prevProps.match.params.galleryCategory !== this.props.match.params.galleryCategory) {
            let graphs = await fetchGraphs(this.props.match.params.galleryCategory)
            this.setState({
                availableGraphs: graphs
            })
        }
    }


    render() {
        return this.state.availableGraphs ?
            <div className={'graph-gallery-container'}>


                <TagListGallery
                    onChange={(vals) => {
                        this.setState({
                                graphFilteringObject: {
                                    ...this.state.graphFilteringObject,
                                    searchTerms: vals
                                }
                            }
                        )
                    }}/>


                <Sliders
                    updateCallback={(rangeDict) => {
                        console.log(rangeDict)
                        this.setState({
                                graphFilteringObject: {
                                    ...this.state.graphFilteringObject,
                                    ...rangeDict
                                }
                            }
                        )
                    }}/>


                <GraphList
                    availableGraphs={this.state.availableGraphs}
                    filter={this.state.graphFilteringObject}
                />
            </div> :
            <LoadingComponent/>
    }
}

export default withRouter(Gallery);

