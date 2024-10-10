# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class StockLot(models.Model):
    _inherit = 'stock.lot'

    #use_pmg = fields.Boolean(string = 'PMG is mandatory for this product (product sale in seed)')
    pmg = fields.Float(string = 'TSW (g)') #TODO l'unite de mesure du produit est graine, le PMG est donc obligatoire pour ce lot
    weight = fields.Float(string = 'Weight (g)', compute='_compute_seeds_weigth')
    is_seeds = fields.Boolean('This product is sold per seed', related = 'product_uom_id.is_seeds', readonly=True)
    tg_ids = fields.One2many('stock.tg', 'lot_id', 'Taux de germination')
    
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


 