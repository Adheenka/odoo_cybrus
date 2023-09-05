odoo.define('pos_receipt.pos_order_extend', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var QWeb = core.qweb;

    models.load_fields('res.partner', ['mobile']);


});