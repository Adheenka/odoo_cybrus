odoo.define('pos_inheritence.DeliveryDetailsPopup', function (require) {
    "use strict";

    const { PopupWidget } = require('point_of_sale.widgets');
    const Registries = require('point_of_sale.Registries');
     const { Gui } = require('point_of_sale.Gui');
   c
    class DeliveryDetailsPopup extends PopupWidget {
        constructor() {
            super(...arguments);
            this.selectedCountry = null;
            this.selectedType = 'standard';
            this.selectedDate = null;
        }

        cancel() {
            this.trigger('close-popup');
        }

        save() {
            // Add your code to handle saving the delivery details here
            const deliveryDetails = {
                country: this.selectedCountry,
                type: this.selectedType,
                date: this.selectedDate,
            };

            // Example: Send the delivery details to the server
            // You can replace this with your actual implementation
            this.rpc({
                model: 'pos.order', // Replace with your model name
                method: 'update_delivery_details',
                args: [this.env.pos.get_order().id, deliveryDetails],
            }).then(() => {
                this.trigger('close-popup');
            });
        }
    }

    DeliveryDetailsPopup.template = 'DeliveryDetailsPopup';

    Registries.Component.add(DeliveryDetailsPopup);

    return DeliveryDetailsPopup;
});

