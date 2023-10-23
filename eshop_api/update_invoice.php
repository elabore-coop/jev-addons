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

$invoice = array('reference' => 'num_de_facture_eshop', # (str) reference ou nom de facture (obligatoire)
                 'payment_state' => 'paid', # (str) status du paiement, 1 valeur possible : 'paid' (obligatoire)
                );

$json_invoice_data = json_encode($invoice);

//call api
$result = $models->execute_kw($db, $uid, $password, 'account.move', 'update_invoice', array(array(),$json_invoice_data));

echo(json_encode($result)) //success if $result = 0, else str

?>
