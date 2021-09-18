import React, {Component} from 'react';
import SearchBar from "../searchBar/SearchBar";
import './tagBox.scss'
import './closeIcon.scss'
import './closeBox.scss'
import Autocompletion from "../autocompletion/Autocompletion";
import {TYPE_ICONS} from "../single-graph/VisualElements";

class TagListGraph extends Component {

    constructor(props) {
        super(props);
        this.state = {
            currentInput: '',
            metadataObjects: [],
            showAutocompletion: false
        }
        this.add = this.add.bind(this);
        this.onBlur = this.onBlur.bind(this);
        this.removeWrapper = this.removeWrapper.bind(this);
    }

    render() {
        return (
            <div className={'d-flex flex-row flex-wrap'}>

                <SearchBar
                    searchCallback={(v) => this.setState({currentInput: v})}
                    onBlur={this.onBlur}
                    onFocus={() => this.setState({showAutocompletion: true})}
                onChange={(v) => this.setState({currentInput: v})}/>

                {this.state.metadataObjects.map((t, i) => {
                    return <div
                        className={'d-flex flex-row'}
                        key={i}>
                        <div className={'tagBox'}>
                            <div className={'d-flex mr-1'}>{TYPE_ICONS[t.type]}</div>
                            <div>{t.value}</div>

                        </div>
                        <div className={'closeBox'}
                             onClick={this.removeWrapper(i)}>
                            <span className={'glyphicon glyphicon-remove closeIcon'}/>
                        </div>
                    </div>
                })}

                <Autocompletion currentInput={this.state.currentInput}
                                shouldRender={this.state.showAutocompletion}
                                autocompletionTerms={this.props.autocompletionTerms}
                                recentMetadataSearches={[]}
                onClick={(e) => {
                    // console.log("from taglist graph ", e)
                    let metadataObjects = [...this.state.metadataObjects, e];
                    this.props.onChange(metadataObjects)
                    this.setState({metadataObjects: metadataObjects, showAutocompletion: false})
                }}/>
            </div>
        );
    }

    add(tagObject) {
        let newTags = [...this.state.metadataObjects, tagObject];
        this.props.onChange(newTags);
        this.setState({metadataObjects: newTags});
        console.log(">>>>>>>>")
    }

    removeWrapper(indexToRemove) {
        return function () {
            let tagsWithoutOne = [...this.state.metadataObjects.slice(0, indexToRemove), ...this.state.metadataObjects.slice(indexToRemove + 1, this.state.metadataObjects.length)];
            this.props.onChange(tagsWithoutOne)
            this.setState({metadataObjects: tagsWithoutOne})
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
}

export default TagListGraph;