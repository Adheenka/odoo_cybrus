from odoo import fields, models, api ,_
from collections import defaultdict






class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'Purchase Request'

    name = fields.Char(string='Sequence', tracking=True, copy=False, readonly=True)
    # material_requisition_id = fields.Many2one('material.requisition', string='Material Requisition')
    stock_picking_id = fields.Many2one('stock.picking', string='Stock Picking')
    material_requisition_id = fields.Many2one('material.requisition', string='Material Requisition')
    request_date = fields.Date(string='Request Date')
    request_line_ids = fields.One2many('purchase.request.line', 'purchase_request_id', string='Request Lines')

    purchase_order_ids = fields.One2many('purchase.order', 'purchase_request_id', string='Purchase Orders',readonly=True)
    purchase_order_count = fields.Integer(string='Purchase Order Count', compute='_compute_purchase_order_count')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,  default=lambda self: self.env.company.id)



    @api.depends('purchase_order_ids')
    def _compute_purchase_order_count(self):
        for request in self:
            request.purchase_order_count = len(request.purchase_order_ids)

    def action_view_purchase_order(self):
        # Use the correct field name for the domain
        action_domain = [('purchase_request_id', '=', self.id)]
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Internal Pickings',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'view_id': False,
            'domain': action_domain,
        }
        return action


    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.request.sequence') or '/'
        return super(PurchaseRequest, self).create(vals)



    def send_purchase_order(self):
        created_purchase_orders = self.env['purchase.order']

        # Group request lines by vendor
        lines_by_vendor = defaultdict(list)
        for line in self.request_line_ids:
            lines_by_vendor[line.vendor_id].append(line)

        # Create purchase order for each vendor
        for vendor, lines in lines_by_vendor.items():
            purchase_order_lines = []
            for line in lines:
                purchase_order_line_vals = {
                    'product_id': line.product_id.id,
                    'product_qty': line.quantity,
                    'product_uom': line.unit_of_measure.id,
                }
                purchase_order_lines.append((0, 0, purchase_order_line_vals))

            purchase_order_vals = {
                'partner_id': vendor.id,
                'date_planned': fields.Datetime.now(),
                'purchase_request_id': self.id,
                'order_line': purchase_order_lines,
            }

            purchase_order = self.env['purchase.order'].create(purchase_order_vals)
            created_purchase_orders += purchase_order
        return created_purchase_orders

            # Assuming you have a Many2many field named 'purchase_order_ids' in purchase.request

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
    #         #

# <<<<<<<<<<<<<<<<<<<<<<<  code for fetching purchase order data placing smart button   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    def action_view_purchase_order(self):
        # Customize the code below based on your requirements and relationships between models.
        action = self.env.ref('purchase.purchase_rfq').read()[0]
        action['domain'] = [('id', 'in', self.purchase_order_ids.ids)]
        action['context'] = {}
        return action


class PurchaseRequestLine(models.Model):
    _name = 'purchase.request.line'
    _description = 'Purchase Request Line'

    product_id = fields.Many2one('product.product', string='Product', required=True, onchange='_onchange_product_id')
    description = fields.Text(string='Description')
    vendor_id = fields.Many2one('res.partner', string='Vendor')
    quantity = fields.Float(string='Quantity', default=1.0)
    unit_of_measure = fields.Many2one('uom.uom', string='Unit of Measure',related='product_id.uom_id')

    purchase_request_id = fields.Many2one('purchase.request', string='Purchase Request')


    @api.onchange('product_id')
    def onchange_product(self):
        if self.product_id:
            self.description = self.product_id.name




    # @api.depends('product_id')
    # def _compute_vendor_id(self):
    #     for record in self:
    #         # Corrected code to access supplier information
    #         seller_info = record.product_id.seller_ids and record.product_id.seller_ids[0]
    #         record.vendor_id = seller_info and seller_info.name.id or False


    # def _compute_seller_partner_ids(self):
    #     for record in self:
    #         seller_partner_ids = record.product_id.seller_ids.mapped('partner_id').ids
    #         record.seller_partner_ids = [(6, 0, seller_partner_ids)]


    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            vendor_infos = self.product_id.seller_ids

            vendors = [(vendor_info.name.id, vendor_info.name.name) for vendor_info in vendor_infos]

            return {'domain': {'vendor_id': [('id', 'in', [vendor[0] for vendor in vendors])]}}