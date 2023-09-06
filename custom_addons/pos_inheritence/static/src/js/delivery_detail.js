//odoo.define('custom_point_of_sale.ActionpadWidgetExtension', function (require) {
//    'use strict';
//
//    const { ActionpadWidget } = require('point_of_sale.ActionpadWidget');
//    const { PopupWidget } = require('point_of_sale.popups');
//
//    ActionpadWidget.include({
//        renderElement() {
//            this._super(...arguments);
//
//            // Create and append the "Delivery Details" button
//            const deliveryDetailsButton = document.createElement('button');
//            deliveryDetailsButton.classList.add('button', 'set-partner', 'delivery-details-button');
//            deliveryDetailsButton.innerHTML = '<span>Delivery Details</span>';
//            deliveryDetailsButton.addEventListener('click', () => this.openDeliveryDetailsPopup());
//
//            const actionpadDiv = this.el.querySelector('.actionpad');
//            if (actionpadDiv) {
//                actionpadDiv.appendChild(deliveryDetailsButton);
//            }
//        },
//
//        openDeliveryDetailsPopup() {
//            const self = this;
//
//            // Create a custom pop-up widget for delivery details
//            const DeliveryDetailsPopup = PopupWidget.extend({
//                template: 'delivery_details_popup_template', // Replace with your actual template name
//                events: {
//                    'click .save-delivery-details': 'saveDeliveryDetails',
//                    'click .cancel-delivery-details': 'cancelDeliveryDetails',
//                },
//
//                saveDeliveryDetails() {
//                    // Handle the save logic here
//                    // Retrieve values from the popup fields
//                    const deliveryCountry = this.$('.delivery-country').val();
//                    const deliveryType = this.$('.delivery-type').val();
//                    const expectedDeliveryDate = this.$('.expected-delivery-date').val();
//
//                    // Perform actions like saving to the server, updating the POS order, etc.
//
//                    self.closePopup();
//                },
//
//                cancelDeliveryDetails() {
//                    self.closePopup();
//                },
//            });
//
//            const popup = new DeliveryDetailsPopup(this, {});
//            popup.appendTo(this.$el);
//        },
//
//        closePopup() {
//            this.$('.popup-widget').remove();
//        },
//    });
//
//    return ActionpadWidget;
//});


//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
////odoo.define('pos_inheritence.custom_actionpad_widget', function (require) {
////    'use strict';
////
////    const { Gui } = require('point_of_sale.Gui');
////    const ActionpadWidget = require('point_of_sale.ActionpadWidget');
////
////    ActionpadWidget.include({
////        renderButtons() {
////            this._super(...arguments);
////            this.$('.delivery-details-button').click(() => this.openDeliveryDetailsPopup());
////        },
////
////        openDeliveryDetailsPopup() {
////            const self = this;
////            const { Widget } = require('point_of_sale.widgets');
////            const PopupWidget = Widget.extend({
////                template: 'YourTemplateName',
////                events: {
////                    'click .confirm-delivery-details': 'confirmDeliveryDetails',
////                    'click .cancel-delivery-details': 'cancelDeliveryDetails',
////                },
////
////                confirmDeliveryDetails() {
////                    // Handle the confirmation logic here
////                    // Get the values from the popup fields
////                    const deliveryCountryId = this.$('.delivery-country').val();
////                    const deliveryType = this.$('.delivery-type').val();
////                    const expectedDeliveryDate = this.$('.expected-delivery-date').val();
////
////                    // You can save these values or perform any required actions
////                    // e.g., save to the server, update the POS order, etc.
////
////                    self.closePopup();
////                },
////
////                cancelDeliveryDetails() {
////                    self.closePopup();
////                },
////            });
////
////            const popup = new PopupWidget(this, {});
////            popup.appendTo(this.$el);
////        },
////
////        closePopup() {
////            this.$('.popup-widget').remove();
////        },
////    });
////});
