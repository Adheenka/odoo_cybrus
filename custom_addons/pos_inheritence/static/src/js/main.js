//odoo.define('pos_inheritence.main', function (require) {
//    "use strict";
//
//    const models = require('point_of_sale.models');
//    const { Gui } = require('point_of_sale.Gui');
//
//    // Define your cstom payment method (e.g., Cheque)
//    models.load_fields('pos.payment.method', ['is_cheque']);
//    models.Order= models.Order.extend({
//        async popup() {
//
//            const { confirmed, payload } = await Gui.showPopup("MyPopup", {});
//
//            if (confirmed) {
//                this.selected_paymentline.cheque_date = payload.ch_date;
//                this.selected_paymentline.cheque_no = payload.ch_no;
//            }
//
//    }
//    // Extend the Order model to add custom behavior for cheque payment
//    add_paymentline: function(payment_method) {
//        if (payment_method.is_cheque === true) {
//            this.popup();
//    }
//        this.assert_editable();
//        if (this.electronic_payment_in_progress()) {
//            return false;
//    } else {
//      var newPaymentline = new models.Paymentline({},{order: this, payment_method: payment_method, pos: this.pos});
//      newPaymentline.set_amount(this.get_due());
//      this.paymentlines.add(newPaymentline);
//      this.select_paymentline(newPaymentline);
//      if(this.pos.config.cash_rounding){
//         this.selected_paymentline.set_amount(0);
//          this.selected_paymentline.set_amount(this.get_due());
//            }
//
//            if (payment_method.payment_terminal) {
//                newPaymentline.set_payment_status('pending');
//            }
//            return newPaymentline;
//        }
//    },
//});


odoo.define('pos_inheritence.main', function (require) {
    "use strict";

    const models = require('point_of_sale.models');
    const { Gui } = require('point_of_sale.Gui');

    // Define your custom payment method (e.g., Cheque)
    models.load_fields('pos.order', ['is_cheque']);

    // Extend the Order model to add custom behavior for cheque payment
    models.load_models([
        {
            model: 'pos.order',
            condition: function (self) {
                return self.config.is_cheque;
            },
            fields: ['is_cheque'],
            loaded: function (self, pos_orders) {
                for (const pos_order of pos_orders) {
                    self.db.pos_orders_by_id[pos_order.id].is_cheque = pos_order.is_cheque;
                }
            },
        },
    ]);

    models.Order = models.Order.extend({
        add_paymentline(payment_method) {
            if (payment_method.is_cheque) {
                // Show a popup for entering cheque details
                Gui.showPopup('pos_inheritence.ChequePopup', {}).then(({ confirmed, payload }) => {
                    if (confirmed) {
                        // Create a new payment line with cheque details
                        const newPaymentline = new models.Paymentline({
                            order: this,
                            payment_method: payment_method,
                            pos: this.pos,
                        });
                        newPaymentline.set_amount(this.get_due());
                        newPaymentline.cheque_date = payload.ch_date;
                        newPaymentline.cheque_no = payload.ch_no;
                        this.paymentlines.add(newPaymentline);
                        this.select_paymentline(newPaymentline);
                        if (this.pos.config.cash_rounding) {
                            this.selected_paymentline.set_amount(0);
                            this.selected_paymentline.set_amount(this.get_due());
                        }
                        if (payment_method.payment_terminal) {
                            newPaymentline.set_payment_status('pending');
                        }
                        return newPaymentline;
                    }
                });
            } else {
                return this._super(payment_method);
            }
        },
    });
});












































//odoo.define('pos_inheritence.main', function (require) {
//    "use strict";
//
//    const models = require('point_of_sale.models');
//    const { Gui } = require('point_of_sale.Gui');
//
//    // Define your custom payment method (e.g., Cheque)
//    models.load_fields('pos.order', ['is_cheque']);
//
//    // Extend the Order model to add custom behavior for cheque payment
//    models.load_models([
//        {
//            model: 'pos.order',
//            condition: function (self) {
//                return self.config.is_cheque;
//            },
//            fields: ['is_cheque'],
//            loaded: function (self, pos_orders) {
//                for (const pos_order of pos_orders) {
//                    self.db.pos_orders_by_id[pos_order.id].is_cheque = pos_order.is_cheque;
//                }
//            },
//        },
//    ]);
//
//    models.Order = models.Order.extend({
//        async add_paymentline(payment_method) {
//            if (payment_method.is_cheque) {
//                // Show a popup for entering cheque details
//                const { confirmed, payload } = await Gui.showPopup('pos_inheritence.ChequePopup', {});
//                if (confirmed) {
//                    // Create a new payment line with cheque details
//                    const newPaymentline = new models.Paymentline({
//                        order: this,
//                        payment_method: payment_method,
//                        pos: this.pos,
//                    });
//                    newPaymentline.set_amount(this.get_due());
//                    newPaymentline.cheque_date = payload.ch_date;
//                    newPaymentline.cheque_no = payload.ch_no;
//                    this.paymentlines.add(newPaymentline);
//                    this.select_paymentline(newPaymentline);
//                    if (this.pos.config.cash_rounding) {
//                        this.selected_paymentline.set_amount(0);
//                        this.selected_paymentline.set_amount(this.get_due());
//                    }
//                    if (payment_method.payment_terminal) {
//                        newPaymentline.set_payment_status('pending');
//                    }
//                    return newPaymentline;
//                }
//            } else {
//                return this._super(payment_method);
//            }
//        },
//    });
//});
