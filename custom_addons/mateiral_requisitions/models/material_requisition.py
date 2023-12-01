from odoo import fields, models, api ,_
from odoo.exceptions import ValidationError
from odoo.tools import format_date
from datetime import datetime, timedelta



class MaterialRequisition(models.Model):
    _name = "material.requisition"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Material Requsition Module"
    _rec_name = 'sequence'

    sequence = fields.Char(string='Sequence', tracking=True, copy=False, readonly=True)


    employee_id=fields.Many2one('res.users', string='Employee', default=lambda self: self.env.user)
    requisition_employee = fields.Many2one('hr.employee', string='Employee')
    department_id = fields.Many2one('hr.department',  related='employee_id.department_id',string='Department')
    project_id = fields.Many2one('project.project', string='Project')
    requisition_stage = fields.Many2one('project.task.type', string='Stage')
    requisition_task = fields.Many2one('project.task', string='Task',domain="[('project_id', '=', project_id)]")

    requisition_date = fields.Date(string='Requisition Date')

    stage = fields.Selection([('new', 'New'),('requested','Requested'),('inventory_confirmed', 'Inventory Confirmed')],
                             string='Stage', default='new', tracking=True)
    materials_line_ids = fields.One2many('materials','material_requisition_id',string='Requisition Lines')
    location = fields.Many2one('stock.location', string='Stock Location')

    material_requisition_ids = fields.One2many('stock.picking','material_requisition_id', string='Stock Pickings',readonly=True)
    picking_count = fields.Integer('Picking Count', compute='_compute_picking_count')
    date_end = fields.Date(string='Requisition Deadline',help='Last date for the product to be needed',copy=True, tracking=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,  default=lambda self: self.env.company.id)


    def _compute_picking_count(self):
        for requisition in self:
            requisition.picking_count = len(requisition.material_requisition_ids)

    def default_get(self, flds):
        result = super(MaterialRequisition, self).default_get(flds)

        result['requisition_date'] = datetime.now()
        return result

    def get_picking(self):
        pickings = self.env['stock.picking'].search([('material_requisition_id', '=', self.id)])
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Internal Pickings',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'view_id': False,
            'domain': [('material_requisition_id', '=', self.id)],
        }
        if pickings:
            action.update({'res_id': pickings[0].id})
        return action





    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('material.requisition.sequence') or 'New'
        return super(MaterialRequisition, self).create(vals)



    def send_request(self):
        self.send_email_notification()

        for rec in self:
            rec.write({'stage': 'requested'})

    def send_email_notification(self):
        mail_template = self.env.ref('mateiral_requisitions.email_template_material_requisition')
        email_to = self.get_email_to()
        mail_template.email_to = email_to
        mail_template.send_mail(self.id, force_send=True)

    def get_email_to(self):
        stock_manager_group = self.env.ref('stock.group_stock_manager')
        email_list = [user.partner_id.email for user in stock_manager_group.users if user.partner_id.email]
        return ";".join(email_list)
    def requisition_confirm(self):

        pass



    def approve_request(self):
        # Update the stage to 'Inventory Confirmed'
        for rec in self:
            rec.write({'stage': 'inventory_confirmed'})

        # Create a picking record
        stock_picking_vals = {
            'partner_id': self.employee_id.partner_id.id,
            'origin': rec.sequence,
            'scheduled_date': rec.requisition_date,
            'location_id': self.env.ref('stock.stock_location_stock').id,
            'location_dest_id': self.env.ref('stock.stock_location_customers').id,
            'picking_type_id': self.env.ref('stock.picking_type_out').id,
            'material_requisition_id': rec.id,
        }
        stock_picking = self.env['stock.picking'].create(stock_picking_vals)

        # Create move lines for the picking
        move_vals = []
        for line in rec.materials_line_ids:
            move_vals.append((0, 0, {
                'product_id': line.product_id.id,
                'name': line.description,
                'product_uom_qty': line.uom._compute_quantity(line.quantity, line.product_id.uom_id),
                # 'product_uom_qty': line.quantity *(line.product_id.product_tmpl_id.uom_po_id.factor_inv) if line.uom != line.product_id.product_tmpl_id.uom_id else line.quantity,
                'product_uom': 1,
                'location_id': self.env.ref('stock.stock_location_stock').id,
                'location_dest_id': self.env.ref('stock.stock_location_customers').id,
                'picking_type_id': self.env.ref('stock.picking_type_out').id,
            }))

        stock_picking.write({'move_ids_without_package': move_vals})

        return True


class Materials(models.Model):
    _name = 'materials'
    _description = 'Expense'

    # product_id = fields.Many2one('product.product', string='Product')
    product_id = fields.Many2one('product.product', string='Product', onchange='_onchange_product_id')
    quantity = fields.Float(string='Quantity', default=1.0)
    description = fields.Char(string='Description', required=True)
    uom = fields.Many2one('uom.uom',string="Unit of Measure")
    unit_price = fields.Float(string='Unit Price')
    total = fields.Float(string='Total', compute='_compute_total', store=True)
    tax = fields.Float(string='Tax')
    material_requisition_id = fields.Many2one('material.requisition', string='Requisition Lines')

    vendor_id = fields.Many2one('res.partner', string='Vendor')

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.uom = self.product_id.uom_po_id
            vendor_infos = self.product_id.seller_ids
            vendors = [(vendor_info.name.id, vendor_info.name.name) for vendor_info in vendor_infos]
            return {'domain': {'vendor_id': [('id', 'in', [vendor[0] for vendor in vendors])]}}



    @api.depends('product_id')
    def _compute_vendor_id(self):
        for material in self:
            vendor_info = material.product_id.seller_ids
            material.vendor_id = vendor_info[0].name if vendor_info else False




    def _compute_total(self):
        for expense in self:
            expense.total = (expense.quantity * expense.unit_price) * (1 + expense.tax / 100)

    @api.depends('unit_price', 'quantity')
    def _get_subtotal(self):
        self.subtotal = self.unit_price * self.quantity


    @api.onchange('product_id')
    def onchange_product(self):
        if self.product_id:
            self.unit_price = self.product_id.list_price
            self.description = self.product_id.name


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    material_requisition_id = fields.Many2one('material.requisition', string='Material Requisition', ondelete="cascade")
    email_sent = fields.Boolean(string="email")



    def _compute_product_available(self):
        for picking in self:
            picking.products_availability = True

    def add_product_request(self):
        created_purchase_requests = self.env['purchase.request']
        purchase_request_vals = {
            'material_requisition_id': self.material_requisition_id.id,
            'stock_picking_id': self.id,
            'request_date': fields.Datetime.now(),
            'request_line_ids': [],
        }
        for line in self.move_ids_without_package:
            if line.forecast_availability != line.product_uom_qty:
                purchase_request_vals['request_line_ids'].append((0, 0, {
                    'product_id': line.product_id.id,
                    'quantity': abs(line.forecast_availability - line.product_uom_qty) if line.forecast_availability > 0 else line.product_uom_qty,
                    'unit_of_measure': line.product_id.uom_id.id,
                }))
        if purchase_request_vals['request_line_ids']:
            purchase_request = self.env['purchase.request'].create(purchase_request_vals)
            if purchase_request:
                self.email_sent = True
            # self.send_email_notification()
            # self.write({'products_availability': True})
        return True

    def send_email_notification(self):
        mail_template = self.env.ref('mateiral_requisitions.email_template_purchase_order_notification')
        email_to = self.get_email_to()
        mail_template.email_to = email_to
        mail_template.send_mail(self.id, force_send=True)


    def get_email_to(self):
        purchase_manager_group = self.env.ref('purchase.group_purchase_manager')
        email_list = [user.partner_id.email for user in purchase_manager_group.users if user.partner_id.email]
        return ";".join(email_list)



class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    purchase_request_id = fields.Many2one('purchase.request', string='Purchase Requisition', ondelete="cascade")

    def send_email_notification(self):
        mail_template = self.env.ref('mateiral_requisitions.email_template_purchase_order_notification')
        email_to = self.get_email_to()
        mail_template.email_to = email_to
        mail_template.send_mail(self.id, force_send=True)

    def get_email_to(self):
        purchase_manager_group = self.env.ref('purchase.group_purchase_manager')
        email_list = [user.partner_id.email for user in purchase_manager_group.users if user.partner_id.email]
        return ";".join(email_list)


class ProjectProject(models.Model):
    _inherit = 'project.project'



    material_requisition_ids = fields.One2many('material.requisition', 'project_id', string='Material Requisitions')
    requisition_count = fields.Integer(string='Material Requisitions Count', compute='_compute_requisition_count')

    @api.depends('material_requisition_ids')
    def _compute_requisition_count(self):
        for project in self:
            project.requisition_count = len(project.material_requisition_ids)

    def action_view_material_requisitions(self):
        material_requisitions = self.env['material.requisition'].search([('project_id', '=', self.id)])
        action = self.env.ref('mateiral_requisition.action_material_requisition').read()[0]

        if len(material_requisitions) > 1:
            action['domain'] = [('id', 'in', material_requisitions.ids)]
            action['context'] = {'default_project_id': self.id}
        elif len(material_requisitions) == 1:
            action['views'] = [(self.env.ref('mateiral_requisition.view_material_requisition_form').id, 'form')]
            action['res_id'] = material_requisitions.ids[0]

        # Add count to the button label
        action['name'] = 'Material Requisitions (%d)' % len(material_requisitions)

        return action
    








    # def add_product_request(self):
    #     created_purchase_requests = self.env['purchase.request']
    #
    #     # Create a purchase request for the entire stock picking
    #     purchase_request_vals = {
    #         'material_requisition_id': self.material_requisition_id.id,
    #         'stock_picking_id': self.id,
    #         'request_date': fields.Datetime.now(),
    #         'request_line_ids': [],
    #     }
    #
    #     # Add each product line to the purchase request
    #     for line in self.move_ids_without_package:
    #         purchase_request_vals['request_line_ids'].append((0, 0, {
    #             'product_id': line.product_id.id,
    #             'quantity': line.product_uom_qty,
    #             'unit_of_measure': line.product_id.uom_id.id,
    #         }))
    #
    #     # Create the purchase request
    #     purchase_request = self.env['purchase.request'].create(purchase_request_vals)
    #
    #     # Send email notification
    #     purchase_request.send_email_notification()
    #
    #     # Set products_availability to True after creating the purchase request
    #     self.write({'products_availability': True})





