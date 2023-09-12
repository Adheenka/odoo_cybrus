from datetime import datetime
from odoo import models, fields, api

# class PosOrder(models.Model):
#     _inherit = 'pos.order'
#
#
#     @api.model
#     def payment_fields(self, order, ui_paymentline):
#         res = super(PosOrder, self).payment_fields(order, ui_paymentline)
#
#         c_date = datetime.datetime.strptime(ui_paymentline['cheque_date'],'%Y-%m-%d')if len(ui_paymentline['cheque_date'])> 0 else
#         res['cheque_date'] = c_date
#         res['cheque_no'] = ui_paymentline.get('cheque_no')
#
#         return res
from datetime import datetime
from odoo import models, fields, api


# class PosOrder(models.Model):
#     _inherit = 'pos.order'
#
#     @api.model
#     def payment_fields(self, order, ui_paymentline):
#         res = super(PosOrder, self).payment_fields(order, ui_paymentline)
#
#         if ui_paymentline.get('cheque_date') and len(ui_paymentline['cheque_date']) > 0:
#             c_date = datetime.strptime(ui_paymentline['cheque_date'], '%Y-%m-%d')
#             res['cheque_date'] = c_date
#         else:
#             res['cheque_date'] = False
#
#         res['cheque_no'] = ui_paymentline.get('cheque_no')
#
#         return res

class PosOrder(models.Model):
    _inherit = 'pos.order'

    input_field_value = fields.Char(string='Input Field Value')

    @api.model
    def _order_fields(self, ui_order):
        res = super(PosOrder, self)._order_fields(ui_order)
        res['input_field_value'] = ui_order['field_input_value'] if ui_order['field_input_value'] else False
        return res