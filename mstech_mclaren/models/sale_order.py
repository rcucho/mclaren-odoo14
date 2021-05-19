from odoo import models,fields,api,_
from odoo.exceptions import UserError

class SaleMclaren(models.Model):
    _inherit = 'sale.order'
    
    pickup_place = fields.Char(string="Lugar de Recojo", compute='_compute_oportunity_data', store=True)
    pickup_date = fields.Datetime(string="Fecha de Recojo", compute='_compute_oportunity_data', store=True)
    devolution_place = fields.Char(string="Lugar de Devolucion", compute='_compute_oportunity_data', store=True)
    devolution_date = fields.Datetime(string="Fecha de Devolucion", compute='_compute_oportunity_data', store=True)
    type_car = fields.Char(string="Tipo de Carro", compute='_compute_oportunity_data', store=True)
    
    @api.depends('opportunity_id')
    def _compute_oportunity_data(self):
        for record in self:
            record.pickup_place = record.opportunity_id.pickup_place
            record.pickup_date = record.opportunity_id.pickup_date
            record.devolution_place = record.opportunity_id.devolution_place
            record.devolution_date = record.opportunity_id.devolution_date 
            record.type_car = record.opportunity_id.type_car
            


