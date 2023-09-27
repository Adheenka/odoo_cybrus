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

    # @api.depends('order_line.price_total', 'order_line.product_uom_qty', 'order_line.quantity')
    # def _amount_all(self):
    #     for order in self:
    #         # Call the original _amount_all method using super
    #         super(SaleOrder, order)._amount_all()
    #
    #         # Calculate the total amount including the quantity and product_uom_qty fields
    #         total_with_quantity = order.amount_total
    #
    #         for line in order.order_line:
    #             total_with_quantity += (line.product_uom_qty + line.quantity) * line.price_unit
    #
    #         order.update({
    #             'amount_total': total_with_quantity,
    #         })

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
    quantity = fields.Float(string="Quantity")
    seq = fields.Integer(string='Serial No', compute='_compute_serial_number', readonly=True)
    colour_ids = fields.One2many('colour', 'colour_id', string='Estimations')
    colour_name = fields.Char(string='Colour Name', store=True)

    @api.depends('price_total', 'product_uom_qty', 'quantity')
    def _amount_all(self):

        for order in self:
            # Call the original _amount_all method using super
            super(SaleOrder, order)._amount_all()

            # Calculate the total amount including the quantity and free_item_qty fields
            total_with_quantity = order.amount_total

            for line in order.order_line:
                total_with_quantity += (line.product_uom_qty + line.quantity) * line.price_unit

            order.update({
                'amount_total': total_with_quantity,
            })
    # @api.depends('price_total', 'product_uom_qty', 'quantity')
    # def _compute_amount(self):
    #     for order_line in self:
    #         if order_line.product_uom_qty == 0.0:
    #             order_line.price_total = order_line.price_unit * order_line.quantity
    #         else:
    #             order_line.price_total = order_line.price_unit * order_line.product_uom_qty
    # @api.depends('price_total', 'product_uom_qty', 'quantity')
    # def _compute_amount(self):
    #     for order_line in self:
    #         if order_line.product_uom_qty == 0.0:
    #
    #             order_line.price_total = order_line.price_unit * order_line.quantity
    #         else:
    #
    #             order_line.price_total = order_line.price_unit * order_line.product_uom_qty



    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.product_uom_qty = 0.0

    # @api.depends('quantity','price_unit','tax_id')
    # def compute_amount(self):
    #
    #     for obj in self:
    #         price_before_tax = obj.price_unit * obj.quantity
    #         taxes = obj.tax_id.compute_all(price_before_tax, obj.order_id.currency_id, obj.quantity,
    #                                        product=obj.product_id)
    #         obj.subtotal = taxes['total_included']

    # total = 0
    # for obj in self:
    #     total += obj.price_unit * obj.quantity + obj.tax_id
    # obj.subtotal = total
    def _compute_serial_number(self):
        for line in self:
            no = 0
            line.seq = no
            for i in line.order_id.order_line:
                no += 1
                i.seq = no
