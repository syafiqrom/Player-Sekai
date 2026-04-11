import json

def extract_assetbundle_names(data, result):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "givenNameEnglish":
                result.append(value.capitalize())
            else:
                extract_assetbundle_names(value, result)
    elif isinstance(data, list):
        for item in data:
            extract_assetbundle_names(item, result)

# read input file
with open("gameCharacters.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# extract values
given_name_english = []
extract_assetbundle_names(data, given_name_english)

# write to new file
with open("char.json", "w", encoding="utf-8") as f:
    json.dump(given_name_english, f, indent=2, ensure_ascii=False)

print(f"Extracted {len(given_name_english)} givenNameEnglish values.")