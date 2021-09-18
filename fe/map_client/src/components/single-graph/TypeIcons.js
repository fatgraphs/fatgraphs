import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faTag} from "@fortawesome/free-solid-svg-icons";
import React from "react";


export const TYPE_ICONS = {
    label: <FontAwesomeIcon
        className={'m-1 block'}
        icon={faTag}/>,
    type: <span
        className={'glyphicon glyphicon-text-width'}/>,
    eth: <div
        className={'flex border-black border-2 h-4 w-8 m-1 text-xs justify-center items-center p-2'}>ETH</div>

}