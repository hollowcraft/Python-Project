import json

save_file = r"C:\Users\Adam\AppData\LocalLow\Hopoo Games, LLC\Risk of Rain 2\ProperSave\Saves\9bd28171-08b2-473c-bd8e-0df603743fef.json"
with open(save_file, "r", encoding="utf-8") as f:
    save_content = json.load(f)

for i in range(len(save_content["p"][1]["m"]["i"]["i"])):
    if save_content["p"][1]["m"]["i"]["i"][i]["i"] == 216:
        save_content["p"][1]["m"]["i"]["i"][i]["c"] += 10
        print(save_content["p"][1]["m"]["i"]["i"][i]["c"])

with open(save_file, "w", encoding="utf-8") as f:
    json.dump(save_content, f, ensure_ascii=False, indent=4)
