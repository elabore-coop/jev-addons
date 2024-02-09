# Copyright 2022 Stéphan Sainléger (Elabore)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "JEV : PLU code in pricelist rules",
    "version": "16.0.1.0.0",
    "author": "Elabore",
    "website": "",
    "maintainer": "Laetitia Da Costa",
    "license": "AGPL-3",
    "category": "",
    "summary": "add PLU field in pricelist item model",
    "description": """
   :image: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3
=================
jev_plu
=================

add PLU code in pricelist rules in order to indicated which PLU code corresponds to the pricelist rule

Installation
============

Install ``jev_plu``, all dependencies will be installed by default.

Known issues / Roadmap
======================

None yet.

Bug Tracker
===========

Bugs are tracked on `our issues website
<https://github.com/elabore-coop/jev-addons/issues>`_. In case of
trouble, please check there if your issue has already been
reported. If you spotted it first, help us smashing it by providing a
detailed and welcomed feedback.

Credits
=======

Images
------

* Elabore: `Icon <https://elabore.coop/web/image/res.company/1/logo?unique=f3db262>`_.

Contributors
------------

* Laetitia Da Costa


Funders
-------

The development of this module has been financially supported by:
* Elabore (https://elabore.coop)


Maintainer
----------
This module is maintained by Elabore.

""",
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "product",
    ],
    "qweb": [
        # "static/src/xml/*.xml",
    ],
    "external_dependencies": {
        "python": [],
    },
    # always loaded
    "data": [
        "views/product_product_views.xml"
    ],
    # only loaded in demonstration mode
    "demo": [],
    "js": [],
    "css": [],
    "installable": True,
    # Install this module automatically if all dependency have been previously
    # and independently installed.  Used for synergetic or glue modules.
    "auto_install": False,
    "application": True,
}