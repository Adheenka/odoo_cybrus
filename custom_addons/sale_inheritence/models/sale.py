from odoo import fields, models, api ,_
from odoo.exceptions import ValidationError


class SaleOrderInherit(models.Model):
    _name = 'sale'
    _description = 'Your Estimation Model'
    _rec_name = 'sequence'

    sequence = fields.Char(string='Sequence')
    description = fields.Char(string='description')
    customer_name = fields.Many2one('res.partner', string='Customer Name')
    creation_date = fields.Date(string='Creation Date')
    estimation_ids = fields.One2many('estimation', 'estimations_id', string='Estimations')
    estimation_id = fields.Many2one('estimation', ondelete='cascade')
    estimation_ids = fields.One2many('estimation', 'estimations_id', string='Estimations')

    #job order
    # job_order_ids = fields.One2many('job.order', 'job_order_id', string='job_order')

    # code for  report printing

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('sale')
        return super(SaleOrderInherit, self).create(vals)
    def convert_to_quotation(self):
        val={
            'related_estimation':self.id,
             'partner_id':self.customer_name.id,
             'state':'sale',
             'date_order':self.creation_date,
             'estimation_line_ids':self.estimation_ids,

        }
        self.env['sale.order'].create(val)



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


    @api.depends('estimation_id', 'estimation_id.estimation_ids')
    def _compute_serial_number(self):
        for line in self:
            no = 1
            for l in line.estimation_id.estimation_ids:
                l.seq = no
                no += 1


    # def _compute_serial_number(self):
    #     for line in self:
    #         no = 0
    #         line.seq = no
    #         for i in line.order_id.order_line:
    #             no += 1
    #             i.seq = no


    @api.depends('width', 'length',)
    def _compute_area(self):
        for estimation in self:
            estimation.area = estimation.width * estimation.length

    @api.depends('area', 'quantity')
    def _compute_total(self):
        for estimation in self:
            estimation.total = estimation.area + estimation.quantity


class DescriptionMaster(models.Model):
    _name = 'description'
    _description = 'Description Master'

    name = fields.Char(string='Description')


   # task 8 code













# class SaleOrder(models.Model):
#      _inherit = 'sale.order'
#
#      related_estimation = fields.Many2one('sale', string='Estimation_id', ondelete='cascade')
#
#      estimation_line_ids = fields.One2many('estimation', 'estimation_i', string='Estimations')





    # # Add any additional fields you need for your estimation
    # description = fields.Many2one('description', string='Description')
    # # sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    #
    # width = fields.Float(string='Width')
    # length = fields.Float(string='Length')
    # area = fields.Float(string='Area')
    # quantity = fields.Float(string='Quantity')
    # total = fields.Float(string='Total')


#
# # In models.py
#
#
#
#     @api.model
#     def create(self, vals):
#         if vals.get('related_estimation'):
#             estimation = self.env['estimation'].browse(vals['related_estimation'])
#             if estimation:
#                 vals.update({
#                     'description': estimation.description.id,
#                     'width': estimation.width,
#                     'length': estimation.length,
#                     'area': estimation.area,
#                     'quantity': estimation.quantity,
#                     'total': estimation.total,
#                 })
#         return super(SaleOrder, self).create(vals)
