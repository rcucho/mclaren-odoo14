from odoo import models,fields,api,_
from odoo.exceptions import UserError

class SaleMclaren(models.Model):
    _inherit = 'crm.lead'
    
    pickup_place = fields.Char(string="Lugar de Recojo")
    pickup_date = fields.Datetime(string="Fecha y Hora de Recojo")
    devoluiton_place = fields.Char(string="Lugar de Devolucion")
    devolution_date = fields.Datetime(string="Fecha y Hora de Devolucion")
    type_car = fields.Char(string="Tipo de Carro")
    
    
