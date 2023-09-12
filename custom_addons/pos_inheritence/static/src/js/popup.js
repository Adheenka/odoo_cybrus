//odoo.define('pos_inheritence.popup', function (require) {
//    'use strict';
//
//    const { useState, useRef } = owl.hooks;
//    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
//    const Registries = require('point_of_sale.Registries');
//
//    class MyPopup extends AbstractAwaitablePopup {
//        constructor() {
//            super(...arguments);
//            this.state = useState({ c_dt:this.props.ch_date, c_no:this.props.ch_no});
//        }
//
//        getPayload() {
//            return this.state;
//        }
//    }
//
//    MyPopup.template = 'MyPopup';
//
//    MyPopup.defaultProps = {
//        confirmText: 'Confirm', // Text for the Confirm button
//        cancelText: 'Cancel',   // Text for the Cancel button
//        title: 'Enter Cheque Details',
//        body: '',
//        startingValue: '',// Title for the popup
//    };
//
//    Registries.Component.add(MyPopup);
//
//    return MyPopup;
//});





















//odoo.define('pos_inheritence.popup', function (require) {
//    'use strict';
//
//    const { useState } = owl.hooks;
//    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
//    const Registries = require('point_of_sale.Registries');
//
//    class MyPopup extends AbstractAwaitablePopup {
//        constructor() {
//            super(...arguments);
//            this.state = useState({ c_dt: this.props.ch_date, c_no: this.props.ch_no });
//        }
//
//        getPayload() {
//            return this.state;
//        }
//    }
//
//    MyPopup.template = 'MyPopup';
//
//    MyPopup.defaultProps = {
//        confirmText: 'Confirm', // Text for the Confirm button
//        cancelText: 'Cancel',   // Text for the Cancel button
//        title: 'Enter Cheque Details',
//        body: '',
//        startingValue: '',      // Title for the popup
//    };
//
//    Registries.Component.add(MyPopup);
//
//    return MyPopup;
//});
