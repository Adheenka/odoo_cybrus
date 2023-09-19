odoo.define("pos_inheritence.DeliveryDetailsPopup", function (require) {
    "use strict";
    const { useState } = owl.hooks;
    const AbstractAwaitablePopup = require("point_of_sale.AbstractAwaitablePopup");
    const Registries = require("point_of_sale.Registries");

    class DeliveryDetailsPopup extends AbstractAwaitablePopup {
        constructor() {
            super(...arguments);
            this.state = useState({
                delivery_country_id: null,
                delivery_country_name: "",
                delivery_type: "domestic",
                expected_delivery_date: new Date(),
            });
        }

        openCountrySelectionPopup() {
            this.showPopup("CountrySelectionPopup", {
                confirm: this.confirmCountrySelection.bind(this),
            });
        }

        confirmCountrySelection(selectedCountry) {
            this.state.delivery_country_id = selectedCountry.id;
            this.state.delivery_country_name = selectedCountry.name;
        }

        async confirm() {
            const payload = {
                delivery_country_id: this.state.delivery_country_id,
                delivery_country_name: this.state.delivery_country_name,
                delivery_type: this.state.delivery_type,
                expected_delivery_date: this.state.expected_delivery_date.toISOString(),
            };

            // Create a new record in the DeliveryDetails model
            const deliveryDetails = await this.rpc({
                model: 'pos.order',
                method: 'create',
                args: [payload],
            });

            // Link the delivery details to the POS order
            const order = this.env.pos.get_order();
            order.delivery_details_id = deliveryDetails;

            this.trigger('close-popup');
        }
    }

    DeliveryDetailsPopup.template = "DeliveryDetailsPopup";

    Registries.Component.add(DeliveryDetailsPopup);

    return DeliveryDetailsPopup;
});







//odoo.define("pos_inheritence.DeliveryDetailsPopup", function (require) {
//    "use strict";
//    const { useState } = owl.hooks;
//    const AbstractAwaitablePopup = require("point_of_sale.AbstractAwaitablePopup");
//    const PosComponent = require("point_of_sale.PosComponent");
//    const ProductScreen = require("point_of_sale.ProductScreen");
//    const { useListener } = require("web.custom_hooks");
//    const Registries = require("point_of_sale.Registries");
//
//
//    class DeliveryDetailsPopup extends AbstractAwaitablePopup {
//        constructor() {
//            super(...arguments);
//            this.state = useState({
//                delivery_country_id: null,
//                delivery_country_name: "",
//                delivery_type: "domestic",
//                expected_delivery_date: new Date(),
//            });
//        }
//
//        openCountrySelectionPopup() {
//            this.showPopup("CountrySelectionPopup", {
//                confirm: this.confirmCountrySelection.bind(this),
//            });
//        }
//
//        confirmCountrySelection(selectedCountry) {
//            this.state.delivery_country_id = selectedCountry.id;
//            this.state.delivery_country_name = selectedCountry.name;
//        }
//
//        getPayload() {
//            return {
//                delivery_country_id: this.state.delivery_country_id,
//                delivery_country_name: this.state.delivery_country_name,
//                delivery_type: this.state.delivery_type,
//                expected_delivery_date: this.state.expected_delivery_date.toISOString(),
//            };
//        }
//    }
//
//    DeliveryDetailsPopup.template = "DeliveryDetailsPopup";
//
//    Registries.Component.add(DeliveryDetailsPopup);
//
//    return DeliveryDetailsPopup;
//});






















//errorcode


//odoo.define('point_of_sale.DeliveryDetailsPopup', function (require) {
//    'use strict';
//
//    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
//    const Registries = require('point_of_sale.Registries');
//    const { useState, useRef } = owl;
//    const { _lt } = require('@web/core/l10n/translation');
//    const { Gui } = require('point_of_sale.Gui');
//
//    class DeliveryDetailsPopup extends AbstractAwaitablePopup {
//        constructor() {
//            super(...arguments);
//            this.state = useState({
//                deliveryCountryId: null,
//                deliveryCountryName: '',
//                deliveryType: '',
//                expectedDeliveryDate: '',
//            });
//            this.deliveryTypeRef = useRef('deliveryType');
//            this.expectedDeliveryDateRef = useRef('expectedDeliveryDate');
//        }
//
//        openCountrySelectionPopup() {
//            this.showPopup('CountrySelectionPopup', {
//                confirm: this.confirmCountrySelection.bind(this),
//            });
//        }
//
//        confirmCountrySelection(selectedCountry) {
//            this.state.deliveryCountryId = selectedCountry.id;
//            this.state.deliveryCountryName = selectedCountry.name;
//        }
//
//        async confirm() {
//            if (!this.state.deliveryCountryId || !this.state.deliveryType || !this.state.expectedDeliveryDate) {
//                this.showError('Incomplete Details', 'Please fill in all required fields.');
//                return;
//            }
//
//            const payload = {
//                delivery_country_id: this.state.deliveryCountryId,
//                delivery_country_name: this.state.deliveryCountryName,
//                delivery_type: this.state.deliveryType,
//                expected_delivery_date: this.state.expectedDeliveryDate,
//            };
//
//            this.trigger('delivery-details-confirmed', payload);
//            this.trigger('close-popup');
//        }
//
//        showError(title, body) {
//            Gui.showPopup('ErrorPopup', {
//                title: _lt(title),
//                body: _lt(body),
//            });
//        }
//
//        getPayload() {
//            return {
//                delivery_country_id: this.state.deliveryCountryId,
//                delivery_country_name: this.state.deliveryCountryName,
//                delivery_type: this.state.deliveryType,
//                expected_delivery_date: this.state.expectedDeliveryDate,
//            };
//        }
//    }
//
//    DeliveryDetailsPopup.template = 'DeliveryDetailsPopup';
//
//    Registries.Component.add(DeliveryDetailsPopup);
//
//    return DeliveryDetailsPopup;
//});
//



















//    class DeliveryDetailsPopup extends AbstractAwaitablePopup {
//        constructor() {
//            super(...arguments);
//        }
//
//        getPayload() {
//            return {
//                delivery_country: this.el.querySelector('#delivery_country').value,
//                delivery_type: this.el.querySelector('#delivery_type').value,
//                expected_delivery_date: this.el.querySelector('#expected_delivery_date').value,
//            };
//        }
//    }
//
//    DeliveryDetailsPopup.template = 'DeliveryDetailsPopup';
//
//    Registries.Component.add(DeliveryDetailsPopup);
//
//    return DeliveryDetailsPopup;
//});