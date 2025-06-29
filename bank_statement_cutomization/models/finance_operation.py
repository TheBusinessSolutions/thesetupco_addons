# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FinanceOperation(models.Model):
    _name = 'finance.operation'
    _description = "Finance Operations"
    # _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _order = 'name, id'


    name = fields.Char(required=True, copy=False)
    operation_sequence_id = fields.Many2one('ir.sequence', required=True)