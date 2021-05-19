# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError, ValidationError, Warning

import datetime
import json

class MailComposer(models.TransientModel) :
    _inherit = 'mail.compose.message'
    
    @api.model
    def default_get(self, fields) :
        result = super().default_get(fields)
        lead = self.env[self._context.get('active_model')].sudo().search([('id','in',self._context.get('active_ids'))])
        if lead._name == 'crm.lead' :
            attachment_field = 'foto_ids'
            if len(lead) and (attachment_field in lead) :
                fotos = lead.mapped(attachment_field)
                if len(fotos) :
                    result.update({
                        'attachment_ids': [(4, foto.id, 0) for foto in fotos],
                    })
        return result

class FleetVehicle(models.Model) :
    _inherit = 'fleet.vehicle'
    
    tanque = fields.Char(string='Tanque')
    rld = fields.Char(string='RLD')
    rlm = fields.Char(string='RLM')
    grupo = fields.Char(string='Grupo')
    #combustible = fields.Char(string='Combustible')
    extras = fields.Char(string='Extras')
    lector_rfid = fields.Char(string='Lector RFID')

class Partner(models.Model) :
    _inherit = 'res.partner'
    
    tarjeta_numero = fields.Char(string='Número de Tarjeta')
    tarjeta_validez = fields.Date(string='Fecha de Expiración de Tarjeta')
    tarjeta_identificacion = fields.Char(string='Tarjeta de Identificación')
    tipo_separacion = fields.Char(string='Tipo de Separación')
    bonus_programa = fields.Char(string='Bonus de Programa')
    correo_agendador = fields.Char(string='Correo de Agendador')
    
    edad = fields.Char(string='Edad')
    fecha_nacimiento = fields.Date(string='Fecha de Nacimiento')
    lugar_nacimiento = fields.Char(string='Lugar de Nacimiento')
    pais_nacimiento_id = fields.Many2one(comodel_name='res.country', string='País de Nacimiento')
    numero_pasaporte = fields.Char(string='Número de Pasaporte')
    fecha_pasaporte = fields.Char(string='Fecha de Pasaporte')
    pais_pasaporte_id = fields.Many2one(comodel_name='res.country', string='País de Pasaporte')
    numero_licencia = fields.Char(string='Número de Licencia')
    fecha_emision_licencia = fields.Char(string='Fecha de Emisión de Licencia')
    fecha_vencimiento_licencia = fields.Char(string='Fecha de Vencimiento de Licencia')
    lugar_emision_licencia = fields.Char(string='Lugar de Emisión de Licencia')

class Lead(models.Model) :
    _inherit = 'crm.lead'
    
    foto_ids = fields.Many2many(comodel_name='ir.attachment', relation='crm_lead_fotos_sixt_tabla', column1='lead_id', column2='attachment_id', string='Fotos')
    
    partner_l10n_latam_identification_type_id = fields.Many2one(comodel_name='l10n_latam.identification.type', string='Tipo Doc. Identidad de Cliente', compute='_compute_partner_data', store=True, readonly=True)
    partner_vat = fields.Char(string='Nro. Doc. Identidad de Cliente', compute='_compute_partner_data', store=True, readonly=True)
    
    @api.depends('partner_id')
    def _compute_partner_data(self) :
        for record in self :
            record.partner_l10n_latam_identification_type_id = record.partner_id.l10n_latam_identification_type_id
            record.partner_vat = record.partner_id.vat

class AccountPayment(models.Model) :
    _inherit = 'account.payment'
    
    contrato_id = fields.Many2one(comodel_name='sale.order', string='Contrato')
    garantia_pago = fields.Boolean(string='Garantía de Pago')

class AccountMove(models.Model) :
    _inherit = 'account.move'
    
    alquiler_id = fields.Many2one(comodel_name='sale.order', string='Alquiler', compute='_compute_alquiler', store=True, readonly=True)
    alquiler_name = fields.Char(string='Código de Alquiler', compute='_compute_alquiler', store=True, readonly=True)
    alquiler_check_in_dias = fields.Integer(string='Número de días de Check In', compute='_compute_alquiler', store=True, readonly=True)
    
    @api.depends('invoice_line_ids.sale_line_ids.order_id')
    def _compute_alquiler(self) :
        for record in self :
            alquiler = record.invoice_line_ids.mapped('sale_line_ids.order_id')
            if alquiler :
                alquiler = alquiler[0]
                record.alquiler_id = alquiler
                record.alquiler_name = alquiler.name
                record.alquiler_check_in_dias = alquiler.check_in_dias
            else :
                record.alquiler_id = False
                record.alquiler_name = False
                record.alquiler_check_in_dias = False

class ProductTemplate(models.Model) :
    _inherit = 'product.template'
    
    alquiler_dia = fields.Boolean(string='Alquiler por Día')
    alquiler_mes = fields.Boolean(string='Alquiler por Mes')

class SaleOrderLine(models.Model) :
    _inherit = 'sale.order.line'
    
    vehiculo_id = fields.Many2one(comodel_name='fleet.vehicle', string='Vehículo')
    vehiculo_vin_sn = fields.Char(string='N° de Identificación o Serie del Vehículo', related='vehiculo_id.vin_sn', store=True, readonly=True)

class SaleOrder(models.Model) :
    _inherit = 'sale.order'
    
    partner_name = fields.Char(string='Nombre de Cliente', compute='_compute_partner_data', store=True, readonly=True)
    partner_l10n_latam_identification_type_id = fields.Many2one(comodel_name='l10n_latam.identification.type', string='Tipo Doc. Identidad de Cliente', compute='_compute_partner_data', store=True, readonly=True)
    partner_vat = fields.Char(string='Nro. Doc. Identidad de Cliente', compute='_compute_partner_data', store=True, readonly=True)
    partner_email = fields.Char(string='Correo de Cliente', compute='_compute_partner_data', store=True, readonly=True)
    partner_phone = fields.Char(string='Teléfono de Cliente', compute='_compute_partner_data', store=True, readonly=True)
    partner_mobile = fields.Char(string='Celular de Cliente', compute='_compute_partner_data', store=True, readonly=True)
    partner_tarjeta_numero = fields.Char(string='Número de Tarjeta de Cliente', compute='_compute_partner_data', store=True, readonly=True)
    partner_tarjeta_validez = fields.Date(string='Fecha de Expiración de Tarjeta de Cliente', compute='_compute_partner_data', store=True, readonly=True)
    partner_tipo_separacion = fields.Char(string='Tipo de Separación de Cliente', compute='_compute_partner_data', store=True, readonly=True)
    partner_bonus_programa = fields.Char(string='Bonus de Programa de Cliente', compute='_compute_partner_data', store=True, readonly=True)
    
    contrato_acuerdo = fields.Binary(string='Acuerdo de Contrato')
    contrato_acuerdo_filename = fields.Char(string='Nombre del Archivo de Acuerdo de Contrato')
    contrato_agencia = fields.Boolean(string='Agencia de Contrato')
    contrato_observacion = fields.Text(string='Observación de Contrato')
    contrato_preferencia = fields.Text(string='Preferencia de Contrato')
    contrato_alquiler_anterior = fields.Text(string='Alquiler Anterior (Contrato)')
    
    cliente_voucher = fields.Char(string='Voucher de Cliente')
    cliente_total_dias = fields.Integer(string='Total de Días de Cliente')
    cliente_voucher_online = fields.Boolean(string='Voucher de Cliente Online')
    cliente_garantia_pago_id = fields.Many2one(comodel_name='account.payment', string='Garantía de Pago de Cliente')
    
    check_in_ciudad = fields.Char(string='Ciudad de Check In')
    check_in_dia_hora = fields.Datetime(string='Día y Hora de Check In')
    check_in_dias = fields.Integer(string='Número de días de Check In')
    check_in_calificacion = fields.Char(string='Calificación de Check In')
    check_in_plan = fields.Char(string='Plan de Check In')
    check_out_ciudad = fields.Char(string='Ciudad de Check Out')
    check_out_dia_hora = fields.Datetime(string='Día y Hora de Check Out')
    check_out_calificacion_cdno = fields.Char(string='Calificación CDNO de Check Out')
    check_out_numero_vuelo = fields.Char(string='Número de Vuelo de Check Out')
    
    montos_deposito = fields.Monetary(string='Monto de Depósito')
    montos_total_bruto = fields.Monetary(string='Monto Total Bruto')
    montos_valor_voucher = fields.Monetary(string='Monto de Valor del Voucher')
    montos_total_neto = fields.Monetary(string='Monto Total Neto')
    
    conductor_id = fields.Many2one(comodel_name='res.partner', string='Conductor')
    conductor_name = fields.Char(string='Nombre de Conductor', compute='_compute_conductor_data', store=True, readonly=True)
    conductor_l10n_latam_identification_type_id = fields.Many2one(comodel_name='l10n_latam.identification.type', string='Tipo Doc. Identidad de Conductor', compute='_compute_conductor_data', store=True, readonly=True)
    conductor_vat = fields.Char(string='Nro. Doc. Identidad de Conductor', compute='_compute_conductor_data', store=True, readonly=True)
    conductor_email = fields.Char(string='Correo de Conductor', compute='_compute_conductor_data', store=True, readonly=True)
    conductor_phone = fields.Char(string='Teléfono de Conductor', compute='_compute_conductor_data', store=True, readonly=True)
    conductor_mobile = fields.Char(string='Celular de Conductor', compute='_compute_conductor_data', store=True, readonly=True)
    
    recurrente_factura = fields.Boolean(string='Generar Factura Recurrente')
    recurrente_dias = fields.Integer(string='Días entre Facturas')
    recurrente_inicio = fields.Date(string='Siguiente Fecha de Factura')
    recurrente_fin = fields.Date(string='Última Fecha de Factura')
    recurrente_factura_ids = fields.Many2many(comodel_name='account.move', relation='recurrente_facturas_tabla', column1='sale_id', column2='move_id', string='Facturas Generadas')
    
    state = fields.Selection(selection_add=[('pre_aprobado','Pre-aprobado'),('sale',)], ondelete={'pre_aprobado': 'set default'})
    
    aseguradora_nro_siniestro = fields.Char(string='Nro. de Siniestro')
    aseguradora_nro_caso = fields.Char(string='Nro. de Caso')
    aseguradora_nro_servicio = fields.Char(string='Nro. de Servicio')
    aseguradora_placa_siniestro = fields.Char(string='Placa del siniestro')
    aseguradora_dias_cobertura = fields.Integer(string='Días de Cobertura')
    aseguradora_tipo_deducible = fields.Boolean(string='Deducible monto fijo')
    aseguradora_deducible_siniestro_monto = fields.Monetary(string='Deducible de Siniestro')
    aseguradora_deducible_siniestro_percent = fields.Float(string='Deducible de Siniestro')
    
    pago_ids = fields.One2many(comodel_name='account.payment',inverse_name='contrato_id', string='Pagos asociados')
    pago_garantia = fields.Boolean(string='Posee Garantía', compute='_compute_pagos_totales', store=False, readonly=True)
    pago_monto = fields.Monetary(string='Monto de Pagos Registrados', compute='_compute_pagos_totales', store=False, readonly=True)
    pagos_totales_ids = fields.Many2many(comodel_name='account.payment', string='Pagos de este contrato', compute='_compute_pagos_totales', store=False, readonly=True)
    #
    process_type=fields.Selection([('nation','Nacional'),('inter','Internacional')],string='Proceso',default='nation')
    #
    def _compute_pagos_totales(self) :
        for record in self :
            pagos_totales_ids = record.pago_ids
            for move in record.order_line.mapped('invoice_lines.move_id') :
                pagos = json.loads(move.invoice_payments_widget)
                if pagos :
                    pagos = pagos.get('content')
                    for pago in pagos :
                        pagos_totales_ids |= pagos_totales_ids.browse(pago.get('account_payment_id'))
            
            record.pagos_totales_ids = pagos_totales_ids
            record.pago_monto = sum(pagos_totales_ids.mapped('amount') or [0])
            record.pago_garantia = bool(pagos_totales_ids.filtered('garantia_pago'))
    
    @api.depends('partner_id')
    def _compute_partner_data(self) :
        for record in self :
            record.partner_name = record.partner_id.name
            record.partner_l10n_latam_identification_type_id = record.partner_id.l10n_latam_identification_type_id
            record.partner_vat = record.partner_id.vat
            record.partner_email = record.partner_id.email
            record.partner_phone = record.partner_id.phone
            record.partner_mobile = record.partner_id.mobile
            record.partner_tarjeta_numero = record.partner_id.tarjeta_numero
            record.partner_tarjeta_validez = record.partner_id.tarjeta_validez
            record.partner_tipo_separacion = record.partner_id.tipo_separacion
            record.partner_bonus_programa = record.partner_id.bonus_programa
    
    @api.depends('conductor_id')
    def _compute_conductor_data(self) :
        for record in self :
            record.conductor_name = record.conductor_id.name
            record.conductor_l10n_latam_identification_type_id = record.conductor_id.l10n_latam_identification_type_id
            record.conductor_vat = record.conductor_id.vat
            record.conductor_email = record.conductor_id.email
            record.conductor_phone = record.conductor_id.phone
            record.conductor_mobile = record.conductor_id.mobile
    
    def generar_factura_recurrente(self) :
        move_ids = self.env['account.move']
        action = True
        sequence = 0
        for record in self :
            recurrente_dias = record.recurrente_dias
            if record.recurrente_factura and (recurrente_dias > 0) :
                recurrente_inicio = record.recurrente_inicio
                recurrente_fin = record.recurrente_fin
                if recurrente_inicio and recurrente_fin and (recurrente_inicio <= recurrente_fin) and (recurrente_inicio not in record.recurrente_factura_ids.mapped('invoice_date')) :
                    move_id = record._prepare_invoice()
                    move_id.update({
                        'invoice_date': str(recurrente_inicio),
                    })
                    for line in record.order_line :
                        move_id.get('invoice_line_ids').append((0, 0, line._prepare_invoice_line(sequence=sequence, quantity=line.product_uom_qty)))
                        sequence = sequence + 1
                    
                    move_id = self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(move_id)
                    move_ids |= move_id
                    move_id = {
                        'recurrente_factura_ids': [(4, move_id.id, 0)],
                    }
                    recurrente_inicio = recurrente_inicio + datetime.timedelta(days=recurrente_dias)
                    move_id.update({
                        'recurrente_inicio': str(recurrente_inicio),
                    })
                    if recurrente_inicio > recurrente_fin :
                        move_id.update({
                            'recurrente_factura': False,
                        })
                    
                    record.write(move_id)
        
        if len(move_ids) :
            action = {
                'name': 'Facturas',
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
            }
            if len(move_ids) == 1 :
                action.update({
                    'view_mode': 'form',
                    'res_id': move_ids.id,
                })
            else :
                action.update({
                    'view_mode': 'tree,form',
                    'domain': [('id','in',move_ids.ids)],
                })
        
        return action
    
    def _action_confirm(self) :
        res = super()._action_confirm()
        self._compute_partner_data()
        return res
    
    def action_confirm(self) :
        res = False
        if set(self.mapped('state')) & {'draft', 'sent'} :
            res = self.write({
                'state': 'pre_aprobado',
            })
        else :
            res = super().action_confirm()
        return res
    
    def registrar_pago(self) :
        self.ensure_one()
        action = self.env.ref('account.action_account_payments').read()[0]
        action.update({
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(self.env.ref('account.view_account_payment_form').id, 'form')],
        })
        if (not isinstance(action.get('context'), dict)) :
            if not action.get('context') :
                action['context'] = {}
            else :
                action['context'] = safe_eval(action.get('context'))
        
        action.get('context').update({
            'default_payment_type': 'inbound',
            'default_partner_type': 'customer',
            'default_partner_id': self.partner_id.id,
            'default_contrato_id': self.id,
            'default_date': str(fields.Date.today()),
            'default_move_journal_types': ('bank', 'cash'),
        })
        return action
    
    def ver_pagos(self) :
        action = self.env.ref('account.action_account_payments').read()[0]
        if (not isinstance(action.get('context'), dict)) :
            if not action.get('context') :
                action['context'] = {}
            else :
                action['context'] = safe_eval(action.get('context'))
        
        if (not isinstance(action.get('domain'), list)) :
            if not action.get('domain') :
                action['domain'] = []
            else :
                action['domain'] = safe_eval(action.get('domain'))
        
        action['domain'] = [('id','in',self.pagos_totales_ids.ids)] + action['domain']
        if len(self) :
            record = self[0]
            action.get('context').update({
                'default_payment_type': 'inbound',
                'default_partner_type': 'customer',
                'default_partner_id': record.partner_id.id,
                'default_contrato_id': record.id,
                'default_date': str(fields.Date.today()),
                'default_move_journal_types': ('bank', 'cash'),
            })
        return action
    
    def generar_garantia(self) :
        con_garantia = self.filtered('cliente_garantia_pago_id')
        payment_ids = self.env['account.payment']
        action = True
        for record in (self.filtered('id') - con_garantia) :
            payment = {
                'default_payment_type': 'inbound',
                'default_partner_type': 'customer',
                'default_partner_id': record.partner_id.id,
                'default_date': str(fields.Date.today()),
                'default_move_journal_types': ('bank', 'cash'),
            }
            payment = self.env['account.payment'].sudo().with_context(payment).create({
                'contrato_id': record.id,
                'garantia_pago': 1,
            })
            record.cliente_garantia_pago_id = payment
            payment_ids |= payment
        
        if len(payment_ids) :
            action = {
                'name': 'Garantías',
                'type': 'ir.actions.act_window',
                'res_model': 'account.payment',
            }
            if len(payment_ids) == 1 :
                action.update({
                    'view_mode': 'form',
                    'res_id': payment_ids.id,
                })
            else :
                action.update({
                    'view_mode': 'tree,form',
                    'domain': [('id','in',payment_ids.ids)],
                })
        
        return action
    
    def ver_garantias(self) :
        action = self.env.ref('account.action_account_payments').read()[0]
        if (not isinstance(action.get('context'), dict)) :
            if not action.get('context') :
                action['context'] = {}
            else :
                action['context'] = safe_eval(action.get('context'))
        
        if (not isinstance(action.get('domain'), list)) :
            if not action.get('domain') :
                action['domain'] = []
            else :
                action['domain'] = safe_eval(action.get('domain'))
        
        action['domain'] = [('contrato_id','in',self.ids), ('garantia_pago','!=',False)] + action['domain']
        action['context'].update({
            'create': 0,
        })
        return action

class SaleAdvancePaymentInv(models.TransientModel) :
    _inherit = 'sale.advance.payment.inv'
    
    invoice_multiple = fields.Boolean(string='Múltiples Comprobantes')
    invoice_max_quantity = fields.Integer(string='Máxima Cantidad de Días por Comprobante', default=30)
    
    def create_invoices(self) :
        var = {
            'type': 'ir.actions.act_window_close',
        }
        #if self.advance_payment_method == 'edramgas' :
        #if (self.advance_payment_method == 'delivered') and self.has_down_payments and self.deduct_down_payments and self.multiple_invoices :
        if (self.advance_payment_method == 'delivered') and self.invoice_multiple :
            l10n_latam_einvoice_vals = self._create_invoices_add_context()
            if l10n_latam_einvoice_vals :
                self = self.with_context(l10n_latam_einvoice_vals=l10n_latam_einvoice_vals)
            #sale_orders = self.env['sale.order'].with_context(dict(self._context)).browse(self._context.get('active_ids', []))
            sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
            #invoice_number = self.invoice_number
            invoice_vals_list = []
            final_payment = self.deduct_down_payments
            decimal_places_quantity = self.env.ref('product.decimal_product_uom').digits
            decimal_places_price = self.env.ref('product.decimal_price').digits
            for sale_order in sale_orders :
                special_invoice_dict = dict()
                #############################
                invoice_max_quantity = self.invoice_max_quantity
                invoice_number = sum(sale_order.order_line.mapped('product_uom_qty') or [0])
                invoice_number = int(-(-invoice_number // invoice_max_quantity))
                product_ids = sale_order.order_line.mapped('product_id.id')
                read_dict = dict()
                for rec in sale_order.order_line :
                    read_dict.update({
                        rec.product_id.id: read_dict.get(rec.product_id.id, 0) + rec.product_uom_qty,
                    })
                #############################
                for iiiiiiiiiii in range(invoice_number) :
                    individual_invoice_vals_list = sale_order._create_invoices_before(final=final_payment)
                    for special_invoice_index in range(len(individual_invoice_vals_list)) :
                        if special_invoice_index not in special_invoice_dict :
                            special_invoice_dict.update({
                                special_invoice_index: [],
                            })
                        special_invoice_dict.get(special_invoice_index).append(individual_invoice_vals_list[special_invoice_index])
                if invoice_number > 1 :
                    write_dict = dict()
                    for special_invoice_index in special_invoice_dict :
                        write_dict.update({
                            special_invoice_index: [dict()],
                        })
                        list_index_done = []
                        for invoice_vals_dict in special_invoice_dict.get(special_invoice_index) :
                            current_dict = dict(read_dict)
                            for actual_dicts in write_dict.get(special_invoice_index) :
                                for actual_dict in actual_dicts.items() :
                                    current_dict.update({
                                        actual_dict[0]: current_dict.get(actual_dict[0], 0) - actual_dict[1],
                                    })
                            invoice_line_vals_list = invoice_vals_dict.get('invoice_line_ids')
                            for jjjjjjjj in list_index_done :
                                invoice_line_vals_list.pop(jjjjjjjj)
                            current_number = 0
                            line_number = len(invoice_line_vals_list)
                            number_list = list(range(line_number - 1, -1, -1))
                            list_index_keep = []
                            for jjjjjjjj in range(line_number - 1, -1, -1) :
                                list_index_keep.append(jjjjjjjj)
                                invoice_line_vals_dict = invoice_line_vals_list[jjjjjjjj][2]
                                current_value = min(invoice_line_vals_dict.get('quantity'), current_dict.get(invoice_line_vals_dict.get('product_id')))
                                current_number = current_number + current_value
                                current_write_dict = write_dict.get(special_invoice_index)[-1]
                                if current_number >= invoice_max_quantity :
                                    if current_number == invoice_max_quantity :
                                        list_index_done.append(jjjjjjjj)
                                    current_number = current_number - invoice_max_quantity
                                    current_value = current_value - current_number
                                    current_write_dict.update({
                                        invoice_line_vals_dict.get('product_id'): current_write_dict.get(invoice_line_vals_dict.get('product_id'), 0) + current_value,
                                    })
                                    invoice_line_vals_dict.update({
                                        'quantity': current_value
                                    })
                                    write_dict.get(special_invoice_index).append(dict())
                                    break
                                else :
                                    list_index_done.append(jjjjjjjj)
                                    current_write_dict.update({
                                        invoice_line_vals_dict.get('product_id'): current_write_dict.get(invoice_line_vals_dict.get('product_id'), 0) + current_value,
                                    })
                                    invoice_line_vals_dict.update({
                                        'quantity': current_value,
                                    })
                            index_to_remove = list(set(number_list) - set(list_index_keep))
                            for jjjjjjjj in number_list :
                                if jjjjjjjj in index_to_remove :
                                    invoice_line_vals_list.pop(jjjjjjjj)
                        invoice_vals_list.extend(special_invoice_dict.get(special_invoice_index))
            moves = sale_orders._create_invoices_during(invoice_vals_list)
            move_number = len(moves)
            while move_number > 0 :
                move_number = move_number - 1
                move = moves[move_number]
                #if (not (move.amount_total > 0)) and (not (move.amount_total < 0)) :
                if fields.Float.is_zero(move.amount_total, precision_rounding=2) :
                    moves -= move
                    move.unlink()
            sale_orders._create_invoices_after(moves, final=final_payment)
            if self._context.get('open_invoices', False) :
                var = sale_orders.action_view_invoice()
        else :
            var = super().create_invoices()
        return var
