{
    'name': 'Asistente de Desarrollo Personal',
    'version': '1.0.0',
    'category': 'Desarrollo Personal',
    'summary': 'Módulo inteligente para seguimiento de metas y desarrollo personal',
    'description': """
    Módulo avanzado para gestión de metas personales
    - Seguimiento de progreso
    - Recomendaciones inteligentes
    - Análisis de desarrollo personal
    """,
    'author': 'Oohel',
    'website': 'https://github.com/tu-usuario',
    'depends': [
        'base',
        'mail',
        "contacts",
        'web'
    ],
    'data': [
        'security/grupos_seguridad.xml',
        'security/ir.model.access.csv',
        'report/meta_personal_report.xml',
        'report/meta_personal_report_template.xml',
        'views/partner_inherit_views.xml',
        'views/metas_personales_views.xml',
        'views/recomendaciones_inteligentes_views.xml',
        'views/seguimiento_actividades_views.xml',
        'views/menu_principal.xml',


    ],

    # No cargar archivos inexistentes
    # 'views/etiquetas_metas_views.xml',
    # 'data/datos_iniciales.xml',

    'demo': [
        # 'demo/demo_data.xml'
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
