import React, {Component} from 'react';

class CenteredElement extends Component {
    render() {
        return (
            <div className={'flex flex-col place-content-center justify-center text-center'}>
                {this.props.children}
            </div>
        );
    }
}

export default CenteredElement;