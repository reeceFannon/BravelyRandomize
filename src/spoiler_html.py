def render_html(spoiler_data: dict) -> str:
  html = []
  append = html.append

  append("<!DOCTYPE html>")
  append("<html><head>")
  append("<meta charset='utf-8'>")
  append("<title>Bravely Spoiler</title>")
  append("<style>")
  append("""body {font-family: Arial, sans-serif; margin: 20px}
            h1, h2, h3 {margin-top: 1.2em}
            table {border-collapse: collapse; margin-bottom: 20px}
            th, td {border: 1px solid #ccc; padding: 6px 10px}
            th {background: #eee}""")
  append("</style>")
  append("</head><body>")

  append(f"<h1>Spoiler Log</h1>")
  append(f"<p><b>Game:</b> {spoiler_data.get('game')}</p>")
  append(f"<p><b>Seed:</b> {spoiler_data.get('seed')}</p>")

  # -------------------
  # JOBS
  # -------------------
  jobs = spoiler_data.get("jobs", {})
  if jobs:
    append("<h2>Jobs</h2>")

    for job_name, job in jobs.items():
      append(f"<h3>{job_name}</h3>")

      # Stats
      if "stats" in job:
        append("<h4>Stats</h4>")
        append("<table>")
        append("<tr><th>Stat</th><th>Rank</th></tr>")
        for stat, val in job["stats"].items():
          append(f"<tr><td>{stat}</td><td>{val}</td></tr>")
        append("</table>")

      # Equipment (BS)
      if "equipment" in job:
        append("<h4>Equipment</h4>")
        append("<table>")
        append("<tr><th>Type</th><th>Rank</th></tr>")
        for eq, val in job["equipment"].items():
          append(f"<tr><td>{eq}</td><td>{val}</td></tr>")
        append("</table>")

      # Abilities
      if "abilities" in job:
        append("<h4>Abilities</h4>")
        append("<table>")
        append("<tr><th>Level</th><th>Name</th><th>Type</th></tr>")
        for abil in job["abilities"]:
          append(f"<tr><td>{abil.get('level')}</td>"
                 f"<td>{abil.get('name')}</td>"
                 f"<td>{abil.get('type')}</td></tr>")
        append("</table>")

  # -------------------
  # MAGIC
  # -------------------
  magic = spoiler_data.get("magic", {})
  if magic:
    append("<h2>Magic</h2>")

    for mage, spells in magic.items():
      append(f"<h3>{mage}</h3>")
      append("<table>")
      append("<tr><th>Level</th><th>Spell</th></tr>")

      for spell in spells:
        append(f"<tr><td>{spell.get('level')}</td>"
               f"<td>{spell.get('name')}</td></tr>")

      append("</table>")

  append("</body></html>")
  return "\n".join(html)


def writeHTML(spoiler_data: dict, path: str):
  spoilers = render_html(spoiler_data)
  with open(path, "w", encoding = "utf-8") as f: f.write(spoilers)
