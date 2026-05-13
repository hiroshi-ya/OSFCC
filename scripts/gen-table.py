# Generates the table for everything in the font-db.
# Author: HiroshiYa

from ruamel.yaml import YAML
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
db_path = f"{BASE_DIR}/../font-db"
family_path = f"{db_path}/families"
header_path = f"{BASE_DIR}/md-header"
gen_path = f"{BASE_DIR}/../table-gen"

yaml = YAML()

# read licenses and styles
with open(f"{db_path}/licenses.yaml", "r", encoding="utf-8") as f:
    licenses = yaml.load(f)
    licenses = licenses["licenses"]
with open(f"{db_path}/styles.yaml", "r", encoding="utf-8") as f:
    styles = yaml.load(f)
    styles = styles["styles"]

# load font families
families = {}
glob_yaml = Path(family_path)
for family_yaml_file in glob_yaml.glob("*.y*ml"):
    with open(family_yaml_file, "r", encoding="utf-8") as f:
        family_yaml = yaml.load(f)
        family_name = family_yaml_file.name.split('.')[0]
        families[family_name] = family_yaml[family_name]

# load the markdown header
with open(f"{header_path}/general.md", 'r', encoding='utf-8') as f:
    header = f.read()

# write the table
with open(f"{gen_path}/gen.md", 'w', encoding='utf-8') as f:
    f.write(header)

    # iterate through families
    for family in families:
        curr_family = families[family]
        ##############################
        # family name
        if curr_family["url"] is None:
            family_name = f"|{curr_family["name"]}|"
        else:
            family_name = f"|[{curr_family["name"]}]({curr_family["url"]})|"
        ##############################
        # iterate through fonts under the family
        for font in curr_family["fonts"]:
            f.write(family_name)
            if font["url"] is None:
                f.write(f"{font["name"]}|")
            else:
                f.write(f"[{font["name"]}]({font["url"]})|")
            ##############################
            # iterate through devs
            dev_len = len(font["dev"])
            dev_count = 0
            for dev in font["dev"]:
                if dev["url"] is None:
                    f.write(f"{dev["name"]}")
                else:
                    f.write(f"[{dev["name"]}]({dev["url"]})")
                dev_count += 1
                if dev_count != dev_len:
                    f.write(" & ")
            f.write('|')
            ##############################
            # font style
            font_style = font["style"]
            f.write(f"{styles[font_style]["abbr"]}|")
            ##############################
            # font weight count
            font_weight = font["weight_count"]
            f.write(f"{font_weight}|")
            ##############################
            # iterate through font licenses
            lic_len = len(font["licenses"])
            lic_count = 0
            for lic in font["licenses"]:
                lic_name = licenses[lic["id"]]
                f.write(f"[{lic["id"]}]({lic_name["url"]})")
                lic_count += 1
                if lic_count != lic_len:
                    div = r" \| " # default to use "or"
                    if "relation" in lic:
                        if lic["relation".lower()] == "and":
                            div = " & "
                    f.write(div)
            f.write('|')
            ##############################
            # check language support
            support = font["support"]
            if support["chs"]:
                f.write("✓|")
            else:
                f.write('|')
            if support["cht"]:
                f.write("✓|")
            else:
                f.write('|')
            if support["jpn"]:
                f.write("✓|")
            else:
                f.write('|')
            if support["kor"]:
                f.write("✓|")
            else:
                f.write('|')
            ##############################
            # ending the row
            f.write('\n')
            ##############################
            family_name = "|〃|" # avoid repeating the family name

        
# print(families.keys())