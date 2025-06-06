# Copyright 2019 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Petty Cash",
    "version": "15.0.2.0.0",
    "category": "Human Resources",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/hr-expense",
    "depends": ["hr_expense"],
    "data": [
        "security/ir.model.access.csv",
        "security/petty_cash_security.xml",
        "views/account_move_views.xml",
        "views/hr_expense_sheet_views.xml",
        "views/hr_expense_views.xml",
        "views/petty_cash_views.xml",
    ],
    "installable": True,
}
