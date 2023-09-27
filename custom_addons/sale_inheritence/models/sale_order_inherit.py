from odoo import fields, models, api ,_
# from odoo.addons.sale.models.sale_order import SaleOrder


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    related_estimation = fields.Many2one('sale', string='Estimation_id',ondelete='cascade')

    estimation_line_ids = fields.One2many('estimation','estimation_i', string='Estimations')


    def action_open_job_order(self):
        return {
           'type': 'ir.actions.act_window',

            'res_model': 'job.order',

            'view_mode': 'form',

            'view_id': self.env.ref('sale_inheritence.view_job_order_form').id,

        }


class JobOrder(models.Model):
    _name = 'job.order'
    _description = 'Job Order'

    job_no = fields.Char(string='Job No')
    customer_name = fields.Many2one('res.partner', string='Customer Name')
    sale_order_line_ids = fields.One2many('sale.order.line', 'job_order_id', string='Job Order Lines')
    date = fields.Date(string='Date')
    product_id = fields.Many2one('product.product', string="Product_id")
    # job_order_id = fields.Many2one('sale.order.line', string='estimation')
    colour_name = fields.Char(string='Colour Name', store=True)

    # @api.depends('sale_order_line_ids.job_no.colour_widget.name')
    # def _compute_colour_name(self):
    #     for job_order in self:
    #         if job_order.sale_order_line_ids and job_order.sale_order_line_ids[0].job_no.colour_widget:
    #             job_order.colour_name = job_order.sale_order_line_ids[0].job_no.colour_widget.name
    #         else:
    #             job_order.colour_name = ''
class ColourMaster(models.Model):
    _name = 'colour'
    _description = 'Colour Master'

    name = fields.Char(string='Colour Name')
    job_number = fields.Char(string='Job Number')
    colour_widget = fields.Integer(string="color")
    colour_id = fields.Many2one('sale.order.line')
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    #
    job_no = fields.Many2one('colour',string="Job_No")
    job_order_id = fields.Many2one('job.order', string='Job Order')
    quantity = fields.Float(string="Quantity",compute='_compute_remaining_qty')
    seq = fields.Integer(string='Serial No', compute='_compute_serial_number', readonly=True)
    colour_ids = fields.One2many('colour', 'colour_id', string='Estimations')
    colour_name = fields.Char(string='Colour Name', store=True)
    @api.depends('product_uom_qty','price_unit')
    def _compute_remaining_qty(self):
        for line in self:
            line.quantity = line.product_uom_qty * line.price_unit

    def _compute_serial_number(self):
        for line in self:
            no = 0
            line.seq = no
            for i in line.order_id.order_line:
                no += 1
                i.seq = no
