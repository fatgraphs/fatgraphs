import React, {Component} from 'react';
import {bool, string} from "prop-types";
import AddableElement from "./AddableElement";
import {MyContext} from "../../../Context";

class Autocompletion extends Component {

    static contextType = MyContext

    constructor(props) {
        super(props);
        this.state = {
            howManyToShow: 100
        }
        this.handleScroll = this.handleScroll.bind(this)
    }

    componentDidMount() {
    }

    render() {
        let containsCurrentInputRegex = new RegExp('.*' + this.props.currentInput.toLowerCase() + '.*');
        let matchingAutocompleteTerms = this.context['autocompleteTerms'].filter(s => s['metadata_value'].toLowerCase().match(containsCurrentInputRegex));
        // limit showed autocompletion terms for performance reasons
        matchingAutocompleteTerms = matchingAutocompleteTerms.slice(0, this.state.howManyToShow)

        return (
            matchingAutocompleteTerms.length > 0 && this.props.shouldRender ?
            <div className={'fixed z-50'}>
                <ul
                    onScroll={this.handleScroll}
                    className={'border-black border-2 p-2 flex flex-col absolute top-0 left-0 ml-1 bg-gray-100 w-48 h-72 overflow-y-auto'}>
                    {/* Quicklist metadata  */}
                    {this.props.recentMetadata.map((term, i) => <AddableElement
                        key={i}
                        metadata={term}
                        addMetadataCallback={this.props.addMetadataCallback}
                        bgColor={'bg-green-100'}/>)}
                    {/*  Other metadata  */}
                    {matchingAutocompleteTerms.map((term, i) => {
                        return <AddableElement
                        key={i + 5}
                        metadata={term}
                        addMetadataCallback={this.props.addMetadataCallback}/>
                        }
                    )}
                </ul>
            </div> : <></>
        );
    }

    handleScroll(e) {
        /**
         * Show more autocompletion terms when the user scrolls to the bottom
         * @type {boolean}
         */
        const reachBottomScrollbar = e.target.scrollHeight - e.target.scrollTop === e.target.clientHeight;
        if(reachBottomScrollbar){
            this.setState({
                howManyToShow: this.state.howManyToShow * 2
            })
        }
    }
}

Autocompletion.propTypes = {
    currentInput: string.isRequired,
    graphName: string.isRequired,
    shouldRender: bool.isRequired,
};

Autocompletion.defaultProps = {
    currentInput: ''
};

export default Autocompletion;