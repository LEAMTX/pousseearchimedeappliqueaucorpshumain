ansur <- read.csv("ANSUR_II_MALE_Public.csv", stringsAsFactors = FALSE)

set.seed(42)
p <- ansur[sample(nrow(ansur), 1), ]

mm_to_m <- function(x) x / 1000

# Longueurs dédiées jambe (en mm)
thigh_L_mm <- p$buttockkneelength
calf_L_mm  <- p$kneeheightmidpatella - p$lateralmalleolusheight

# Sécurité : éviter une longueur négative 
if (is.na(calf_L_mm) || calf_L_mm <= 0) {
  calf_L_mm <- NA
}

vals <- data.frame(
  subjectid = p$subjectid,
  m_kg = p$weightkg / 10, 

  head_C_m = mm_to_m(p$headcircumference),

  hand_C_m = mm_to_m(p$handcircumference),
  hand_L_m = mm_to_m(p$handlength),

  biceps_C_m  = mm_to_m(p$bicepscircumferenceflexed),
  forearm_C_m = mm_to_m(p$forearmcircumferenceflexed),
  arm_L_m     = mm_to_m(p$shoulderelbowlength),

  # Jambe : CUISSE + MOLLET (2 cylindres)
  thigh_C_m = mm_to_m(p$thighcircumference),
  thigh_L_m = mm_to_m(thigh_L_mm),

  calf_C_m  = mm_to_m(p$calfcircumference),
  calf_L_m  = mm_to_m(calf_L_mm),

  foot_C_m = mm_to_m(p$balloffootcircumference),
  foot_L_m = mm_to_m(p$footlength),

  trunk_C_m = mm_to_m(p$waistcircumference),
  trunk_H_m = mm_to_m(p$sittingheight - p$headlength)
)

print(vals, row.names = FALSE)
write.csv(vals, "one_person_for_python.csv", row.names = FALSE)
