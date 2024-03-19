# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class StockLot(models.Model):
    _inherit = 'stock.lot'

    #use_pmg = fields.Boolean(string = 'PMG is mandatory for this product (product sale in seed)')
    pmg = fields.Float(string = 'TSW (g)') #TODO l'unite de mesure du produit est graine, le PMG est donc obligatoire pour ce lot
    weight = fields.Float(string = 'Weight (g)')
    tg = fields.Float(string = 'TG')
    tg_date = fields.Date(string = 'TG date')
    is_seeds = fields.Boolean('This product is sold per seed', related = 'product_uom_id.is_seeds', readonly=True)

    @api.onchange('product_id')
    def onchange_pmg(self):
        if self.product_id.variety_ids:
            self.pmg = self.product_id.variety_ids[0].species_id.default_pmg