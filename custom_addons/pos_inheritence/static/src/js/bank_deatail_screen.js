//odoo.define('point_of_sale.screens', function (require) {
//    "use strict";
//
//    var PaymentScreen = require('point_of_sale.PaymentScreen');
//    var core = require('web.core');
//    var QWeb = core.qweb;
//    var _t = core._t;
//    var rpc = require('web.rpc');
//    const Registries = require('point_of_sale.Registries');
//
//    const CustomPosModel = (PosModel) =>
//        class extends PosModel {
//            constructor() {
//                super(...arguments);
//                useListener('click', this.onClickBankDetails);
//            }
//
//            async onClickBankDetails() {
//                if (this.get_order()) {
//                    const order = this.get_order();
//                    if (order.card_number && order.expiry_date) {
//                        const popup = new PopupWidget(this, {
//                            title: 'Bank Details',
//                            body: this.env.qweb.render('popup_bank_details_template', {
//                                order: order,
//                            }),
//                        });
//                        popup.open();
//                    } else {
//                        Gui.showPopup('ErrorPopup', {
//                            title: 'Bank Details',
//                            body: 'No bank details found for this order.',
//                        });
//                    }
//                }
//            }
//        };
//
//    return CustomPosModel;
//});

odoo.define('pos_inheritence.custom_pos', function (require) {
    "use strict";

    var PaymentScreen = require('point_of_sale.PaymentScreen');
    var PopupWidget = require('point_of_sale.Popups');

    PaymentScreen.include({
        events: _.extend({}, PaymentScreen.prototype.events, {
            'click .js_bank_details': 'showBankDetailsPopup',
        }),

        showBankDetailsPopup: function () {
            var self = this;

            var popup = new PopupWidget(this, {
                title: 'Bank Details',
                body: 'Add your bank details here.',
                buttons: [
                    {
                        text: 'Close',
                        click: function () {
                            popup.close();
                        },
                    },
                ],
            });

            popup.open();
        },
    });
});





























//odoo.define('pos_inheritence.bank_details_popup', function (require) {
//    'use strict';
//
//    const { PopupWidget } = require('point_of_sale.widgets');
//    const Registries = require('point_of_sale.Registries');
//
//    class BankDetailsPopup extends PopupWidget {
//        constructor() {
//            super(...arguments);
//        }
//
//        getPayload() {
//            // Retrieve the bank details from the PoS order
//            const order = this.env.pos.get_order();
//            return {
//                cardNumber: order.get_card_number() || '',
//                expiryDate: order.get_expiry_date() || '',
//            };
//        }
//    }
//
//    BankDetailsPopup.template = 'BankDetailsPopup';
//    Registries.Component.add(BankDetailsPopup);
//
//    return BankDetailsPopup;
//});
