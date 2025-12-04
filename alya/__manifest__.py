{
    'name': 'Asistente de Desarrollo Personal',
    'version': '1.0.0',
    'summary': 'Módulo inteligente para seguimiento de metas y desarrollo personal',
    'author': 'Oohel Technologies S.A. de C.V.',
    'maintainer': 'Geovani Daniel Nolasco Negrete <geovani.negrete@oohel.net>',
    'contributors': [
        'Gio <geovani.negrete@oohel.net>',
    ],
    'category': 'Productivity/Personal Development',
    'description': """
        Módulo para la gestión y seguimiento de metas personales.

        Funcionalidades:
        - Seguimiento de progreso de metas
        - Recomendaciones inteligentes basadas en actividad
        - Registro de actividades realizadas
        - Integración con contactos (res.partner)
        - Reportes PDF personalizados
    """,
    'website': 'https://github.com/tu-usuario',

    'depends': [
        'base',
        'mail',
        'contacts',
        'web',
    ],

    'data': [
        'security/alya_groups.xml',
        'security/ir.model.access.csv.csv',

        # REPORTES
        'report/meta_personal/meta_personal_report.xml',
        'report/meta_personal/meta_personal_templates.xml',

        # VISTAS
        'views/res_partner_views.xml',
        'views/alya_metas_personales_views.xml',
        'views/alya_recomendaciones_inteligentes_views.xml',
        'views/alya_seguimiento_actividades_views.xml',
        'views/alya_menus.xml',
    ],

    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
