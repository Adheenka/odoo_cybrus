from odoo import fields, models, api ,_
from odoo.exceptions import ValidationError


class SaleOrderInherit(models.Model):
    _name = 'sale'
    _description = 'Your Estimation Model'
    _rec_name = 'sequence'

    sequence = fields.Char(string='Sequence', tracking=True, copy=False, readonly=True)
    description = fields.Char(string='description')
    customer_name = fields.Many2one('res.partner', string='Customer Name')
    creation_date = fields.Date(string='Creation Date')
    estimation_ids = fields.One2many('estimation', 'estimations_id', string='Estimations')
    estimation_id = fields.Many2one('estimation', ondelete='cascade')
    estimation_ids = fields.One2many('estimation', 'estimations_id', string='Estimations')


    total_area_less_than_0_5 = fields.Float(
        string='Total Area Less Than 0.5',
        compute='_compute_total_area_less_than_0_5',
        store=True
    )

    total_quantity_less_than_0_5 = fields.Float(
        string='Total Quantity for Total Area Less Than 0.5',
        compute='_compute_total_area_less_than_0_5',
        store=True
    )

    total_area_between_0_3_and_0_5 = fields.Float(
        string='Total Area Between 0.3 and 0.5',
        compute='_compute_total_area_between_0_3_and_0_5',
        store=True
    )

    total_quantity_between_0_3_and_0_5 = fields.Float(
        string='Total Quantity for Total Area Between 0.3 and 0.5',
        compute='_compute_total_area_between_0_3_and_0_5',
        store=True
    )

    total_area_more_than_0_5 = fields.Float(
        string='Total Area More Than 0.5',
        compute='_compute_total_area_more_than_0_5',
        store=True
    )

    total_quantity_more_than_0_5 = fields.Float(
        string='Total Quantity for Total Area More Than 0.5',
        compute='_compute_total_area_more_than_0_5',
        store=True
    )

    total_area_overall = fields.Float(
        string='Total Area (Overall)',
        compute='_compute_total_area_overall',
        store=True
    )

    total_quantity_overall = fields.Float(
        string='Total Quantity (Overall)',
        compute='_compute_total_quantity_overall',
        store=True
    )

    # ... other fields and methods ...

    @api.depends('estimation_ids.area', 'estimation_ids.quantity')
    def _compute_total_area_less_than_0_5(self):
        for order in self:
            total_area = sum(est.area for est in order.estimation_ids if est.area < 0.5)
            total_quantity = sum(est.quantity for est in order.estimation_ids if est.area < 0.5)
            order.total_area_less_than_0_5 = total_area
            order.total_quantity_less_than_0_5 = total_quantity

    @api.depends('estimation_ids.area', 'estimation_ids.quantity')
    def _compute_total_area_between_0_3_and_0_5(self):
        for order in self:
            total_area = sum(est.area for est in order.estimation_ids if 0.3 <= est.area <= 0.5)
            total_quantity = sum(est.quantity for est in order.estimation_ids if 0.3 <= est.area <= 0.5)
            order.total_area_between_0_3_and_0_5 = total_area
            order.total_quantity_between_0_3_and_0_5 = total_quantity

    @api.depends('estimation_ids.area', 'estimation_ids.quantity')
    def _compute_total_area_more_than_0_5(self):
        for order in self:
            total_area = sum(est.area for est in order.estimation_ids if est.area > 0.5)
            total_quantity = sum(est.quantity for est in order.estimation_ids if est.area > 0.5)
            order.total_area_more_than_0_5 = total_area
            order.total_quantity_more_than_0_5 = total_quantity

    @api.depends('estimation_ids.area', 'estimation_ids.quantity')
    def _compute_total_area_overall(self):
        for order in self:
            total_area = sum(est.area for est in order.estimation_ids)
            total_quantity = sum(est.quantity for est in order.estimation_ids)
            order.total_area_overall = total_area
            order.total_quantity_overall = total_quantity



    #job order
    # job_order_ids = fields.One2many('job.order', 'job_order_id', string='job_order')

    # code for  report printing

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('sale.sequence') or 'New'
        return super(SaleOrderInherit, self).create(vals)
    def convert_to_quotation(self):
        val={
            'related_estimation':self.id,
             'partner_id':self.customer_name.id,
             'state':'draft',
             'date_order':self.creation_date,
             'estimation_line_ids':self.estimation_ids,

              # Aestimation calculation code

            'total_area_less_than_0_5': self.total_area_less_than_0_5,
            'total_quantity_less_than_0_5': self.total_quantity_less_than_0_5,
            'total_area_between_0_3_and_0_5': self.total_area_between_0_3_and_0_5,
            'total_quantity_between_0_3_and_0_5': self.total_quantity_between_0_3_and_0_5,
            'total_area_more_than_0_5': self.total_area_more_than_0_5,
            'total_quantity_more_than_0_5': self.total_quantity_more_than_0_5,
            'total_area_overall': self.total_area_overall,
            'total_quantity_overall': self.total_quantity_overall,

        }
        new_quotation = self.env['sale.order'].create(val)
        # self.env['sale.order'].create(val)
        return {
            'name': 'quatation Order',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order',
            'res_id': new_quotation.id,
            'type': 'ir.actions.act_window',
            'target': 'self',
        }


class EstimationModel(models.Model):
    _name = 'estimation'
    _description = 'Your Estimation Model'
    # _rec_name = 'seq'



    estimations_id = fields.Many2one('sale', string='estimation')
    estimation_i = fields.Many2one('sale.order', string='estimation')
    esti_i = fields.Many2one('job.order', string='estimation')


    estimation_id = fields.Many2one('sale.order', string='estimation')


    amount = fields.Float(string='Estimation Amount')


    description = fields.Many2one('description', string='Description')
    # sale_order_id = fields.Many2one('sale.order', string='Sale Order')

    width = fields.Float(string='Width')
    length = fields.Float(string='Length')
    area = fields.Float(string='Area', compute='_compute_area', store=True)
    quantity = fields.Float(string='Quantity')
    total = fields.Float(string='Total', compute='_compute_total', store=True)

    seq = fields.Integer(string='Serial No', compute='_compute_serial_number', store=True)



    cus_ref =fields.Float(string='CUS REF' )


    job_number = fields.Char(string='Job Number')

    color = fields.Char(string='Color')

    job_number_id = fields.Many2one('colour', string='Job Number (Reference)')



    @api.onchange('job_number')
    def _onchange_job_number(self):

        if self.job_number:

            colour = self.env['colour'].search([('job_number', '=', self.job_number)], limit=1)

            if colour:
                self.job_number_id = colour

                self.color = colour.name
    @api.depends('estimations_id')
    def _compute_serial_number(self):
        for estimation in self:
            no = 0
            estimation.seq = no
            for line in estimation.estimations_id.estimation_ids:
                no += 1
                line.seq = no

  #new area calculation
    @api.depends('width', 'length', )
    def _compute_area(self):
        for estimation in self:
            estimation.area = estimation.width * estimation.length / 10000

    # old area calculation

    # @api.depends('width', 'length',)
    # def _compute_area(self):
    #     for estimation in self:
    #         estimation.area = estimation.width * estimation.length

    @api.depends('area', 'quantity')
    def _compute_total(self):
        for estimation in self:
            estimation.total = estimation.area + estimation.quantity


class DescriptionMaster(models.Model):
    _name = 'description'
    _description = 'Description Master'

    name = fields.Char(string='Description')


