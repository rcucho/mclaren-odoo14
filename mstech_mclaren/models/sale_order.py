from odoo import models,fields,api,_
from odoo.exceptions import UserError

class SaleMclaren(models.Model):
    _inherit = 'sale.order'
    
    pickup_place = fields.Char(string="Lugar de Recojo")
    pickup_date = fields.Datetime(string="Fecha de Recojo")
    devolution_place = fields.Char(string="Lugar de Devolucion")
    devolution_date = fields.Datetime(string="Fecha de Devolucion")
    type_car = fields.Char(string="Tipo de Carro")
        
    @api.onchange('opportunity_id')
    def onchange_oportunity_data(self):  
        for record in self:
            if self.opportunity_id:
                record.pickup_place = record.opportunity_id.pickup_place
                record.pickup_date = record.opportunity_id.pickup_date
                record.devolution_place = record.opportunity_id.devolution_place
                record.devolution_date = record.opportunity_id.devolution_date 
                record.type_car = record.opportunity_id.type_car
            else:             
                record.pickup_place = False
                record.pickup_date = False
                record.devolution_place = False
                record.devolution_date = False
                record.type_car = False
                
                
class PartnerMclaren(models.Model):
    _inherit = 'res.partner'
    
    @api.onchange('l10n_latam_identification_type_id')
    def onchange_l10n_latam_identification_type_id(self):
        for record in self:
            if record.company_type == 'person':
                record.l10n_latam_identification_type_id.display_name = 'DNI'
            else:
                record.l10n_latam_identification_type_id.display_name = 'RUC'
                
                



