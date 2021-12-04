import React, {Component} from 'react';
import SearchBar from "../searchBar/SearchBar";
import './tagBox.scss'
import './closeIcon.scss'
import './closeBox.scss'
import './tagContainer.scss'

import Autocompletion from "../autocompletion/Autocompletion";
import {TagElement} from "./tagElement";
import {TYPE_ICONS} from "../single-graph/TypeIcons";
import {connect} from "react-redux";
import {fetchVertices, removeVertices} from "../../redux/selectedVerticesSlice";

class TagListGraph extends Component {

    constructor(props) {
        super(props);
        this.state = {
            currentInput: '',
            metadataObjects: [],
            showAutocompletion: false,
            previousClearSignal: 0
        }
        this.onBlur = this.onBlur.bind(this);
        this.removeWrapper = this.removeWrapper.bind(this);
        this.onAutocompletionElementClick = this.onAutocompletionElementClick.bind(this);
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (this.props.clearSignal !== this.state.previousClearSignal) {
            this.setState({
                metadataObjects: [],
                previousClearSignal: this.props.clearSignal
            })
        }
    }

    render() {
        return (
            <div
                // the clear signal prop needs to be passed with connect and a derive propsFromState.
                // when the clar button is pressed the clearSignal in the slice is incremented. The side effect is that
                // the tagListGraph will re-render, deleting it's state!
                key={this.props.clearSignal + 89843}
                className={'d-flex flex-row flex-wrap overflow-auto'}>

                {/*The current input from search bar is only used to filter the autocompletion list*/}

                <SearchBar
                    placeholder={"Search graph"}
                    searchCallback={(v) => {
                        this.setState({currentInput: v});
                        if (v.slice(0, 2) === '0x') {
                            this.onAutocompletionElementClick({type: 'vertex', value: v, fetchEdges: true, flyTo: true})
                            this.setState({currentInput: ""});
                            this.props.sendSingleVertexSearch(v);
                        }
                    }}
                    onBlur={this.onBlur}
                    onFocus={() => this.setState({showAutocompletion: true})}
                    onChange={(v) => this.setState({currentInput: v})}
                />

                {this.state.metadataObjects.map((metaObject, i) => <TagElement
                    key={i}
                    closeCallback={this.removeWrapper(i)}>
                    <div className={'d-flex mr-1'}>{TYPE_ICONS[metaObject.type]}</div>
                    <div>{metaObject.value}</div>
                </TagElement>)}

                <Autocompletion currentInput={this.state.currentInput}
                                shouldRender={this.state.showAutocompletion}
                                autocompletionTerms={this.props.autocompletionTerms}
                                recentMetadataSearches={[]}
                                onClick={this.onAutocompletionElementClick}/>
            </div>
        );
    }

    removeWrapper(indexToRemove) {

        return function () {

            let removed = this.state.metadataObjects[indexToRemove]

            let tagsWithoutOne = [...this.state.metadataObjects.slice(0, indexToRemove),
                ...this.state.metadataObjects.slice(indexToRemove + 1,
                    this.state.metadataObjects.length)];

            this.props.removeVertices(removed.type === 'type' ? {type: removed.value} : {label: removed.value})

            this.setState({metadataObjects: tagsWithoutOne})
        }.bind(this)
    }

    onBlur(e) {
        let wasAutocompleteTermClicked = e.relatedTarget !== null && e.relatedTarget.className.includes('dont-lose-focus');
        if (wasAutocompleteTermClicked) {
            return
        }
        // the user clicked somewhere else on the map
        this.setState({
            showAutocompletion: false
        })
    }

    onAutocompletionElementClick(e) {
        let metadataObjects = [...this.state.metadataObjects, e];
        console.log("metadataObjects ", metadataObjects)
        this.props.fetchVertices({
            metadataObject: e,
            fetchEdges: e['fetchEdges'] || false,
            flyTo: e['flyTo'] || false,
            persistOnNewClick: true,
        })
        this.setState({metadataObjects: metadataObjects, showAutocompletion: false})
    }
}

let mapStateToProps = (state) => {
    return {
        clearSignal: state.marker.clearSignal,
    }
};

export default connect(mapStateToProps, {fetchVertices, removeVertices})(TagListGraph);