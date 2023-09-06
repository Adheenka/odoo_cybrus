odoo.define('point_of_sale_assets', function (require) {
    'use strict';

    const models = require('point_of_sale.models');
    const CustomClientLine = require('point_of_sale.ClientLine'); // Import your custom client line widget here


    models.load_fields('res.partner', ['dob','mobile']);



    return {

    };
});
//odoo.define('pos_custom_addons.ClientLine', function (require) {
//    'use strict';
//
//    const ClientLine = require('point_of_sale.ClientLine');
//    const Registries = require('point_of_sale.Registries');
//
//    const NewClientLine = ClientLine =>
//        class extends ClientLine {
//            get dob() {
//                return this.props.partner.dob || 'No DOB';
//            }
//        }
//
//    Registries.Component.extend(ClientLine, NewClientLine);
//    return NewClientLine;
//});
