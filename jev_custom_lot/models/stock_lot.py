# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class StockLot(models.Model):
    _inherit = 'stock.lot'

    pmg = fields.Float(string = 'TSW (g)')
    pmg_date = fields.Date(string = 'Date du PMG')
    weight = fields.Float(string = 'Weight (g)', compute='_compute_seeds_weigth')
    is_seeds = fields.Boolean('This product is sold per seed', related = 'product_uom_id.is_seeds', readonly=True)
    tg_ids = fields.One2many('stock.tg', 'lot_id', 'Taux de germination')
    purchase_price_ids = fields.One2many('stock.lot.purchase.price', 'lot_id', "Prix d'achat du lot")
    
    @api.onchange('product_id')
    def onchange_pmg(self):
        if self.product_id.variety_ids:
            self.pmg = self.product_id.variety_ids[0].species_id.default_pmg

    @api.depends('quant_ids', 'quant_ids.inventory_weight_for_seeds')
    def _compute_seeds_weigth(self):
        # compute le poid saisie dans les stocks quant et l'afficher dans le lot
        for lot in self:
            if lot.is_seeds:
                # We only care for the quants in internal or transit locations.
                quants = lot.quant_ids.filtered(lambda q: q.location_id.usage == 'internal' or (q.location_id.usage == 'transit' and q.location_id.company_id))
                lot.weight = sum(quants.mapped('inventory_weight_for_seeds'))
            else:
                lot.weight = None


 