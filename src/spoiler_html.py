import html
import json

def esc(x: str):
    return html.escape(str(x))

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

def ability_description(ability_descriptions: dict, job: str, ability: str):
    return ability_descriptions.get(job, {}).get(ability, {}).get("Description", "")

def job_filter_js():
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
    </script>
    """

def render_html(spoiler_data: dict) -> str:
    html_parts = []
    append = html_parts.append
    game = spoiler_data.get('game')
    seed = spoiler_data.get('seed')
    with open(f"assets/{game}/abilities.json", "r", encoding="utf-8") as f: ability_descriptions = json.load(f) 

    append("<!DOCTYPE html>")
    append("<html><head>")
    append("<meta charset='utf-8'>")
    append("<title>Bravely Spoiler</title>")
    append("<style>")
    append("""body {font-family: Arial, sans-serif; margin: 20px}
              h1, h2, h3, h4 {margin-top: 1.2em}
              table {border-collapse: collapse; margin-bottom: 20px}
              th, td {border: 1px solid #ccc; padding: 6px 10px}
              th {background: #eee}
              details {margin: 1em 0 1.5em}
              summary {cursor: pointer; font-size: 1.17em; font-weight: bold; margin: 1em 0}
              summary:hover {text-decoration: underline}
              details > table {margin-top: 0.5em}
              .job-card-grid {display: grid; gap: 18px; max-width: 1100px}
              .job-card {display: grid; grid-template-columns: 190px minmax(0, 1fr); gap: 18px; align-items: start; background: white; border: 1px solid #ddd; border-radius: 12px; padding: 14px; box-shadow: 0 2px 8px rgba(0,0,0,0.06)}
              .job-card-left {text-align: center}
              .job-portrait {width: 170px; max-width: 100%; height: auto; object-fit: contain}
              .job-name {font-weight: bold; font-size: 1.15em; margin-top: 8px}
              .job-specialty {font-size: 0.95em; color: #555; margin-top: 4px}
              .job-abilities-table {width: 100%; margin-bottom: 0}
              .job-abilities-table th:first-child, .job-abilities-table td:first-child {text-align: center; width: 70px}
              .job-abilities-table th:last-child, .job-abilities-table td:last-child {text-align: center; width: 90px}
              .ability-command {background-color: #ffe5cc}
              .ability-support {background-color: #cce5ff}
              .ability-magic {background-color: #f8cccc}
              .ability-tooltip-row {position: relative; cursor: help}
              .ability-tooltip-row:hover {filter: brightness(0.97)}
              .tooltip-container {position: absolute; left: 0; top: 0; width: 0; height: 0; padding: 0; border: none}
              .tooltip-text {visibility: hidden; opacity: 0; position: absolute; left: 0; top: 100%; width: 300px; background: #222; color: white; padding: 10px 12px; border-radius: 8px; font-size: 0.9em; line-height: 1.35; box-shadow: 0 4px 12px rgba(0,0,0,0.25); z-index: 100; transition: opacity 0.15s ease}
              .ability-tooltip-row:hover .tooltip-text {visibility: visible; opacity: 1}
              .job-filter-grid {display: flex; flex-wrap: wrap; gap: 10px; margin: 12px 0 18px}
              .job-filter-btn {width: 54px; height: 54px; border: 2px solid #ccc; border-radius: 10px; background: white; cursor: pointer; padding: 4px; opacity: 1}
              .job-filter-btn.inactive {opacity: 0.35; filter: grayscale(100%)}
              .job-filter-btn img {width: 100%; height: 100%; object-fit: contain}
              .section-image {display: block; max-width: 520px; width: 100%; height: auto; margin: 8px 0 14px; border-radius: 10px}
              .aptitude-table th, .aptitude-table td {text-align: center; vertical-align: middle}
              .aptitude-table th:first-child, .aptitude-table td:first-child {text-align: left}
              .aptitude-icon {width: 34px; height: 34px; object-fit: contain; display: block; margin: 0 auto}
              @media (max-width: 700px) {
                .job-card {grid-template-columns: 1fr}
                .job-card-left {text-align: left}
                .job-portrait {width: 140px}}""")
    append("</style>")
    append(job_filter_js())
    append("</head><body>")

    append("<h1>Spoiler Log</h1>")
    append(f"<p><b>Game:</b> {esc(game)}</p>")
    append(f"<p><b>Seed:</b> {esc(seed)}</p>")

    jobs = spoiler_data.get("jobs", {})
    if jobs:
        append("<h2>Jobs</h2>")

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

                for abil in row.get("abilities", []):
                    cls = ability_class(abil.get('type', ''))
                    ability = abil.get('name', '')
                    level = abil.get('level', '')
                    cost = abil.get('sp_cost', '')
                    description = ability_description(ability_descriptions, job, ability)

                    append(
                        f"<tr class='{esc(cls)} ability-tooltip'>"
                        f"<td>{esc(level)}</td>"
                        f"<td>{esc(ability)}</td>"
                        f"<td>{esc(cost)}</td>"
                        f"<td class='tooltip-container'>"
                        f"<span class='tooltip-text'>{esc(description)}</span>"
                        f"</td>"
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

            for row in stat_rows:
                append(
                    f"<tr><td>{esc(row['job'])}</td>"
                    + "".join(f"<td>{esc(row['stats'][s])}%</td>" for s in stats)
                    + "</tr>"
                )

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
    magic = spoiler_data.get("magic", {})
    if magic:
        append("<details>")
        append("<summary><strong>Magic</strong></summary>")

        for mage in magic.get("mages", []):
            mage_name = mage.get('name', '')
            img = magic_path(game, mage_name)

            append(f"<h3>{esc(mage_name)}</h3>")
            append(f"<img class='section-image' src='{esc(img)}'>")
            append("<table>")
            append("<tr><th>Level</th><th>Spells</th></tr>")

            for level_row in mage.get("levels", []):
                spell_names = ", ".join(
                    spell.get("name", "")
                    for spell in level_row.get("spells", [])
                )

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
    treasures = spoiler_data.get("treasures", {})
    if treasures:
        treasure_locations = treasures.get("locations", [])

        if treasure_locations:
            append("<details>")
            append("<summary><strong>Treasure Locations</strong></summary>")

            for loc in treasure_locations:
                loc_name = loc.get('location', '')
                img = location_path(loc_name)

                append(f"<h3>{esc(loc_name)}</h3>")
                append(f"<img class='section-image' src='{esc(img)}'>")
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

    append("</body></html>")
    return "\n".join(html_parts)


def writeHTML(spoiler_data: dict, path: str):
    spoilers = render_html(spoiler_data)
    with open(path, "w", encoding="utf-8") as f: f.write(spoilers)
