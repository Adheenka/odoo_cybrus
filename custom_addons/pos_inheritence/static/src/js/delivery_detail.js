//odoo.define('pos_delivery_details.ActionpadWidget', function (require) {
//    'use strict';
//
//    const PosComponent = require('point_of_sale.PosComponent');
//    const Registries = require('point_of_sale.Registries');
//    const DeliveryDetailsPopup = require('pos_delivery_details.DeliveryDetailsPopup');
//
//    class ActionpadWidget extends PosComponent {
//        constructor() {
//            super(...arguments);
//        }
//
//        async openDeliveryDetailsPopup() {
//            const { confirmed, payload } = await this.showPopup(DeliveryDetailsPopup, {});
//            if (confirmed) {
//                // Handle the payload (delivery details) here
//                const { deliveryCountry, deliveryType, expectedDeliveryDate } = payload;
//                // You can now save these details to your custom model or perform any other action.
//            }
//        }
//    }
//
//    ActionpadWidget.template = 'ActionpadWidget';
//    ActionpadWidget.defaultProps = {
//        isActionButtonHighlighted: false,
//    }
//
//    Registries.Component.add(ActionpadWidget);
//
//    return ActionpadWidget;
//});
//async onClick() {
//    const selectedOrder = this.env.pos.get_order();
//    if (selectedOrder) {
//        // Show the delivery details popup when the button is clicked
//        this.showPopup('view_delivery_details_popup');
//    }
//}
