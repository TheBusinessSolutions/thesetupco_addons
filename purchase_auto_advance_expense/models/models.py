# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    create_auto_expense = fields.Boolean(string='Create Auto Expense')

    def button_confirm(self):
        result = super(PurchaseOrder, self).button_confirm()
        for rec in self:
            # Check if status is 'purchase' or 'done'
            if rec.state not in ['purchase', 'done']:
                continue
                
            employee_id = self.env['hr.employee'].sudo().search([('user_id', '=', rec.user_id.id)])
            if not employee_id:
                raise UserError(
                    "No employee found for the current user. Please ensure the user is linked to an employee.")

            if rec.create_auto_expense:
                lines = []
                for line in rec.order_line:
                    lines.append((0, 0, {
                        'date': rec.date_order.date(),
                        'name': line.product_id.name,
                        'quantity': line.product_qty,
                        'total_amount':line.price_subtotal,
                        'unit_amount':line.price_unit,
                        'employee_id': employee_id.id,
                    }))

                vals={
                    'name':rec.name,
                    'employee_id' : employee_id.id,
                    'clearing_date_due' :rec.date_order.date(),
                    'total_amount':rec.amount_total,
                    'advance': True,
                    'advance_purchase_order_id': rec.id,
                    'expense_line_ids':lines,
                }
                advance_expense_id = self.env['hr.expense.sheet'].create(vals)
                advance_expense_id.action_submit_sheet()
                advance_expense_id.approve_expense_sheets()
        return result


    def open_advance_expense_sheet(self):
        for rec in self:
            expense_sheet = self.env['hr.expense.sheet'].search([('advance_purchase_order_id', '=', rec.id)], limit=1)
            if not expense_sheet:
                raise UserError("No related expense sheet found for this purchase order.")
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'hr.expense.sheet',
                'view_mode': 'form',
                'res_id': expense_sheet.id,
            }

class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    advance_purchase_order_id = fields.Many2one('purchase.order')