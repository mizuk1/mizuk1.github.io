import numpy as np

# Informações base de cada tipo de arma
BASE_WEAPONS = {
    "weapon.bow": {
        "Expert Shortbow": {"phyDamage": 58.5, "attacksPs": 1.25},
        "Expert Composite Bow": {"phyDamage": 65.5, "attacksPs": 1.2},
        "Expert Warden Bow": {"phyDamage": 66.5, "attacksPs": 1.15},
        "Expert Dualstring Bow": {"phyDamage": 56, "attacksPs": 1.2},
        "Expert Cultist Bow": {"phyDamage": 69.5, "attacksPs": 1.2},
        "Expert Zealot Bow": {"phyDamage": 70, "attacksPs": 1.2},
    },
    "weapon.crossbow": {
        "Expert Sturdy Crossbow": {"phyDamage": 63.5, "attacksPs": 1.55},
        "Expert Varnished Crossbow": {"phyDamage": 65.5, "attacksPs": 1.6},
        "Expert Tense Crossbow": {"phyDamage": 66, "attacksPs": 1.6},
        "Expert Dyad Crossbow": {"phyDamage": 55.5, "attacksPs": 1.6},
        "Expert Bombard Crossbow": {"phyDamage": 60.5, "attacksPs": 1.65},
        "Expert Forlorn Crossbow": {"phyDamage": 70, "attacksPs": 1.6}
    },
    "weapon.twomace": {
        "Expert Forge Maul": {"phyDamage": 131.5, "attacksPs": 1.05},
        "Expert Temple Maul": {"phyDamage": 117, "attacksPs": 1.2},
        "Expert Oak Greathammer": {"phyDamage": 134, "attacksPs": 1.05},
        "Expert Cultist Greathammer": {"phyDamage": 104.5, "attacksPs": 1.05},
        "Expert Crumbling Maul": {"phyDamage": 125.5, "attacksPs": 1.1},
        "Expert Leaden Greathammer": {"phyDamage": 140, "attacksPs": 1.1}
    },
    "weapon.warstaff": {
        "Expert Gothic Quarterstaff": {"phyDamage": 73.5, "attacksPs": 1.4},
        "Expert Crescent Quarterstaff": {"phyDamage": 76.5, "attacksPs": 1.5},
        "Expert Long Quarterstaff": {"phyDamage": 82, "attacksPs": 1.4},
        "Expert Barrier Quarterstaff": {"phyDamage": 77.5, "attacksPs": 1.4},
        "Expert Slicing Quarterstaff": {"phyDamage": 86.5, "attacksPs": 1.4}
    },
}

# TODO
# Usar os mods pra calcular o dps direito, ta tudo bagunçado essa porra
family = {
    "PhysicalDamage": ["Glinting", "Burnished", "Polished", "Honed", "Gleaming", "Annealed", "Razor-sharp", "Tempered", "Flaring"],
    "LocalPhysicalDamagePercent": ["Heavy", "Serrated", "Wicked", "Vicious", "Bloodthirsty", "Cruel", "Tyrannical", "Merciless"],
    "LocalIncreasedPhysicalDamagePercentAndAccuracyRating": ["Squire's", "Journeyman's", "Reaver's", "Mercenary's", "Champion's", "Conqueror's", "Emperor's", "Dictator's"],
    "IncreasedAttackSpeed": ["of Skill", "of Ease", "of Mastery", "of Renown", "of Acclaim", "of Fame", "of Infamy", "of Celebration"]
}

def calculate_dps(weapon_type, weapon, dmg_mods):
    """Calcula o DPS real do item."""
    if weapon["base_type"] not in BASE_WEAPONS[weapon_type]:
        return 0, 0, 0

    base_stats = BASE_WEAPONS[weapon_type][weapon["base_type"]]
    physical_damage = base_stats["phyDamage"]
    attack_speed = base_stats["attacksPs"]

    try:
        min_added_physical_damage = dmg_mods.get("add_physical", {}).get("min", 0) / 2
        max_added_physical_damage = dmg_mods.get("add_physical", {}).get("max", 0) / 2
    except:
        pass

    try:
        min_increased_physical_damage = dmg_mods.get("increased_physical", {}).get("min", 0)
        max_increased_physical_damage = dmg_mods.get("increased_physical", {}).get("max", 0)
    except:
        pass
    
    try:
        min_increased_attack_speed = dmg_mods.get("attack_speed", {}).get("min", 0)
        max_increased_attack_speed = dmg_mods.get("attack_speed", {}).get("max", 0)
    except:
        pass

    min_increased_physical_damage += 40
    max_increased_physical_damage += 40

    min_dps = ((physical_damage + min_added_physical_damage) * 1.2) * (1 + (min_increased_physical_damage / 100)) * (attack_speed * (1 + (min_increased_attack_speed / 100)))
    max_dps = ((physical_damage + max_added_physical_damage) * 1.2) * (1 + (max_increased_physical_damage / 100)) * (attack_speed * (1 + (max_increased_attack_speed / 100)))
    
    return round(min_dps, 2), round(max_dps, 2)

def process_weapon(weapon_type, item_data):
    """Processa qualquer tipo de arma e calcula DPS."""
    if weapon_type not in BASE_WEAPONS:
        return None

    weapon = {
        "id": item_data.get("id", ""),
        "type": weapon_type,
        "base_type": item_data.get("item", {}).get("baseType", ""),
        "name": item_data.get("item", {}).get("name", ""),
        "pdps": item_data.get("item", {}).get("extended", {}).get("pdps", 0.0),
        "min_dps": None,
        "max_dps": None,
        "avg_dps": None,
        "mods": item_data.get("item", {}).get("extended", {}).get("mods", {}).get("explicit", []),
        "afix": item_data.get("item", {}).get("explicitMods", {}),
        "price": item_data.get("listing", {}).get("price", {}).get("amount", 0.0),
        "currency": item_data.get("listing", {}).get("price", {}).get("currency", ""),
    }

    # Processa modificações específicas
    dmg_mods = {
        "add_physical": {"min": 0, "max": 0},
        "increased_physical": {"min": 0, "max": 0},
        "attack_speed": {"min": 0, "max": 0}
    }

    for mod in weapon["mods"]:
        if mod["name"] in family["PhysicalDamage"]:
            dmg_mods["add_physical"]["min"] += int(mod["magnitudes"][0]["min"])
            dmg_mods["add_physical"]["max"] += int(mod["magnitudes"][0]["max"])
            dmg_mods["add_physical"]["min"] += int(mod["magnitudes"][1]["min"])
            dmg_mods["add_physical"]["max"] += int(mod["magnitudes"][1]["max"])
        elif mod["name"] in family["LocalPhysicalDamagePercent"]:
            dmg_mods["increased_physical"]["min"] += int(mod["magnitudes"][0]["min"])
            dmg_mods["increased_physical"]["max"] += int(mod["magnitudes"][0]["max"])
        elif mod["name"] in family["LocalIncreasedPhysicalDamagePercentAndAccuracyRating"]:
            dmg_mods["increased_physical"]["min"] += int(mod["magnitudes"][0]["min"])
            dmg_mods["increased_physical"]["max"] += int(mod["magnitudes"][0]["max"])
        elif mod["name"] in family["IncreasedAttackSpeed"]:
            dmg_mods["attack_speed"]["min"] += int(mod["magnitudes"][0]["min"])
            dmg_mods["attack_speed"]["max"] += int(mod["magnitudes"][0]["max"])

    if weapon["base_type"] in BASE_WEAPONS[weapon_type]:
        weapon["min_dps"], weapon["max_dps"] = calculate_dps(weapon_type, weapon, dmg_mods)

    weapon["avg_dps"] = float(np.mean([weapon["min_dps"] or 0.0, weapon["max_dps"] or 0.0]))
    weapon["avg_dps"] = round(weapon["avg_dps"], 2)
    
    return weapon
