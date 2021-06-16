import React, {Component} from 'react';

class DeleatableTag extends Component {

    constructor(props) {
        super(props);
        this.remove = this.remove.bind(this)
    }

    render() {
        return (
            <div className={'border-black ml-1 border-2 p-1'}
                 onClick={this.remove}>
                <div className={'float-left w-5 mr-1 border-red-600 border-2 bg-red-100 text-center align-middle'}>x
                </div>
                <span>{this.props.tag}</span>
            </div>
        );
    }

    remove(){
        this.props.closeCallback(this.props.tag)
    }
}

export default DeleatableTag;