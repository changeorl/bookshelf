from pathlib import Path
import re

book = "atomic-habits"
speaker = "en-US-ChristopherNeural"
audioformat = ".m4b"

files = [f for f in Path.cwd().rglob('*.m4b')]
for f in sorted(files):
    part_number = re.findall(r'\d+', f.name)[0]
    match part_number:
        case "0":
            part_number = "00"
            chapter = "Intro"
        case "21":
            chapter = "Conclusion"
        case "22":
            chapter = "Epilogue"
        case "23":
            chapter = "Lessons"
        case _:
            chapter = "chap" + part_number

    new_name = f"{part_number}_{chapter}_{book}_{speaker}{audioformat}"

    f.rename(new_name)


