# Observatoire du nucléaire français

Revue de presse automatisée consacrée au nucléaire en France.

## Fonctions
- Collecte des actualités des 7 derniers jours via les flux RSS de Google Actualités.
- Classement : parc et production EDF ; EPR et nouveaux réacteurs ; sûreté et régulation ; combustible et déchets ; politique énergétique ; industrie, investissements et emplois.
- Résumés détaillés par IA avec une clé OpenAI, ou résumé extractif sans clé.
- Interface web avec recherche et filtre thématique.
- Publication chaque lundi à 7 h, heure de Paris ; lancement manuel possible depuis **Actions**.

## Activer les résumés IA
Le dépôt étant public, ne publiez jamais de clé ou mot de passe dans les fichiers.
1. Créez une clé API dans votre compte OpenAI.
2. Dans GitHub : **Settings → Secrets and variables → Actions → New repository secret**.
3. Nom : `OPENAI_API_KEY`. Valeur : votre clé API.
Sans ce secret, la collecte fonctionne en mode résumé extractif.

## Activer le site web
Dans **Settings → Pages**, choisissez **GitHub Actions** comme source de publication. Le workflow `Publier le site` construira le site. Son adresse sera affichée dans **Actions** après le premier déploiement.

## Déclencher une collecte
Dans **Actions → Revue de presse hebdomadaire → Run workflow**. Le déclenchement manuel force une édition immédiatement.

## Sources et limites
Les articles sont découverts via les flux RSS Google Actualités. Le collecteur tente de lire les pages accessibles publiquement ; il ne contourne pas les paywalls. Les résumés automatiques peuvent comporter des erreurs : vérifiez les sources originales. Les articles et leurs droits restent ceux des éditeurs.
