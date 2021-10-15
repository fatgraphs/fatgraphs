import React from "react";
import {Nav, Navbar, NavItem,} from "reactstrap";


import s from "./Navbar.module.scss";
import "animate.css";
import {Link} from "react-router-dom";
const configs = require('configurations')

class NavBar extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        let gts = Object.keys(configs['galleryTypes'])
        return (
            <Navbar className={`d-print-none p-3 ${s.navbar}`}>

                <div className={`d-print-none ${s.root}`}>
                    <div>
                            <h1 className={s.inlineTitle}>The Token Gallery</h1>
                    </div>


                    <Nav className="ml-md-0 p-3">

                        {
                            gts.map((e, i) => {
                                return(
                                <React.Fragment key={i*98}>
                                    <NavItem>
                                    <Link
                                        className={`${s.navItem} text-white`}
                                        to={"/gallery/" + e}>

                                        {e}

                                    </Link>
                                </NavItem>
                                <NavItem
                                   className={`${s.divider} d-none d-sm-block`}/>
                                </React.Fragment>
                            )}

                        )}

                        <NavItem>
                            <Link
                                className={`${s.navItem} text-white`}
                                to='/about'>

                                About

                            </Link>
                        </NavItem>

                    </Nav>
                </div>
            </Navbar>
        );
    }
}

export default NavBar;
