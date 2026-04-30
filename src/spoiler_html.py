import html

def esc(x):
    return html.escape(str(x))

def portrait_path(game, job_name):
    return f"imgs/{game}/Portraits/{job_name}.webp"

def icon_path(game, job_name):
    return f"imgs/{game}/Icons/{job_name}.png"

def render_html(spoiler_data: dict) -> str:
    html_parts = []
    append = html_parts.append
    game = spoiler_data.get('game')
    seed = spoiler_data.get('seed')

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
              .job-card {display: grid; grid-template-columns: 190px minmax(0, 1fr); gap: 18px; align-items: start;
                         background: white; border: 1px solid #ddd; border-radius: 12px; padding: 14px;
                         box-shadow: 0 2px 8px rgba(0,0,0,0.06)}
              .job-card-left {text-align: center}
              .job-portrait {width: 170px; max-width: 100%; height: auto; object-fit: contain}
              .job-name {font-weight: bold; font-size: 1.15em; margin-top: 8px}
              .job-specialty {font-size: 0.95em; color: #555; margin-top: 4px}
              .job-abilities-table {width: 100%; margin-bottom: 0}
              .job-abilities-table th:first-child, .job-abilities-table td:first-child {text-align: center; width: 70px}
              .job-abilities-table th:last-child, .job-abilities-table td:last-child {text-align: center; width: 90px}
              @media (max-width: 700px) {
                .job-card {grid-template-columns: 1fr}
                .job-card-left {text-align: left}
                .job-portrait {width: 140px}}""")
    append("</style>")
    append("</head><body>")

    append("<h1>Spoiler Log</h1>")
    append(f"<p><b>Game:</b> {esc(game)}</p>")
    append(f"<p><b>Seed:</b> {esc(seed)}</p>")

    jobs = spoiler_data.get("jobs", {})

    if jobs:
        append("<h2>Jobs</h2>")

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

        equip_rows = jobs.get("equipment_aptitudes", [])
        if equip_rows:
            append("<details>")
            append("<summary><strong>Job Equipment Aptitudes</strong></summary>")
            append("<table>")
            equips = list(equip_rows[0]["aptitudes"].keys())
            append("<tr><th>Job</th>" + "".join(f"<th>{esc(e)}</th>" for e in equips) + "</tr>")

            for row in equip_rows:
                append(
                    f"<tr><td>{esc(row['job'])}</td>"
                    + "".join(
                        f"<td>{esc(row['aptitudes'][e]['grade'])}</td>"
                        for e in equips
                    )
                    + "</tr>"
                )

            append("</table>")
            append("/details>")

        ability_rows = jobs.get("job_abilities", [])
        if ability_rows:
            append("<h3>Job Abilities</h3>")
            append("<div class='job-card-grid'>")

            for row in ability_rows:
                job = row['job']
                specialty = row['specialty']['name']
                img = portrait_path(game, job)

                append("<div class='job-card'>")
                append("<div class='job-card-left'>")
                append(f"<img class='job-portrait' src='{esc(img)}'>")
                append(f"<div class='job-name'>{esc(job)}</div>")
                append(f"<div class='job-specialty'>{esc(specialty)}</div>")
                append("</div>")

                append("<div class='job-card-right'>")
                append("<table class='job-abilities-table'>")
                append("<tr><th>Level</th><th>Ability</th><th>SP Cost</th></tr>")

                for abil in row.get("abilities", []):
                    append(
                        f"<tr>"
                        f"<td>{esc(abil.get('level', ''))}</td>"
                        f"<td>{esc(abil.get('name', ''))}</td>"
                        f"<td>{esc(abil.get('sp_cost', ''))}</td>"
                        f"</tr>"
                    )

                append("</table>")
                append("</div>")
                append("</div>")

            append("</div>")

    magic = spoiler_data.get("magic", {})

    if magic:
        append("<h2>Magic</h2>")

        for mage in magic.get("mages", []):
            append(f"<h3>{esc(mage['name'])}</h3>")
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

    treasures = spoiler_data.get("treasures", {})

    if treasures:
        treasure_locations = treasures.get("locations", [])

        if treasure_locations:
            append("<h2>Treasures</h2>")

            for loc in treasure_locations:
                append(f"<h3>{esc(loc.get('location', ''))}</h3>")
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

    append("</body></html>")
    return "\n".join(html_parts)


def writeHTML(spoiler_data: dict, path: str):
    spoilers = render_html(spoiler_data)
    with open(path, "w", encoding="utf-8") as f: f.write(spoilers)
