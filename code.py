# ============================================================
# Projet : Poussée d’Archimède avec modèle "corps humain"
# ============================================================
# Objectif (cas d’usage réel)
# - Estimer le volume d’un corps humain à partir de mesures anthropométriques (circonférences + longueurs)
# - En déduire :
#   1) la poussée d’Archimède dans l’eau
#   2) le poids apparent dans l’eau (si le corps est maintenu immobile/suspendu)
#   3) la tendance à flotter ou couler
#
# ------------------------------------------------------------
# 1) Modèle géométrique (approximation)
# ------------------------------------------------------------
# On approxime des parties du corps par des solides simples :
#   - Tronc : cylindre
#   - Tête : sphère
#   - Bras (x2) : cylindre (circonférence moyenne biceps/avant-bras)
#   - Mains (x2) : cylindre
#   - Jambe (x2) : cylindre (faute de longueurs cuisse/mollet dans le CSV actuel)
#   - Pieds (x2) : cylindre
#
# NOTE IMPORTANTE (correction du bug rencontré)
# - Ton fichier one_person_for_python.csv contient : "leg_L_m"
# - Il ne contient PAS : "thigh_L_m" ni "calf_L_m"
# => On adapte donc le modèle jambe au contenu réel du CSV :
#    une jambe = un cylindre basé sur la circonférence de cuisse (thigh_C_m)
#    et la longueur totale de jambe (leg_L_m)
#
# ------------------------------------------------------------
# 2) Données d'entrée (mesures réelles)
# ------------------------------------------------------------
# Les valeurs proviennent d’un fichier CSV exporté depuis ANSUR II.
# Ici, on lit "one_person_for_python.csv" (généré par mon script R).
#
# Important :
# - Les circonférences C sont en mètres (m)
# - Les longueurs L sont en mètres (m)
# - La masse m est en kilogrammes (kg)
#
# ANSUR II (dataset et description) :
# - https://www.openlab.psu.edu/ansur2/
#
# ------------------------------------------------------------
# 3) Formules utilisées (avec unités)
# ------------------------------------------------------------
# (A) Conversion circonférence -> rayon
#   C = 2πr  =>  r = C / (2π)
# - C en m
# - r en m
#
# (B) Volume cylindre :
#   V = π r² h
# - r en m
# - h en m
# - V en m³
#
# (C) Volume sphère :
#   V = (4/3) π r³
# - r en m
# - V en m³
#
# (D) Poids :
#   P = m g
# - m en kg
# - g en m/s²
# - P en N
#
# (E) Poussée d’Archimède :
#   F_A = ρ g V_immergé
# - ρ : masse volumique du fluide en kg/m³ (eau douce ≈ 1000 kg/m³)
# - g : accélération de la pesanteur en m/s² (≈ 9,81 m/s² sur Terre)
# - V_immergé : volume de fluide déplacé en m³
# - F_A : intensité de la poussée d’Archimède en N
#
# Source (Archimède, statique des fluides) :
# - ENS Lyon – CultureSciences Physique
#   https://culturesciencesphysique.ens-lyon.fr/ressource/statique-fluides.xml
#
# Hypothèse :
# - corps entièrement immergé => V_immergé ≈ V_total
#
# ------------------------------------------------------------
# 4) Sorties
# ------------------------------------------------------------
# - Volume total V_total (m³)
# - Densité moyenne estimée rho_obj = m / V_total (kg/m³)
# - Poids P (N)
# - Poussée F_A (N)
# - Poids apparent P_app = P - F_A (N)
# - Masse apparente équivalente m_app = P_app / g (kg)
# - Verdict : flotte/coule/équilibre
# ============================================================

import math
import csv


def circumference_to_radius(C_m: float) -> float:
    """
    Convertit une circonférence C (m) en rayon r (m) en supposant une section circulaire.

    Formule :
        C = 2πr  =>  r = C / (2π)

    Unités :
        C_m : m
        retour : m

    Doc :
      https://www.khanacademy.org/math/geometry/hs-geo-circles/hs-geo-radius-diameter/v/radius-diameter-and-circumference
    """
    return C_m / (2 * math.pi)


def volume_cylinder_from_circumference(C_m: float, L_m: float) -> float:
    """
    Volume d’un cylindre à partir d’une circonférence C (m) et d’une longueur/hauteur L (m).

    Étapes :
      1) r = C / (2π)
      2) V = π r² L

    Unités :
      C_m : m
      L_m : m
      V : m³
    """
    r = circumference_to_radius(C_m)
    return math.pi * r * r * L_m


def volume_sphere_from_circumference(C_m: float) -> float:
    """
    Volume d’une sphère à partir d’une circonférence C (m) (ex : tour de tête).

    Étapes :
      1) r = C / (2π)
      2) V = (4/3) π r³

    Unités :
      C_m : m
      V : m³
    """
    r = circumference_to_radius(C_m)
    return (4 / 3) * math.pi * (r ** 3)


def read_one_person_csv(path: str) -> dict:
    """
    Lit un CSV contenant UNE ligne (une personne) et renvoie {colonne: valeur_float}.
    Ignore la colonne 'subjectid' si elle est présente.

    Doc :
      https://docs.python.org/3/library/csv.html
    """
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        row = next(reader)

    return {k: float(v) for k, v in row.items() if k != "subjectid"}


def main():
    # Constantes physiques (eau douce + gravité terrestre)
    rho = 1000.0  # kg/m³
    g = 9.81      # m/s²

    # Lecture des mesures (1 personne)
    data = read_one_person_csv("one_person_for_python.csv")

    # Masse (kg)
    m_kg = data["m_kg"]

    # ----------------------------
    # Volumes (m³)
    # ----------------------------

    # Tête : sphère
    V_head = volume_sphere_from_circumference(data["head_C_m"])

    # Tronc : cylindre
    V_trunk = volume_cylinder_from_circumference(data["trunk_C_m"], data["trunk_H_m"])

    # Mains : cylindres (x2)
    V_hand_one = volume_cylinder_from_circumference(data["hand_C_m"], data["hand_L_m"])

    # Bras : cylindres (x2) — moyenne biceps/avant-bras
    C_arm_avg = (data["biceps_C_m"] + data["forearm_C_m"]) / 2
    V_arm_one = volume_cylinder_from_circumference(C_arm_avg, data["arm_L_m"])

    # Jambes : cylindres (x2)
    # Correction : le CSV contient "leg_L_m" (pas "thigh_L_m" / "calf_L_m")
    V_leg_one = volume_cylinder_from_circumference(data["thigh_C_m"], data["leg_L_m"])

    # Pieds : cylindres (x2)
    V_foot_one = volume_cylinder_from_circumference(data["foot_C_m"], data["foot_L_m"])

    # Volume total
    V_total = (
        V_trunk
        + V_head
        + 2 * V_arm_one
        + 2 * V_hand_one
        + 2 * V_leg_one
        + 2 * V_foot_one
    )

    # ----------------------------
    # Physique : poids, poussée, apparent
    # ----------------------------

    P = m_kg * g                    # N
    F_A = rho * g * V_total         # N (V_immergé ≈ V_total)
    P_app = P - F_A                 # N
    rho_obj = m_kg / V_total        # kg/m³
    m_app = P_app / g               # kg

    # ----------------------------
    # Affichage
    # ----------------------------

    print("--- Volumes par segment (m³) ---")
    print(f"V_trunk      = {V_trunk:.6f}")
    print(f"V_head       = {V_head:.6f}")
    print(f"V_arm_one    = {V_arm_one:.6f}  (x2 => {2*V_arm_one:.6f})")
    print(f"V_hand_one   = {V_hand_one:.6f} (x2 => {2*V_hand_one:.6f})")
    print(f"V_leg_one    = {V_leg_one:.6f}  (x2 => {2*V_leg_one:.6f})")
    print(f"V_foot_one   = {V_foot_one:.6f} (x2 => {2*V_foot_one:.6f})")

    print("\n--- Résultats ---")
    print(f"Volume total V_total = {V_total:.6f} m³")
    print(f"Densité moyenne rho_obj = {rho_obj:.2f} kg/m³")
    print(f"Poids P = {P:.2f} N")
    print(f"Poussée F_A = {F_A:.2f} N")
    print(f"Poids apparent P_app = {P_app:.2f} N")
    print(f"Masse apparente équivalente = {m_app:.2f} kg")

    # Verdict (via poids apparent)
    if P_app > 0:
        print("Verdict : tendance à COULER (P > F_A).")
    elif P_app < 0:
        print("Verdict : tendance à FLOTTER (F_A > P).")
    else:
        print("Verdict : équilibre (P ≈ F_A).")


if __name__ == "__main__":
    main()
