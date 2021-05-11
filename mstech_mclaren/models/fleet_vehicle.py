from odoo import models,fields,api,_
from odoo.exceptions import UserError

class FleetMclaren(models.Model):
    _inherit = 'fleet.vehicle'

     #voucher_file_ids = fields.Many2many(comodel_name='ir.attachment', relation='payment_register_voucher_file_tabla', column1='payment_register_id', column2='attachment_id', string='Foto de Placa')
     license_plate_file_id = fields.Many2many('ir.attachment', 'license_plate_file_attachments_rel',
                                  'license_plate', 'attachment_id', string="License plate attachments",
                                  help="Picture of the license plate of vehicle ")