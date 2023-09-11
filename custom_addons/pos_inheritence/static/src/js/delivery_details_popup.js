//odoo.define('pos_inheritence.delivery_details_popup', function (require) {
//    "use strict";
//
//    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
//    const Registries = require('point_of_sale.Registries');
//
//    class DeliveryDetailsPopup extends AbstractAwaitablePopup {
//        constructor() {
//            super(...arguments);
//            this.order = arguments[1].order;
//        }
//
//        getPayload() {
//            return {};
//        }
//    }
//
//    DeliveryDetailsPopup.template = 'delivery_details_popup';
//
//    Registries.Component.add(DeliveryDetailsPopup);
//
//    return DeliveryDetailsPopup;
//});
