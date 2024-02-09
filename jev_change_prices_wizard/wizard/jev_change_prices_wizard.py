from odoo import models, fields, api

class JevChangePricesWizard(models.TransientModel):
    _name = 'jev.change.prices.wizard'

    attribut_id = fields.Many2one(
        comodel_name='product.attribute.value',
        string="attribut value")
    
    cat_id = fields.Many2one(
        comodel_name='product.category',
        string="Product Category")
    
    plu = fields.Integer(string="PLU Code")

    min_quantity = fields.Float(
        string="Min. Quantity",
        default=0,
        digits='Product Unit of Measure',
        help="For the rule to apply, bought/sold quantity must be greater "
             "than or equal to the minimum quantity specified in this field.\n"
             "Expressed in the default unit of measure of the product.")

    fixed_price = fields.Float(string="Fixed Price", digits='Product Price')

    def change_prices_from_rules(self):
        active_ids = self.env.context.get('active_ids')
        pricelists = self.env['product.pricelist'].browse(active_ids)
        cat = self.cat_id
        attribut_value = self.attribut_id
        new_min_quantity = self.min_quantity
        new_price = self.fixed_price

        for pricelist in pricelists:


            pricelist_items_applied_on_variant = self.env['product.pricelist.item'].search([
                ('applied_on', '=', '0_product_variant'),
                ('product_id.categ_id', '=', cat.id),
                ('product_id.product_template_attribute_value_ids.product_attribute_value_id','=',attribut_value.id),
                ('pricelist_id','=',pricelist.id)
            ])

            #change price in priceliste rules
            for pricelist_item in pricelist_items_applied_on_variant:
                pricelist_item.write({
                    'min_quantity': new_min_quantity,
                    'fixed_price': new_price,
                })
    
    def change_prices_from_plu(self):

        active_ids = self.env.context.get('active_ids')
        pricelists = self.env['product.pricelist'].browse(active_ids)
        new_min_quantity = self.min_quantity
        new_price = self.fixed_price
        plu = self.plu

        for pricelist in pricelists:

            pricelist_items = self.env['product.pricelist.item'].search([
                ('plu', '=', plu),
            ])

            #change price in priceliste rules
            for pricelist_item in pricelist_items:
                pricelist_item.write({
                    'min_quantity': new_min_quantity,
                    'fixed_price': new_price,
                })             
