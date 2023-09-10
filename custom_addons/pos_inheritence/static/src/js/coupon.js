/** @odoo-module **/
    import rpc from 'web.rpc';
    import { Gui } from 'point_of_sale.Gui';
    import PosComponent from 'point_of_sale.PosComponent';
    import AbstractAwaitablePopup from 'point_of_sale.AbstractAwaitablePopup';
    import Registries from 'point_of_sale.Registries';
    import ProductItem from 'point_of_sale.ProductItem';
    import ProductScreen from 'point_of_sale.ProductScreen';
class CouponButton extends PosComponent{
      //Generate popup
      display_popup_products() {
      var core = require('web.core');
      var _t = core._t;
       Gui.showPopup("CouponProductsPopup", {
       title : _t("Coupon Products"),
       confirmText: _t("Exit")
          });
      }
  }
  //Add coupon button and set visibility
      ProductScreen.addControlButton({
      component: CouponButton,
      condition: function() {
          return this.env.pos.config.coupon_category;
      },
  });
  Registries.Component.add(CouponButton);
  export default CouponButton;