/** @odoo-module **/
   import AbstractAwaitablePopup from 'point_of_sale.AbstractAwaitablePopup';
   import Registries from 'point_of_sale.Registries';
   import PosComponent from 'point_of_sale.PosComponent';
   import ControlButtonsMixin from 'point_of_sale.ControlButtonsMixin';
   import NumberBuffer from 'point_of_sale.NumberBuffer';
   import { useListener } from 'web.custom_hooks';
   import { onChangeOrder, useBarcodeReader } from 'point_of_sale.custom_hooks';
   const { useState } = owl.hooks;
   class CouponProductsPopup extends AbstractAwaitablePopup {
    constructor() {
    super(...arguments);
    useListener('click-product', this._clickProduct);
    }
   //To get coupon products category
    get productsToDisplay() {
    return this.env.pos.db.get_product_by_category(this.env.pos.config.category_id[0]);
    }
     get currentOrder() {
           return this.env.pos.get_order();
       }
//      get products details in orderlines when clicking on popup product
     async _clickProduct(event) {
           if (!this.currentOrder) {
               this.env.pos.add_new_order();
           }

           const product = event.detail;
           let price_extra = 0.0;
           let description, packLotLinesToEdit;
           // Add the product after having the extra information.
           this.currentOrder.add_product(product, {
               description: description,
           });
       }
    }
    //Create products popup
   CouponProductsPopup.template = 'CouponProductsPopup';
   CouponProductsPopup.defaultProps = {
       confirmText: 'Ok',
       cancelText: 'Cancel',
       title: 'Coupon Products',
       body: '',
   };
   Registries.Component.add(CouponProductsPopup);
//   return CouponProductsPopup;
   export default  CouponProductsPopup;