from odoo import fields, models, api ,_





class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'Purchase Request'

    name = fields.Char(string='Sequence', tracking=True, copy=False, readonly=True)
    # material_requisition_id = fields.Many2one('material.requisition', string='Material Requisition')
    stock_picking_id = fields.Many2one('stock.picking', string='Stock Picking')
    material_requisition_id = fields.Many2one('material.requisition', string='Material Requisition')

    request_date = fields.Date(string='Request Date')

    request_line_ids = fields.One2many('purchase.request.line', 'purchase_request_id', string='Request Lines')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.request.sequence') or '/'
        return super(PurchaseRequest, self).create(vals)

    def send_email_notification(self):
        mail_template = self.env.ref('mateiral_requisition.email_template_purchase_order_notification')
        email_to = self.get_email_to()
        mail_template.email_to = email_to
        mail_template.send_mail(self.id, force_send=True)

    def get_email_to(self):
        purchase_manager_group = self.env.ref('purchase.group_purchase_manager')
        email_list = [user.partner_id.email for user in purchase_manager_group.users if user.partner_id.email]
        return ";".join(email_list)


    # def send_purchase_order(self):
    #     pass

    # def send_purchase_order(self):
    #     created_purchase_orders = self.env['purchase.order']
    #
    #     for line in self.request_line_ids:
    #         # You need to customize the code below based on your requirements and relationships between models.
    #
    #         # Create purchase order values
    #         purchase_order_vals = {
    #             'partner_id': line.vendor_id.id,  # Use the vendor from the purchase request line
    #             'date_planned': fields.Datetime.now(),  # Adjust this based on your requirements
    #             'order_line': [(0, 0, {
    #                 'product_id': line.product_id.id,
    #                 'product_qty': line.quantity,
    #                 'product_uom': line.unit_of_measure.id,
    #             })],
    #         }
    #
    #         # Create purchase order
    #         purchase_order = self.env['purchase.order'].create(purchase_order_vals)
    #         purchase_order.send_email_notification()


    def send_purchase_order(self):
        created_purchase_orders = self.env['purchase.order']

        for line in self.request_line_ids:
            # You need to customize the code below based on your requirements and relationships between models.

            # Create purchase order values
            purchase_order_vals = {
                'partner_id': line.vendor_id.id,  # Use the vendor from the purchase request line
                'date_planned': fields.Datetime.now(),  # Adjust this based on your requirements
                'order_line': [(0, 0, {
                    'product_id': line.product_id.id,
                    'product_qty': line.quantity,
                    'product_uom': line.unit_of_measure.id,
                })],
            }

            # Create purchase order
            purchase_order = self.env['purchase.order'].create(purchase_order_vals)
            purchase_order.send_email_notification()

            # Link the created purchase order to the purchase request



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
    def onchange_product(self):
        if self.product_id:

            self.description = self.product_id.name
    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            vendor_infos = self.product_id.seller_ids

            vendors = [(vendor_info.name.id, vendor_info.name.name) for vendor_info in vendor_infos]

            return {'domain': {'vendor_id': [('id', 'in', [vendor[0] for vendor in vendors])]}}