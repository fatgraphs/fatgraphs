import React, {Component} from 'react';

class DeleatableTag extends Component {

    constructor(props) {
        super(props);
        this.remove = this.remove.bind(this)
    }

    render() {
        return (
            <div className={'border-black ml-1 border-2 p-2 flex flex-row items-center'}
                 onClick={this.remove}>
                <div className={'w-5 mr-1 border-red-600 border-2 bg-red-100 text-center'}>x</div>
                <span>{this.props.tag}</span>
            </div>
        );
    }

    remove(){
        this.props.closeCallback(this.props.tag)
    }
}

export default DeleatableTag;