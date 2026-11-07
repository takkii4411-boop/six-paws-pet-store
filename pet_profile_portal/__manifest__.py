{
    'name': 'Pet Profile Portal 2',
    'version': '1.0',
    'category': 'Portal',
    'summary': 'Portal access for Pet Profiles',
    'depends': [
        'portal',
        'website',
        'mail',
        'pet_profile',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        # 'security/pet_portal_rules.xml',
        'views/portal_pet_menu.xml',
        'views/portal_pet_templates.xml',
        'views/portal_pet_create.xml',
    ],
    'installable': True,
}
