# Projet – Poussée d’Archimède appliquée au corps humain

## Présentation générale

Ce projet a pour objectif d’illustrer concrètement le **principe de la poussée d’Archimède** en l’appliquant à un cas réel : le corps humain.

À partir de **mesures anthropométriques réelles** (issues du dataset ANSUR II), on cherche à estimer le **volume total du corps** grâce à un modèle géométrique simplifié, puis à en déduire :

- la poussée d’Archimède exercée par l’eau,
- le poids apparent du corps lorsqu’il est immergé,
- la tendance du corps à flotter ou à couler.

Le projet a une vocation **pédagogique et scientifique**. Il ne vise pas une précision médicale, mais une modélisation physique cohérente et explicable.

---

## Principe physique utilisé

Le projet repose sur le **principe d’Archimède** :

> Tout objet immergé dans un fluide au repos subit une force verticale dirigée vers le haut, appelée poussée d’Archimède, dont l’intensité est égale au poids du fluide déplacé.

Formule utilisée :

\[
F_A = \rho \, g \, V_{\text{immergé}}
\]

où :
- \( \rho \) est la masse volumique du fluide (eau douce ≈ 1000 kg/m³),
- \( g \) est l’accélération de la pesanteur (≈ 9,81 m/s²),
- \( V_{\text{immergé}} \) est le volume de fluide déplacé.

### Source principale
- ENS Lyon – CultureSciences Physique, *Statique des fluides*  
  https://culturesciencesphysique.ens-lyon.fr/ressource/statique-fluides.xml

---

## Modélisation du corps humain

Le corps humain ayant une géométrie complexe, il est approximé par des **solides géométriques simples**, ce qui est courant en physique lorsqu’on cherche des ordres de grandeur sans disposer d’un scan 3D.

Modèle utilisé :

- Tête → sphère  
- Tronc → cylindre  
- Bras (x2) → cylindre (circonférence moyenne biceps / avant-bras)  
- Mains (x2) → cylindre  
- Jambes (x2) → deux cylindres
- Pieds (x2) → cylindre  

Ce découpage permet de limiter les erreurs majeures tout en gardant un modèle simple et compréhensible.

---

## Données utilisées

Les données anthropométriques proviennent du **dataset ANSUR II**, qui contient des mesures détaillées sur une large population.

### Workflow des données

1. Sélection aléatoire d’un individu dans ANSUR II via un script R.
2. Conversion des mesures en unités SI (mètres, kilogrammes).
3. Export des données dans un fichier CSV (`one_person_for_python.csv`).
4. Lecture et exploitation de ce fichier par le script Python.

### Source ANSUR II
- https://www.openlab.psu.edu/ansur2/

---

## Organisation du projet

### Langages utilisés

- **R** : extraction, sélection et préparation des données ANSUR II.
- **Python** : calculs géométriques et physiques.

### Fichiers principaux

- Script R  
  - génère `one_person_for_python.csv` à partir d’ANSUR II.
- Script Python  
  - lit le CSV,
  - calcule les volumes par segment,
  - calcule le poids, la poussée d’Archimède et le poids apparent,
  - affiche les résultats et un verdict qualitatif.

---

## Hypothèses du modèle

- Le corps est considéré **entièrement immergé**.
- Le volume immergé est assimilé au volume total.
- La masse volumique de l’eau est constante (eau douce).
- Les segments du corps ont une section circulaire.

Ces hypothèses sont simplificatrices mais adaptées à un cadre pédagogique.

---

## Résultats fournis par le programme

Le programme affiche :

- le volume de chaque segment du corps,
- le volume total estimé,
- la densité moyenne du corps,
- le poids réel dans l’air,
- la poussée d’Archimède,
- le poids apparent dans l’eau,
- un verdict :
  - tendance à flotter,
  - tendance à couler,
  - équilibre.

---

## Limites du modèle

- Le corps humain n’est pas homogène (os, muscles, graisse, air dans les poumons).
- Les sections ne sont pas parfaitement circulaires.
- La posture du corps dans l’eau n’est pas prise en compte.
- La respiration et la flottabilité pulmonaire ne sont pas modélisées.

Ces limites sont connues et assumées. Le but est de comprendre les mécanismes physiques, pas de prédire un comportement exact.

---

## Objectif pédagogique

Ce projet permet de :

- relier un principe de physique à un cas concret,
- manipuler des unités et des ordres de grandeur,
- illustrer l’intérêt des approximations en physique,
- croiser données réelles, mathématiques et programmation.

---

## Références complémentaires

- ENS Lyon – CultureSciences Physique, *Statique des fluides*  
  https://culturesciencesphysique.ens-lyon.fr/ressource/statique-fluides.xml
- OpenStax – *College Physics 2e*, Archimedes’ Principle  
  https://openstax.org/details/books/college-physics-2e

