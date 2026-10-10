# Bible RAG

Système de questions-réponses sur la Bible (Sainte Bible néo-Crampon Libre) basé sur le
*Retrieval-Augmented Generation* (RAG) : le système recherche les passages
pertinents, puis rédige une réponse en citant les versets.

## Objectifs
- Construire un pipeline RAG complet, en local et avec des outils open source
- Évaluer chaque choix technique (chunking, embeddings, recherche hybride, reranking)
- Documenter la démarche et les résultats

## Feuille de route
- [x] Jalon 0 : Mise en place du projet
- [ ] Jalon 1 : Ingestion des données
- [ ] Jalon 2 : Jeu d'évaluation
- [ ] Jalon 3 : Chunking
- [ ] Jalon 4 : Embeddings
- [ ] Jalon 5 : Base vectorielle et recherche
- [ ] Jalon 6 : Recherche hybride et reranking
- [ ] Jalon 7 : Génération de réponses
- [ ] Jalon 8 : Interface et déploiement

## Structure
```
Bible-RAG/
├── data/
│   ├── raw/          # texte brut téléchargé (non versionné)
│   ├── processed/    # données nettoyées (non versionnées)
│   └── sample/       # petit échantillon versionné
├── docs/
│   └── journal.md    # journal de bord du projet
├── eval/             # questions et scripts d'évaluation
├── notebooks/        # explorations
├── src/bible_rag/    # code du pipeline
└── tests/            # tests automatiques
```

## Installation
```bash
git clone https://github.com/RafaelROMERA0906/Bible-RAG.git
cd Bible-RAG
uv sync
```

## Données
Texte de la **Sainte Bible néo-Crampon Libre**, © 2022 Fraternité de Tibériade,
publié sous licence [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.fr),
source : [eBible.org](https://ebible.org/francl/).

- Canon catholique : 73 livres, dont les livres deutérocanoniques.
- Les données transformées (`data/sample/`) sont redistribuées sous la même licence.
  Seules les balises de mise en forme USFM sont retirées ; le texte n'est pas modifié.
- Le code du projet est sous licence MIT.
