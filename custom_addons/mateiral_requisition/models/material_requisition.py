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

    # employee_id = fields.Many2one(
    #     'hr.employee',
    #     string='Employee',
    #     default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1),
    #     required=True,
    #     copy=True,
    # )
    employee_id=fields.Many2one('res.users', string='Requested By', default=lambda self: self.env.user)
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
    def _compute_picking_count(self):
        for requisition in self:
            requisition.picking_count = len(requisition.material_requisition_ids)
    # def _compute_picking_count(self):
    #     picking_data = self.env['stock.picking'].with_context(active_test=False).read_group([], [], [])
    #     total_count = sum(data.get('__count', 0) for data in picking_data)
    #     for record in self:
    #         record.picking_count = total_count

    def default_get(self, flds):
        result = super(MaterialRequisition, self).default_get(flds)

        result['requisition_date'] = datetime.now()
        return result




    def get_picking(self):
        pickings = self.env['stock.picking'].search([('material_requisition_id', '=', self.id)])
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Internal Pickings',
            'view_mode': 'tree,form',
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
        mail_template = self.env.ref('mateiral_requisition.email_template_material_requisition')
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
                'product_uom_qty': line.quantity,
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

    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity', default=1.0)
    description = fields.Char(string='Description', required=True)
    uom = fields.Many2one('uom.uom',string="Unit of Measure", related='product_id.uom_id')
    unit_price = fields.Float(string='Unit Price')
    total = fields.Float(string='Total', compute='_compute_total', store=True)
    tax = fields.Float(string='Tax')
    material_requisition_id = fields.Many2one('material.requisition', string='Requisition Lines')

    @api.depends('quantity', 'unit_price', 'tax')
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



    def _compute_product_available(self):

        for picking in self:

            picking.products_availability = True

    def add_product_request(self):
        created_purchase_orders = self.env['purchase.order']

        purchase_order_vals = {
            'partner_id': self.partner_id.id,
            'date_planned': fields.Datetime.now(),
            'order_line': [(0, 0, {
                'product_id': line.product_id.id,
                'product_qty': line.product_uom_qty,
            }) for line in self.move_ids_without_package],
        }

        purchase_order = self.env['purchase.order'].create(purchase_order_vals)
        purchase_order.send_email_notification()

        # Set products_availability to True after creating the purchase order
        self.write({'products_availability': True})
#     >>>>>>>>>>>>>>      stock picking  cde  <<<<<<<<<<<<<<<

#     def add_product_request(self):
#         created_purchase_orders = self.env['purchase.order']
#
#         purchase_order_vals = {
#             'partner_id': self.partner_id.id,
#             'date_planned': fields.Datetime.now(),
#             'order_line': [(0, 0, {
#                 'product_id': line.product_id.id,
#
#                 'product_qty': line.product_uom_qty,
#
#             }) for line in self.move_ids_without_package],
#         }
#
#         purchase_order = self.env['purchase.order'].create(purchase_order_vals)
#         purchase_order.send_email_notification()







    # def add_product_request(self):
    #     created_purchase_orders = self.env['purchase.order']
    #
    #     for picking in self:
    #         if picking.product_available:
    #             continue
    #
    #         purchase_order_lines = []
    #         for line in self.move_ids_without_package:
    #             # Calculate price with taxes
    #             price_unit_with_tax = line.product_id.list_price * (
    #                         1 + sum(line.product_id.supplier_taxes_id.mapped('amount')))
    #
    #             # Get taxes IDs
    #             taxes_ids = [x.id for x in line.product_id.supplier_taxes_id]
    #
    #             purchase_order_lines.append((0, 0, {
    #                 'product_id': line.product_id.id,
    #                 'product_qty': line.product_uom_qty,
    #                 'taxes_id': [(6, 0, taxes_ids)],
    #                 'price_unit': price_unit_with_tax,
    #                 'price_subtotal': price_unit_with_tax * line.product_uom_qty,
    #             }))
    #
    #         purchase_order_vals = {
    #             'partner_id': self.partner_id.id,
    #             'date_planned': fields.Datetime.now(),
    #             'order_line': purchase_order_lines,
    #             # Add other mandatory fields here
    #         }
    #
    #         # Create the purchase order
    #         purchase_order = self.env['purchase.order'].create(purchase_order_vals)
    #
    #         purchase_order.send_email_notification()
    #
    #     return True


#     >>>>>>>>>>>>>>      purchase order cde  <<<<<<<<<<<<<<<

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    def send_email_notification(self):
        mail_template = self.env.ref('mateiral_requisition.email_template_purchase_order_notification')
        email_to = self.get_email_to()
        mail_template.email_to = email_to
        mail_template.send_mail(self.id, force_send=True)

    def get_email_to(self):
        purchase_manager_group = self.env.ref('purchase.group_purchase_manager')
        email_list = [user.partner_id.email for user in purchase_manager_group.users if user.partner_id.email]
        return ";".join(email_list)

    def send_for_approval(self):
        pass

    # def add_product_request(self):
    #     created_purchase_orders = self.env['purchase.order']
    #
    #     for picking in self:
    #         if picking.products_availability:
    #             continue
    #
    #         purchase_order_vals = {
    #             'partner_id': self.partner_id.id,
    #             'date_planned': fields.Datetime.now(),
    #             'order_line': [(0, 0, {
    #                 'product_id': line.product_id.id,
    #
    #                 'product_qty': line.product_uom_qty,
    #
    #             }) for line in self.move_ids_without_package],
    #         }
    #
    #         purchase_order = self.env['purchase.order'].create(purchase_order_vals)
    #
    #         # Set the product_available field to True after the purchase order is added
    #         # picking.write({'product_available': True})
    #
    #     return True



    # def add_product_request(self):
    #     created_purchase_orders = self.env['purchase.order']
    #
    #     for picking in self:
    #         if picking.product_available:
    #
    #             continue
    #
    #
    #         purchase_order_vals = {
    #             'partner_id': self.partner_id.id,
    #             'date_planned': fields.Datetime.now(),
    #             'order_line': [(0, 0, {
    #                 'product_id':line.product_id.id,
    #
    #                 'product_qty': line.product_uom_qty,
    #                 'price_unit': line.product_id.list_price,  # You may adjust this based on your requirements
    #                 'price_subtotal': line.product_id.list_price * line.product_uom_qty,
    #
    #             })for line in self.move_ids_without_package],
    #         }
    #
    #
    #         purchase_order = self.env['purchase.order'].create(purchase_order_vals)
    #
    #         # Set the product_available field to True after the purchase order is added
    #         # picking.write({'product_available': True})
    #
    #
    #     return {
    #         'name': 'Created Purchase Orders',
    #         'type': 'ir.actions.act_window',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'purchase.order',
    #         'target': 'self',
    #         'res_id': purchase_order.id,
    #     }

    # new code create purchase order tax fiels addedd

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
    
    # def action_view_material_requisitions(self):
    #     material_requisitions = self.env['material.requisition'].search([('project_id', '=', self.id)])
    #     action = self.env.ref('mateiral_requisition.action_material_requisition').read()[0]
    #
    #     if len(material_requisitions) > 1:
    #         action['domain'] = [('id', 'in', material_requisitions.ids)]
    #     elif len(material_requisitions) == 1:
    #         action['views'] = [(self.env.ref('mateiral_requisition.view_material_requisition_form').id, 'form')]
    #         action['res_id'] = material_requisitions.ids[0]
    #
    #     return action













