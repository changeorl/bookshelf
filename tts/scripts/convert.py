import re
from pathlib import Path


def update_part_numbers(src: Path, dest: Path):

    with open(dest, "w", encoding="utf-8") as f_dest:

        with open(src, "r", encoding="utf-8") as f_src:

            part_pattern = re.compile(r"# Part (\d+)")
            chapter_pattern = re.compile(r"^(\d+)$")

            part_number = 0
            lines = f_src.readlines()

            for i, line in enumerate(lines):

                part_match = part_pattern.match(line)
                if part_match:
                    chapter_number = lines[i + 2].strip()

                    chapter_match = chapter_pattern.match(chapter_number.strip())
                    if chapter_match:
                        lines[i + 2] = f"Chapter {chapter_number}\n"

                    first_line = lines[i + 4]
                    is_blank = first_line[2] == " "
                    if is_blank:
                        lines[i + 4] = first_line[:2] + first_line[3:]

                    part = f"# Part {part_number}\n"
                    part_number += 1

                    f_dest.write(part)

                else:
                    f_dest.write(line)


src, dest = Path("atomic_new.txt"), Path("atomic_new_2.txt")
update_part_numbers(src, dest)
