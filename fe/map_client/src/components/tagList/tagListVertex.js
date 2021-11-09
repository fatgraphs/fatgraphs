import React, {Component} from 'react';
import SearchBar from "../searchBar/SearchBar";
import {func, bool} from "prop-types";
import './tagBox.scss'
import './closeIcon.scss'
import './closeBox.scss'
import './tagContainer.scss'

import Autocompletion from "../autocompletion/Autocompletion";
import {TagElement} from "./tagElement";
import {TYPE_ICONS} from "../single-graph/TypeIcons";

class TagListVertex extends Component {

    constructor(props) {
        super(props);
        this.state = {
            currentInput: '',
            showAutocompletion: false,
            recentlyDeleted: [],
            recentlyAdded: [],
        }
        this.onBlur = this.onBlur.bind(this);
        this.removeWrapper = this.removeWrapper.bind(this);
        this.onAutocompletionElementClick = this.onAutocompletionElementClick.bind(this);
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (this.props.receiveClearSignal) {
            this.props.sendClearAck()
        }
    }

    render() {
        return (
            <div className={'d-flex flex-row flex-wrap overflow-auto'}>

                {[...this.props.metadataObjects, ...this.state.recentlyAdded]
                    .filter(e => {
                        console.log(this.state.recentlyDeleted.some(rd => rd.type === e.type && rd.value === e.value))
                        return !this.state.recentlyDeleted.some(rd => rd.type === e.type && rd.value === e.value)
                    })
                    .map((metaObject, i) =>
                        <TagElement
                            key={i}
                            closeCallback={this.removeWrapper(i, metaObject)}>
                            <div className={'d-flex mr-1'}>{TYPE_ICONS[metaObject.type]}</div>
                            <div>{metaObject.value}</div>
                        </TagElement>)}

                {this.props.isLabellingEnabled === 'true' ?
                    <>
                        <SearchBar
                            placeholder={"Add Type"}
                            searchCallback={(v) => {
                                this.onAutocompletionElementClick({
                                    type: 'type',
                                    value: v
                                })
                                this.setState({currentInput: ""});

                            }}
                            onBlur={this.onBlur}
                            onFocus={() => this.setState({showAutocompletion: true})}
                            onChange={(v) => this.setState({currentInput: v})}
                        />
                         <SearchBar
                            placeholder={"Add Label"}
                            searchCallback={(v) => {
                                this.onAutocompletionElementClick({
                                    type: 'label',
                                    value: v
                                })
                                this.setState({currentInput: ""});

                            }}
                            onBlur={this.onBlur}
                            onFocus={() => this.setState({showAutocompletion: true})}
                            onChange={(v) => this.setState({currentInput: v})}
                        />


                        <Autocompletion currentInput={this.state.currentInput}
                                        shouldRender={this.state.showAutocompletion}
                                        autocompletionTerms={this.props.autocompletionTerms}
                                        recentMetadataSearches={[]}
                                        onClick={this.onAutocompletionElementClick}
                                        isBottomAligned/>
                    </> :
                    <div>Labelling disabled</div>}
            </div>
        );
    }

    removeWrapper(indexToRemove, deletedTag) {
        return function () {
            console.log("remove wrapper")
            this.setState({
                recentlyDeleted: [...this.state.recentlyDeleted, deletedTag]
            })
            this.props.deleteTag(deletedTag)
        }.bind(this)
    }

    onBlur(e) {
        let wasAutocompleteTermClicked = e.relatedTarget !== null && e.relatedTarget.className.includes('dont-lose-focus');
        console.log("blurring, wasAutocompleteTermClicked ", wasAutocompleteTermClicked)
        if (wasAutocompleteTermClicked) {
            return
        }
        // the user clicked somewhere else on the map
        this.setState({
            showAutocompletion: false
        })
    }

    onAutocompletionElementClick(e) {
        this.props.addTag(e)
        this.setState({showAutocompletion: false, recentlyAdded: [...this.state.recentlyAdded, e]})
    }

}

TagListVertex.propTypes = {
    isLabellingEnabled: bool.isRequired,
    addTag: func.isRequired,
    deleteTag: func.isRequired
}

export default TagListVertex;