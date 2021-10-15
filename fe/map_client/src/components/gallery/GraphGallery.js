import React, {Component} from 'react';
import {fetchGraphs} from "../../APILayer";
import {MyContext} from "../../Context";
import GraphList from "./GraphList";
import TagListGallery from "../tagList/tagListGallery"; import {withRouter} from "react-router-dom";

class Gallery extends Component {

    /**
     * A gallery of available graphs that can be clicked and visualised.
     */

    static contextType = MyContext

    constructor(props) {
        super(props);
        this.state = {
            availableGraphs: undefined,
            searchTerms: []
        }
    }

    async componentDidMount() {
        let graphs = await fetchGraphs(this.props.match.params.galleryType)
                this.setState({
                    availableGraphs: graphs
                })
    }

    async componentDidUpdate(prevProps) {
        if(prevProps.match.params.galleryType !== this.props.match.params.galleryType){
            let graphs = await fetchGraphs(this.props.match.params.galleryType)
                this.setState({
                    availableGraphs: graphs
                })
            }
    }


    render() {
        return this.state.availableGraphs ?
            <div className={`p-3`}>

                <TagListGallery
                    onChange={(vals) => {
                        this.setState({searchTerms: vals})
                    }}/>

                <GraphList
                    availableGraphs={this.state.availableGraphs}
                    filterTerms={this.state.searchTerms}/>
            </div> :
            <div>Loading . . .</div>
    }
}

export default withRouter(Gallery);

