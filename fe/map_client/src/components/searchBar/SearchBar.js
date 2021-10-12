import React, {Component} from 'react';
import {Form, FormGroup, Input, InputGroup, InputGroupAddon, InputGroupText} from "reactstrap";
import SearchIcon from "../../reactBlueTemplate/src/components/Icons/HeaderIcons/SearchIcon";

import s from "./SearchBar.module.scss";
import PropTypes from "prop-types";

class SearchBar extends Component {

    constructor() {
        super();

        this.state = {
            searchFocused: false,
            currentInput: ''
        }
        this.onSubmit = this.onSubmit.bind(this);
    }

    render() {
        return (
            <div>
                <Form inline
                    onSubmit={this.onSubmit}
                    onBlur={this.props.onBlur}>
                    <FormGroup>
                        <InputGroup className={`input-group-no-border ${s.searchForm}`}>
                            <InputGroupAddon addonType="prepend">
                                <InputGroupText className={s.inputGroupText}>
                                    <SearchIcon className={s.headerIcon}/>
                                </InputGroupText>
                            </InputGroupAddon>
                            <Input
                                id="search-input"
                                className="input-transparent"
                                placeholder="Search Dashboard"
                                value={this.state.currentInput}
                                onChange={(e) => {
                                    this.setState({currentInput: e.target.value})
                                    this.props.onChange(e.target.value)
                                }}
                                onFocus={this.props.onFocus}
                            />
                        </InputGroup>
                    </FormGroup>
                </Form>
            </div>
        );
    }

    onSubmit(e){
        e.target[0].blur();
        e.preventDefault();
        if(this.state.currentInput.length === 0){
            return;
        }
        this.props.searchCallback(this.state.currentInput)
        this.setState({currentInput: ''})
    }

}

SearchBar
    .propTypes = {searchCallback: PropTypes.func};

SearchBar.defaultProps = {
    onChange: (e) => e
};

export default SearchBar;