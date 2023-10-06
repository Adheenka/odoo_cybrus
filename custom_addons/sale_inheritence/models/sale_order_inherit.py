from odoo import fields, models, api ,_
# from odoo.addons.sale.models.sale_order import SaleOrder


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    related_estimation = fields.Many2one('sale', string='Estimation_id',ondelete='cascade')
    opportunity_id= fields.Char(string="opportunity_id")
    estimation_line_ids = fields.One2many('estimation','estimation_i', string='Estimations')

    sale_order_line_ids = fields.One2many('sale.order.line', 'sale_order_id', string='sale_job_order')
    sale_order_id = fields.Many2one('sale.order.line', ondelete='cascade')
    job_order_ids = fields.One2many('job.order', 'job_order_id', string='sale_job_order')

    estimation_ids = fields.One2many('estimation', 'estimation_id', string='Estimations')
    estimation_id = fields.Many2one('estimation', string='Estimations')
    # job order
    job_order_ids = fields.One2many('job.order', 'job_order_id', string='job_order')
    @api.depends('order_line.price_total', 'order_line.product_uom_qty', 'order_line.quantity')
    def _amount_all(self):
        for order in self:
            # Call the original _amount_all method using super
            super(SaleOrder, order)._amount_all()


            total_with_quantity = order.amount_total

            for line in order.order_line:
                total_with_quantity += line.price_total

            order.update({
                'amount_total': total_with_quantity,
            })


    # tax included code  without any single error
    # def action_open_job_order(self):
    #     # Ensure the sale order is confirmed
    #     super(SaleOrder, self).action_confirm()
    #
    #     # Create a new job order record
    #     job_order = self.env['job.order'].create({
    #         'customer_name': self.partner_id.id,
    #         'date': self.date_order,
    #         'job_no': self.name,
    #     })
    #
    #     job_order_lines = [(0, 0, {
    #         'order_id': self.id,
    #         'product_id': line.product_id.id,
    #         'quantity': line.product_uom_qty,
    #         'price_total': line.price_total,
    #         'colour_name': line.seq,
    #         'job_no': line.seq,
    #         'tax_amount': line.tax_id.compute_all(
    #             line.price_unit * (1 - (line.discount or 0.0) / 100.0),
    #             self.currency_id,
    #             line.product_uom_qty,
    #             line.product_id,
    #             self.partner_shipping_id)['total_included'],
    #     }) for line in self.order_line]
    #
    #     # Set the job_order_lines on the job_order record
    #     job_order.sale_order_line_ids = job_order_lines
    #
    #
    #     job_order.estimation_line_ids = [(4, estimation.id) for estimation in self.estimation_line_ids]
    #
    #     return {
    #         'name': 'Job Order',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'job.order',
    #         'res_id': job_order.id,
    #         'type': 'ir.actions.act_window',
    #         'target': 'self',
    #     }

    def action_open_job_order(self):
        super(SaleOrder, self).action_confirm()

        for line in self.order_line:
            line.colour_name = line.seq
            line.job_no = line.seq

        job_order = self.env['job.order'].create({
            'customer_name': self.partner_id.id,
            'date': self.date_order,
            'job_no': self.name,
            'sale_order_line_ids':self.order_line,  # Assign the existing order lines
            'estimation_line_ids': [(4, estimation.id) for estimation in self.estimation_line_ids],
        })

        return {
            'name': 'Job Order',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'job.order',
            'res_id': job_order.id,
            'type': 'ir.actions.act_window',
            'target': 'self',
        }

    # def action_open_job_order(self):
    #
    #     super(SaleOrder, self).action_confirm()
    #
    #     # Create a new job order record
    #     job_order = self.env['job.order'].create({
    #         'customer_name': self.partner_id.id,
    #
    #         'date': self.date_order,
    #         'job_no': self.name,
    #
    #
    #         'sale_order_line_ids':  self.order_line,
    #         'estimation_line_ids':self.estimation_line_ids,
    #     })
    #
    #     return {
    #         'name': 'Job Order',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'job.order',
    #         'res_id': job_order.id,
    #         'type': 'ir.actions.act_window',
    #         'target': 'self',
    #     }


    #

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.product_uom_qty = 0

class JobOrder(models.Model):
    _name = 'job.order'
    _description = 'Job Order'




    #for colour feching

    #print paf task code
    related_estimation = fields.Many2one('sale.order', string='Estimation_id', ondelete='cascade')

    estimation_line_ids = fields.One2many('estimation', 'esti_i', string='Estimations')




    sale_order_line_ids = fields.One2many('sale.order.line', 'sale_order_id', string='sale_job_order')

    related_estimation = fields.Many2one('sale', string='Estimation_id', ondelete='cascade')


    sale_order_id = fields.Many2one('sale.order', ondelete='cascade')
    sale_id =fields.Char(string="sale_id")
    job_no = fields.Char(string='Quatation_id')

    customer_name = fields.Many2one('res.partner', string='Customer Name')
    sale_order_line_ids = fields.One2many('sale.order.line', 'job_order_id', string='Job Order Lines')
    date = fields.Date(string='Date')
    product_id = fields.Many2one('product.product', string="Product_id")
    job_order_id = fields.Many2one('sale.order.line', string='job order')
    total = fields.Float(
        string='Total',
        compute='_compute_total',
        store=True,
    )
    total_quantity =fields.Float(string="Total QTY",compute='_compute_qty',store=True)

    @api.depends('sale_order_line_ids.quantity')
    def _compute_qty(self):
        for job_order in self:
            total_quantity = sum(job_order.sale_order_line_ids.mapped('quantity'))
            job_order.total_quantity = total_quantity

    @api.depends('sale_order_line_ids.price_total')
    def _compute_total(self):
        for job_order in self:
            total = sum(job_order.sale_order_line_ids.mapped('price_total'))
            job_order.total = total

    total = fields.Float(
        string='Total',
        compute='_compute_total',
        store=True,
    )
    def print_pdf_report(self):
        return self.env.ref('sale_inheritence.report_job_order_card').report_action(self)


class ColourMaster(models.Model):
    _name = 'colour'
    _description = 'Colour Master'

    name = fields.Char(string='Colour Name')
    job_number = fields.Char(string='Job Number')
    colour_widget = fields.Integer(string="color")
    colour_id = fields.Many2one('sale.order.line')
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    job_no = fields.Many2one('colour', string="Colour Name")
    job_order_id = fields.Many2one('job.order', string='Job Order')

    quantity = fields.Float(string="Quantity")
    seq = fields.Integer(string='Serial No', compute='_compute_serial_number', readonly=True)
    colour_ids = fields.One2many('colour', 'colour_id', string='Estimations')
    colour_name = fields.Char(string='job_no', store=True)


    sale_order_id = fields.Many2one('sale.order', string='Job Order')












    job_order_ids = fields.One2many('job.order', 'job_order_id', string='sale_job_order')

    price_total = fields.Float(string="Product Price")
    tax_amount = fields.Float(string="Total")







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
