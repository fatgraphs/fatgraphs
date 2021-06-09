import React, {Component} from 'react';
import PropTypes from 'prop-types';

class DescriptionTable extends Component {
    /**
     * A description table is a list of key-values, rendered either vertically (stack_vertically = true)
     * or horizontally.
     * @param props
     */
    constructor(props) {
        super(props);
    }

    render() {
        let outer_style = 'flex flex-row flex-wrap';
        let inner_style = 'flex flex-row mr-4 mt-4 odd:bg-gray-100';
        if(this.props.stack_vertically !== undefined && this.props.stack_vertically){
            outer_style = 'flex flex-col flex-wrap';
            inner_style = 'flex flex-col mr-4 mt-4 odd:bg-gray-100';
        }
        return (
            <div>
                <dl className={outer_style}>
                    {this.props.keys.map((key, index) => {
                        return <div key={index} className={inner_style}>
                            <dt>{key + ':'}</dt>
                            <dd>{this.props.values[index]}</dd>
                    </div>;
                })}
                </dl>
            </div>
        );
    }
}

DescriptionTable.propTypes = {
    keys: PropTypes.array.isRequired,
    values: PropTypes.array.isRequired,
    stack_vertically: PropTypes.bool,
};

export default DescriptionTable;