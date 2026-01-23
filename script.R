# ============================================================
# Projet : Poussée d’Archimède — préparation des données ANSUR II (R)
# ============================================================
# Objectif
# - Tirer 1 individu depuis ANSUR II de façon reproductible
# - Convertir les mesures en unités SI (m, kg)
# - Exporter un CSV minimal et cohérent avec le modèle Python :
#     jambe = 1 cylindre (circonférence de cuisse + longueur de jambe proxy)
#
# Source ANSUR II : https://www.openlab.psu.edu/ansur2/
# ============================================================

ansur <- read.csv("ANSUR_II_MALE_Public.csv", stringsAsFactors = FALSE)

set.seed(42)
p <- ansur[sample(nrow(ansur), 1), ]

mm_to_m <- function(x) x / 1000

# Contrôle simple : on arrête si une mesure indispensable est manquante ou non positive
assert_positive <- function(x, name) {
  if (length(x) != 1 || is.na(x) || !is.numeric(x) || x <= 0) {
    stop(paste0("Valeur invalide pour '", name, "': ", x))
  }
  x
}

# ------------------------------------------------------------
# 1) Masse : le fichier, weightkg est encodé *10
# montré par : médiane ~846 -> 84.6 kg)
# ------------------------------------------------------------
assert_positive(p$weightkg, "weightkg")
m_kg <- p$weightkg / 10

# ------------------------------------------------------------
# 2) Longueur jambe (proxy)
# Choix : buttockkneelength (mm)  —  la distance horizontale entre l’arrière de la fesse (buttock) et l’avant du genou (knee), approximation assumée.
# ------------------------------------------------------------
leg_L_mm <- assert_positive(p$buttockkneelength, "buttockkneelength")

# ------------------------------------------------------------
# 3) Tronc = hauteur du tronc ≈ hauteur assise hauteur (du siège jusqu’au sommet de la tête ) − hauteur de la tête (menton → sommet du crâne) : sittingheight - headlength doit être > 0
# ------------------------------------------------------------
trunk_H_mm <- p$sittingheight - p$headlength
assert_positive(trunk_H_mm, "trunk_H_mm = sittingheight - headlength")

# ------------------------------------------------------------
# 4) Contrôles des champs nécessaires
# ------------------------------------------------------------
assert_positive(p$headcircumference, "headcircumference")
assert_positive(p$handcircumference, "handcircumference")
assert_positive(p$handlength, "handlength")
assert_positive(p$bicepscircumferenceflexed, "bicepscircumferenceflexed")
assert_positive(p$forearmcircumferenceflexed, "forearmcircumferenceflexed")
assert_positive(p$shoulderelbowlength, "shoulderelbowlength")
assert_positive(p$thighcircumference, "thighcircumference")
assert_positive(p$balloffootcircumference, "balloffootcircumference")
assert_positive(p$footlength, "footlength")
assert_positive(p$waistcircumference, "waistcircumference")

# ------------------------------------------------------------
# 5) Construction du CSV (colonnes alignées avec Python)
# ------------------------------------------------------------
vals <- data.frame(
  subjectid = p$subjectid,
  m_kg = m_kg,

  head_C_m = mm_to_m(p$headcircumference),

  hand_C_m = mm_to_m(p$handcircumference),
  hand_L_m = mm_to_m(p$handlength),

  biceps_C_m  = mm_to_m(p$bicepscircumferenceflexed),
  forearm_C_m = mm_to_m(p$forearmcircumferenceflexed),
  arm_L_m     = mm_to_m(p$shoulderelbowlength),

  # Jambe : 1 cylindre (cuisse + longueur jambe proxy)
  thigh_C_m = mm_to_m(p$thighcircumference),
  leg_L_m   = mm_to_m(leg_L_mm),

  foot_C_m = mm_to_m(p$balloffootcircumference),
  foot_L_m = mm_to_m(p$footlength),

  trunk_C_m = mm_to_m(p$waistcircumference),
  trunk_H_m = mm_to_m(trunk_H_mm)
)

print(vals, row.names = FALSE)
write.csv(vals, "one_person_for_python.csv", row.names = FALSE)
message("CSV exporté : one_person_for_python.csv")
