# gfcodex

Documentation publique du site [GFCodex.com](https://gfcodex.com) — base de données communautaire et gratuite pour le jeu Grand Fantasia (ORIGIN, GLOBAL, VIOLET, GENESIS, EXILE).

Ce dépôt contient un site statique (HTML/CSS pur, sans dépendance de build) prêt à être publié sur GitHub Pages.

## Consulter la documentation

Ouvrir `index.html` (localement ou via GitHub Pages une fois publié).

## Publier sur GitHub Pages

1. Pousser ce dépôt sur GitHub.
2. Dans les paramètres du dépôt : **Settings → Pages**.
3. Source : `Deploy from a branch`.
4. Branche : `main`, dossier : `/ (root)`.
5. Enregistrer — le site sera disponible à `https://<utilisateur-ou-organisation>.github.io/<nom-du-depot>/`.

Aucune étape de build n'est nécessaire : les fichiers `.html` sont servis tels quels.

## Régénérer les pages

Les pages sont générées à partir de `scripts/build.py` (Python, aucune dépendance externe) pour garder le menu de navigation cohérent sur toutes les pages :

```
python scripts/build.py
```

Modifier les données de contenu directement dans ce script, puis relancer la commande.

## Structure

- `index.html` — page d'accueil
- `codex/` — une page par catalogue du Codex (objets, compétences, monstres, PNJ, quêtes, titres, enchantements, elfes, cartes, recherche globale)
- `ressources/` — une page par guide (cabine d'essayage, hauts faits, agenda, archives, récoltes de sprites, XP, combinaisons, spécialisations, talents, changelog)
- `a-propos/` — fonctionnement du site et politique de confidentialité
- `assets/style.css` — feuille de style partagée

Contenu en français. Traduction dans d'autres langues à faire ultérieurement.
