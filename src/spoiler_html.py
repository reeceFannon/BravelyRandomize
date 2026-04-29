import html


def esc(x):
    return html.escape(str(x))


def render_html(spoiler_data: dict) -> str:
    html_parts = []
    append = html_parts.append

    append("<!DOCTYPE html>")
    append("<html><head>")
    append("<meta charset='utf-8'>")
    append("<title>Bravely Spoiler</title>")
    append("<style>")
    append("""body {font-family: Arial, sans-serif; margin: 20px}
              h1, h2, h3, h4 {margin-top: 1.2em}
              table {border-collapse: collapse; margin-bottom: 20px}
              th, td {border: 1px solid #ccc; padding: 6px 10px}
              th {background: #eee}""")
    append("</style>")
    append("</head><body>")

    append("<h1>Spoiler Log</h1>")
    append(f"<p><b>Game:</b> {esc(spoiler_data.get('game'))}</p>")
    append(f"<p><b>Seed:</b> {esc(spoiler_data.get('seed'))}</p>")

    jobs = spoiler_data.get("jobs", {})

    if jobs:
        append("<h2>Jobs</h2>")

        stat_rows = jobs.get("stat_affinities", [])
        if stat_rows:
            append("<h3>Job Stat Affinities</h3>")
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

        equip_rows = jobs.get("equipment_aptitudes", [])
        if equip_rows:
            append("<h3>Job Equipment Aptitudes</h3>")
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

        ability_rows = jobs.get("job_abilities", [])
        if ability_rows:
            append("<h3>Job Abilities</h3>")

            for row in ability_rows:
                append(f"<h4>{esc(row['job'])}</h4>")
                append(
                    f"<p><b>Specialty:</b> "
                    f"{esc(row['specialty']['name'])}</p>"
                )

                append("<table>")
                append("<tr><th>Level</th><th>Name</th><th>Type</th><th>SP Cost</th></tr>")

                for abil in row["abilities"]:
                    append(
                        f"<tr>"
                        f"<td>{esc(abil.get('level', ''))}</td>"
                        f"<td>{esc(abil.get('name', ''))}</td>"
                        f"<td>{esc(abil.get('type', ''))}</td>"
                        f"<td>{esc(abil.get('sp_cost', ''))}</td>"
                        f"</tr>"
                    )

                append("</table>")

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
