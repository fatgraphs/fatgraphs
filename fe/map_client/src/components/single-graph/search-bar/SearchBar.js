import React, {Component} from 'react';
import ClosableElement from "./ClosableElement";
import Autocompletion from "./Autocompletion";
import {MyContext} from "../../../Context";
import _ from 'underscore';
import {array, bool, func, string, number} from "prop-types";
import {postRecentMetadataSearches} from "../../../APILayer";

class SearchBar extends Component {

    static contextType = MyContext

    constructor(props) {
        super(props);
        this.state = {
            metadataSelected: [],
            currentInput: "",
            showAutocompletion: false,
            searchInputElement: undefined
        }
        this.closeMetadataCallback = this.closeMetadataCallback.bind(this)
        this.searchBarAddMetadataCallback = this.searchBarAddMetadataCallback.bind(this)
        this.onBlur = this.onBlur.bind(this)
    }

    render() {
        let displaySelectedMetadata = <>{
            this.props.showSelected ?
                this.state.metadataSelected
                    .map((metadata, i) =>
                        <ClosableElement
                            metadata={metadata}
                            closeCallback={this.closeMetadataCallback}
                            key={i}/>
                    ) :
                <></>
        }</>;

        return (
            <div className={'flex flex-col justify-center p-2 overflow-y-auto ' + this.props.className}>
                <div className={'flex flex-row flex-wrap justify-start overflow-y-auto'}>
                    <form
                        onSubmit={() => this.pressedEnterCallback(this.state.currentInput)}
                        onBlur={this.onBlur}
                        className={'w-60'}>
                        <label>
                            <input className={'p-2 focus:outline-none'}
                                   type="text"
                                   ref={inputEl => (this.state.searchInputElement = inputEl)}
                                   placeholder={this.props.placeholder}
                                   value={this.state.currentInput}
                                   onChange={(event) => {
                                       this.setState({currentInput: event.target.value})
                                   }}
                                   onFocus={() => {
                                       this.setState({showAutocompletion: true})
                                   }}
                            />
                        </label>
                    </form>

                    {displaySelectedMetadata}

                </div>
                <Autocompletion
                    shouldRender={this.state.showAutocompletion}
                    currentInput={this.state.currentInput}
                    addMetadataCallback={this.searchBarAddMetadataCallback}
                    graphId={this.props.graphId}
                    recentMetadataSearches={this.props.recentMetadataSearches}
                />
            </div>
        );
    }

    pressedEnterCallback(currentInput) {
        // logic to deal with the user pressing enter
        // as opposed to the user clicking on the item they want to add

        if (currentInput.substring(0, 2) === '0x') {
            this.searchBarAddMetadataCallback({
                metadataValue: currentInput,
                metadataType: 'eth'
            })
            return
        }

        // we only have free text from the user, we need to figure if it's a type or a label
        let match = this.context['autocompleteTerms'].find((e) => e['metaValue'] === currentInput);
        if (match) {
            this.searchBarAddMetadataCallback(match)
        }
    }

    searchBarAddMetadataCallback(metadataObject) {
        this.state.searchInputElement.blur()
        let metadataNow = [...this.state.metadataSelected, metadataObject];

        // Update the quicklist
        if (!this.props.recentMetadataSearches.some(metaOj => _.isEqual(metaOj, metadataObject))) {
            postRecentMetadataSearches(metadataObject).then(r => console.log("ffddhbjdhjbdh"))
        }

        // Update parent component
        this.props.selectedMetadataCallback(metadataNow)

        this.setState({
            metadataSelected: metadataNow,
            currentInput: '',
            showAutocompletion: false
        });

    }

    closeMetadataCallback(metadataObject) {
        let metadataNow = this.state.metadataSelected.filter(m => !_.isEqual(m, metadataObject));
        this.setState({metadataSelected: metadataNow})
        this.props.selectedMetadataCallback(metadataNow)
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
}

SearchBar.propTypes = {
    graphName: string.isRequired,
    graphId: number.isRequired,
    placeholder: string.isRequired,
    recentMetadataSearches: array.isRequired,
    showSelected: bool,
    selectedMetadataCallback: func.isRequired
};

SearchBar.defaultProps = {
    showSelected: true
};

export default SearchBar;