# Stock Simple + Inventaire

Module Odoo pour la gestion simple de stock et d'inventaires.

## Fonctionnalités

- Gestion des produits avec calcul automatique du stock total.
- Gestion des emplacements (internal, supplier, customer, inventory).
- Gestion des quants (stock par emplacement).
- Mouvements de stock avec validation et mise à jour automatique des quants.
- Inventaires avec génération automatique de mouvements d'ajustement.

## Installation

1. Copiez le dossier `simple_stock_inventory` dans votre répertoire d'addons Odoo (ex: `C:\odoo_custom_addons\`).
2. Ajoutez le chemin dans `odoo.conf` : `addons_path = C:\odoo_custom_addons`.
3. Redémarrez Odoo.
4. Activez le mode développeur.
5. Mettez à jour la liste des applications.
6. Installez le module "Stock Simple + Inventaire".

## Mise à jour après modification

- Utilisez la commande : `odoo-bin -c odoo.conf -d votre_db -u simple_stock_inventory --log-level=debug`.
- Ou via l'interface : Applications > Mettre à jour.

## Logs

Pour voir les logs : `odoo-bin -c odoo.conf --log-level=debug`.
