odoo.define('point_of_sale_assets', function (require) {
    'use strict';

    const models = require('point_of_sale.models');
    const CustomClientLine = require('point_of_sale.ClientLine'); // Import your custom client line widget here

    // Load the 'dob' field for the 'res.partner' model
    models.load_fields('res.partner', ['dob']);

    // Define your custom models, screens, and widgets here

    return {
        // Export any objects or functions that should be accessible outside this module
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
