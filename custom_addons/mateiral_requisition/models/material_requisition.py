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
    project_id = fields.Many2one('project.task', string='Project')
    stage = fields.Selection([('new', 'New'), ('request', 'Request'), ('inventory_confirmed', 'Inventory Confirmed')],
                             string='Stage', default='new')

    # @api.model
    # def create(self, vals):
    #     if vals.get('name', _('New')) == _('New'):
    #         vals['name'] = self.env['ir.sequence'].next_by_code('material.requisition') or _('New')
    #     result = super(MaterialRequisition, self).create(vals)
    #     return result

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
            'res_model': 'stock.picking',  # Replace with the actual model you want to display
            'view_mode': 'tree,form',
            'domain': [('material_requisition_id', 'in', self.ids)],  # Adjust the domain as needed
        }