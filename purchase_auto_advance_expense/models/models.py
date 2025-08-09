# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    create_auto_expense = fields.Boolean(string='Create Auto Expense')

    def button_approve(self):
        result = super(PurchaseOrder, self).button_approve()
        for rec in self:
            employee_id = self.env['hr.employee'].sudo().search([('user_id', '=', rec.user_id.id)])
            if not employee_id:
                raise UserError(
                    "No employee found for the current user. Please ensure the user is linked to an employee.")

            if rec.create_auto_expense:
                # First create the expense sheet
                expense_sheet = self.env['hr.expense.sheet'].create({
                    'name': rec.name,
                    'employee_id': employee_id.id,
                    'clearing_date_due': rec.date_order.date(),
                    'total_amount': rec.amount_total,
                    'advance': True,
                    'advance_purchase_order_id': rec.id,
                })

                # Then create individual expense lines and link them to the sheet
                for line in rec.order_line:
                    expense_line = self.env['hr.expense'].create({
                        'name': line.product_id.name or line.name or 'Expense from PO',  # This is the mandatory field
                        'date': rec.date_order.date(),
                        'quantity': line.product_qty,
                        'total_amount': line.price_subtotal,
                        'unit_amount': line.price_unit,
                        'employee_id': employee_id.id,
                        'sheet_id': expense_sheet.id,  # Link to the expense sheet
                        'product_id': line.product_id.id if line.product_id else False,
                        'tax_ids': [(6, 0, line.taxes_id.ids)],  # Copy taxes from PO line
                    })

                # Now submit and approve the expense sheet
                expense_sheet.action_submit_sheet()
                expense_sheet.approve_expense_sheets()
                
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