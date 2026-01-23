# ============================================================
# Projet : Poussée d’Archimède avec modèle "corps humain"
# ============================================================
# Objectif
# - Lire 1 personne (CSV) issue d'ANSUR II (préparée par le script R)
# - Estimer le volume du corps via un modèle géométrique simplifié
# - Calculer : poids, poussée d'Archimède, poids apparent, verdict flotte/coule
#
# Hypothèses principales
# - Corps entièrement immergé : V_immergé ≈ V_total
# - Eau douce : rho ≈ 1000 kg/m³ ; gravité terrestre g ≈ 9.81 m/s²
# - Sections circulaires pour convertir circonférences -> rayons
#
# Source physique (poussée d’Archimède) :
# ENS Lyon – CultureSciences Physique : statique des fluides
# https://culturesciencesphysique.ens-lyon.fr/ressource/statique-fluides.xml
# ============================================================

import csv
import math
from typing import Dict


def circumference_to_radius(c_m: float) -> float:
    """
    Convertit une circonférence (m) en rayon (m) : r = C / (2π).
    On valide que C > 0 pour éviter des volumes incohérents.
    """
    if c_m <= 0:
        raise ValueError(f"Circonférence invalide (<=0): {c_m}")
    return c_m / (2 * math.pi)


def volume_cylinder_from_circumference(c_m: float, l_m: float) -> float:
    """
    Volume d'un cylindre : V = π r² L avec r = C / (2π).
    On valide L > 0 pour éviter des volumes négatifs ou nuls.
    """
    if l_m <= 0:
        raise ValueError(f"Longueur invalide (<=0): {l_m}")
    r = circumference_to_radius(c_m)
    return math.pi * r * r * l_m


def volume_sphere_from_circumference(c_m: float) -> float:
    """
    Volume d'une sphère : V = (4/3) π r³ avec r = C / (2π).
    """
    r = circumference_to_radius(c_m)
    return (4 / 3) * math.pi * (r ** 3)


import csv

def read_one_person_csv(path):
    """
    Lit un CSV contenant une seule personne
    et renvoie un dictionnaire {nom_colonne: valeur_float}.
    """
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        row = next(reader)

    data = {}
    for key, value in row.items():
        if key != "subjectid":
            data[key] = float(value)

    return data



def main() -> None:
    rho = 1000.0  # kg/m³ (eau douce)
    g = 9.81      # m/s²

    try:
        data = read_one_person_csv("one_person_for_python.csv")
    except FileNotFoundError as e:
        print(f"Erreur: fichier CSV introuvable: {e}")
        return
    except (StopIteration, ValueError) as e:
        print(f"Erreur: CSV invalide: {e}")
        return

    # Vérification des colonnes attendues 
    required = [
        "m_kg",
        "head_C_m",
        "trunk_C_m", "trunk_H_m",
        "hand_C_m", "hand_L_m",
        "biceps_C_m", "forearm_C_m", "arm_L_m",
        "thigh_C_m", "leg_L_m",
        "foot_C_m", "foot_L_m",
    ]
    missing = [k for k in required if k not in data]
    if missing:
        print(f"Erreur: colonnes manquantes dans le CSV: {missing}")
        return

    m_kg = data["m_kg"]

    try:
        # Volumes (m³)
        v_head = volume_sphere_from_circumference(data["head_C_m"])
        v_trunk = volume_cylinder_from_circumference(data["trunk_C_m"], data["trunk_H_m"])

        v_hand_one = volume_cylinder_from_circumference(data["hand_C_m"], data["hand_L_m"])

        c_arm_avg = (data["biceps_C_m"] + data["forearm_C_m"]) / 2
        v_arm_one = volume_cylinder_from_circumference(c_arm_avg, data["arm_L_m"])

        # Jambe : 1 cylindre (cuisse + longueur jambe proxy)
        v_leg_one = volume_cylinder_from_circumference(data["thigh_C_m"], data["leg_L_m"])

        v_foot_one = volume_cylinder_from_circumference(data["foot_C_m"], data["foot_L_m"])
    except ValueError as e:
        print(f"Erreur: mesure invalide: {e}")
        return

    v_total = (
        v_trunk
        + v_head
        + 2 * v_arm_one
        + 2 * v_hand_one
        + 2 * v_leg_one
        + 2 * v_foot_one
    )

    # Physique
    weight_n = m_kg * g
    buoyant_force_n = rho * g * v_total
    apparent_weight_n = weight_n - buoyant_force_n
    density_kg_m3 = m_kg / v_total
    apparent_mass_kg = apparent_weight_n / g

    print("--- :) Résultats  :) ---")
    print(f"Volume total V_total = {v_total:.6f} m³")
    print(f"Densité moyenne rho_obj = {density_kg_m3:.2f} kg/m³")
    print(f"Poids P = {weight_n:.2f} N")
    print(f"Poussée F_A = {buoyant_force_n:.2f} N")
    print(f"Poids apparent P_app = {apparent_weight_n:.2f} N")
    print(f"Masse apparente équivalente = {apparent_mass_kg:.2f} kg")

    if apparent_weight_n > 0:
        print("Verdict : tendance à COULER (P > F_A).")
    elif apparent_weight_n < 0:
        print("Verdict : tendance à FLOTTER (F_A > P).")
    else:
        print("Verdict : équilibre (P ≈ F_A).")


if __name__ == "__main__":
    main()

def main():
    data = read_one_person_csv("one_person_for_python.csv")

    # test
    print("Masse (kg) =", data["m_kg"])
    print("Tour de taille (m) =", data["trunk_C_m"])

  

