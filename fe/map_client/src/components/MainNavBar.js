import React, {Component} from 'react';
import {Link} from "react-router-dom";

class MainNavBar extends Component {
    render() {
        return (
            <div className={'p-4'}>
                <nav>
                    <ul className={'flex flex-row'}>
                        <li className={'ml-2'}>
                            <Link to="/">Home</Link>
                        </li>
                        <li className={'ml-2'}>
                            <Link to="/about">About</Link>
                        </li>
                    </ul>
                </nav>
            </div>
        );
    }
}

export default MainNavBar;