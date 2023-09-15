odoo.define("point_of_sale.DeliveryDetailsPopup", function (require) {
    "use strict";
    const { useState, useRef, onPatched, useComponent} = owl.hooks;
    const AbstractAwaitablePopup = require("point_of_sale.AbstractAwaitablePopup");
    const PosComponent = require("point_of_sale.PosComponent");
    const ProductScreen = require("point_of_sale.ProductScreen");
    const { useListener } = require("web.custom_hooks");
    const Registries = require("point_of_sale.Registries");

//    class DeliveryDetailsPopup extends AbstractAwaitablePopup {
//        constructor() {
//            super(...arguments);
//            this.state = useState({ inputValue: this.props.startingValue });
//            this.inputCountry = useRef('inputCountry');
//            this.inputDeliveryType = useRef('inputDeliveryType');
//            this.inputDeliveryDate = useRef('inputDeliveryDate');
//            this.inputDatePicker = null;
//        }
//
//        mounted() {
//            this.inputCountry.el.focus();
//            this.initializeDatePicker();
//        }
//
//        async confirm() {
//            const payload = {
//                delivery_country: this.state.delivery_country,
//                delivery_type: this.state.delivery_type,
//                expected_delivery_date: this.state.expected_delivery_date,
//            };
//            this.trigger('delivery-details-confirmed', payload);
//            this.trigger('close-popup');
//        }
//
//        initializeDatePicker() {
//            var self = this;
//            this.inputDatePicker = new Pikaday({
//                field: this.inputDeliveryDate.el,
//            });
//        }
//    }
//
//    DeliveryDetailsPopup.template = 'DeliveryDetailsPopup';
//
//    Registries.Component.add(DeliveryDetailsPopup);
//
//    return DeliveryDetailsPopup;
//});

     class DeliveryDetailsPopup extends AbstractAwaitablePopup {
        constructor() {
            super(...arguments);
            this.state = {
                delivery_country_id: null,
                delivery_country_name: "",
            };
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

        getPayload() {
            return {
                delivery_country_id: this.state.delivery_country_id,
                delivery_country_name: this.state.delivery_country_name,
                delivery_type: this.el.querySelector("#delivery_type").value,
                expected_delivery_date: this.el.querySelector("#expected_delivery_date").value,
            };
        }
    }

    DeliveryDetailsPopup.template = "DeliveryDetailsPopup";

    Registries.Component.add(DeliveryDetailsPopup);

    return DeliveryDetailsPopup;
});










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