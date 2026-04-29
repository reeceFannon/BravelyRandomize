from html import escape

def render_table(headers, rows):
  html = ["<table>"]
  html.append("<tr>" + "".join(f"<th>{escape(str(h))}</th>" for h in headers) + "</tr>")
  for row in rows: html.append("<tr>" + "".join(f"<td>{escape(str(cell))}</td>" for cell in row) + "</tr>")
  html.append("</table>")
  return "\n".join(html)


def render_html(spoiler_data: dict) -> str:
  html = []
  append = html.append

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
  append(f"<p><b>Game:</b> {escape(str(spoiler_data.get('game', '')))}</p>")
  append(f"<p><b>Seed:</b> {escape(str(spoiler_data.get('seed', '')))}</p>")

  jobs = spoiler_data.get("jobs", {})
  if jobs: append("<h2>Jobs</h2>")

  # Job stat affinities
  stat_affinities = jobs.get("stat_affinities", [])
  if stat_affinities:
    append("<h3>Job Affinities</h3>")
    stat_names = list(stat_affinities[0]["stats"].keys())
    rows = []
    for entry in stat_affinities: rows.append([entry["job"]] + [entry["stats"].get(stat, "") for stat in stat_names])
    append(render_table(["Job"] + stat_names, rows))

  # BS equipment aptitudes
  equipment_aptitudes = jobs.get("equipment_aptitudes", [])
  if equipment_aptitudes:
    append("<h3>Job Equipment Aptitudes</h3>")
    equipment_names = list(equipment_aptitudes[0]["equipment"].keys())
    rows = []
    for entry in equipment_aptitudes: rows.append([entry["job"]] + [entry["equipment"].get(eq, "") for eq in equipment_names])
    append(render_table(["Job"] + equipment_names, rows))

  # Job abilities
  abilities = jobs.get("job_abilities", [])
  if abilities:
    append("<h3>Job Abilities</h3>")

    for entry in abilities:
      append(f"<h4>{escape(str(entry['job']))}</h4>")
      specialty = entry.get("specialty", {})
      append(f"<p><b>Specialty:</b> {escape(str(specialty.get('name', '')))}</p>")

      rows = []
      for ability in entry.get("abilities", []):
        cost = ability.get("sp_cost", "")
        rows.append([ability.get("level", ""), ability.get("name", ""), ability.get("type", ""), cost])

      append(render_table(["Level", "Ability", "Type", "SP Cost"], rows))

  # Magic
  magic = spoiler_data.get("magic", {})
  mages = magic.get("mages", [])

  if mages:
    append("<h2>Magic</h2>")

    for mage in mages:
      append(f"<h3>{escape(str(mage.get('name', '')))}</h3>")

      rows = []
      for level_group in mage.get("levels", []):
        level = level_group.get("level", "")
        spell_names = [spell.get("name", "") for spell in level_group.get("spells", [])]
        rows.append([level, ", ".join(spell_names)])

      append(render_table(["Level", "Spells"], rows))

  append("</body></html>")
  return "\n".join(html)


def writeHTML(spoiler_data: dict, path: str):
  with open(path, "w", encoding="utf-8") as f: f.write(render_html(spoiler_data))
