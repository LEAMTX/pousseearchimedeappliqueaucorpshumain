### Projet – Poussée d’Archimède appliquée au corps humain (ANSUR II) **
###  Présentation  

Ce projet illustre le principe de la poussée d’Archimède en l’appliquant à un cas concret : le corps humain.

À partir de mesures anthropométriques réelles issues du dataset ANSUR II, on estime un volume corporel à l’aide d’un modèle géométrique simplifié, puis on calcule :

la poussée d’Archimède exercée par l’eau,

le poids apparent du corps en immersion,

la tendance du corps à flotter ou bien à couler.

Le but est pédagogique et scientifique : obtenir un modèle cohérent et explicable (ordre de grandeur), et non une précision médicale.

###  Principe physique  

Le projet repose sur le principe d’Archimède, selon lequel tout corps plongé dans un fluide subit une force verticale dirigée vers le haut, égale au poids du fluide déplacé.

Formule utilisée :

F_A = ρ · g · V_immergé


où :

ρ est la masse volumique du fluide (eau douce ≈ 1000 kg/m³),

g est l’accélération de la pesanteur (≈ 9,81 m/s²),

V_immergé est le volume de fluide déplacé.

Dans ce modèle, on suppose que le corps est entièrement immergé, donc
V_immergé ≈ V_total.

### Source

ENS Lyon – CultureSciences Physique, Statique des fluides
https://culturesciencesphysique.ens-lyon.fr/ressource/statique-fluides.xml

###  Modèle géométrique 

Le corps humain étant géométriquement complexe, il est approximé par des solides simples.
Modèle retenu :

tête → sphère

tronc → cylindre

bras (x2) → cylindre (circonférence moyenne biceps / avant-bras)

mains (x2) → cylindre

jambes (x2) → un cylindre (circonférence de cuisse + longueur de jambe proxy coorespondant à buttockkneelength)

pieds (x2) → cylindre

Ce choix réduit la complexité du modèle et évite l’introduction de longueurs complexes (mollet) qui se sont avérées ambiguës dans les calculs.

Données (ANSUR II)

Les données anthropométriques proviennent du dataset ANSUR II :
https://www.openlab.psu.edu/ansur2/

Workflow des données

Un script R sélectionne un individu dans ANSUR II, convertit les unités en système international et exporte un fichier one_person_for_python.csv.

Un script Python lit ce fichier CSV, calcule les volumes corporels et les grandeurs physiques associées.

Note sur la masse (weightkg)

Dans le fichier ANSUR II utilisé, la variable weightkg apparaît encodée avec un facteur 10 (par exemple, une médiane ≈ 846).

La conversion suivante est donc appliquée dans le script R :

m_kg = weightkg / 10


Cela ramène les valeurs de masse dans une plage réaliste (ex. 846 → 84,6 kg).

Note sur la reproductibilité (set.seed)

Un individu est sélectionné aléatoirement dans le jeu de données.
Afin de garantir la reproductibilité des résultats, on initialise avec set.seed(42).

Ce choix ne sert pas à « choisir » un individu particulier, mais à s’assurer que toute exécution du script conduit au même individu, et donc aux mêmes résultats.

 ### Interprétation des résultats

 ###  Résultats obtenus pour l’individu étudié :

lea@MacBook-Air-de-monthieux projetpousseearchimede % python3 code.py
--- :) Résultats  :) ---
Volume total V_total = 0.106731 m³
Densité moyenne rho_obj = 876.97 kg/m³
Poids P = 918.22 N
Poussée F_A = 1047.03 N
Poids apparent P_app = -128.82 N
Masse apparente équivalente = -13.13 kg
Verdict : tendance à FLOTTER (F_A > P).

## Interprétation des résultats – Poussée d’Archimède

Les calculs effectués à partir des données anthropométriques donnent les valeurs suivantes :

- Volume total : V = 0.106731 m³
- Densité moyenne de l’objet : ρ_obj = 876.97 kg/m³
- Poids : P = 918.22 N
- Poussée d’Archimède : F_A = 1047.03 N
- Poids apparent : P_app = -128.82 N

### Analyse physique

Selon le principe de la poussée d’Archimède, tout corps immergé dans un fluide
subit une force verticale dirigée vers le haut, égale au poids du fluide déplacé :

F_A = ρ_fluide · g · V

Dans le cas présent, la poussée d’Archimède est supérieure au poids propre
de l’objet (F_A > P). La résultante des forces est donc dirigée vers le haut,
ce qui indique une tendance à flotter.
car : ### Justification de la direction de la résultante des forces

Deux forces principales s’exercent sur un objet immergé dans un fluide au repos :

- le poids de l’objet, dirigé vers le bas :
  
  P = m · g

- la poussée d’Archimède, dirigée vers le haut :
  
  F_A = ρ_fluide · g · V

La résultante verticale des forces est donnée par :

R = F_A − P

Dans le cas présent, les valeurs calculées sont :

- F_A = 1047.03 N
- P = 918.22 N

Donc :

R = 1047.03 − 918.22 = +128.81 N

Le signe positif de la résultante indique que la force nette est dirigée vers
le haut. Cela signifie que, si l’objet est libre de se déplacer, il subira une
accélération verticale ascendante.

Cette condition correspond à une tendance à flotter, conformément à la
seconde loi de Newton appliquée au mouvement vertical :

ΣF = m · a

Lorsque ΣF > 0, l’accélération est orientée vers le haut.

Cette conclusion est cohérente avec la densité moyenne calculée :
ρ_obj = 876.97 kg/m³, valeur inférieure à la masse volumique de l’eau douce
(ρ_eau ≈ 1000 kg/m³). Un objet dont la densité est inférieure à celle du fluide
dans lequel il est plongé flotte partiellement jusqu’à atteindre un équilibre
tel que F_A = P. L’objet commence donc à remonter vers la surface.

### Évolution lors de la remontée

Pendant la remontée, le volume immergé de l’objet diminue progressivement.
Or, la poussée d’Archimède dépend du volume immergé :

F_A = ρ_fluide · g · V_immergé

Ainsi, lorsque V_immergé diminue, F_A diminue également car ils sont proportionnels, tandis que le poids
P de l’objet reste constant.

### Position d’équilibre

La remontée s’arrête lorsque les deux forces s’équilibrent :

F_A = P
À cet instant, la résultante des forces est nulle (R = 0), l’accélération
devient nulle, et l’objet reste partiellement immergé. Cette position correspond
à l’état de flottaison stable à la surface du fluide.

### Poids apparent négatif

Le poids apparent est défini par :

P_app = P − F_A

Dans le cas présent, P_app < 0, ce qui signifie que la poussée d’Archimède est
supérieure au poids propre de l’objet (F_A > P). La résultante des forces est
donc dirigée vers le haut.

Si l’objet est maintenu totalement immergé, une force extérieure dirigée vers
le bas, de norme au moins égale à |P_app|, doit être appliquée pour empêcher sa
remontée.

Il ne s’agit pas d’une masse négative, mais de l’expression d’une résultante
de forces orientée vers le haut, conformément aux lois de la mécanique.
Cette situation est physiquement équivalente à l’application d’une force
extérieure dirigée vers le bas (par exemple une force exercée par une main).

### Conclusion

Les résultats numériques indiquent que l’objet étudié est globalement moins
dense que l’eau. Il présente donc une tendance à flotter, avec une immersion
partielle à l’équilibre statique, conformément aux lois fondamentales de la
mécanique des fluides.


Exécution
1) Générer le fichier CSV (R)
Rscript script.R
fichier généré -> one_person_for_python.csv

2) Lancer le calcul physique (Python)
python3 code.py

Limites du modèle

le corps humain n’est pas homogène (os, muscles, graisse, air pulmonaire),

les sections corporelles ne sont pas réellement circulaires,

la posture et la respiration ne sont pas prises en compte,

le modèle vise des ordres de grandeur, pas une prédiction biomécanique exacte.

Ces limites sont connues et assumées dans un cadre pédagogique.

La longueur de jambe est approximée à partir de la mesure buttockkneelength,
utilisée comme proxy de la longueur réelle de la jambe, afin de conserver
un modèle simple, cohérent et reproductible.

Références techniques

ENS Lyon – Statique des fluides
https://culturesciencesphysique.ens-lyon.fr/ressource/statique-fluides.xml