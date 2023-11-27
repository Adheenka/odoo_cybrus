from odoo import fields, models, api ,_



# class PurchaseRequest(models.Model):
#     _name = 'purchase.request'
#     _description = 'Purchase Request'
#
#     name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default=lambda self: ('New'))
#     requested_by = fields.Many2one('res.users', string='Requested By', default=lambda self: self.env.user, required=True)
#     requisition_lines = fields.One2many('purchase.request.line', 'requisition_id', string='Requisition Lines')
#     material_requisition_id = fields.Many2one('material.requisition', string='Material Requisition')
#
#     @api.model
#     def create(self, vals):
#         if vals.get('name', 'New') == 'New':
#             vals['name'] = self.env['ir.sequence'].next_by_code('purchase.request.sequence') or '/'
#         return super(PurchaseRequest, self).create(vals)

#
# class PurchaseRequestLine(models.Model):
#     _name = 'purchase.request.line'
#     _description = 'Purchase Request Line'
#
#     requisition_id = fields.Many2one('purchase.request', string='Purchase Request', ondelete='cascade')
#     product_id = fields.Many2one('product.product', string='Product', required=True)
#     vendor_id = fields.Many2one('res.partner', string='Vendor')
#     description = fields.Text(string='Description')
#     quantity = fields.Float(string='Quantity', default=1.0)
#     uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
#
    # @api.onchange('product_id')
    # def onchange_product_id(self):
    #     if self.product_id:
    #         vendor_infos = self.product_id.seller_ids
    #
    #         vendors = [(vendor_info.name.id, vendor_info.name.name) for vendor_info in vendor_infos]
    #
    #         return {'domain': {'vendor_id': [('id', 'in', [vendor[0] for vendor in vendors])]}}

class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'Purchase Request'

    name = fields.Char(string='Sequence', tracking=True, copy=False, readonly=True)
    material_requisition_id = fields.Many2one('material.requisition', string='Material Requisition')
    stock_picking_id = fields.Many2one('stock.picking', string='Stock Picking')
    request_date = fields.Date(string='Request Date')

    request_line_ids = fields.One2many('purchase.request.line', 'purchase_request_id', string='Request Lines')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.request.sequence') or '/'
        return super(PurchaseRequest, self).create(vals)



class PurchaseRequestLine(models.Model):
    _name = 'purchase.request.line'
    _description = 'Purchase Request Line'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    description = fields.Text(string='Description')
    vendor_id = fields.Many2one('res.partner', string='Vendor')
    quantity = fields.Float(string='Quantity', default=1.0)
    unit_of_measure = fields.Many2one('uom.uom', string='Unit of Measure')

    purchase_request_id = fields.Many2one('purchase.request', string='Purchase Request')

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            vendor_infos = self.product_id.seller_ids

            vendors = [(vendor_info.name.id, vendor_info.name.name) for vendor_info in vendor_infos]

            return {'domain': {'vendor_id': [('id', 'in', [vendor[0] for vendor in vendors])]}}