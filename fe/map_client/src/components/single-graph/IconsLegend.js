import React, {Component} from 'react';
import './iconImageLegend.css'
import ca from '../../../../../assets/vertex_icons/generic/ca.png';
import ca_labelled from '../../../../../assets/vertex_icons/generic/ca_labelled.png';
import eoa from '../../../../../assets/vertex_icons/generic/eoa.png';
import eoa_labelled from '../../../../../assets/vertex_icons/generic/eoa_labelled.png';
import fake_inactive from '../../../../../assets/vertex_icons/generic/inactive_fake.png'; import {Table} from "reactstrap"; import {truncateEth} from "../../utils/Utils";

export class IconsLegend extends Component {

    constructor() {
        super();

    }
    render() {
        return <div>
        <Table className="my-table-hover">
            <thead>
                <tr>
                    <th>Img</th>
                    <th>Meaning</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>
                        <img src={ca_labelled} alt={"Contract account labelled"} className={"iconImageLegend"}/>
                    </td>
                    <td>
                       Contract account labelled
                    </td>
                </tr>
                <tr>
                    <td>
                        <img src={ca} alt={"Contract account unlabelled"} className={"iconImageLegend"}/>
                    </td>
                    <td>
                       Contract account unlabelled
                    </td>
                </tr>
                <tr>
                    <td>
                        <img src={eoa_labelled} alt={"Externally owned account labelled"} className={"iconImageLegend"}/>
                    </td>
                    <td>
                       EOA labelled
                    </td>
                </tr>
                <tr>
                    <td>
                        <img src={eoa} alt={"Externally owned account unlabelled"} className={"iconImageLegend"}/>
                    </td>
                    <td>
                       EOA unlabelled
                    </td>
                </tr>

                <tr>
                    <td>
                        <img src={fake_inactive} alt={"Inactive or fake account"} className={"iconImageLegend"}/>
                    </td>
                    <td>
                       Inactive/Fake
                    </td>
                </tr>

            </tbody>
        </Table>
        </div>
  }
}