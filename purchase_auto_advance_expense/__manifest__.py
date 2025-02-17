# -*- coding: utf-8 -*-
{
    'name': "Purchase Auto Advance Expense",

    'summary': """ Purchase Auto Advance Expense
        """,

    'description': """
        Purchase Auto Advance Expense
    """,

    'author': " TheSetupCo ",


    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase','hr_expense_advance_clearing'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode

}
