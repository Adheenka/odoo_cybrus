from odoo import fields, models, api ,_
# from odoo.addons.sale.models.sale_order import SaleOrder


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    related_estimation = fields.Many2one('sale', string='Estimation_id',ondelete='cascade')

    estimation_line_ids = fields.One2many('estimation','estimation_i', string='Estimations')
    job_order_line_ids = fields.One2many('sale.order.line','job_order_id', string='sale_job_order')

    @api.depends('order_line.price_total', 'order_line.product_uom_qty', 'order_line.quantity')
    def _amount_all(self):
        for order in self:
            # Call the original _amount_all method using super
            super(SaleOrder, order)._amount_all()

            # Calculate the total amount including the quantity and product_uom_qty fields
            total_with_quantity = order.amount_total

            for line in order.order_line:
                total_with_quantity += line.price_total

            order.update({
                'amount_total': total_with_quantity,
            })

    def action_open_job_order(self):
        job_order_values = {
            'sale_id': self.id,  # Add a reference to the sale order
            'job_no': self.name,  # Set the job number as needed
            'customer_name': self.partner_id.id,
            'date': self.date_order,
        }

        job_order_lines = []

        for order_line in self.order_line:
            job_order_lines.append((0, 0, {
                'order_id': self.id,  # Set the reference to the sale order
                'product_id': order_line.product_id.id,
                'quantity': order_line.product_uom_qty,
                'price_unit': order_line.price_unit,
            }))

        job_order_values['sale_order_line_ids'] = job_order_lines

        job_order = self.env['job.order'].create(job_order_values)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'job.order',
            'view_mode': 'form',
            'res_id': job_order.id,
            'view_id': self.env.ref('sale_inheritence.view_job_order_form').id,
        }
    # def action_open_job_order(self):
    #
    #     return {
    #        'type': 'ir.actions.act_window',
    #
    #         'res_model': 'job.order',
    #
    #         'view_mode': 'form',
    #
    #         'view_id': self.env.ref('sale_inheritence.view_job_order_form').id,
    #
    #     }

    # @api.onchange('product_id')
    # def _onchange_product_id(self):
    #     self.product_uom_qty = 0
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.product_uom_qty = 0

class JobOrder(models.Model):
    _name = 'job.order'
    _description = 'Job Order'


    sale_id =fields.Char(string="sale_id")
    job_no = fields.Char(string='Job No')
    customer_name = fields.Many2one('res.partner', string='Customer Name')
    sale_order_line_ids = fields.One2many('sale.order.line', 'job_order_id', string='Job Order Lines')
    date = fields.Date(string='Date')
    product_id = fields.Many2one('product.product', string="Product_id")
    # job_order_id = fields.Many2one('sale.order.line', string='estimation')
    colour_name = fields.Char(string='Colour Name', store=True)



class ColourMaster(models.Model):
    _name = 'colour'
    _description = 'Colour Master'

    name = fields.Char(string='Colour Name')
    job_number = fields.Char(string='Job Number')
    colour_widget = fields.Integer(string="color")
    colour_id = fields.Many2one('sale.order.line')
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    job_no = fields.Many2one('colour',string="Job_No")
    job_order_id = fields.Many2one('job.order', string='Job Order')
    quantity = fields.Float(string="Quantity")
    seq = fields.Integer(string='Serial No', compute='_compute_serial_number', readonly=True)
    colour_ids = fields.One2many('colour', 'colour_id', string='Estimations')
    colour_name = fields.Char(string='Colour Name', store=True)






    @api.depends('price_unit', 'product_uom_qty', 'quantity', 'tax_id')
    def _compute_amount(self):
        for order_line in self:
            # Calculate taxes for quantity
            quantity_taxes = order_line.tax_id.compute_all(
                order_line.price_unit * (1 - (order_line.discount or 0.0) / 100.0),
                order_line.order_id.currency_id,
                order_line.quantity,
                order_line.product_id,
                order_line.order_id.partner_shipping_id
            )
            # Calculate taxes for product_uom_qty
            uom_quantity_taxes = order_line.tax_id.compute_all(
                order_line.price_unit * (1 - (order_line.discount or 0.0) / 100.0),
                order_line.order_id.currency_id,
                order_line.product_uom_qty,
                order_line.product_id,
                order_line.order_id.partner_shipping_id
            )

            # Calculate the total amount including taxes for both quantity and product_uom_qty
            total_with_quantity_and_tax = (
                quantity_taxes['total_included'] if order_line.product_uom_qty == 0.0 else uom_quantity_taxes[
                    'total_included'])

            # Update price_total with tax included
            order_line.price_total = total_with_quantity_and_tax


    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.product_uom_qty = 0




    def _compute_serial_number(self):
        for line in self:
            no = 0
            line.seq = no
            for i in line.order_id.order_line:
                no += 1
                i.seq = no
