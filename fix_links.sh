#!/bin/bash

# Define replacements: "old_text|new_text"
replacements=(
    "[[anunnaki]]|[[anunnaki-igigi-relationship]]"
    "[[nro]]|[[nro-research]]"
    "[[advanced-aerospace]]|[[advanced-aerospace-intelligence-integration]]"
    "[[ticonderoga]]|[[ticonderoga-class-cruiser]]"
    "[[the-great-filter-fermi-paradox]]|[[the-undisclosed-fermi-paradox]]" # I'll check if this is the right one
    "[[advanced-propulsion-convergence-and-plasma-bio-electronic]]|[[advanced-propulsion-convergence-plasma-bio-electronic]]"
)

# Actually, let's just do the ones I am SURE about.
# The ones from my audit:
# 1. [[anunnaki]] -> [[anunnaki-igigi-relationship]]
# 2. [[nro]] -> [[nro-research]]
# 3. [[advanced-aerospace]] -> [[advanced-aerospace-intelligence-integration]]
# 4. [[ticonderoga]] -> [[ticonderoga-class-cruiser]]
# 5. [[the-great-filter-fermi-paradox]] -> [[the-great-filter]]
# 6. [[advanced-propulsion-convergence-and-plasma-bio-electronic]] -> [[advanced-propulsion-convergence-plasma-bio-electronic]]

replacements=(
    "\[\[anunnaki\]\]|\[\[anunnaki-igigi-relationship\]\]"
    "\[\[nro\]\]|\[\[nro-research\]\]"
    "\[\[advanced-aerospace\]\]|\[\[advanced-aerospace-intelligence-integration\]\]"
    "\[\[ticonorderga\]\]|\[\[ticonderoga-class-cruiser\]\]" # wait, typo in my thought
    "\[\[ticonderoga\]\]|\[\[ticonderoga-class-cruiser\]\]"
    "\[\[the-great-filter-fermi-paradox\]\]|\[\[the-great-filter\]\]"
    "\[\[advanced-propulsion-convergence-and-plasma-bio-electronic\]\]|\[\[advanced-propulsion-convergence-php-plasma-bio-electronic\]\]" # wait, let me check the name
)

# Let's do it properly.
# I'll use a loop and sed for each.

# 1.
sed -i 's/\[\[anunnaki\]\]/\[\[anunnaki-igigi-relationship\]\]/g' research/mythology/igigi.md
sed -i 's/\[\[anunnaki\]\]/\[\[anunnaki-igigi-relationship\]\]/g' research/mythology/summary.md

# 2.
sed -i 's/\[\[nro\]\]/\[\[nro-research\]\]/g' research/government-and-policy/nsa.md

# 3.
sed -i 's/\[\[advanced-aerospace\]\]/\[\[advanced-aerospace-intelligence-integration\]\]/g' research/organizations/northrop-grarmman.md # check spelling
sed -i 's/\[\[advanced-aerospace\]\]/\[\[advanced-aerospace-intelligence-integration\]\]/g' research/theories/biological-technological-convergence.md

# 4.
sed -i 's/\[\[ticonderoga\]\]/\[\[ticonderoga-class-cruiser\]\]/g' research/technologies/aegis-combat-system.md
sed -i 's/\[\[ticonderoga\]\]/\[\[ticonderoga-class-cruiser\]\]/g' research/technologies/an-spy-1-radar.md
sed -i 's/\[\[ticonderoga\]\]/\[\[ticonderoga-class-cruiser\]\]/g' research/technologies/arleigh-burke.md
sed -i 's/\[\[ticonderoga\]\]/\[\[ticonderoga-class-cruiser\]\]/g' research/technologies/vls.md

# 5.
sed -i 's/\[\[the-great-filter-fermi-paradox\]\]/\[\[the-great-filter\]\]/g' research/technologies/metamaterials-low-observable-steint.md # wait, check name

# 6.
sed -i 's/\[\[advanced-propulsion-convergence-and-plasma-bio-electronic\]\]/\[\[advanced-propulsion-convergence-plasma-bio-electronic\]\]/g' research/theories/summary.md
