import ReactDOMServer from "react-dom/server";
import L from "leaflet";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faTag} from "@fortawesome/free-solid-svg-icons";
import React from "react";
import LabelVertex from "./LabelVertex";
import VertexPopup from "./VertexPopup";

export function getCircleIcon(className, iconSize) {
    let html = ReactDOMServer.renderToString(
        <div></div>
    )
    let circleIcon = L.divIcon(
        {
            html: html,
            className: className,
            iconSize: iconSize
        });
    return circleIcon
}

export function getTextLabelIcon(eth, pos, labels, types) {

    let textLabelsIcon = <>
        {types.map((typ, index) => <LabelVertex key={index} label={typ}/>)}
    </>

    let html = ReactDOMServer.renderToString(textLabelsIcon)
    let icon = L.divIcon({
        html: html,
        className: ''
    });
    return icon
}

export function getVertexPopup(typesString, labelsString, eth, graphName, graphId, callBack, recentMetadataSearches) {
    /**
     * The popup when you click on a vertex-marker
     */
    return <VertexPopup
        typesConcatenated={typesString}
        labelsConcatenated={labelsString}
        eth={eth}
        graphName={graphName}
        graphId={graphId}
        selectionCallback={callBack}
        recentMetadataSearches={recentMetadataSearches}
    />;
}

export const TYPE_ICONS = {
    label: <FontAwesomeIcon
        className={'m-1 block'}
        icon={faTag}/>,
    type: <div
        className={'flex border-black border-2 rounded-full h-4 w-4 m-1 font-bold text-xs justify-center items-center p-2'}>T</div>,
    eth: <div
        className={'flex border-black border-2 h-4 w-8 m-1 text-xs justify-center items-center p-2'}>ETH</div>

}