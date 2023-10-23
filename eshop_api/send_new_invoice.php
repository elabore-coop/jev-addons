<?php

$url = 'https://mon-eshop.com';
$db = 'mon_odoo';
$username = 'eshop@jardinenvie.org';
$password = 'mon_mdp';

require_once('ripcord/ripcord.php');

// Create a connection to the Odoo XML-RPC server
$common = ripcord::client("$url/xmlrpc/2/common");
$version = $common->version();

// Authenticate and obtain the user ID (uid)
$uid = $common->authenticate($db, $username, $password, array());

// Create a connection to the Odoo object (models) XML-RPC server
$models = ripcord::client("$url/xmlrpc/2/object");

$invoice = array('customer_email' => 'my_customer@email.com', # (str) (obligatoire)
                 'customer_name' => 'customer_name', # (str) (obligatoire)
                 'customer_street' => '1 rue des Cêdres', # (str) adresse du client (obligatoire)
                 'customer_street2' => 'BP 10000', # (str) adresse du client (optionnel)
                 'customer_zip' => '75001', # (str) code postal du client (obligatoire)
                 'customer_city' => 'Paris', # (str) ville du client (obligatoire)
                 'customer_country' => 'FR', # (str) Code pays du client - exemple : BE pour Belgique (optionnel)
                 'delivery_street' => '1 rue des Cêdres', # (str) adresse de livraison (obligatoire)
                 'delivery_street2' => 'BP 10000', # (str) adresse de livraison (optionnel)
                 'delivery_zip' => '75001', # (str) code postal de livraison (obligatoire)
                 'delivery_city' => 'Paris', # (str) ville de livraison (obligatoire)
                 'delivery_country' => 'FR', # (str) Code pays de livraison - exemple : BE pour Belgique (optionnel)
                 'invoice_date' => '2023-10-18', # (str) date de facturation au format 'yyyy-mm-dd' (obligatoire)
                 'reference' => 'num_de_facture_eshop', # (str) reference ou nom de facture (obligatoire)
                 'payment_state' => 'not_paid', # (str) status du paiement, 2 valeurs possibles : 'not_paid' ou 'paid' (obligatoire)
                 'invoice_date_due' => '2023-10-23', # (str) date d'échéance du paiement au format 'yyyy-mm-dd' (obligatoire)
                 'payment_mode' => 'CH', # (str) mode de paiement, 4 valeurs possibles : 'CB' pour les CB, 'CH' pour les chèques, 'PREL' pour les prélèvement, 'VIR' pour les virement (obligatoire)
                 'invoice_lines' => array(
                                        array(
                                            'product_name' => 'Tomate', # (str) nom du produit (obligatoire)
                                            'product_quantity' => 2, # (float) quantité (obligatoire)
                                            'product_price_unit' => 5.40, # (float) prix unitaire (obligatoire)
                                            'product_uom' => 'kg', # (str) unité de mesure (obligatoire)
                                            'tax' => 5.5, # (float) Taux de TVA. Par example : 5.5 pour 5,50% / 20 pour 20%
                                        ),
                                        array(
                                            'product_name' => 'Carottes',
                                            'product_quantity' => 4,
                                            'product_price_unit' => 3.50,
                                            'product_uom' => 'Botte',
                                            'tax' => 20,
                                        ),
                                    ), 
                );

$json_invoice_data = json_encode($invoice);

//call api
$result = $models->execute_kw($db, $uid, $password, 'account.move', 'create_invoice', array(array(),$json_invoice_data));

echo(json_encode($result)) //success if $result = 0, else str

?>
