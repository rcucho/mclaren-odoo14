from odoo import models,fields,api,_
from odoo.exceptions import UserError

class FleetMclaren(models.Model):
    _inherit = 'fleet.vehicle'

    license_plate_file_id = fields.Many2many('ir.attachment', 'license_plate_file_attachments_rel',
                                  'license_plate', 'attachment_id', string="License plate",
                                  help="Picture of the license plate of vehicle ")
