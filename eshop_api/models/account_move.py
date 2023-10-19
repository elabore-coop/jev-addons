# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import json
import re


class AccountMove(models.Model):

    _inherit = 'account.move'

    def _get_or_create_customer(self, email, name):
        '''
        Get or create an Odoo partner based on email eshop customer

        Args:
        email (str) : customer email from eshop invoice (mandatory)
        name (str) : customer name from eshop invoice (optional, used for partner creation)

        Return: instance of res_partner
        '''
        partner = self.env['res.partner'].search([('email', '=', email),('parent_id','=', None)], limit=1)
        if partner:
            return partner
        else:
            if name:
                new_partner = self.env['res.partner'].create({'email': email, 'name': name})
            else:
                raise UserError(_("Missing 'client_name' in invoice data JSON."))
            return new_partner

    def _get_country_id(self, customer_country_code):
        '''
        Get Odoo country ID based on country in customer address

        Args:
        customer_country_code (str) : country code in customer address (mandatory). Ex : FR for France, BE for Belgium

        Return: ID of country in Odoo
        '''      

        odoo_country = self.env['res.country'].search([('code', '=', customer_country_code)], limit=1)
        if odoo_country:
            return odoo_country.id
        else:
            raise UserError(_("No country found in Odoo for country code : {}".format(customer_country_code)))

    def _set_partner_address(self, partner, street, street2, zip, city, country_id):
        '''
        Set Odoo partner address based on eshop customer address

        Args:
        partner (str) : instance of res_partner (mandatory)
        street (str) : street from eshop invoice (mandatory)
        street2 (str) : street 2 (optional)
        zip (str) : zip from eshop invoice (mandatory)
        city (str) : city from eshop invoice (mandatory)
        country_id (int) : country ID in Odoo (optional)
        '''
        # Si le client a pour adresse celle passée en paramètre, ne rien faire
        if partner.street == street and partner.zip == zip and partner.city == city:
            return

        # Si l'adresse passée en paramètre n'est pas connue pour ce client, changer l'adresse du client
        partner.write({
            'street': street,
            'street2': street2,
            'zip': zip,
            'city': city,
            'country_id': country_id,
        })

    def _get_or_create_delivery_address(self, partner, street, street2, zip, city, country_id):
        '''
        Get or create Odoo partner delivery address based on eshop customer address

        Args:
        partner (str) : instance of res_partner (mandatory)
        street (str) : delivery street from eshop invoice (mandatory)
        street (str) : delivery street 2 (optionnal)
        zip (str) : delivery zip from eshop invoice (mandatory)
        city (str) : delivery city from eshop invoice (mandatory)
        country (int) : country ID in Odoo (optionnal)

        Return: ID of instance of res_partner
        '''
        # si le client a pour adresse celle passée en parametre, alors partner_shipping_id = partner.id
        if partner.street == street and partner.zip == zip and partner.city == city:
            return partner.id

        # si l'adresse passée en parametre n'est pas connue pour ce client, la rechercher dans tous les contacts associés au client
        contact = self.env['res.partner'].search([('parent_id', '=', partner.id),('street', '=', street),('zip', '=', zip),('city', '=', city)], limit=1)
        if contact:
            return contact.id

        # si l'adresse passée en parametre n'est pas connue pour le client, ni pour ces contacts associés, 
        # et si le client n'a pas d'adresse, alors mettre à jour le client avec l'adresse passée en parametre
        if not partner.street and not partner.zip and not partner.city:
            partner.write({'street': street,
                           'street2': street2,
                           'zip': zip,
                           'city': city,
                           'country_id': country_id,
                          })
            return partner.id
        # si l'adresse passée en parametre n'est pas connue pour le client, ni pour ces contacts associés, 
        # mais que le client a déjà une adresse, alors lui créer un nouveau contact avec l'adresse passée en parametre
        else:
            new_contact = self.env['res.partner'].create({'parent_id': partner.id,
                                                          'name': 'contact_from_BeL', #pour créer un partner, un nom est obligatoire
                                                          'type': 'delivery',
                                                          'street': street,
                                                          'street2': street2,
                                                          'zip': zip,
                                                          'city': city,
                                                          'country_id': country_id,
                                                        })
            return new_contact.id
            
    def _get_uom(self, product_uom):
        '''
        Get Odoo UOM ID based on the product UOM.

        Args:
        product_uom (str): uom name (ex: 'kg', 'botte','piece')

        Return:
        int: ID of instance of uom_uom
        '''
        uom_record = self.env['uom.uom'].search([('name', '=', product_uom)], limit=1)
        if uom_record:
            return uom_record.id
        else:
            raise UserError(_("No uom found in Odoo for {}. Please make sure that the uom is valid and exists in Odoo.".format(product_uom)))

    def _get_product(self, product_uom_id):
        '''
        Get Odoo "eshop generic" product ID based on the product UOM.

        Args:
        product_uom (int): ID of instance of uom_uom

        Return:
        int: ID of instance of product_product
        '''
        generic_product = self.env['product.product'].search([('categ_id', '=', 9),('uom_id','=',product_uom_id)], limit=1) #category 9 est la categorie "eshop" TODO mettre l'identifiant de la bdd en prod
        if generic_product:
            return generic_product
        else:
            raise UserError(_("No related generic product found in Odoo for {}".format(product_uom_id)))
  
    def _get_tax(self, tax):
        '''
        Get Odoo tax ID based on the tax rate.

        Args:
        tax (float): Taux de taxe, par exemple 5.5 pour 5,50%

        Return:
        int: ID de la taxe Odoo
        '''
        tax_record = self.env['account.tax'].search([('amount', '=', tax)], limit=1)
        if tax_record:
            return tax_record.id
        else:
            raise UserError(_("No tax rate found in Odoo for {}. Please make sure that the tax rate is valid and exists in Odoo. Example : 5.5 for 5,50% / 20 for 20%".format(tax)))

    def _get_payment_mode(self, eshop_payment_code):
        '''
        Get Odoo payment_mode ID based on the eshop invoice payment code.

        Args:
        eshop_payment_code (str): payment code ('CB' or 'VIR' or 'CH' or 'PREL')

        Return:
        int: ID of corresponding payment mode in Odoo
        '''
        payment_code_dict = {'CB':'CB',
                             'VIR':'Virement',
                             'CH':'Chèque',
                             'PREL':'Prélèment'}

        if eshop_payment_code in payment_code_dict :
            eshop_payment_mode = payment_code_dict[eshop_payment_code]
            odoo_payment_mode = self.env['account.payment.mode'].search([('name', '=', eshop_payment_mode)], limit=1)                    
            if odoo_payment_mode:
                return odoo_payment_mode.id
            else:
                raise UserError(_("No payment mode in Odoo for {}. Please contact administrator of Jardin'en Vie's Odoo".format(eshop_payment_code)))
        else:
            raise UserError(_("No payment mode in Odoo for {}.".format(eshop_payment_code)))             

    def _check_date_format(self, date):
        # regex pattern for format "yyyy-mm-dd"
        pattern = r"\d{4}-\d{2}-\d{2}"
        if re.match(pattern, date):
            return True
        return False

    def _get_invoice_line_value(self, customer_id, invoice_line):
        '''
        Build invoice line data from eshop invoice

        Cette fonction recherche le produit générique dans Odoo qui correspond aux produits de la boutique en ligne.
        Il y a plusieurs produits génériques "eshop" : un pour chaque unité de mesure
        1 - Trouver l'unité de mesure du produit
        2 - Trouver parmi les produits génériques "eshop" celui qui a la même unité de mesure
        3 - Associer ce produit générique à la ligne de facture

        '''
        # Get Odoo uom product id
        if 'product_uom' in invoice_line:
            product_uom_id = self._get_uom(invoice_line['product_uom'])
        else :            
            raise UserError(_("Missing 'product_uom' in invoice data JSON for the product : {}.". product_name))
        
        # Get eshop generic product in Odoo
        product = self._get_product(product_uom_id)

        # Find product name
        if 'product_name' in invoice_line:
            product_name = invoice_line['product_name']
        else :
            raise UserError(_("Missing 'product_name' in invoice data JSON."))

        tax_ids = []
        # Get Odoo tax id
        if 'tax' in invoice_line:
            tax_ids.append(self._get_tax(invoice_line['tax']))
        else :
            raise UserError(_("Missing 'tax' in invoice data JSON."))

        invoice_line_values = {
            'partner_id': customer_id,
            'product_id': product.id,
            'name': invoice_line['product_name'],
            'quantity': invoice_line['product_quantity'],
            'price_unit': invoice_line['product_price_unit'],
            'product_uom_id': product_uom_id,
            'tax_ids': [(6, 0, tax_ids)]
        }
        return invoice_line_values
        
    def _get_invoice_data(self, parsed_eshop_invoice_data):
        '''
        Build new invoice data from eshop api result
        '''
        # Get or create Odoo partner (as customer)
        if 'customer_email' in parsed_eshop_invoice_data:
            # Recherchez ou créez le client
            customer_name = parsed_eshop_invoice_data.get('customer_name', None)
            customer = self._get_or_create_customer(parsed_eshop_invoice_data['customer_email'], customer_name)
        else:
            raise UserError(_("Missing 'customer_email' in invoice data JSON."))

        #Find partner adress
        required_keys = ['customer_street', 'customer_zip', 'customer_city']
        if all(key in parsed_eshop_invoice_data for key in required_keys): # check if all 3 keys (street,zip,city) are in parsed_eshop_invoice_data keys
            street2 = parsed_eshop_invoice_data.get('customer_street2', None)
            if 'customer_country' in parsed_eshop_invoice_data:
                country_id = self._get_country_id(parsed_eshop_invoice_data['customer_country'])
            else :
                country_id = None

            #Set Odoo partner adress
            self._set_partner_address(customer, 
                                    parsed_eshop_invoice_data['customer_street'],
                                    street2,
                                    parsed_eshop_invoice_data['customer_zip'],
                                    parsed_eshop_invoice_data['customer_city'],
                                    country_id)
        else:
            missing_keys_str = ', '.join(["'{}'".format(key) for key in missing_keys])
            raise UserError(_("Missing {} in invoice data JSON.".format(missing_keys_str)))


       # Get or create Odoo partner delivery address
        required_keys = ['delivery_street', 'delivery_zip', 'delivery_city']
        if all(key in parsed_eshop_invoice_data for key in required_keys): # check if all 3 keys (street,zip,city) are in parsed_eshop_invoice_data keys
            street2 = parsed_eshop_invoice_data.get('delivery_street2', None)
            if 'delivery_country' in parsed_eshop_invoice_data:
                country_id = self._get_country_id(parsed_eshop_invoice_data['delivery_country'])
            else :
                country_id = None

            partner_shipping_id = self._get_or_create_delivery_address(customer, 
                                                                      parsed_eshop_invoice_data['delivery_street'],
                                                                      street2,
                                                                      parsed_eshop_invoice_data['delivery_zip'],
                                                                      parsed_eshop_invoice_data['delivery_city'],
                                                                      country_id)
        else:
            missing_keys_str = ', '.join(["'{}'".format(key) for key in missing_keys])
            raise UserError(_("Missing {} in invoice data JSON.".format(missing_keys_str)))

        # Get numero de facture
        if 'reference' in parsed_eshop_invoice_data:
            name = parsed_eshop_invoice_data['reference']
        else:
            raise UserError(_("Missing 'reference' in invoice data JSON."))   
        
        #Get payment mode
        if 'payment_mode' in parsed_eshop_invoice_data :
            payment_mode_id = self._get_payment_mode(parsed_eshop_invoice_data['payment_mode'])
        else :
            raise UserError(_("Missing 'payment_mode' in invoice data JSON."))

        # Get invoice date
        if 'invoice_date' in parsed_eshop_invoice_data:
            if self._check_date_format(parsed_eshop_invoice_data['invoice_date']):
                invoice_date = parsed_eshop_invoice_data['invoice_date']
            else:
                raise UserError(_("'invoice_date' has to be in format yyyy-mm-dd.")) 
        else:
            raise UserError(_("Missing 'invoice_date' in invoice data JSON.")) 

        # Get invoice date due
        if 'invoice_date_due' in parsed_eshop_invoice_data:
            if self._check_date_format(parsed_eshop_invoice_data['invoice_date_due']):
                invoice_date_due = parsed_eshop_invoice_data['invoice_date_due']
            else:
                raise UserError(_("'invoice_date_due' has to be in format yyyy-mm-dd.")) 
        else :
            raise UserError(_("Missing 'invoice_date_due' in invoice data JSON.")) 

        # Find eshop invoice lines
        if 'invoice_lines' in parsed_eshop_invoice_data:
            # Get all invoice lines values in eshop invoice
            invoice_lines_data = []
            for invoice_line in parsed_eshop_invoice_data['invoice_lines']:
                invoice_lines_data.append(self._get_invoice_line_value(customer.id, invoice_line))
        else:
            raise UserError(_("Missing 'invoice_lines' in invoice data JSON."))

        invoice_data = ({
            'name': name,
            'move_type': 'out_invoice', # pour que ma facture apparaisse en ligne, il faut que move_type =  'out_invoice'
            'invoice_date': invoice_date,
            'invoice_date_due': invoice_date_due,
            'partner_id': customer.id,
            'partner_shipping_id': partner_shipping_id,
            'payment_mode_id': payment_mode_id,
            'invoice_line_ids' : [(0, 0, d) for d in invoice_lines_data],
        })

        return invoice_data

    def _get_payment_state(self, parsed_eshop_invoice_data):
        '''
        get eshop invoice payment state

        Args:
        json form eshop

        Return: invoice payment state if 'paid' or 'not_paid' otherwise raise error
        '''

        if 'payment_state' in parsed_eshop_invoice_data:
            payment_state = parsed_eshop_invoice_data['payment_state']
            if payment_state not in ['paid', 'not_paid']:
                raise UserError(_("'payment_state' must be 'paid' or 'not_paid' in invoice data JSON."))
            else :
                return payment_state
        else:
            raise UserError(_("Missing 'payment_state' in invoice data JSON.")) 

    def _get_odoo_invoice(self, parsed_updated_invoice_data):
        '''
        get odoo invoice based on invoice ref

        Args:
        json form eshop

        Return:
        a odoo invoice instance
        '''
        
        # Find invoice name
        if 'reference' in parsed_updated_invoice_data:
            invoice_reference = parsed_updated_invoice_data['reference']
        else:
            raise UserError(_("Missing 'reference' in invoice data JSON.")) 

        #Get Odoo invoice
        invoice = self.env['account.move'].search([('name', '=', invoice_reference)], limit=1)
        if invoice:
            return invoice
        else:
            raise UserError(_("No invoice found in Odoo with ref : {}.".format(invoice_reference)))

    def _create_payments(self):
        '''
        create a singleton of account.payment.register model and call account.payment.register_create_payments()
        '''
        self.env['account.payment.register'].with_context(active_model='account.move', active_ids=self.id).create({
            'payment_date': self.date,
        })._create_payments()
        
    def create_invoice(self, eshop_invoice_data):
        '''
        Create invoice from eshop

        Args:
        eshop_invoice_data (JSON): invoice data from eshop in JSON format.
        '''
        try:
            # Check format of the api result
            parsed_eshop_invoice_data = json.loads(eshop_invoice_data)
            print(parsed_eshop_invoice_data)
        except json.decoder.JSONDecodeError as e:
            raise UserError(_("Invalid JSON format: %s" % str(e)))

        #Get invoice data
        invoice_data = self._get_invoice_data(parsed_eshop_invoice_data)

        #Create invoice
        invoice = self.env['account.move'].create(invoice_data)

        #Change state from 'draft' to 'posted'
        invoice.action_post()

        #Get payment state
        if self._get_payment_state(parsed_eshop_invoice_data) == 'paid':
            invoice._create_payments()

        return "Invoice created !"

    def update_invoice(self, eshop_updated_invoice_data):
        '''
        Update invoice from eshop

        Args:
        eshop_invoice_data (JSON): invoice data from eshop in JSON format.
        '''
        try:
            # Check format of the api result
            parsed_eshop_updated_invoice_data = json.loads(eshop_updated_invoice_data)
        except json.decoder.JSONDecodeError as e:
            raise UserError(_("Invalid JSON format: %s" % str(e)))

        #Get odoo invoice
        invoice = self._get_odoo_invoice(parsed_eshop_updated_invoice_data)

        #TODO est-ce que je dois ajouter la date de paiement?
        #Get payment state
        if self._get_payment_state(parsed_eshop_invoice_data) == 'paid':
            invoice._create_payments()

        return "Invoice updated !"

