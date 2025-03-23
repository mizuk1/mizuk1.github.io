from .weapon_processor import calculate_dps, BASE_WEAPONS, family


def normalize_mods(parsed_data):
    """
    Converte a saída de parse_item_modifiers para o formato usado por weapon_processor.py
    """
    mods = parsed_data["modifiers"]
    dmg_mods = {
        "add_physical": {"min": 0, "max": 0},
        "increased_physical": {"min": 0, "max": 0},
        "attack_speed": {"min": 0, "max": 0}
    }

    for mod in mods:
        name = mod["mod_name"]
        values = mod["values_normalized"]

        if name in family["PhysicalDamage"] and len(values) >= 2:
            dmg_mods["add_physical"]["min"] += values[0]["min"]
            dmg_mods["add_physical"]["max"] += values[0]["max"]
            dmg_mods["add_physical"]["min"] += values[1]["min"]
            dmg_mods["add_physical"]["max"] += values[1]["max"]

        elif name in family["LocalPhysicalDamagePercent"]:
            dmg_mods["increased_physical"]["min"] += values[0]["min"]
            dmg_mods["increased_physical"]["max"] += values[0]["max"]

        elif name in family["LocalIncreasedPhysicalDamagePercentAndAccuracyRating"]:
            dmg_mods["increased_physical"]["min"] += values[0]["min"]
            dmg_mods["increased_physical"]["max"] += values[0]["max"]

        elif name in family["IncreasedAttackSpeed"]:
            dmg_mods["attack_speed"]["min"] += values[0]["min"]
            dmg_mods["attack_speed"]["max"] += values[0]["max"]

    return dmg_mods


def detect_weapon_type(item_class):
    """
    Traduz o nome da classe para a chave usada em BASE_WEAPONS
    """
    class_map = {
        "Bows": "weapon.bow",
        "Crossbows": "weapon.crossbow",
        "Two Hand Maces": "weapon.twomace",
        "Quarterstaves": "weapon.warstaff"
    }
    return class_map.get(item_class, None)


def calculate_weapon_dps(parsed_data):
    """
    Função principal: junta tudo e calcula o DPS real
    """
    weapon_type = detect_weapon_type(parsed_data["item_class"])
    if weapon_type is None:
        raise ValueError(f"Classe de arma não suportada: {parsed_data['item_class']}")

    base_type = parsed_data["item_type"]
    if base_type not in BASE_WEAPONS.get(weapon_type, {}):
        raise ValueError(f"Tipo de arma não encontrado em BASE_WEAPONS: {base_type}")

    dmg_mods = normalize_mods(parsed_data)
    weapon_info = {"base_type": base_type}
    min_dps, max_dps = calculate_dps(weapon_type, weapon_info, dmg_mods)
    avg_dps = round((min_dps + max_dps) / 2, 2)

    return {
        "min_dps": min_dps,
        "max_dps": max_dps,
        "avg_dps": avg_dps
    }
