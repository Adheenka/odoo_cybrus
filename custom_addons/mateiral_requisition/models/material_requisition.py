from odoo import fields, models, api ,_
from odoo.exceptions import ValidationError
from odoo.tools import format_date


# from odoo.addons.sale.models.sale_order import SaleOrder


class MaterialRequisition(models.Model):
    _name = "material.requisition"

    _description = "Material Requsition Module"

    sequence = fields.Char(string='Sequence', tracking=True, copy=False, readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Employee')
    department_id = fields.Many2one('hr.department', string='Department')
    requisition_date = fields.Date(string='Requisition Date')
    project_id = fields.Many2one('project.project', string='Project')
    task_id = fields.Many2one('project.task', required=True, string="Task",
                              domain="[('project_id', '=', project_id)]")
    stage = fields.Selection([('new', 'New'),('request','Request'),('inventory_confirmed', 'Inventory Confirmed')],
                             string='Stage', default='new')
    materials_line_ids = fields.One2many('materials','material_requisition_id',string='Requisition Lines')



    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            sequence = self.env['ir.sequence'].next_by_code('material.requisition.sequence') or 'New'

            current_date = fields.Date.today()
            year = fields.Date.from_string(current_date).year
            month = fields.Date.from_string(current_date).month

            vals['sequence'] = f"MT/{year}/{month:02d}/{sequence[-4:]}"

        return super(MaterialRequisition, self).create(vals)

    def show_picking(self):
        # Implement the logic for the 'show_picking' function
        # For example, you can open a wizard or perform any other actions
        # This is a placeholder, replace it with your actual implementation
        return {
            'type': 'ir.actions.act_window',
            'name': _('Internal Picking'),
            'res_model': 'stock.picking',
            'view_mode': 'list,form',
            'domain': [('material_requisition_id', 'in', self.ids)],  # Adjust the domain as needed
        }

    # def show_picking(self):
    #     for rec in self:
    #         res = self.env.ref('stock.action_picking_tree_all')
    #         res = res.read()[0]
    #         res['domain'] = str([('custom_requisition_id', '=', rec.id)])
    #     return res

    def send_request(self):

        self.send_email_notification()

        # Update the stage to 'Request'

        for rec in self:
            rec.write({'stage': 'request'})

    def send_email_notification(self):



        # Compose and send the email using the email template
        template = self.env.ref('mateiral_requisition.email_template_material_requisition')
        template.send_mail(self.id, force_send=True)

    def approve_request(self):
        # Update the stage to 'Inventory Confirmed'
        for rec in self:
            rec.write({'stage': 'inventory_confirmed'})


        purchase_order_vals = {
            'partner_id': self.employee_id.id,
            'name': self.sequence,
            'date_planned':self.requisition_date,
            'order_line': [(0, 0, {
                'product_id': line.product_id.id,
                'name': line.description,
                'product_qty': line.quantity,
                'product_uom': 1,
                'price_unit': line.unit_price,

            }) for line in self.materials_line_ids],

        }
        purchase_order = self.env['purchase.order'].create(purchase_order_vals)

        return {
            'name': 'Purchase Order',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'purchase.order',
            'res_id': purchase_order.id,
            'type': 'ir.actions.act_window',
            'target': 'self',
        }

    def requisition_confirm(self):
        # Logic for requisition confirmation (for admin employees)
        # This is a placeholder, replace it with your actual implementation
        pass




class Materials(models.Model):
    _name = 'materials'
    _description = 'Expense'

    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity', default=1.0)
    description = fields.Char(string='Description', required=True)
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


