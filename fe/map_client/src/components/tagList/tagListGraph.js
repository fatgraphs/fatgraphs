import React, {Component} from 'react';
import SearchBar from "../searchBar/SearchBar";
import './tagBox.scss'
import './closeIcon.scss'
import './closeBox.scss'
import Autocompletion from "../autocompletion/Autocompletion"; import {TagElement} from "./tagElement"; import {TYPE_ICONS} from "../single-graph/TypeIcons";

class TagListGraph extends Component {

    constructor(props) {
        super(props);
        this.state = {
            currentInput: '',
            metadataObjects: [],
            showAutocompletion: false
        }
        this.onBlur = this.onBlur.bind(this);
        this.removeWrapper = this.removeWrapper.bind(this);
        this.onAutocompletionElementClick = this.onAutocompletionElementClick.bind(this);
    }

    render() {
        return (
            <div className={'d-flex flex-row flex-wrap overflow-auto'}>

            {/*The current input from search bar is only used to filter the autocompletion list*/}

                <SearchBar
                    searchCallback={(v) => {
                        this.setState({currentInput: v});
                        if(v.slice(0,2) === '0x'){
                            this.onAutocompletionElementClick({type: 'eth', value: v})
                            this.setState({currentInput: ""});
                            this.props.onSpecificVertexSearch();
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
            let tagsWithoutOne = [...this.state.metadataObjects.slice(0, indexToRemove),
                ...this.state.metadataObjects.slice(indexToRemove + 1,
                this.state.metadataObjects.length)];
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

    onAutocompletionElementClick(e) {
        let metadataObjects = [...this.state.metadataObjects, e];
        this.props.onChange(metadataObjects)
        this.setState({metadataObjects: metadataObjects, showAutocompletion: false})
    }
}

export default TagListGraph;