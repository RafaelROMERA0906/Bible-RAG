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

A mesure que j'explore les balises du format USFM, je me rends compte que le travail de préparation des donnée sera plus important que ce que je pensais. En effet, il existe beaucoup de balises dont je n'ai pas besoin qu'il faudra donc supprimer (ou au moins ignorer) pour le parseur. Voici le détail du traitment qui sera réservé aux différentes balises : 

## 1. Fichiers à lire
| Point | Traitement |
|---|---|
| 66 fichiers `.usfm` + fichiers annexes (`copr.htm`, `keys.asc`, `latin.css`) | Lire uniquement les `*.usfm` |
| Ordre des livres | Trier les fichiers par nom (préfixe `02-GEN` … `96-REV`) |
| Testament | GEN à MAL = AT (39 livres), MAT à REV = NT (27 livres) |

## 2. Balises de ligne
| Balise | Rôle | Traitement |
|---|---|---|
| `\id` | Code du livre | Garder le premier mot (`GEN`) |
| `\toc2` | Nom court du livre | Garder comme nom affiché (`Genèse`) |
| `\h`, `\toc1`, `\mt1`, `\mt2` | Autres titres | Ignorer |
| `\imt1-3`, `\ip`, `\ipi`, `\io1-2`, `\ior`, `\is1`, `\ib`, `\ie` | Introduction moderne | Ignorer |
| `\tr`, `\tc1-3`, `\th1-2` | Tableaux | Ignorer (⚠️ vérifier qu'ils sont dans les introductions) |
| `\c` | Chapitre | Mettre à jour le chapitre courant |
| `\v` | Verset | Commencer un nouveau verset (⚠️ vérifier que les numéros sont des entiers) |
| `\s1` | Intertitre | Mémoriser comme section courante des versets suivants |
| `\ms1`, `\ms2`, `\mr` | Grandes divisions | Ignorer |
| `\r` | Références parallèles | Ignorer la ligne |
| `\p`, `\m`, `\q1`, `\pi1` | Paragraphe, poésie | Retirer la balise, garder le texte |
| `\b` | Ligne vide | Ignorer |

Règle générale : ignorer tout ce qui précède le premier `\c` de chaque livre.

## 3. Balises en ligne
| Balise | Exemple | Traitement |
|---|---|---|
| `\x … \x*` | `\x b \xo 1.2 \xt Ge 21:2.\x*` | Supprimer le bloc, extraire la référence cible à part |
| `\w … \w*` | `\w Abraham\|strong="G1161"\w*` | Garder seulement le mot |
| `\+w … \+w*` | idem, dans les paroles de Jésus | Même traitement que `\w` |
| `\wj … \wj*` | Paroles de Jésus | Garder le texte, marquer `words_of_jesus: true` |
| `\it … \it*` | Mots ajoutés par le traducteur | Garder le texte |
| `\ord … \ord*` | Ordinaux | Garder le texte |
| `\qs … \qs*` | « Sélah » | Garder le texte |

## 4. Points de vigilance
- [ ] Supprimer les blocs `\x … \x*` **avant** tout autre nettoyage
- [ ] Tolérer les variantes d'écriture (`\xo 1.2` et `\xo1.2`)
- [ ] Regex non gourmande pour `\x … \x*` (s'arrêter au premier `\x*`)
- [ ] Accumuler les versets écrits sur plusieurs lignes (poésie)
- [ ] Normaliser les espaces (multiples, début, fin)
- [ ] Garder la typographie d'origine (apostrophes, ponctuation)
- [ ] Ignorer les numéros Strong (mal alignés)
- [ ] Aucun reste de balise (`\`, `|strong`) dans le texte final

## 5. Format de sortie
`data/processed/lsg1910.jsonl` :
```json
{"id": "MAT.1.2", "book": "MAT", "book_name": "Matthieu", "testament": "NT", "chapter": 1, "verse": 2, "section": "Généalogie de Jésus-Christ", "text": "Abraham engendra Isaac; Isaac engendra Jacob; Jacob engendra Juda et ses frères;", "words_of_jesus": false}
```

`data/processed/cross_refs.jsonl` :
```json
{"source": "MAT.1.2", "target": "Ge 21:2."}
```

## 6. Contrôles attendus (voir #10)
66 livres, 1 189 chapitres, 31 170 versets, aucun verset vide, identifiants uniques, aucun reste de balise.
