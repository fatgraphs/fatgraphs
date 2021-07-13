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
        let outerStyle = 'flex flex-row flex-wrap';
        let innerStyle = 'flex flex-row mr-4 mt-4 odd:bg-gray-100';
        if(this.props.stackVertically !== undefined && this.props.stackVertically){
            outerStyle = 'flex flex-col flex-wrap';
            innerStyle = 'flex flex-col mr-4 mt-4 odd:bg-gray-100';
        }
        return (
            <div>
                <dl className={outerStyle}>
                    {this.props.keys.map((key, index) => {
                        return <div key={index} className={innerStyle}>
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
    stackVertically: PropTypes.bool,
};

export default DescriptionTable;