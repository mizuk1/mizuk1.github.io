import re
from typing import List, Dict, Any


def parse_item_modifiers(text: str) -> Dict[str, Any]:
    lines = text.splitlines()
    item_data = {
        "item_class": "",
        "item_type": "",
        "modifiers": []
    }

    current_mod = None
    reading_mods = False

    mod_header_pattern = re.compile(
        r'^\{\s*(Prefix|Suffix) Modifier "(.+?)"\s+\(Tier: (\d+)\)(?: — (.+?))?\s*\}$'
    )
    value_range_pattern = re.compile(r'([-+]?\d+)(?:\((\d+)-(\d+)\))?')

    for line in lines:
        stripped = line.strip()

        # Detect item class
        if stripped.startswith("Item Class:"):
            item_data["item_class"] = stripped.split(":", 1)[1].strip()
            continue

        # Detect item type (linha após o nome do item)
        if not item_data["item_type"] and "--------" not in stripped and not stripped.startswith("Rarity:") and not stripped.startswith("Item Level") and not ":" in stripped:
            if item_data.get("name_seen"):
                item_data["item_type"] = stripped
            else:
                item_data["name_seen"] = True
            continue

        header_match = mod_header_pattern.match(stripped)
        if header_match:
            # Começo de um novo modificador
            current_mod = {
                'mod_type': header_match.group(1).lower(),  # prefix/suffix
                'mod_name': header_match.group(2),
                'tier': int(header_match.group(3)),
                'mod_group': header_match.group(4) or '',
                'text_line': '',
                'values_normalized': {}
            }
            reading_mods = True
            continue

        if current_mod and stripped != "":
            current_mod['text_line'] = stripped

            # Extração de valores
            matches = value_range_pattern.findall(stripped)
            values = []
            for val, r_min, r_max in matches:
                if r_min and r_max:
                    values.append({
                        'value': int(val),
                        'min': int(r_min),
                        'max': int(r_max)
                    })
                else:
                    values.append({
                        'value': int(val)
                    })

            current_mod['values_normalized'] = values
            item_data["modifiers"].append(current_mod)
            current_mod = None

    return item_data