# -*- coding: utf-8 -*-
"""
Générateur du site statique de documentation GFCodex.
Usage : python build.py
Produit des fichiers .html purs (aucune dépendance requise pour les consulter,
ce script sert uniquement à éviter de dupliquer le menu à la main).
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NAV = [
    ("Accueil", "index.html", None),
    ("Codex", None, [
        ("Objets", "codex/objets.html"),
        ("Compétences", "codex/competences.html"),
        ("Monstres", "codex/monstres.html"),
        ("PNJ", "codex/pnjs.html"),
        ("Quêtes", "codex/quetes.html"),
        ("Titres", "codex/titres.html"),
        ("Effets d'enchantement", "codex/enchantements.html"),
        ("Sprites (Elfes)", "codex/elfes.html"),
        ("Cartes", "codex/cartes.html"),
        ("Recherche globale", "codex/recherche.html"),
    ]),
    ("Guides & Ressources", None, [
        ("Cabine d'essayage", "ressources/cabine-essayage.html"),
        ("Hauts faits (Succès)", "ressources/hauts-faits.html"),
        ("Agenda des activités", "ressources/agenda.html"),
        ("Archives (Collections)", "ressources/archives.html"),
        ("Récoltes de sprites", "ressources/recoltes-sprites.html"),
        ("Valeur d'XP par niveau", "ressources/experience.html"),
        ("Combinaisons d'objets", "ressources/combinaisons.html"),
        ("Guide des spés (Masters)", "ressources/specialisations.html"),
        ("Combinaisons de talents", "ressources/talents.html"),
        ("Changelog", "ressources/changelog.html"),
    ]),
    ("À propos", None, [
        ("Comment fonctionne GFCodex", "a-propos/fonctionnement.html"),
        ("Politique de confidentialité", "a-propos/confidentialite.html"),
    ]),
]

HEAD = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Documentation GFCodex</title>
<meta name="description" content="{description}">
<link rel="stylesheet" href="{rel}assets/style.css">
</head>
<body>
<div class="layout">
<header class="topbar">
  <div class="topbar-inner">
    <a class="brand" href="{rel}index.html">GFCodex<span class="dot">.</span>Docs</a>
    <button class="menu-toggle" type="button" onclick="document.querySelector('nav.main-nav').classList.toggle('open')">Menu ☰</button>
    <nav class="main-nav">
{nav_html}
    </nav>
  </div>
</header>
<main>
{content}
<footer class="page-footer">
  <p>Documentation du site GFCodex — Grand Fantasia est une marque de X-LEGEND Entertainment Co., Ltd.</p>
</footer>
</main>
</div>
</body>
</html>
"""

def rel_prefix(path):
    depth = path.count("/")
    return "../" * depth

def build_nav_html(current_path, rel):
    out = []
    for entry in NAV:
        label, href, children = entry
        if children is None:
            active = " active" if href == current_path else ""
            out.append(f'      <div class="nav-single"><a class="{active.strip()}" href="{rel}{href}">{label}</a></div>')
        else:
            group_active = any(chref == current_path for _, chref in children)
            active = " active" if group_active else ""
            out.append(f'      <div class="nav-group">')
            out.append(f'        <a href="{rel}{children[0][1]}" class="{active.strip()}">{label}</a>')
            out.append(f'        <ul class="dropdown">')
            for clabel, chref in children:
                cactive = " active" if chref == current_path else ""
                out.append(f'          <li><a class="{cactive.strip()}" href="{rel}{chref}">{clabel}</a></li>')
            out.append("        </ul>")
            out.append("      </div>")
    return "\n".join(out)

def page(path, title, description, content):
    rel = rel_prefix(path)
    nav_html = build_nav_html(path, rel)
    html = HEAD.format(title=title, description=description, rel=rel, nav_html=nav_html, content=content)
    full_path = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("écrit :", path)

# ---------------------------------------------------------------------------
# CONTENU DES PAGES
# ---------------------------------------------------------------------------

def card(title, href, desc):
    return f'''<div class="card"><h3><a href="{href}">{title}</a></h3><p>{desc}</p></div>'''

# ----- INDEX -----
page("index.html", "Accueil", "Documentation publique du site GFCodex, base de données pour Grand Fantasia.", f'''
<h1>Bienvenue sur la documentation de GFCodex</h1>
<p class="lead">GFCodex est une base de données communautaire et gratuite pour le jeu <strong>Grand Fantasia</strong>, couvrant les versions ORIGIN, GLOBAL, VIOLET, GENESIS et EXILE (serveurs officiels et privés). Cette documentation présente toutes les pages du site, leur contenu et leur utilisation.</p>

<div class="callout">Le site propose un sélecteur de version en haut de page (ORIGIN / GLOBAL / VIOLET / GENESIS / EXILE) : les données affichées (objets, monstres, quêtes, etc.) s'adaptent à la version choisie, car le contenu du jeu diffère d'une version à l'autre.</div>

<h2>Codex — bases de données du jeu</h2>
<div class="card-grid">
{card("Objets", "codex/objets.html", "Recherche et filtre tous les objets du jeu : équipements, consommables, matériaux, etc.")}
{card("Compétences", "codex/competences.html", "Compétences de chaque classe et spécialisation, avec leurs effets.")}
{card("Monstres", "codex/monstres.html", "Fiches des monstres, butins et statistiques par type.")}
{card("PNJ", "codex/pnjs.html", "Liste des personnages non-joueurs et leur localisation.")}
{card("Quêtes", "codex/quetes.html", "Quêtes du jeu filtrables par faction/réputation.")}
{card("Titres", "codex/titres.html", "Titres de personnage classés par couleur/rareté.")}
{card("Effets d'enchantement", "codex/enchantements.html", "Effets d'enchantement applicables à l'équipement.")}
{card("Sprites (Elfes)", "codex/elfes.html", "Compagnons Elfes classés par tribu.")}
{card("Cartes", "codex/cartes.html", "Cartes et zones du monde de Grand Fantasia.")}
{card("Recherche globale", "codex/recherche.html", "Recherche unique dans toutes les catégories du Codex.")}
</div>

<h2>Guides & Ressources</h2>
<div class="card-grid">
{card("Cabine d'essayage", "ressources/cabine-essayage.html", "Essayez équipements, costumes et montures sur un personnage 3D.")}
{card("Hauts faits (Succès)", "ressources/hauts-faits.html", "Guide des succès du jeu et leurs récompenses.")}
{card("Agenda des activités", "ressources/agenda.html", "Événements et activités en cours dans le jeu.")}
{card("Archives (Collections)", "ressources/archives.html", "Suivi des collections à compléter.")}
{card("Récoltes de sprites", "ressources/recoltes-sprites.html", "Guide de récolte pour les compagnons Elfes.")}
{card("Valeur d'XP par niveau", "ressources/experience.html", "Courbes d'expérience nécessaires par palier de niveaux.")}
{card("Combinaisons d'objets", "ressources/combinaisons.html", "Recherche des recettes de combinaison/craft d'objets.")}
{card("Guide des spés (Masters)", "ressources/specialisations.html", "Spécialisations disponibles par classe.")}
{card("Combinaisons de talents", "ressources/talents.html", "Builds de talents recommandés par classe.")}
{card("Changelog", "ressources/changelog.html", "Historique des mises à jour du site et des données.")}
</div>
''')

# ----- CODEX PAGES -----
codex_pages = [
    ("codex/objets.html", "Objets", "Codex des objets", "Objets",
     "Le Codex des objets recense l'ensemble des objets du jeu : armes, armures, costumes, montures, consommables, matériaux de craft, objets de quête, etc.",
     ["Recherche par nom et filtres par catégorie/sous-catégorie d'objet (accessibles aussi depuis le menu déroulant « Objets »).",
      "Chaque fiche objet détaille ses statistiques, son niveau requis, sa description et, selon le type d'objet, ses sources d'obtention.",
      "Un aperçu (tooltip) apparaît au survol des objets référencés ailleurs sur le site (quêtes, monstres, combinaisons…)."]),
    ("codex/competences.html", "Compétences", "Codex des compétences", "Compétences",
     "Le Codex des compétences liste les compétences actives et passives de chaque classe et de leurs spécialisations.",
     ["Filtre par classe et sous-classe via le menu déroulant « Compétences », organisé selon l'arbre de classes du jeu.",
      "Chaque fiche détaille les effets, le coût et les prérequis de la compétence."]),
    ("codex/monstres.html", "Monstres", "Codex des monstres", "Monstres",
     "Le Codex des monstres regroupe tous les monstres rencontrables dans Grand Fantasia.",
     ["Filtre par type de monstre (menu déroulant « Monstres »).",
      "Chaque fiche présente les statistiques du monstre et la liste de ses butins possibles."]),
    ("codex/pnjs.html", "PNJ", "Codex des PNJ", "PNJ",
     "Le Codex des PNJ (personnages non-joueurs) recense marchands, dresseurs de compétences, donneurs de quêtes et autres personnages du jeu.",
     ["Filtre par carte/zone d'apparition via le menu déroulant « PNJ ».",
      "Chaque fiche indique la localisation du PNJ et, le cas échéant, les quêtes ou services qu'il propose."]),
    ("codex/quetes.html", "Quêtes", "Codex des quêtes", "Quêtes",
     "Le Codex des quêtes liste les quêtes disponibles dans le jeu, avec leurs objectifs et récompenses.",
     ["Filtre par faction/réputation associée à la quête (menu déroulant « Quêtes »).",
      "Chaque fiche détaille le déroulé de la quête, les prérequis et les récompenses obtenues."]),
    ("codex/titres.html", "Titres", "Codex des titres", "Titres",
     "Le Codex des titres liste les titres de personnage disponibles dans le jeu, classés par couleur de rareté.",
     ["Filtre par couleur/rareté du titre (menu déroulant « Titres »).",
      "Chaque fiche indique les bonus procurés par le titre et comment l'obtenir."]),
    ("codex/enchantements.html", "Effets d'enchantement", "Codex des enchantements", "Effets d'enchantement",
     "Le Codex des enchantements recense les effets pouvant être appliqués à l'équipement (statistiques bonus, effets spéciaux).",
     ["Recherche et consultation de tous les effets d'enchantement disponibles dans le jeu."]),
    ("codex/elfes.html", "Sprites (Elfes)", "Codex des elfes", "Sprites (Elfes)",
     "Le Codex des Elfes présente les compagnons Elfes (« sprites ») du jeu, classés par tribu.",
     ["Filtre par tribu d'Elfe via le menu déroulant « Sprites ».",
      "Chaque fiche détaille les caractéristiques et compétences propres à l'Elfe."]),
    ("codex/cartes.html", "Cartes", "Codex des cartes", "Cartes",
     "Le Codex des cartes recense les zones et cartes du monde de Grand Fantasia.",
     ["Recherche et filtres pour retrouver une carte précise.",
      "Chaque fiche de carte peut être utilisée pour identifier la zone d'apparition de monstres, PNJ ou ressources."]),
    ("codex/recherche.html", "Recherche globale", "Recherche globale", "Recherche globale",
     "La recherche globale, accessible depuis la barre de recherche en haut de chaque page (ou via le raccourci clavier <strong>Ctrl + K</strong>), interroge simultanément toutes les catégories du Codex (objets, monstres, quêtes, PNJ, compétences, cartes, etc.).",
     ["Tapez au moins 3 caractères puis validez avec la touche Entrée pour lancer la recherche.",
      "Les résultats sont regroupés par catégorie pour un accès rapide à la fiche correspondante."]),
]

for path, title, h1, menu_name, intro, points in codex_pages:
    lis = "\n".join(f"<li>{p}</li>" for p in points)
    page(path, title, f"{h1} — GFCodex", f'''
<div class="breadcrumb"><a href="../index.html">Accueil</a> / Codex / {menu_name}</div>
<h1>{h1}</h1>
<p class="lead">{intro}</p>
<h2>Fonctionnalités</h2>
<ul>{lis}</ul>
''')

# ----- RESSOURCES PAGES -----
res_pages = [
    ("ressources/cabine-essayage.html", "Cabine d'essayage", "Cabine d'essayage", "Cabine d'essayage",
     "La cabine d'essayage permet de visualiser en 3D le rendu d'équipements, costumes et montures sur un personnage, avant de les obtenir en jeu.",
     ["Choix du genre du personnage (masculin/féminin).",
      "Ajout d'objets d'équipement, costumes et montures pour composer une tenue.",
      "Partage de la tenue composée via un lien copiable.",
      "Fonctionnalité disponible uniquement avec les données de la version GLOBAL (un bouton permet de basculer automatiquement sur cette version si besoin)."]),
    ("ressources/hauts-faits.html", "Hauts faits (Succès)", "Guide des hauts faits", "Hauts faits (Succès)",
     "Ce guide recense les hauts faits (succès) du jeu ainsi que les récompenses associées à leur accomplissement.",
     ["Parcours des catégories de succès et de leurs conditions d'obtention."]),
    ("ressources/agenda.html", "Agenda des activités", "Agenda des activités", "Agenda")
    ,
    ("ressources/archives.html", "Archives (Collections)", "Guide des collections", "Archives (Collections)",
     "Ce guide aide à suivre la progression dans les collections d'objets du jeu (archives) à compléter.",
     ["Suivi des ensembles d'objets à collectionner et de leurs récompenses de complétion."]),
    ("ressources/recoltes-sprites.html", "Récoltes de sprites", "Guide des récoltes de sprites", "Récoltes de sprites",
     "Ce guide détaille les récoltes réalisables grâce aux compagnons Elfes (sprites), utiles pour obtenir certaines ressources.",
     ["Présentation des types de récolte disponibles selon la tribu de l'Elfe."]),
    ("ressources/experience.html", "Valeur d'XP par niveau", "Valeur d'expérience par niveau", "Valeur d'XP par niveau",
     "Cette page présente, sous forme de graphique, la quantité d'expérience nécessaire pour progresser à chaque niveau de personnage.",
     ["Navigation par onglets correspondant à des paliers de niveaux.",
      "Les valeurs affichées s'adaptent à la version du jeu sélectionnée (ORIGIN / GLOBAL / VIOLET / GENESIS / EXILE)."]),
    ("ressources/combinaisons.html", "Combinaisons d'objets", "Combinaisons d'objets", "Combinaisons d'objets",
     "Cette page permet de rechercher les recettes de combinaison (craft) d'objets : quels objets sont nécessaires pour en fabriquer un autre.",
     ["Barre de recherche par nom d'objet.",
      "Filtres additionnels pour affiner les résultats de combinaisons."]),
    ("ressources/specialisations.html", "Guide des spés (Masters)", "Guide des spécialisations", "Guide des spés (Masters)",
     "Ce guide présente les spécialisations (« masters ») disponibles pour chaque classe du jeu.",
     ["Sélection de la classe via une barre d'icônes en haut de page.",
      "Détail des spécialisations propres à la classe choisie."]),
    ("ressources/talents.html", "Combinaisons de talents", "Combinaisons de talents", "Combinaisons de talents",
     "Ce guide propose des combinaisons (builds) de talents recommandées pour chaque classe.",
     ["Sélection de la classe via une barre d'icônes en haut de page.",
      "Détail des talents conseillés selon la classe choisie."]),
    ("ressources/changelog.html", "Changelog", "Changelog", "Changelog",
     "Cette page recense l'historique des mises à jour du site GFCodex et de ses données, classées par version du jeu.",
     ["Consultation chronologique des changements apportés au site et aux bases de données."]),
]

for entry in res_pages:
    if len(entry) == 4:
        path, title, h1, menu_name = entry
        page(path, title, f"{h1} — GFCodex", f'''
<div class="breadcrumb"><a href="../index.html">Accueil</a> / Ressources / {menu_name}</div>
<h1>{h1}</h1>
<p class="lead">Cette page présente les événements et activités actuellement disponibles dans Grand Fantasia (événements temporaires, activités récurrentes).</p>
<h2>Fonctionnalités</h2>
<ul><li>Vue d'ensemble des activités en cours avec leur période de disponibilité.</li></ul>
''')
        continue
    path, title, h1, menu_name, intro, points = entry
    lis = "\n".join(f"<li>{p}</li>" for p in points)
    page(path, title, f"{h1} — GFCodex", f'''
<div class="breadcrumb"><a href="../index.html">Accueil</a> / Ressources / {menu_name}</div>
<h1>{h1}</h1>
<p class="lead">{intro}</p>
<h2>Fonctionnalités</h2>
<ul>{lis}</ul>
''')

# ----- À PROPOS -----
page("a-propos/fonctionnement.html", "Comment fonctionne GFCodex", "Comment fonctionne GFCodex", '''
<div class="breadcrumb"><a href="../index.html">Accueil</a> / À propos / Fonctionnement</div>
<h1>Comment fonctionne GFCodex</h1>
<p class="lead">GFCodex est un site communautaire, gratuit et non affilié à l'éditeur du jeu, qui met à disposition des joueurs de Grand Fantasia une base de données consultable en ligne.</p>

<h2>Sources des données</h2>
<p>Les données affichées (objets, monstres, quêtes, compétences, cartes, etc.) sont extraites des fichiers du jeu et mises à jour à chaque nouvelle version disponible. Un panneau accessible depuis l'icône « info » (en haut de page) indique, pour chaque version du jeu (ORIGIN, GLOBAL, VIOLET, GENESIS, EXILE), si la base de données du site est à jour par rapport aux fichiers du jeu, ainsi que la date de la dernière vérification.</p>

<h2>Versions du jeu prises en charge</h2>
<p>Grand Fantasia existe sous plusieurs versions (ORIGIN, GLOBAL, VIOLET, GENESIS, EXILE), dont le contenu diffère. GFCodex permet de basculer entre ces versions via les boutons situés en haut de chaque page ; les données affichées (objets, monstres, compétences, sprites, etc..) s'adaptent automatiquement à la version choisie.</p>

<h2>Langues</h2>
<p>Le site est disponible en plusieurs langues, sélectionnables via le menu de langue en haut de page.</p>

<h2>Équipe</h2>
<p>GFCodex est développé et maintenu par une petite équipe de bénévoles de la communauté (développement, gestion des fichiers de données, hébergement). Le site est financé par les dons de la communauté.</p>

<h2>Liens utiles</h2>
<ul>
<li>Discord de la communauté (lien disponible depuis le pied de page du site).</li>
<li>Dons via Liberapay (lien disponible en haut et en bas de page).</li>
<li>Code source sur GitHub (lien disponible en pied de page).</li>
</ul>
''')

page("a-propos/confidentialite.html", "Politique de confidentialité", "Politique de confidentialité", '''
<div class="breadcrumb"><a href="../index.html">Accueil</a> / À propos / Confidentialité</div>
<h1>Politique de confidentialité</h1>
<p class="lead">GFCodex propose une page dédiée à la politique de confidentialité, accessible depuis le pied de page du site (lien « Politique de confidentialité »).</p>
<p>Cette page détaille les données éventuellement collectées lors de la navigation sur le site et la manière dont elles sont utilisées. Pour le contenu exact et à jour de cette politique, veuillez consulter directement la page correspondante sur le site GFCodex.</p>
''')

print("\nGénération terminée.")
