# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class BankStatementLine(models.Model):
    _inherit = 'account.bank.statement'

    @api.onchange('balance_start','line_ids')
    def get_end_balance(self):
        for this in self:
            this.balance_end_real = this.balance_start + sum(this.line_ids.mapped('amount'))

    

class BankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    line_sequence = fields.Char( string='Sequence')
    operation_type = fields.Many2one('finance.operation')

    analytic_account_id = fields.Many2one(comodel_name="account.analytic.account", string="Analytic Account" )

    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')


    @api.onchange('operation_type')
    def get_line_sequence(self):
        for line in self:
            if line.operation_type :
                line.line_sequence = self.env['ir.sequence'].next_by_code(
                    line.operation_type.operation_sequence_id.code) or _('New')
            else:
                line.line_sequence = ""

    # @api.model
    # def create(self, values):
    #     if 'operation_type' in values:
    #         operation = self.env['finance.operation'].browse(values.get('operation_type'))
    #         values['line_sequence'] = self.env['ir.sequence'].next_by_code(
    #             operation.operation_sequence_id.code) or _('New')
    #     res = super(BankStatementLine, self).create(values)

    #     return res



    @api.model
    def _prepare_liquidity_move_line_vals(self):
        res = super(BankStatementLine, self)._prepare_liquidity_move_line_vals()

        res['analytic_account_id'] = self.analytic_account_id.id
        res['analytic_tag_ids'] = [(6, 0, self.analytic_tag_ids.ids)]

        return res

    @api.model
    def _prepare_counterpart_move_line_vals(self, counterpart_vals, move_line=None):
        res = super(BankStatementLine, self)._prepare_counterpart_move_line_vals(counterpart_vals, move_line)

        res['analytic_account_id'] = self.analytic_account_id.id
        res['analytic_tag_ids'] = [(6, 0, self.analytic_tag_ids.ids)]

        return res

