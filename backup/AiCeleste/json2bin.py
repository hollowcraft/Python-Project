import json
import lzma
import yaml

json_file = r"C:\Program Files (x86)\Steam\steamapps\common\Celeste\Mods\AllHollow\Maps\IAtest\test.bin.saving.json"
bin_file = r"C:\Program Files (x86)\Steam\steamapps\common\Celeste\Mods\AllHollow\Maps\IAtest\test.bin"

# Conversion JSON → structure YAML
def convert_node(node):
    if isinstance(node, dict):
        if "__name" in node:
            name = node["__name"]
            children = node.get("__children", [])
            value = {k: convert_node(v) for k, v in node.items() if k not in ["__name", "__children"]}
            for child in children:
                converted = convert_node(child)
                if isinstance(converted, dict):
                    value.update(converted)
            return {name: value}
        elif "__children" in node:
            children = node["__children"]
            value = {k: convert_node(v) for k, v in node.items() if k != "__children"}
            for child in children:
                converted = convert_node(child)
                if isinstance(converted, dict):
                    value.update(converted)
            return value
        else:
            return {k: convert_node(v) for k, v in node.items()}
    elif isinstance(node, list):
        return [convert_node(item) for item in node]
    else:
        return node

# Lire le JSON
with open(json_file, "r", encoding="utf-8") as f:
    json_data = json.load(f)

data = convert_node(json_data["data"])
yaml_text = yaml.dump(data, allow_unicode=True, sort_keys=False)

# Configuration LZMA brute (format RAW comme dans Celeste)
filters = [{
    "id": lzma.FILTER_LZMA1,
    "dict_size": 1 << 23,
    "lc": 3,
    "lp": 0,
    "pb": 2
}]

# Compression RAW
compressed = lzma.compress(yaml_text.encode("utf-8"), format=lzma.FORMAT_RAW, filters=filters)

# Sauvegarde
with open(bin_file, "wb") as f:
    f.write(compressed)

print("✅ Fichier .bin encodé au format brut (raw) pour Celeste.")