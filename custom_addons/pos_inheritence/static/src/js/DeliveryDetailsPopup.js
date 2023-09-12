odoo.define("point_of_sale.DeliveryDetailsPopup", function (require) {
    "use strict";
    const { useState, useRef, onPatched, useComponent} = owl.hooks;
    const AbstractAwaitablePopup = require("point_of_sale.AbstractAwaitablePopup");
    const PosComponent = require("point_of_sale.PosComponent");
    const ProductScreen = require("point_of_sale.ProductScreen");
    const { useListener } = require("web.custom_hooks");
    const Registries = require("point_of_sale.Registries");

    class DeliveryDetailsPopup extends AbstractAwaitablePopup {
        constructor() {
            super(...arguments);
        }

        getPayload() {
            return {
                delivery_country: this.el.querySelector('#delivery_country').value,
                delivery_type: this.el.querySelector('#delivery_type').value,
                expected_delivery_date: this.el.querySelector('#expected_delivery_date').value,
            };
        }
    }

    DeliveryDetailsPopup.template = 'DeliveryDetailsPopup';

    Registries.Component.add(DeliveryDetailsPopup);

    return DeliveryDetailsPopup;
});