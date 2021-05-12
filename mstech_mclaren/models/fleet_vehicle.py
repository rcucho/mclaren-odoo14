from odoo import models,fields,api,_
from odoo.exceptions import UserError

class FleetMclaren(models.Model):
    _inherit = 'fleet.vehicle'

    license_plate_file_id = fields.Many2many('ir.attachment', 'license_plate_file_attachments_rel',
                              'license_plate', 'attachment_id', string="License plate",
                              help="Foto de la placa del vehiculo")
    acriss = fields.Char(string='ACRISS')
    property_card = fields.Many2many('ir.attachment', 'property_card_file_attachments_rel',
                              'property_card', 'attachment_id', string="Property card",
                              help="Documento de la tarjeta de propiedad")
                              
    insurance_company = fields.Many2one('res.partner','Compañia de Seguro')
    
    policy_number = fields.Char(string = "Numero de Poliza")
    policy_expiration = fields.Date(string = "Vencimiento de Poliza")
    policy_amount = fields.Float(string = "Suma Asegurada")
    policy_file_id = fields.Many2many('ir.attachment', 'policy_file_attachments_rel',
                              'policy_number', 'attachment_id', string="Documento de poliza",
                              help="Documento de la poliza")

    soat_number = fields.Char(string = "SOAT")
    soat_expiration = fields.Date(string = "Vencimiento de Soat")
    soat_file_id = fields.Many2many('ir.attachment', 'soat_file_attachments_rel',
                              'soat_number', 'attachment_id', string="Documento de SOAT",
                              help="Documento del Soat")
