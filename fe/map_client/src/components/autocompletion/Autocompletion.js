import React, {Component} from 'react';
import {array, bool, string} from "prop-types";
import AddableElement from "./AddableElement";
import {MyContext} from "../../Context";
import './autocompletionOuter.scss'

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
        let matchingAutocompleteTerms = this.context['autocompleteTerms'].filter(s => s['value'].toLowerCase().match(containsCurrentInputRegex));
        // limit showed autocompletion terms for performance reasons
        matchingAutocompleteTerms = matchingAutocompleteTerms.slice(0, this.state.howManyToShow)

        return (
            matchingAutocompleteTerms.length > 0 && this.props.shouldRender ?
            <div className={'autocompletionOuter'}>
                <ul
                    onScroll={this.handleScroll}
                    className={'autocompletionInner'}>
                    {/* Quicklist vertex_metadata  */}
                    {this.props.recentMetadataSearches.map((metaObject, i) => <AddableElement
                        key={i}
                        metadata={metaObject}
                        onClick={this.props.onClick}
                        bgColor={'bg-green-100'}/>)}
                    {/*  Other vertex_metadata  */}
                    {matchingAutocompleteTerms.map((term, i) => {
                        return <AddableElement
                        key={i + 5}
                        metadata={term}
                        onClick={this.props.onClick}/>
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
    shouldRender: bool.isRequired,
    recentMetadataSearches: array.isRequired
};

Autocompletion.defaultProps = {
    currentInput: ''
};

export default Autocompletion;