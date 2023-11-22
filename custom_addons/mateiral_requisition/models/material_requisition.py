from odoo import fields, models, api ,_
from odoo.exceptions import ValidationError
from odoo.tools import format_date




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
    location = fields.Many2one('stock.location', string='Stock Location')


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
    # #
    # #
        for rec in self:
            rec.write({'stage': 'request'})

    def send_email_notification(self):
        mail_template = self.env.ref('mateiral_requisition.email_template_material_requisition')
        mail_template.send_mail(self.id, force_send=True)
    # def approve_request(self):
    #     # Update the stage to 'Inventory Confirmed'
    #     for rec in self:
    #         rec.write({'stage': 'inventory_confirmed'})
    #
    #     stock_picking_vals = {
    #         'partner_id': self.employee_id.id,
    #         'name': self.sequence,
    #         'scheduled_date': self.requisition_date,
    #         'location_id': self.env.ref('stock.stock_location_stock').id,  # Default Stock Location
    #         'location_dest_id': self.env.ref('stock.stock_location_customers').id,  # Default Customers Location
    #         'picking_type_id': self.env.ref('stock.picking_type_out').id,
    #
    #
    #
    #     }
    #     stock_moves = []
    #     for line in rec.materials_line_ids:
    #         stock_move_vals = {
    #             'name': line.description,
    #             'product_id': line.product_id.id,
    #             'product_uom_qty': line.quantity,
    #             'product_uom': 1,
    #             'location_id': self.env.ref('stock.stock_location_stock').id,  # Default Stock Location
    #             'location_dest_id': self.env.ref('stock.stock_location_customers').id,  # Default Customers Location
    #             'picking_type_id': self.env.ref('stock.picking_type_out').id,
    #             'sale_line_id': False,  # You may set it based on your needs
    #         }
    #         stock_moves.append(self.env['stock.move'].create(stock_move_vals))
    #     stock_picking = self.env['stock.picking'].create(stock_picking_vals)
    #
    #     return {
    #         'name': 'Stock Picking',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'stock.picking',
    #         'res_id': stock_picking.id,
    #         'type': 'ir.actions.act_window',
    #         'target': 'self',
    #     }

    def requisition_confirm(self):

        pass

    def approve_request(self):
        # Update the stage to 'Inventory Confirmed'
        for rec in self:
            rec.write({'stage': 'inventory_confirmed'})

        stock_picking_vals = {
            'partner_id': self.employee_id.id,
            'name': self.sequence,
            'scheduled_date': self.requisition_date,
            'location_id': self.env.ref('stock.stock_location_stock').id,  # Default Stock Location
            'location_dest_id': self.env.ref('stock.stock_location_customers').id,  # Default Customers Location
            'picking_type_id': self.env.ref('stock.picking_type_out').id,

            'move_ids_without_package': [(0, 0, {
                'product_id': line.product_id.id,
                'name': line.description,
                'product_uom_qty': line.quantity,
                'product_uom': 1,
                'location_id': self.env.ref('stock.stock_location_stock').id,  # Default Stock Location
                'location_dest_id': self.env.ref('stock.stock_location_customers').id,  # Default Customers Location
                'picking_type_id': self.env.ref('stock.picking_type_out').id,

            }) for line in self.materials_line_ids],
        }

        stock_picking = self.env['stock.picking'].create(stock_picking_vals)

        return {
            'name': 'Stock Picking',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'res_id': stock_picking.id,
            'type': 'ir.actions.act_window',
            'target': 'self',
        }


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


