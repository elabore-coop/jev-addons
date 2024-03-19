# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    inventory_weight_for_seeds = fields.Float('Weight in stock (g)')
    is_seeds = fields.Boolean('This product is sold per seed', related = 'product_uom_id.is_seeds', readonly=True)

    @api.onchange('inventory_weight_for_seeds','lot_id')
    def onchange_inventory_weight_for_seeds(self):
        for rec in self:
            if rec.inventory_weight_for_seeds:
                    if rec.lot_id and rec.lot_id.pmg:
                        rec.inventory_quantity = rec.inventory_weight_for_seeds * 1000 / rec.lot_id.pmg #poid de mille graines en G
                    else:
                        raise UserError(_("No lot or no tsw found in {}. Please create a lot or enter the tsw in the lot to calculate the number of seeds in stock.".format(rec.display_name)))

    @api.model
    def _get_inventory_fields_write(self):
        """ Returns a list of fields user can edit when editing a quant in `inventory_mode`."""
        res = super()._get_inventory_fields_write()
        res += ['inventory_weight_for_seeds']
        return res