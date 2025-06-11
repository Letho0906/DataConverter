import sys
import os
import json
import yaml
import xml.etree.ElementTree as ET

def parse_args():
    if len(sys.argv) != 3:
        print("Użycie: converter.exe pathWejsciowy pathWyjsciowy")
        sys.exit(1)
    return sys.argv[1], sys.argv[2]

def detect_format(path):
    if path.endswith(".json"):
        return "json"
    elif path.endswith(".yaml") or path.endswith(".yml"):
        return "yaml"
    elif path.endswith(".xml"):
        return "xml"
    else:
        raise ValueError(f"Nieznane rozszerzenie pliku: {path}")

def read_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Błąd wczytywania JSON: {e}")
        sys.exit(1)

def read_yaml(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Błąd wczytywania YAML: {e}")
        sys.exit(1)

def read_xml(path):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        return {child.tag: child.text for child in root}
    except Exception as e:
        print(f"Błąd wczytywania XML: {e}")
        sys.exit(1)



def write_json(data, path):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Błąd zapisu JSON: {e}")
        sys.exit(1)

def write_yaml(data, path):
    try:
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f)
    except Exception as e:
        print(f"Błąd zapisu YAML: {e}")
        sys.exit(1)

def write_xml(data, path):
    try:
        root = ET.Element("root")
        for key, val in data.items():
            ET.SubElement(root, key).text = str(val)
        tree = ET.ElementTree(root)
        tree.write(path, encoding="utf-8", xml_declaration=True)
    except Exception as e:
        print(f"Błąd zapisu XML: {e}")
        sys.exit(1)


def convert(in_path, out_path):
    in_fmt = detect_format(in_path)
    out_fmt = detect_format(out_path)


    if in_fmt == "json":
        data = read_json(in_path)
    elif in_fmt == "yaml":
        data = read_yaml(in_path)
    elif in_fmt == "xml":
        data = read_xml(in_path)


    if out_fmt == "json":
        write_json(data, out_path)
    elif out_fmt == "yaml":
        write_yaml(data, out_path)
    elif out_fmt == "xml":
        write_xml(data, out_path)

    print(f"Pomyślnie przekonwertowano z {in_fmt} na {out_fmt}.")

if __name__ == "__main__":
    in_file, out_file = parse_args()
    convert(in_file, out_file)
