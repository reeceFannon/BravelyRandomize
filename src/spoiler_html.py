import html
import json

def esc(x: str, quote: bool = True):
    return html.escape(str(x), quote = quote)

def portrait_path(game: str, job_name: str):
    return f"assets/{game}/Portraits/{job_name}.webp"

def icon_path(game: str, job_name: str):
    return f"assets/{game}/Icons/{job_name}.png"

def magic_path(game: str, mage_name: str):
    return f"assets/{game}/Magic/{mage_name}.png"

def location_path(loc_name: str):
    return f"assets/BD/Locations/{loc_name}.png"

def aptitude_path(grade: str):
    return f"assets/BS/Aptitudes/{grade}.png"

def ability_class(ability_type: str):
    match ability_type:
        case "command": return "ability-command"
        case "support": return "ability-support"
        case "magic_or_summon_level": return "ability-magic"
        case "job_or_magic_command": return "ability-magic"
        case _: return ""

def json_path(game: str):
    return f"assets/{game}/abilities.json"

def mage_to_magic(mage: str):
    match mage:
        case "Black Mage": return "Black Magic"
        case "White Mage": return "White Magic"
        case "Time Mage": return "Time Magic"
        case "Spell Fencer": return "Sword Magic"
        case "Summoner": return "Summoning"
        case "Red Mage": return "B/W Magic"
        case "Conjurer": return "Invocation"
        case "Bishop": return "Holy Magic"
        case "Wizard": return "Spirit Magic"
        case "Astrologian": return "Astral Magic"
        case "Yōkai": return "Diabolism"
        case _: return mage

def get_mage_spells(magic_data: dict):
    return {f"{mage_to_magic(mage.get('name',''))} Lv.{lvl.get('level','')}": ", ".join(spell.get("name","") for spell in lvl.get("spells",[])) for mage in magic_data.get("mages", []) for lvl in mage.get("levels", [])}

def resolve_BS_magic_ability_names(ability: str, level: str):
    if ability == "Black Magic":
        match level:
            case "1": return "Black Magic Lv.1"
            case "3": return "Black Magic Lv.2"
            case "4": return "Black Magic Lv.3"
            case "6": return "Black Magic Lv.4"
            case "7": return "Black Magic Lv.5"
            case "9": return "Black Magic Lv.6"
            case "11": return "Black Magic Lv.7"
    
    if ability == "White Magic":
        match level:
            case "1": return "White Magic Lv.1"
            case "3": return "White Magic Lv.2"
            case "4": return "White Magic Lv.3"
            case "5": return "White Magic Lv.4"
            case "7": return "White Magic Lv.5"
            case "9": return "White Magic Lv.6"
            case "11": return "White Magic Lv.7"

    if ability == "Time Magic":
        match level:
            case "1": return "Time Magic Lv.1"
            case "3": return "Time Magic Lv.2"
            case "5": return "Time Magic Lv.3"
            case "7": return "Time Magic Lv.4"
            case "8": return "Time Magic Lv.5"
            case "10": return "Time Magic Lv.6"
            case "11": return "Time Magic Lv.7"

    if ability == "Summoning":
        match level:
            case "1": return "Summoning Lv.1"
            case "2": return "Summoning Lv.2"
            case "5": return "Summoning Lv.3"
            case "9": return "Summoning Lv.4"
            case "11": return "Summoning Lv.5"

    if ability == "B/W Magic":
        match level:
            case "1": return "B/W Magic Lv.1"
            case "2": return "B/W Magic Lv.2"
            case "4": return "B/W Magic Lv.3"
            case "6": return "B/W Magic Lv.4"

    if ability == "Holy Magic":
        match level:
            case "1": return "Holy Magic Lv.1"
            case "2": return "Holy Magic Lv.2"
            case "4": return "Holy Magic Lv.3"
            case "5": return "Holy Magic Lv.4"
            case "8": return "Holy Magic Lv.5"
            case "9": return "Holy Magic Lv.6"
            case "11": return "Holy Magic Lv.7"

    if ability == "Spellcraft":
        match level:
            case "2": return "Spellcraft Lv.1"
            case "4": return "Spellcraft Lv.2"
            case "5": return "Spellcraft"
            case "6": return "Spellcraft Lv.3"
            case "9": return "Spellcraft Lv.4"
            case "11": return "Spellcraft Lv.5"

    if ability == "Astral Magic":
        match level:
            case "1": return "Astral Magic Lv.1"
            case "2": return "Astral Magic Lv.2"
            case "4": return "Astral Magic Lv.3"
            case "5": return "Astral Magic Lv.4"
            case "7": return "Astral Magic Lv.5"
            case "8": return "Astral Magic Lv.6"
            case "11": return "Astral Magic Lv.7"

    if ability == "Diabolism":
        match level:
            case "1": return "Diabolism Lv.1"
            case "3": return "Diabolism Lv.2"
            case "4": return "Diabolism Lv.3"
            case "5": return "Diabolism Lv.4"
            case "6": return "Diabolism Lv.5"
            case "8": return "Diabolism Lv.6"
            case "9": return "Diabolism Lv.7"
            case "11": return "Diabolism Lv.8"

    return ability.replace("’", "'")

def ability_description(ability_descriptions: dict, magic_descriptions: dict, ability: str):
    return ability_descriptions.get(ability, {}).get("Description", "").format(spells = magic_descriptions.get(ability, ""))

def write_magic_debug(spoiler_data: dict, path: str):
    jobs = spoiler_data.get("jobs", {})
    magic = spoiler_data.get("magic", {})

    lines = []
    lines.append("=== JOB ABILITY DEBUG ===")
    lines.append("")

    for row in jobs.get("job_abilities", []):
        job = row.get("job", "")
        lines.append(f"JOB: {repr(job)}")

        for abil in row.get("abilities", []):
            name = abil.get("name", "")
            level = abil.get("level", "")

            lines.append(
                f"  ability name: {repr(name)} | "
                f"level: {repr(level)} | "
                f"level type: {type(level).__name__}"
            )

        lines.append("")

    lines.append("")
    lines.append("=== MAGIC / MAGE DEBUG ===")
    lines.append("")

    for mage in magic.get("mages", []):
        mage_name = mage.get("name", "")
        lines.append(f"mage name: {repr(mage_name)}")

        for lvl in mage.get("levels", []):
            level = lvl.get("level", "")
            spell_names = [
                spell.get("name", "")
                for spell in lvl.get("spells", [])
            ]

            lines.append(
                f"  magic level: {repr(level)} | "
                f"level type: {type(level).__name__} | "
                f"spells: {repr(spell_names)}"
            )

        lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def insert_styles():
    return """
    <style>
    :root {--bg-main: #0b0c10; --text: #e6e6e6; --card: #111318; --border: #DFE0E8; --bg-dark: #272930; --bg-light: #505057}

    body {font-family: Arial, sans-serif; margin: 0 auto; background: var(--bg-main); color: var(--text); text-align: center}
    h1 {font-size: 3rem; margin: 0.4em 0 0.25em; color: var(--text)}
    h2 {font-size: 2.25rem; margin-top: 1.4em; color: var(--text)}
    table {border-collapse: collapse; margin: 0 auto; color: var(--text)}
    th, td {border: 1px solid var(--border); color: var(--text); padding: 6px 10px}
    th {background-color: var(--bg-dark)}
    td {background-color: var(--bg-light)}
    details {margin: 1em 0 1.5em}
    summary {cursor: pointer; font-size: 2.25em; font-weight: bold; margin: 1em 0}
    summary:hover {text-decoration: underline}
    details > table {margin-top: 0.5em}
    .job-card-grid {display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; max-width: 1500px; margin: 0 auto; justify-items: center}
    .job-card {width: 100%; max-width: 460px; display: grid; grid-template-columns: 135px minmax(0, 1fr); gap: 12px; align-items: stretch; background: var(--bg-dark); border: 2px solid var(--border); border-radius: 12px; padding: 10px; box-shadow: 0 2px 8px #000000}
    .job-card-left {display: grid; grid-template-rows: 1fr auto auto; text-align: center; align-items: end; min-height: 100%}
    .job-portrait {width: 125px; height: 170px; max-width: 100%; object-fit: contain; align-self: end; justify-self: center}
    .job-name {font-weight: bold; font-size: 1.15em; margin-top: 8px; color: var(--text)}
    .job-specialty {font-size: 0.95em; color: var(--text); margin-top: 4px}
    .job-abilities-table {width: 100%; margin-bottom: 0 auto; border-collapse: collapse; border-radius: 12px; overflow: hidden}
    .job-abilities-table th {border: 1px solid var(--border); color: var(--text); padding: 6px 10px; background-color: var(--bg-dark)}
    .job-abilities-table td {border: 1px solid var(--border); color: #000; padding: 6px 10px}
    .job-abilities-table th:first-child, .job-abilities-table td:first-child {text-align: center; width: 42px}
    .job-abilities-table th:last-child, .job-abilities-table td:last-child {text-align: center; width: 52px}
    .ability-command td {background-color: #ffe5cc}
    .ability-support td {background-color: #cce5ff}
    .ability-magic td {background-color: #f8cccc}
    .ability-tooltip:hover {filter: brightness(0.95)}
    #floating-tooltip {display: none; position: fixed; z-index: 999999; max-width: 340px; background: #222; color: var(--text); padding: 10px 12px; border: 1px solid var(--border); font-size: 0.9em; line-height: 1.35; box-shadow: 0 4px 12px var(--bg-main); pointer-events: none; white-space: normal}
    .job-filter-grid {display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin: 12px 0 18px}
    .job-filter-btn {width: 54px; height: 54px; border: 2px solid var(--border); border-radius: 10px; background: var(--bg-dark); cursor: pointer; padding: 4px; opacity: 1}
    .job-filter-btn:hover {filter: brightness(0.95)}
    .job-filter-btn.inactive {opacity: 0.35; filter: grayscale(100%)}
    .job-filter-btn img {width: 100%; height: 100%; object-fit: contain}
    .section-image-wrap {display: inline-block; position: relative; max-width: 800px; width: 100%; margin: 0 auto}
    .section-image-wrap::after {content: ""; position: absolute; inset: 0; box-shadow: 0 0 12px 12px var(--bg-main) inset; pointer-events: none}
    .section-image {display: block; width: 100%; height: auto}
    .aptitude-table th, .aptitude-table td {text-align: center; vertical-align: middle}
    .aptitude-table th:first-child, .aptitude-table td:first-child {text-align: left}
    .aptitude-icon {width: 34px; height: 34px; object-fit: contain; display: block; margin: 0 auto}
    @media (max-width: 1200px) {.job-card-grid {grid-template-columns: repeat(2, minmax(0, 1fr))}}
    @media (max-width: 760px) {
    .job-card-grid {grid-template-columns: 1fr}
    .job-card {grid-template-columns: 1fr}
    .job-card-left {min-height: auto}
    .job-portrait {width: 140px; height: 170px}}
    </style>
    """

def insert_js():
    return """
    <script>
    function toggleJob(jobName) {
      const btn = document.querySelector(`[data-job-filter="${CSS.escape(jobName)}"]`);
      const cards = document.querySelectorAll(`[data-job-card="${CSS.escape(jobName)}"]`);
    
      btn.classList.toggle("inactive");
    
      const hidden = btn.classList.contains("inactive");
      cards.forEach(card => {
        card.style.display = hidden ? "none" : "";
      });
    }
    
    function showAllJobs() {
      document.querySelectorAll(".job-filter-btn").forEach(btn => btn.classList.remove("inactive"));
      document.querySelectorAll(".job-card").forEach(card => card.style.display = "");
    }
    
    function hideAllJobs() {
      document.querySelectorAll(".job-filter-btn").forEach(btn => btn.classList.add("inactive"));
      document.querySelectorAll(".job-card").forEach(card => card.style.display = "none");
    }

    document.addEventListener("DOMContentLoaded", () => {
      const tooltip = document.getElementById("floating-tooltip");

      document.querySelectorAll("[data-tooltip]").forEach(el => {
        el.addEventListener("mouseenter", () => {
          const text = el.getAttribute("data-tooltip");
          if (!text) return;

          tooltip.textContent = text;
          const offset = 14;
          tooltip.style.left = `${event.clientX + offset}px`;
          tooltip.style.top = `${event.clientY + offset}px`;
          tooltip.style.display = "block";
        });

        el.addEventListener("mouseleave", () => {
          tooltip.style.display = "none";
          tooltip.textContent = "";
        });
      });
    });
    </script>
    """

def render_html(spoiler_data: dict) -> str:
    html_parts = []
    append = html_parts.append
    game = spoiler_data.get('game')
    seed = spoiler_data.get('seed')
    with open(json_path(game), "r", encoding="utf-8") as f: ability_descriptions = json.load(f) 

    append("<!DOCTYPE html>")
    append("<html>")
    append("<head>")
    append("<meta charset='utf-8'>")
    append(f"<title>Bravely Spoiler: Patch {seed}</title>")
    append(insert_styles())
    append(insert_js())
    append("</head>")
    append("<body>")
    
    if game == "BD": append(f"<h1>Patch {seed} Bravely Default Randomizer Spoiler Key</h1>")
    else: append(f"<h1>Patch {seed} Bravely Second Randomizer Spoiler Key</h1>")

    jobs = spoiler_data.get("jobs", {})
    magic = spoiler_data.get("magic", {})
    treasures = spoiler_data.get("treasures", {})

    if jobs:
        #=============
        #JOB ABILITIES
        #=============
        ability_rows = jobs.get("job_abilities", [])
        if ability_rows:
            append("<details>")
            append("<summary><strong>Job Abilities</strong></summary>")

            append("<div style='margin-bottom: 10px'>")
            append("<button onclick='showAllJobs()'>Show All</button> ")
            append("<button onclick='hideAllJobs()'>Hide All</button>")
            append("</div>")

            append("<div class='job-filter-grid'>")
            for row in ability_rows:
                job = row["job"]
                icon = icon_path(game, job)

                append(f"<button class='job-filter-btn' "
                            f"data-job-filter='{esc(job)}' "
                            f"onclick='toggleJob({html.escape(repr(job))})' "
                            f"title='{esc(job)}'>"
                            f"<img src='{esc(icon)}' alt='{esc(job)}'>"
                        f"</button>")
            append("</div>")

            append("<div class='job-card-grid'>")
            for row in ability_rows:
                job = row['job']
                specialty = row['specialty']['name']
                img = portrait_path(game, job)

                append(f"<div class='job-card' data-job-card='{esc(job)}'>")
                append("<div class='job-card-left'>")
                append(f"<img class='job-portrait' src='{esc(img)}'>")
                append(f"<div class='job-name'>{esc(job)}</div>")
                append(f"<div class='job-specialty'>{esc(specialty)}</div>")
                append("</div>")

                append("<div class='job-card-right'>")
                append("<table class='job-abilities-table'>")
                append("<tr><th>Level</th><th>Ability</th><th>SP Cost</th></tr>")

                magic_descriptions = get_mage_spells(magic)
                for abil in row.get("abilities", []):
                    cls = ability_class(abil.get('type', ''))
                    ability = abil.get('name', '')
                    level = abil.get('level', '')
                    cost = abil.get('sp_cost', '')
                    ability = resolve_BS_magic_ability_names(ability, level) if game == "BS" else ability.replace("’", "'")
                    description = ability_description(ability_descriptions, magic_descriptions, ability)

                    append(
                        f"<tr class='{esc(cls)} ability-tooltip' data-tooltip='{esc(description)}'>"
                        f"<td>{esc(level)}</td>"
                        f"<td>{esc(ability)}</td>"
                        f"<td>{esc(cost)}</td>"
                        f"</tr>"
                    )

                append("</table>")
                append("</div>")
                append("</div>")

            append("</div>")
            append("</details>")
        
        #===================
        #JOB STAT AFFINITIES
        #===================
        stat_rows = jobs.get("stat_affinities", [])
        if stat_rows:
            append("<details>")
            append("<summary><strong>Job Stat Affinities</strong></summary>")
            append("<table>")
            stats = list(stat_rows[0]["stats"].keys())
            append("<tr><th>Job</th>" + "".join(f"<th>{esc(s)}</th>" for s in stats) + "</tr>")

            for row in stat_rows: append(f"<tr><td>{esc(row['job'])}</td>" + "".join(f"<td>{esc(row['stats'][s])}%</td>" for s in stats) + "</tr>")

            append("</table>")
            append("</details>")

        #===================
        #JOB EQUIPMENT RANKS
        #===================
        equip_rows = jobs.get("equipment_aptitudes", [])
        if equip_rows:
            append("<details>")
            append("<summary><strong>Job Equipment Aptitudes</strong></summary>")
            append("<table class='aptitude-table'>")
            equips = list(equip_rows[0]["aptitudes"].keys())
            append("<tr><th>Job</th>" + "".join(f"<th>{esc(e)}</th>" for e in equips) + "</tr>")

            for row in equip_rows:
                job = row['job']
                append(f"<tr><td>{esc(job)}</td>")
                for e in equips:
                    grade = row['aptitudes'][e].get('grade', '')
                    img = aptitude_path(grade)
                    append(f"<td><img class='aptitude-icon' src='{esc(img)}' title='{esc(grade)}'></td>")

                append("</tr>")

            append("</table>")
            append("</details>")

    #=============
    #MAGIC LEVELS
    #=============
    if magic:
        append("<details>")
        append("<summary><strong>Magic</strong></summary>")

        for mage in magic.get("mages", []):
            mage_name = mage.get('name', '')
            img = magic_path(game, mage_name)

            append(f"<h2>{esc(mage_name)}</h2>")
            append("<div class='section-image-wrap'>")
            append(f"<img class='section-image' src='{esc(img)}'>")
            append("</div>")
            append("<table>")
            append("<tr><th>Level</th><th>Spells</th></tr>")

            for level_row in mage.get("levels", []):
                spell_names = ", ".join(spell.get("name", "") for spell in level_row.get("spells", []))

                append(
                    f"<tr>"
                    f"<td>{esc(level_row.get('level', ''))}</td>"
                    f"<td>{esc(spell_names)}</td>"
                    f"</tr>"
                )

            append("</table>")
        append("</details>")
    
    #============
    #BD TREASURES
    #============
    if treasures:
        treasure_locations = treasures.get("locations", [])

        if treasure_locations:
            append("<details>")
            append("<summary><strong>Treasure Locations</strong></summary>")

            for loc in treasure_locations:
                loc_name = loc.get('location', '')
                img = location_path(loc_name)

                append(f"<h2>{esc(loc_name)}</h2>")
                append("<div class='section-image-wrap'>")
                append(f"<img class='section-image' src='{esc(img, quote = False)}'>")
                append("</div>")
                append("<table>")
                append("<tr><th>Treasure</th><th>Quantity</th></tr>")

                for t in loc.get("treasures", []):
                    quantity = t.get("quantity", "")
                    append(
                        f"<tr>"
                        f"<td>{esc(t.get('name', ''))}</td>"
                        f"<td>{esc(quantity)}</td>"
                        f"</tr>"
                    )

                append("</table>")
            append("</details>")

    append("<div id='floating-tooltip'></div>")
    append("</body>")
    append("</html>")
    return "\n".join(html_parts)

def writeHTML(spoiler_data: dict, path: str):
    spoilers = render_html(spoiler_data)
    with open(path, "w", encoding="utf-8") as f: f.write(spoilers)

    debug_path = path.rsplit(".", 1)[0] + "_magic_debug.txt"
    write_magic_debug(spoiler_data, debug_path)
