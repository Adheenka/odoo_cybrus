from odoo import fields, models, api
class SaleOrder(models.Model):
    _inherit = 'sale.order'


    related_estimation = fields.Many2one('sale', string='Estimation_id',ondelete='cascade')

    estimation_line_ids = fields.One2many('estimation','estimation_i', string='Estimations')


class JobOrder(models.Model):
    _name = 'job.order'
    _description = 'Job Order'

    job_no = fields.Char(string='Job No')
    customer_name = fields.Many2one('res.partner', string='Customer Name')
    job_order_lines = fields.One2many('sale.order.line', 'job_order_id', string='Job Order Lines')
    job_order_id = fields.Many2one('sale.order.line', string='estimation')

    # name = fields.Char(string='Job Order No.', required=True, copy=False, readonly=True,
    #                    default=lambda self: _('New'), index=True)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    #
    # job_order_id = fields.Many2one('job.order', string='Job Order')
    quantity = fields.Float(string="Quantity")
    seq = fields.Integer(string='Serial No', compute='_compute_serial_number', readonly=True)


    @api.depends('product_id')
    def _compute_serial_number(self):
        for line in self:
            no = 1  # Initialize the serial number to 1
            for l in line.product_id:
                l.seq = no
                no += 1
    # def action_create_job_order(self):
    #
    #     job_order_obj = self.env['job.order']
    #     for order in self:
    #         job_order = job_order_obj.create({
    #             # 'job_no': 'Your Job Number',
    #             # # 'customer_id': order.partner_id.id,  # Link the customer to the job order
    #             # 'order_date': fields.Date.today(),  # Set the order date as today
    #         })
    #     return {
    #         'name': 'Job Order',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'job.order',
    #         'type': 'ir.actions.act_window',
    #         'target': 'current',
    #         'res_id': job_order.id,
    #     }