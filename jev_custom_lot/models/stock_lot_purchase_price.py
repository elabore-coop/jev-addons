# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class StockTg(models.Model):
    _name = 'stock.lot.purchase.price'

    price_paid = fields.Float(string = 'Prix payé')
    price_by_weight = fields.Float(string = 'Prix au gramme')
    purchase_date = fields.Date(string = "Date d'achat")
    lot_id = fields.Many2one('stock.lot', 'lot associé')
    product_id = fields.Many2one('product.product', compute='_compute_product')

    @api.depends('lot_id')
    def _compute_product(self):
        for rec in self:
            rec.product_id = rec.lot_id.product_id if rec.lot_id.product_id else None


    