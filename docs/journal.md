# Journal de bord – Bible RAG

## Jalon 0 – Mise en place du projet
**Date :** 9 octobre 2026

### Objectif
Préparer un dépôt propre et reproductible avant de commencer à coder le RAG.

### Ce que j'ai fait
A l'aide de claude qui m'a guidé tout au long de ce premier jalon, j'ai commencé ce projet par : 
- Créé le dépôt GitHub et défini la feuille de route en 9 jalons.
- Choisi le corpus : Bible Louis Segond 1910, dans le domaine public (source : eBible.org).
- Initialisé le projet Python avec uv (Python 3.14) en structure `src/`.
- Créé l'arborescence : données, documentation, évaluation, notebooks, code, tests.
- Configuré le `.gitignore`, rédigé le README et un `CLAUDE.md`.
- Organisé le suivi avec des milestones et des issues.

### Choix et raisons
- **uv plutôt que pip** : plus rapide, et le fichier `uv.lock` garantit un environnement identique pour tous.
- **Structure `src/`** : le code est un paquet importable depuis les notebooks et les tests.
- **Données non versionnées** (sauf un échantillon) : elles sont lourdes et peuvent être regénérées par script.
- **CLAUDE.md conservé** à côté du plugin ECC : ECC donne des règles générales, CLAUDE.md le contexte propre au projet.

### Problèmes rencontrés
- J'ai modifié par erreur le `.gitignore` interne au dossier `.venv` (créé par uv) au lieu de créer celui de la racine. Sa règle `*` a été écrasée, et le dossier `.venv` s'est retrouvé prêt à être commité.
- **Solution** : annulation du commit (message vide), retrait de `.venv` de la zone de préparation avec `git restore --staged`, restauration du fichier d'origine et création du bon `.gitignore` depuis le terminal.
- **Leçon** : vérifier le fil d'Ariane de VS Code avant de modifier un fichier, et toujours relire `git status` avant de commiter.

### Ce que j'ai appris
- Le rôle du `.gitignore`, de la zone de préparation, des commits et de la convention *Conventional Commits*.
- La différence entre la vue Source Control (versions Git, parfois en lecture seule) et l'Explorer de VS Code.
- L'organisation d'un projet avec milestones et issues.

### Prochaine étape
Jalon 1 : télécharger le texte au format USFM et écrire le parseur.