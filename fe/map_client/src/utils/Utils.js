import L from "leaflet";
import TextLabelMap from "../components/single-graph/graph-map/LabelVertex";
import ReactDOMServer from "react-dom/server";
import React from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faTag} from "@fortawesome/free-solid-svg-icons";

export function symmetricDifference(a, b) {
    /**
     * Given 2 js lists returns the set difference
     * @type {Set<any>}
     * @private
     */
    let setA = new Set(a)
    let setB = new Set(b)
    let _difference = new Set(setA)
    for (let elem of setB) {
        if (_difference.has(elem)) {
            _difference.delete(elem)
        } else {
            _difference.add(elem)
        }
    }
    return _difference
}

function _make_vertex_popup(eth_address, labels, types) {

    let unique_types = Array.from(new Set(types));
    let unique_labels = Array.from(new Set(labels));
    let labels_string = labels === null ? 'NA' : unique_labels.join(', ');
    let types_string = types === null ? 'NA' : unique_types.join(', ');


    let link_etherscan = `<div>

                                <div>
                                    <span>Types : </span>
                                    <span>${types_string}</span>
                                </div>
                                
                                <div>
                                    <span>Labels : </span>
                                    <span style="white-space: nowrap;">${labels_string}</span>
                                </div>
                               
                                <a href="https://etherscan.io/address/${eth_address}"
                                    target="_blank">${eth_address}</a>
                            </div>`
    let popup = L.popup()
        .setContent(link_etherscan)
    return popup
}

export function make_marker_with_popup(className, pos, eth_addresss, labels, types, iconSize) {
    /**
     * Adds a circle on the map that can be clicked and on click it opens a pop up
     */

    let myIcon = L.divIcon({className: className, iconSize: iconSize});
    let marker = L.marker(pos, {icon: myIcon});


    marker.bindPopup(_make_vertex_popup(
        eth_addresss, labels, types)).openPopup();
    return marker
}

export function removeElement(overlay_element, map) {
    /**
     * Given a map and an associated overlayElements (e.g. a marker or a label) it visually removes it from the map.
     */
    map.removeLayer(overlay_element)
}

export function draw_text_label(eth, pos, labels, types) {

    let h = <div>
        {types.map((typ, index) => <TextLabelMap key={index} label={typ}/>)}
    </div>

    let test_html = ReactDOMServer.renderToString(h)
    let icon = L.divIcon({
        html: test_html,
        className: ''
    });
    let marker = L.marker(pos, {icon: icon});
    marker.bindPopup(_make_vertex_popup(
        eth, labels, types)).openPopup();
    return marker
}

export const type_to_icon = {
    label: <FontAwesomeIcon
        className={'m-1'}
        icon={faTag}/>,
    type: <div
        className={'flex border-black border-2 rounded-full h-4 w-4 m-1 font-bold text-xs justify-center items-center p-2'}>T</div>,
    eth: <div
        className={'flex border-black border-2 h-4 w-8 m-1 text-xs justify-center items-center p-2'}>ETH</div>

}