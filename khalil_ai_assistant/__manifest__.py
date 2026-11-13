{
    'name': 'Khalil AI Voice Assistant',
    'version': '1.0',
    'category': 'Extra Tools',
    'summary': 'Native floating voice assistant widget for Odoo',
    'depends': ['base', 'web'],
    'data': [
        'views/assets.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'khalil_ai_assistant/static/src/js/voice_widget.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
