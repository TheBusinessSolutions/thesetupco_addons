# -*- coding: utf-8 -*-
{
    'name': "Bank Statement add sequence on line",

    'summary': """
        Bank Statement add sequence on line & add it to the print layout""",

    'description': """
        Bank Statement add sequence on line & add it to the print layout
    """,

    'author': "Mahmoud Salama",
    'website': "https://www.linkedin.com/in/mahmoudsalama",

    
    'category': 'Accounting',
    'version': '15.0',

    
    'depends': ['account'],

    
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'report/bank_statment_line.xml',
        'views/finance_operation.xml',
        'views/bank_statement.xml',
    ],
   
}
