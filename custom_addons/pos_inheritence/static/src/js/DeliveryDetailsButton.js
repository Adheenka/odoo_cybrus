odoo.define('pos_inheritence.DeliveryDetailsButton', function (require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const { Gui } = require("point_of_sale.Gui");

    class DeliveryDetailsButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }

        async onClick() {
            // Open the 'DeliveryDetailsPopup' when the button is clicked.
            this.showPopup('DeliveryDetailsPopup', { });
        }
    }

    // Define the template for the button.
    DeliveryDetailsButton.template = 'DeliveryDetailsButton';

    // Add the custom button to the Product Screen.
    ProductScreen.addControlButton({
        component: DeliveryDetailsButton,
        condition: function() {
            // You can add a condition here to control when the button should appear.
            return true;
        },
    });

    // Register the custom button component.
    Registries.Component.add(DeliveryDetailsButton);

    return DeliveryDetailsButton;
});
















//odoo.define('pos_inheritence.RewardButton', function(require) {
//'use strict';
//   const { Gui } = require('point_of_sale.Gui');
//   const PosComponent = require('point_of_sale.PosComponent');
//   const { posbus } = require('point_of_sale.utils');
//   const ProductScreen = require('point_of_sale.ProductScreen');
//   const { useListener } = require('web.custom_hooks');
//   const Registries = require('point_of_sale.Registries');
//   const PaymentScreen = require('point_of_sale.PaymentScreen');
//   const models = require('point_of_sale.models');
//
//    // Define a function to load the required fields for pos.order model
//    function loadPosOrderFields(self) {
//        models.load_fields('pos.order', ['delivery_type', 'expected_delivery_date', 'delivery_country']);
//    }
//
//   class CustomRewardButtons extends PosComponent {
//       constructor() {
//           super(...arguments);
//           useListener('click', this.onClick);
//       }
//       is_available() {
//           const order = this.env.pos.get_order();
//           return order
//       }
//       onClick() {
//
//                Gui.showPopup("TextInputPopup", {
//                       title: this.env._t('Delivery Details'),
//
//
//                         placeholder: this.env._t('Gift card or Discount code'),
////                       list: this.env._t('Welcome to OWL'),
//                   });
//       }
//   }
//   CustomRewardButtons.template = 'CustomRewardButtons';
//
//   ProductScreen.addControlButton({
//       component: CustomRewardButtons,
//       condition: function() {
//           return this.env.pos;
//       },
//   });
//   Registries.Component.add(CustomRewardButtons);
//   return CustomRewardButtons;
//
//
//
//
//


//odoo.define("pos_inheritence.WBSampleButton", function(require){
//"use strict";
//
//    const PosComponent = require("point_of_sale.PosComponent");
//    const ProductScreen = require("point_of_sale.ProductScreen");
//    const Registries = require("point_of_sale.Registries");
//    const { useListener } = require("@web/core/utils/hooks");
//    const core  = require("web.core");
//    var _t = core._t;
//
//    class WBSampleButton extends PosComponent {
//
//        setup(){
//            super.setup();
//            useListener("click", this.wb_sample_button_click);
//        }
//
//        async wb_sample_button_click(){
//
//            var multi_lang = await this.rpc({
//                route:"/pos/rpc/example",
//                params:{},
//            })
//
//
//            console.log("language ---> ", multi_lang);
//
//            var multi_lang_list = [];
//
//            multi_lang.forEach(function(value){
//                   multi_lang_list.push({"id": value.id,
//                   "label":value.name,
//                   "item": value});
//            });
//
//            console.log(multi_lang_list);
//
//            var {confirmed, payload: selectedOption} = await this.showPopup("SelectionPopup", {
//                title: "Active Languages!",
//                list: multi_lang_list
//            })
//
//            console.log(confirmed, selectedOption);
//
//
//            console.log("Hello this is button click event pressed........");
//        }
//
//    }
//
//    WBSampleButton.template = "WBSampleButton";
//    ProductScreen.addControlButton({
//        component: WBSampleButton,
//        position: ["before", "OrderlineCustomerNoteButton"],
//    });
//
//    Registries.Component.add(WBSampleButton);
//
//    return WBSampleButton;
//
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
//
//
//
//
//
//
//
//
//
////odoo.define('pos_delivery_details.ActionpadWidget', function (require) {
////    'use strict';
////
////    const PosComponent = require('point_of_sale.PosComponent');
////    const Registries = require('point_of_sale.Registries');
////    const DeliveryDetailsPopup = require('pos_delivery_details.DeliveryDetailsPopup');
////
////    class ActionpadWidget extends PosComponent {
////        constructor() {
////            super(...arguments);
////        }
////
////        async openDeliveryDetailsPopup() {
////            const { confirmed, payload } = await this.showPopup(DeliveryDetailsPopup, {});
////            if (confirmed) {
////                // Handle the payload (delivery details) here
////                const { deliveryCountry, deliveryType, expectedDeliveryDate } = payload;
////                // You can now save these details to your custom model or perform any other action.
////            }
////        }
////    }
////
////    ActionpadWidget.template = 'ActionpadWidget';
////    ActionpadWidget.defaultProps = {
////        isActionButtonHighlighted: false,
////    }
////
////    Registries.Component.add(ActionpadWidget);
////
////    return ActionpadWidget;
////});
////async onClick() {
////    const selectedOrder = this.env.pos.get_order();
////    if (selectedOrder) {
////        // Show the delivery details popup when the button is clicked
////        this.showPopup('view_delivery_details_popup');
////    }
////}
