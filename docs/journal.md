# Journal de bord – Bible RAG

## Jalon 0 – Mise en place du projet

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

## Jalon 1 - gestion des données 

### Objectif 
Préparer les données pour pouvoir les exploiter. 

### Ce que j'ai fait

J'ai commencé par télécharger la bible au format USFM et j'ai regardé comment était organiser le textes (répartition livres, chapitres, versets...). Pour être sûr de ne pas faire d'erreur et de modifier le fichier main de façon irrémédiable, je me suis placée sur une branche correspondant au Jalon 1. C'est d'ailleurs comme cela que je travaillerai désormais : une branche par projet puis un pull request vers le main. 

A mesure que j'explore les balises du format USFM, je me rends compte que le travail de préparation des donnée sera plus important que ce que je pensais. En effet, il existe beaucoup de balises dont je n'ai pas besoin qu'il faudra donc supprimer (ou au moins ignorer) pour le parseur. 
Ex : Le livre contient une partie introduction pour chaque livre qui ne fait pas partit du texte original. Il faudra donc veiller à supprimer les balises correspondants à ces passages (\ip, \ipi...) 
Le détail des traitements réservés aux différentes balises se trouve dans la description du jalon 8 - Parseur USFM → JSONL

Un autre détail important. Pour l'insatnt, j'ai téléchargé les données dans un fichier de mon projet qui n'apparaît pas sur le git (.gitignore) car l'opération serait alors très lourde. Il me faut donc treouver un moyen de permettre aux autres utilisateurs d'accéder aux données. Je vais donc créer un script python qui va chercher les données sur internet tout seul. 
Un autre détail important. Pour l'insatnt, j'ai téléchargé les données dans un fichier de mon projet qui n'apparaît pas sur le git (.gitignore) car l'opération serait alors très lourde. Il me faut donc treouver un moyen de permettre aux autres utilisateurs d'accéder aux données. Je vais donc créer un script python qui va chercher les données sur internet tout seul.
Ce que fait le programme, en trois temps :
Il regarde si les données sont déjà là. Si oui, il s’arrête : pas besoin de les retélécharger.
Sinon, il télécharge le fichier zip depuis eBible.org.
Il décompresse le zip dans data/raw/.

En éxécutant le script, celi à échouer. En fait, j'ai appris que le siste bible.org bloque le user-agent de base de Python. Il faut donc se présenter avec un autre user-agent, qui lui est accepté par le site 