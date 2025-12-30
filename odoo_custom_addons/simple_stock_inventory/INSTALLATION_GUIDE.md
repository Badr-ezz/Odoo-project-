# 📦 Guide d'Installation - Stock Simple + Inventaire

## Table des matières
1. [Prérequis](#prérequis)
2. [Installation du module](#installation-du-module)
3. [Configuration d'Odoo](#configuration-dodoo)
4. [Activation du module](#activation-du-module)
5. [Configuration des permissions](#configuration-des-permissions)
6. [Utilisation du module](#utilisation-du-module)
7. [Mise à jour du module](#mise-à-jour-du-module)
8. [Dépannage](#dépannage)

---

## Prérequis

Avant d'installer ce module, assurez-vous d'avoir :

| Élément | Description |
|---------|-------------|
| **Odoo** | Version 14, 15, 16, 17 ou 18 installée sur Windows |
| **PostgreSQL** | Base de données configurée et fonctionnelle |
| **Accès administrateur** | Droits d'administration sur Odoo et Windows |
| **Python** | Installé avec Odoo (généralement automatique) |

---

## Installation du module

### Étape 1 : Créer un dossier pour les modules personnalisés

Créez un dossier pour vos modules Odoo personnalisés si ce n'est pas déjà fait :

```
C:\odoo_custom_addons\
```

> 💡 **Conseil** : Évitez les espaces et les caractères spéciaux dans le chemin.

### Étape 2 : Copier le module

Copiez le dossier complet `simple_stock_inventory` dans votre dossier d'addons :

```
C:\odoo_custom_addons\simple_stock_inventory\
```

La structure finale doit ressembler à :

```
C:\odoo_custom_addons\
└── simple_stock_inventory\
    ├── __init__.py
    ├── __manifest__.py
    ├── README.md
    ├── data\
    │   └── data.xml
    ├── models\
    │   ├── __init__.py
    │   ├── inventory.py
    │   ├── location.py
    │   ├── move.py
    │   ├── product.py
    │   └── quant.py
    ├── security\
    │   ├── ir.model.access.csv
    │   └── security.xml
    ├── static\
    │   └── description\
    └── views\
        ├── inventory_views.xml
        ├── location_views.xml
        ├── menus.xml
        ├── move_views.xml
        └── product_views.xml
```

---

## Configuration d'Odoo

### Étape 3 : Localiser le fichier odoo.conf

Le fichier de configuration `odoo.conf` se trouve généralement dans :

- `C:\Program Files\Odoo 17.0\server\odoo.conf`
- `C:\Program Files\Odoo\server\odoo.conf`
- `C:\Users\<VotreNom>\odoo\odoo.conf`

### Étape 4 : Modifier le fichier odoo.conf

1. **Ouvrez** `odoo.conf` avec un éditeur de texte (en mode administrateur)

2. **Recherchez** la ligne `addons_path`

3. **Ajoutez** votre dossier personnalisé à la fin, séparé par une virgule :

**Avant :**
```ini
addons_path = C:\Program Files\Odoo 17.0\server\odoo\addons,C:\Program Files\Odoo 17.0\server\addons
```

**Après :**
```ini
addons_path = C:\Program Files\Odoo 17.0\server\odoo\addons,C:\Program Files\Odoo 17.0\server\addons,C:\odoo_custom_addons
```

4. **Enregistrez** le fichier

### Étape 5 : Redémarrer le service Odoo

#### Option A : Via les Services Windows

1. Appuyez sur `Win + R`
2. Tapez `services.msc` et appuyez sur Entrée
3. Trouvez le service **"Odoo"** ou **"odoo-server-17.0"**
4. Clic droit → **Redémarrer**

#### Option B : Via l'invite de commandes (Administrateur)

```cmd
net stop odoo-server-17.0
net start odoo-server-17.0
```

#### Option C : Lancement manuel (pour développement)

```cmd
cd "C:\Program Files\Odoo 17.0\server"
python odoo-bin -c odoo.conf
```

---

## Activation du module

### Étape 6 : Se connecter à Odoo

1. Ouvrez votre navigateur web
2. Accédez à `http://localhost:8069`
3. Connectez-vous avec un compte **administrateur**

### Étape 7 : Activer le mode développeur

1. Allez dans **Paramètres** (Settings)
2. Faites défiler jusqu'en bas de la page
3. Cliquez sur **Activer le mode développeur**

> 💡 **Alternative rapide** : Ajoutez `?debug=1` à l'URL :  
> `http://localhost:8069/web?debug=1`

### Étape 8 : Mettre à jour la liste des applications

1. Allez dans le menu **Applications** (Apps)
2. Cliquez sur le menu **☰** ou **⋮** en haut
3. Sélectionnez **Mettre à jour la liste des applications**
4. Confirmez en cliquant sur **Mettre à jour**

### Étape 9 : Installer le module

1. Dans le menu **Applications**
2. **Supprimez le filtre "Applications"** dans la barre de recherche (important !)
3. Recherchez **"Stock Simple"** ou **"simple_stock_inventory"**
4. Cliquez sur le bouton **Installer**

![Installation](https://via.placeholder.com/600x100?text=Cliquez+sur+Installer)

---

## Configuration des permissions

### Étape 10 : Attribuer les droits aux utilisateurs

Après l'installation, configurez les permissions :

1. Allez dans **Paramètres** → **Utilisateurs et Compagnies** → **Utilisateurs**
2. Sélectionnez un utilisateur
3. Dans l'onglet **Droits d'accès**, vous trouverez deux groupes :

| Groupe | Permissions |
|--------|-------------|
| **Stock Simple / Utilisateur** | Lecture, création, modification (pas de suppression) |
| **Stock Simple / Manager** | Accès complet (lecture, création, modification, suppression) |

4. Cochez le groupe approprié
5. Cliquez sur **Enregistrer**

---

## Utilisation du module

### Menu principal

Après installation, un nouveau menu **"Stock Simple"** apparaît dans la barre de navigation avec :

| Sous-menu | Description |
|-----------|-------------|
| **Produits** | Gérer les produits avec prix, codes-barres et stock automatique |
| **Emplacements** | Gérer les emplacements de stockage |
| **Mouvements** | Enregistrer les entrées, sorties et transferts de stock |
| **Inventaires** | Effectuer des inventaires physiques |

### Emplacements par défaut

Le module crée automatiquement 4 emplacements :

| Emplacement | Usage | Description |
|-------------|-------|-------------|
| **Stock** | Interne | Emplacement principal de stockage |
| **Fournisseurs** | Fournisseur | Source pour les réceptions |
| **Clients** | Client | Destination pour les livraisons |
| **Ajustement Inventaire** | Inventaire | Pour les corrections de stock |

### Workflow des mouvements

```
┌─────────────┐     Valider      ┌─────────────┐
│  Brouillon  │ ───────────────► │   Validé    │
│   (draft)   │                  │   (done)    │
└─────────────┘                  └──────┬──────┘
                                        │
                                   Annuler
                                        │
                                        ▼
                                 ┌─────────────┐
                                 │   Annulé    │
                                 │  (cancel)   │
                                 └─────────────┘
```

### Workflow des inventaires

1. **Créer** un nouvel inventaire
2. **Sélectionner** l'emplacement à inventorier
3. Cliquer sur **"Ajouter tous les produits"**
4. **Saisir** les quantités comptées
5. Cliquer sur **"Valider inventaire"**
6. Les mouvements d'ajustement sont créés automatiquement

---

## Mise à jour du module

### Après modification du code

#### Via ligne de commande (recommandé)

```cmd
cd "C:\Program Files\Odoo 17.0\server"
python odoo-bin -c odoo.conf -d votre_base_de_donnees -u simple_stock_inventory
```

#### Via l'interface Odoo

1. Allez dans **Applications**
2. Recherchez **"Stock Simple"**
3. Cliquez sur le menu **⋮** du module
4. Sélectionnez **Mettre à niveau**

---

## Dépannage

### Problème : Le module n'apparaît pas dans la liste

**Solutions :**
1. Vérifiez que le chemin dans `odoo.conf` est correct
2. Assurez-vous d'avoir supprimé le filtre "Applications" dans la recherche
3. Redémarrez complètement Odoo
4. Mettez à jour la liste des applications

### Problème : Erreur lors de l'installation

**Solutions :**
1. Consultez les logs Odoo :
   ```cmd
   python odoo-bin -c odoo.conf --log-level=debug
   ```
2. Vérifiez que tous les fichiers sont présents
3. Vérifiez la syntaxe des fichiers XML et Python

### Problème : Erreur "Access Denied"

**Solutions :**
1. Vérifiez que vous êtes connecté en tant qu'administrateur
2. Attribuez les permissions appropriées à votre utilisateur

### Problème : Les menus ne s'affichent pas

**Solutions :**
1. Rafraîchissez la page (Ctrl + F5)
2. Videz le cache du navigateur
3. Reconnectez-vous à Odoo

### Consulter les logs

Pour voir les logs détaillés :

```cmd
cd "C:\Program Files\Odoo 17.0\server"
python odoo-bin -c odoo.conf --log-level=debug
```

---

## Informations techniques

| Propriété | Valeur |
|-----------|--------|
| **Nom technique** | `simple_stock_inventory` |
| **Version** | 1.0 |
| **Dépendances** | `base`, `mail` |
| **Licence** | LGPL-3 |
| **Catégorie** | Inventory |

### Modèles créés

| Modèle | Nom technique | Description |
|--------|---------------|-------------|
| Produit | `ssi.product` | Gestion des produits |
| Emplacement | `ssi.location` | Emplacements de stock |
| Quant | `ssi.quant` | Stock par emplacement |
| Mouvement | `ssi.move` | Mouvements de stock |
| Inventaire | `ssi.inventory` | Inventaires physiques |
| Ligne inventaire | `ssi.inventory.line` | Lignes d'inventaire |

---

## Support

Pour toute question ou problème :

1. Consultez ce guide
2. Vérifiez les logs Odoo
3. Consultez la documentation officielle Odoo : https://www.odoo.com/documentation

---

*Guide créé le 28 décembre 2025*
