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
odoo.define('your_module_name.delivery_details', function (require) {
    'use strict';

    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    const { rpc } = require('web.core');

    class DeliveryDetailsPopup extends AbstractAwaitablePopup {
        constructor() {
            super(...arguments);
        }

        getPayload() {
            const deliveryCountry = this.el.querySelector('#delivery-country').value;
            const deliveryType = this.el.querySelector('#delivery-type').value;
            const expectedDeliveryDate = this.el.querySelector('#expected-delivery-date').value;

            return {
                deliveryCountry,
                deliveryType,
                expectedDeliveryDate,
            };
        }

        saveDeliveryDetails() {
            const payload = this.getPayload();
            const orderID = this.env.pos.get_order().id;

            rpc.query({
                model: 'pos.order',
                method: 'write',
                args: [[orderID], payload],
            }).then(() => {
                this.showPopup('SuccessPopup', {
                    title: 'Success',
                    body: 'Delivery details saved successfully!',
                });
                this.trigger('close-popup');
            }).catch((error) => {
                this.showPopup('ErrorPopup', {
                    title: 'Error',
                    body: 'Failed to save delivery details. Please try again.',
                });
                console.error(error);
            });
        }
    }

    DeliveryDetailsPopup.template = 'DeliveryDetailsPopup';
    Registries.Component.add(DeliveryDetailsPopup);

    return DeliveryDetailsPopup;
});

