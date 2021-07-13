import React, {Component} from 'react';
import ClosableMetadata from "./ClosableMetadata";
import Autocompletion from "./Autocompletion";
import {MyContext} from "../../../Context";
import _ from 'underscore';
import {array, bool, func, string} from "prop-types";
import {postRecentMetadata} from "../../../APILayer";

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
        this.addMetadataCallback = this.addMetadataCallback.bind(this)
        this.onBlur = this.onBlur.bind(this)
    }

    render() {
        let displaySelectedMetadata = <>{
            this.props.showSelected ?
                this.state.metadataSelected
                    .map((metadata, i) =>
                        <ClosableMetadata
                            metadata={metadata}
                            closeCallback={this.closeMetadataCallback}
                            key={i}/>
                    ) :
                <></>
        }</>;

        return (
            <div className={'flex flex-row flex-wrap position-relative h-12'}>

                {displaySelectedMetadata}

                {/* logic to deal with the user pressing enter
                as opposed to the user clicking on the item they want to add*/}
                <form
                    onSubmit={() => this.pressedEnterCallback(this.state.currentInput)}
                    onBlur={this.onBlur}
                    className={'h-12 w-60'}>
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

                    <Autocompletion
                        shouldRender={this.state.showAutocompletion}
                        currentInput={this.state.currentInput}
                        addMetadataCallback={this.addMetadataCallback}
                        graphName={this.props.graphName}
                        recentMetadata={this.props.recentMetadataSearches}
                    />
                </form>
            </div>
        );
    }

    pressedEnterCallback(currentInput) {
        if (currentInput.substring(0, 2) === '0x') {
            this.addMetadataCallback({
                metadataValue: currentInput,
                metadataType: 'eth'
            })
            return
        }

        // we only have free text from the user, we need to figure if it's a type or a label
        let match = this.context['autocompleteTerms'].find((e) => e['metadata_value'] === currentInput);
        if (match) {
            this.addMetadataCallback(match)
        }
    }

    addMetadataCallback(metadataObject) {
        this.setState(oldState => {
            this.state.searchInputElement.blur()
            let metadataNow = [...oldState.metadataSelected, metadataObject];

            // Update the quicklist
            if (!this.props.recentMetadataSearches.some(t => _.isEqual(t, metadataObject))) {
                postRecentMetadata(metadataObject)
            }

            // Update parent component
            this.props.selectedMetadataCallback(metadataNow)

            return ({
                metadataSelected: metadataNow,
                currentInput: '',
                showAutocompletion: false
            });
        })

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
    placeholder: string.isRequired,
    recentMetadataSearches: array.isRequired,
    showSelected: bool,
    selectedMetadataCallback: func.isRequired
};

SearchBar.defaultProps = {
    showSelected: true
};

export default SearchBar;