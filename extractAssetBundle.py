import json

def extract_assetbundle_names(data, result):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "assetbundleName":
                result.append(value)
            else:
                extract_assetbundle_names(value, result)
    elif isinstance(data, list):
        for item in data:
            extract_assetbundle_names(item, result)

# read input file
with open("musicVocals.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# extract values
assetbundle_names = []
extract_assetbundle_names(data, assetbundle_names)

# write to new file
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(assetbundle_names, f, indent=2, ensure_ascii=False)

print(f"Extracted {len(assetbundle_names)} assetbundleName values.")