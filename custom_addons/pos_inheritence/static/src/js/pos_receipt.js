odoo.define('pos_receipt.pos_order_extend', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var QWeb = core.qweb;

    models.load_fields('res.partner',['dob']);


});
//odoo.define('pos_receipt.pos_order_extend', function (require) {
//    "use strict";
//
//    var models = require('point_of_sale.models');
//    var screens = require('point_of_sale.screens');
//    var core = require('web.core');
//    var QWeb = core.qweb;
//
//    models.load_fields('res.partner', ['dob']); // Load the 'mobile' and 'dob' fields
//
//    // Extend the ReceiptScreenWidget to customize the receipt template
//    screens.ReceiptScreenWidget.include({
//        render_receipt: function () {
//            var order = this.pos.get_order();
//            var receipt = order.export_for_printing();
//
//            // Render the default receipt template
//            this.$('.pos-receipt-container').html(QWeb.render('OrderReceipt', {
//                widget: this,
//                order: order,
//                receipt: receipt,
//            }));
//
//            // Display Date of Birth and Mobile Number
//            if (receipt.partner_id) {
//                var $contactInfo = this.$('.pos-receipt-contact');
//                $contactInfo.append('<div>Date of Birth: ' + receipt.partner_id[0].dob + '</div>');
////                $contactInfo.append('<div>Mobile Number: ' + receipt.partner_id[0].mobile + '</div>');
//            }
//        },
//    });
//});
