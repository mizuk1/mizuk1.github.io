from django.test import TestCase

# Create your tests here.
from item_parser import parse_item_modifiers
from dps_calculator import calculate_weapon_dps

if __name__ == "__main__":
    item_text = r"""
Item Class: Bows
Rarity: Rare
Glyph Guide
Expert Warden Bow
--------
Quality: +20% (augmented)
Physical Damage: 327-497 (augmented)
Critical Hit Chance: 5.00%
Attacks per Second: 1.36 (augmented)
--------
Requires: Level 77, 212 (unmet) Dex
--------
Sockets: S S 
--------
Item Level: 83
--------
40% increased Physical Damage (rune)
--------
{ Implicit Modifier }
29(20-30)% chance to Chain an additional time (implicit)
--------
{ Prefix Modifier "Merciless" (Tier: 8) — Damage, Physical, Attack }
176(170-179)% increased Physical Damage
{ Prefix Modifier "Razor-sharp" (Tier: 7) — Damage, Physical, Attack }
Adds 22(16-24) to 34(28-42) Physical Damage
{ Prefix Modifier "Champion's" (Tier: 5) — Damage, Physical, Attack }
47(45-54)% increased Physical Damage
+115(98-123) to Accuracy Rating
{ Suffix Modifier "of Glory" (Tier: 7) — Life }
Gain 55(54-68) Life per Enemy Killed
{ Suffix Modifier "of Assimilation" (Tier: 8) — Mana }
Gain 38(36-45) Mana per Enemy Killed
{ Suffix Modifier "of Acclaim" (Tier: 5) — Attack, Speed }
18(17-19)% increased Attack Speed
--------
Corrupted
--------
Note: ~price 20 divine
    """.strip()

    parsed = parse_item_modifiers(item_text)
    dps_info = calculate_weapon_dps(parsed)

    print("DPS Calculado:")
    print(dps_info)