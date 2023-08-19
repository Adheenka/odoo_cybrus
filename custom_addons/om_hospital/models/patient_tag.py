from odoo import api, fields, models,_


class PateintTag(models.Model):
    _name = "patient.tag"
    _description = "Patient Tag"

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string='Active',default=True,copy=False)
    color = fields.Integer(string="color")
    color_2 = fields.Char(string="color_2")
    sequence =fields.Integer(string="Sequence")
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _("%s (copy)",self.name)
        self.sequence = 10
        return super(PateintTag, self).copy(default)

    # @api.returns('self')
    # def copy(self, default=None):
    #     default = default or {}
    #     if not default.get('name'):
    #         default['name'] = f"{self.name} (copy)"
    #     self.sequence = 10
    #     return super().copy(default)

    _sql_constraints = [
        ('unique_name','unique (name)','Name must unique.'),
        ('check_sequence','check(sequence > 0)','Sequence must be non zero..')
    ]