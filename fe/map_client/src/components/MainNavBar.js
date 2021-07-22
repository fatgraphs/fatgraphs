import React, {Component} from 'react';
import {Link} from "react-router-dom";

class MainNavBar extends Component {
    render() {
        return (
                <nav className={'p-4'}>
                    <ul className={'flex flex-row'}>
                        <li className={'ml-2'}>
                            <Link to="/">Home</Link>
                        </li>
                        <li className={'ml-2'}>
                            <Link to="/about">About</Link>
                        </li>
                    </ul>
                </nav>
        );
    }
}

export default MainNavBar;