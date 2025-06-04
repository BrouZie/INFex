# Full length
Lx = 5
Ly = 40
Lz = 5

# Density
RHO_VAPOUR = 0.02
RHO_LIQUID = 0.73

# Ratio of 2:1:2 = 5 (in y direction)
SUM_RATIO = 5

# Ratio for each "box" --> vapour = 2 and liquid = 1
RATIO_VAPOUR = 2
RATIO_LIQUID = 1

# Min and max values for each box along y axis
############################################################
PART_Y = Ly / SUM_RATIO  # Length divided by sum og parts
# ----------------------------------------------------------
Y_VAPOUR_LEFT_MAX = RATIO_VAPOUR * PART_Y  # = 2 / 5 * Ly
# ----------------------------------------------------------
Y_LIQUID_MIN = Y_VAPOUR_LEFT_MAX
Y_LIQUID_MAX = RATIO_VAPOUR * PART_Y + RATIO_LIQUID * PART_Y
# ----------------------------------------------------------
Y_VAPOUR_RIGHT_MIN = Y_LIQUID_MAX
Y_VAPOUR_RIGHT_MAX = Ly
############################################################

DEFAULT_MASS = 1
