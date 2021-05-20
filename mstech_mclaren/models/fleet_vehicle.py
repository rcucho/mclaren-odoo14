from odoo import models,fields,api,_
from odoo.exceptions import UserError

class FleetMclaren(models.Model):
    _inherit = 'fleet.vehicle'
    
    ''' GRUPO VEHICULO '''
    license_plate_file_id = fields.Many2many('ir.attachment', 'license_plate_file_attachments_rel',
                              'license_plate', 'attachment_id', string="License plate",
                              help="Foto de la placa del vehiculo")
    acriss = fields.Char(string='ACRISS')
    property_card = fields.Many2many('ir.attachment', 'property_card_file_attachments_rel',
                              'property_card', 'attachment_id', string="Property card",
                              help="Documento de la tarjeta de propiedad")                           
    ''' GRUPO POLIZAS Y SEGUROS '''
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
    ''' GRUPO MODELO '''
    model_type = fields.Selection([
        ('type1','Sedan'), ('type2','Coupe'), ('type3','Convertible'), ('type4','Suv'), ('type5','Pickup'),
        ('type6','Van'), ('type7','Camion'), ('type8','Pasajeros'), ('type9','Pasajeros'), ('type10','Carga')],
        string = "Tipo")    
    traction = fields.Selection([('traction1','4x2 - Traccion Delantera'),('traction2',' 4x2 - Traccion Trasera'),
        ('traction3','4x4 - Traccion Total')], string="Traccion")
    upholstery = fields.Boolean(string="Tapiceria")
    equipment = fields.Many2many(comodel_name='equipment.vehicles',relation='fleet_vehicle_equipment','equipment_type',string ="Equipamentos")
    
class Equipment_Vehicule(models.Model):
    _name = 'equipment.vehicles'
    _description = "Equipamento de vehiculos"
    
    equipment_name = fields.Char(string="nombre de equipamento")
    equipment_type = fields.Selection([('equip1','Airbags'),('equip2','Bluetooth'),('equip3','Ventanas Electricas'),
        ('equip4','Pestillos Electricos'),('equip5','Camara de Retroceso'),('equip6','Sensores de Retroceso'),
        ('equip7','Encendido sin llave')])


