from odoo import models, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):

        teams = self.env['crm.team'].search([('user_id', '=', self.env.user.id)]).mapped('member_ids')

        if self.env.user.has_group('sales_team.group_sale_manager'):
            domain += ['|', ('user_id', 'in', teams.ids), ('user_id', '=', self.env.user.id)]
        else:
            domain += []

        return super(CrmLead, self).search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)