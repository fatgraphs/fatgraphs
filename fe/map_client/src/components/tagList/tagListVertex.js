import React, {Component} from 'react';
import SearchBar from "../searchBar/SearchBar";
import {func} from "prop-types";
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
            isAddingType: true,
            isAddingLabel: false,
            recentlyDeleted: [],
            recentlyAdded: [],
        }
        this.onBlur = this.onBlur.bind(this);
        this.removeWrapper = this.removeWrapper.bind(this);
        this.onAutocompletionElementClick = this.onAutocompletionElementClick.bind(this);
        this.handleChangingAddedType = this.handleChangingAddedType.bind(this);
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

                <SearchBar
                    searchCallback={(v) => {
                        this.setState({currentInput: v});

                        this.onAutocompletionElementClick({
                            type: this.state.isAddingType ? 'type' : 'label',
                            value: v
                        })
                        this.setState({currentInput: ""});
                        // this.props.sendSingleVertexSearch(v);

                    }}
                    onBlur={this.onBlur}
                    onFocus={() => this.setState({showAutocompletion: true})}
                    onChange={(v) => this.setState({currentInput: v})}
                />

                <div>
                    <div>
                        <span>Add TYPE</span>
                        <input type="checkbox"
                               name="isAddingType"
                               value="1"
                               checked={this.state.isAddingType}
                               onChange={this.handleChangingAddedType}/>
                    </div>
                    <div>
                        <span>Add LABEL</span>
                        <input type="checkbox"
                               name="isAddingLabel"
                               value="1"
                               checked={this.state.isAddingLabel}
                               onChange={this.handleChangingAddedType}/>
                    </div>
                </div>

                <Autocompletion currentInput={this.state.currentInput}
                                shouldRender={this.state.showAutocompletion}
                                autocompletionTerms={this.props.autocompletionTerms}
                                recentMetadataSearches={[]}
                                onClick={this.onAutocompletionElementClick}
                                isBottomAligned/>
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

    handleChangingAddedType(e) {
        this.setState({
            isAddingType: e.target.name === "isAddingType" ? e.target.checked : !e.target.checked,
            isAddingLabel: e.target.name === "isAddingLabel" ? e.target.checked : !e.target.checked
        })
    }

}

TagListVertex.propTypes = {
    addTag: func.isRequired,
    deleteTag: func.isRequired
}

export default TagListVertex;