from odoo import fields, models, api

class SaleOrderInherit(models.Model):
    _name = 'sale'
    _description = 'Your Estimation Model'

    sequence = fields.Char(string='Sequence')
    description = fields.Char(string='description')
    customer_name = fields.Many2one('res.partner', string='Customer Name')
    creation_date = fields.Date(string='Creation Date')
    estimation_ids = fields.One2many('estimation', 'sale_order_id', string='Estimations')

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('SaleOrderInherit.sequence') or 'New'
        return super(SaleOrderInherit, self).create(vals)



class EstimationModel(models.Model):
    _name = 'estimation'
    _description = 'Your Estimation Model'

    sequence = fields.Char(string='Serialno')

    amount = fields.Float(string='Estimation Amount')

    # Add any additional fields you need for your estimation
    description = fields.Many2one('description.master', string='Description')
    sale_order_id = fields.Many2one('sale.order', string='Sale Order')

    width = fields.Float(string='Width')
    length = fields.Float(string='Length')
    area = fields.Float(string='Area', compute='_compute_area', store=True)
    quantity = fields.Float(string='Quantity')
    total = fields.Float(string='Total', compute='_compute_total', store=True)

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('EstimationModel.sequence') or 'New'
        return super(EstimationModel, self).create(vals)
    @api.depends('width', 'length', 'quantity')
    def _compute_area(self):
        for estimation in self:
            estimation.area = estimation.width * estimation.length * estimation.quantity

    @api.depends('amount', 'quantity')
    def _compute_total(self):
        for estimation in self:
            estimation.total = estimation.amount * estimation.quantity



class DescriptionMaster(models.Model):
    _name = 'description.master'
    _description = 'Description Master'

    name = fields.Char(string='Description')


# In models.py

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    related_estimation = fields.Many2one('estimation', string='Related Estimation')

# In models.py



    @api.model
    def create(self, vals):
        if vals.get('related_estimation'):
            estimation = self.env['estimation'].browse(vals['related_estimation'])
            if estimation:
                vals.update({
                    'description': estimation.description.id,
                    'width': estimation.width,
                    'length': estimation.length,
                    'area': estimation.area,
                    'quantity': estimation.quantity,
                    'total': estimation.total,
                })
        return super(SaleOrder, self).create(vals)
