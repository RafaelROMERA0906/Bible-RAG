# Journal de bord – Bible RAG

## Jalon 0 – Mise en place du projet
**Date :** 9 octobre 2026

### Objectif
Préparer un dépôt propre et reproductible avant de commencer à coder le RAG.

### Ce que j'ai fait
À l'aide de Claude, qui m'a guidé tout au long de ce premier jalon, j'ai :
- créé le dépôt GitHub et défini la feuille de route en 9 jalons ;
- choisi le corpus : la Sainte Bible néo-Crampon Libre (source : eBible.org) ;
- initialisé le projet Python avec uv (Python 3.14) en structure `src/` ;
- créé l'arborescence : données, documentation, évaluation, notebooks, code, tests ;
- configuré le `.gitignore`, rédigé le README et un `CLAUDE.md` ;
- organisé le suivi avec des milestones et des issues.

### Choix et raisons
- **La néo-Crampon Libre** : une Bible catholique (73 livres, dont les livres deutérocanoniques comme Tobie, Judith, Sagesse ou les Maccabées), en français moderne, disponible dans un format structuré (USFM). La Crampon originale de 1923 n'existe qu'en images scannées : la convertir aurait été un projet à part entière.
- **Licence des données** : la néo-Crampon (© 2022 Fraternité de Tibériade) est sous licence **CC BY-SA 4.0**. Je dois citer la source, et les données que je publie restent sous la même licence. Le code du projet est sous licence MIT.
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
- Les licences libres (CC BY-SA, MIT) et leurs obligations.

---

## Jalon 1 – Gestion des données *(en cours)*
**Début :** 10 octobre 2026

### Objectif
Télécharger le texte biblique et le transformer en données structurées (un verset par ligne, avec livre, chapitre, numéro et intertitres), prêtes à être exploitées par le RAG.

### Nouvelle organisation : une branche par jalon
Pour ne pas risquer de modifier `main` de façon irréversible, je travaille désormais sur une branche dédiée (`jalon-1-ingestion`). À la fin du jalon, je fusionnerai cette branche dans `main` via une pull request. Ce sera ma méthode pour chaque jalon.

### 1. Exploration des données
J'ai téléchargé la Bible au format USFM, un format texte où des balises (`\c` pour le chapitre, `\v` pour le verset…) structurent le texte. Avec quelques commandes (`grep`, `sort`, `uniq`), j'ai dressé l'inventaire de toutes les balises utilisées.

| Élément | Nombre |
|---|---|
| Livres | 73 |
| Chapitres | 1 334 |
| Versets | 35 530 |
| Notes de bas de page | 2 530 |
| Références croisées | 41 |

J'ai vite compris que la préparation des données serait plus importante que prévu :
- chaque mot est balisé avec un **numéro Strong** (référence au mot hébreu ou grec d'origine), souvent mal aligné, donc inutilisable ;
- le texte contient **2 530 notes de bas de page** (commentaires du traducteur) insérées au milieu des versets ;
- Esther (16 chapitres) et Daniel (14) intègrent les ajouts grecs propres aux Bibles catholiques ;
- les données ne sont pas parfaitement régulières : balises collées au mot (`\wQue`), mots soudés après nettoyage (`couvraientl'abîme`), espaces manquants dans la source (`Absalon,son`, `parTéglathphalasar`).

Deux leçons tirées de l'exploration :
- J'avais prévu d'enregistrer les titres des psaumes comme « verset 0 », mais ils sont déjà numérotés comme verset 1 : **l'hypothèse a été invalidée par les données**.
- Ma première recherche de ces titres n'a rien donné à cause d'une regex trop stricte : **un résultat vide ne prouve pas une absence**.

Le détail du traitement de chaque balise est décrit dans l'issue #8 (Parseur USFM → JSONL), qui sert de cahier des charges au parseur.

### 2. Script de téléchargement
Les données téléchargées sont dans `data/raw/`, ignoré par Git car trop lourd. Pour qu'un visiteur puisse reproduire le projet, j'ai écrit un script Python qui récupère les données tout seul :
1. il vérifie si les données sont déjà là ; si oui, il s'arrête (le script est **idempotent**) ;
2. sinon, il télécharge l'archive zip depuis eBible.org ;
3. il la décompresse dans `data/raw/`.

L'identifiant de la traduction est stocké dans une seule constante (`TRANSLATION_ID`) : changer de traduction ne demande de modifier qu'un mot.

À la première exécution, le script a échoué avec une **erreur HTTP 403**. J'ai appris à lire un *traceback* (de bas en haut) et compris que le site bloque le User-Agent par défaut de Python, alors qu'il acceptait `curl`. Solution : envoyer un User-Agent qui identifie le projet.

### 3. Nettoyage du texte
Le parseur doit isoler les notes de bas de page et supprimer les très nombreuses balises USFM, sans perdre une lettre du texte biblique.

Le nettoyage repose sur trois fonctions qui utilisent des expressions régulières (motifs de recherche dans le texte). `clean_text` est le point d'entrée : elle met de côté les notes de bas de page, puis retire du texte les blocs à supprimer en entier (notes, références croisées, références de citations, numéros de verset alternatifs), en s'arrêtant à chaque fois à la première balise fermante pour ne pas avaler le texte du verset. Elle confie ensuite le reste à `_strip_markers`, qui sépare les mots balisés collés, ne garde que le mot de chaque balise `\w` (en éliminant les numéros Strong), retire toutes les autres balises en conservant leur texte, puis corrige l'espacement. Enfin, `_clean_footnote` traite chaque note mise de côté avant de la passer elle aussi dans `_strip_markers`.

**Les notes ne sont pas supprimées** : elles sont retirées du texte des versets et conservées à part, reliées à leur verset. Ce sont des commentaires du traducteur, pas des paroles bibliques : les mélanger fausserait les citations et la recherche. Elles pourront servir plus tard à enrichir les réponses.

J'ai écrit **7 tests automatiques avec pytest**, chacun construit à partir d'un piège réel rencontré pendant l'exploration. Les 7 passent.

### Choix et raisons
- **Explorer avant de coder** : l'inventaire des balises a révélé des pièges que je n'aurais jamais anticipés.
- **Une spécification écrite dans l'issue #8** avant de coder le parseur : elle sert de cahier des charges et de liste de contrôle.
- **Texte biblique et notes séparés mais reliés.**
- **Ne pas corriger les coquilles de la source**, sauf l'espacement : corriger le texte reviendrait à le modifier, ce que la licence impose de signaler, et ce n'est pas l'objet du projet.
- **Les numéros Strong sont ignorés** car trop souvent mal alignés.

### Problèmes rencontrés
- **Verrou Git (`index.lock`)** : des commits lancés depuis VS Code sans message sont restés en attente dans des terminaux ouverts, bloquant toute opération Git. Solution : fermer ces terminaux et supprimer le verrou.
- **Une commande suspendue** : j'ai quitté l'affichage de Git avec `Ctrl + Z`, ce qui met la commande en pause au lieu de la fermer. On sort de ce visualiseur avec la touche `q`.
- **Désynchronisation entre VS Code et GitHub** : j'ai modifié le README directement sur le site, ce qui a créé un commit sur `main` pendant que je travaillais sur ma branche. Les deux branches ont divergé. Solution : diagnostic avec `git fetch`, `git status` et `git log --graph`, puis fusion de `main` dans ma branche.
- **Leçon** : pendant un jalon, je modifie les fichiers uniquement dans VS Code sur ma branche. Sur GitHub, je me limite aux issues, aux milestones et aux pull requests.

### Ce que j'ai appris
- Explorer un format de données avec `grep`, `sort`, `uniq` et les expressions régulières.
- Lire un traceback Python, comprendre un code HTTP et le rôle du User-Agent.
- Les regex : groupes capturants, recherche non gourmande, regard en avant.
- Écrire des tests unitaires avec pytest.
- Git : branches, `fetch`, `merge`, branches divergentes, verrou d'index, lien entre commits et issues (`closes`, `refs`).

### Prochaines étapes
- Parseur, étape 2 : parcourir un fichier ligne par ligne pour découper les versets (livre, chapitre, intertitres).
- Parseur, étape 3 : traiter les 73 livres et écrire les fichiers JSONL.
- Tests d'intégrité sur l'ensemble du corpus (issue #9).
- Échantillon de données pour GitHub (issue #10).
- Pull request de fin de jalon.