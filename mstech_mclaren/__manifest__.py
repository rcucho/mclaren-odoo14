{
    'name': "Mstech Mclaren",
    "category": "Fleet",
    'author': "Meditech",
    'summary':"Mstech Mclaren",
    'depends': [
    	'fleet',
        'crm',
        'mstech_sixt_prev',

    ],
    'data': [
        'views/fleet_vehicle.xml',
        'views/crm_lead.xml',
        'views/sale_order.xml'
      
    ],
    'installable' : True,
    'auto_install' :  False,
    'application' :  False,
}
