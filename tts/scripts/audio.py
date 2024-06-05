import os
import time

def count_parts(filename: str):
    """
    Counts the number of parts in a text file.

    Args:
    filename: The path to the text file.

    Returns:
    The number of parts in the text file.
    """

    with open(filename, 'r') as f:
        counts = sum([1 for line in f if line.startswith('# Part')])

    return counts


if __name__ == '__main__':
    book = "../atomic_new_2.txt"
    speaker = "en-US-ChristopherNeural"
    lang = "en"

    part_count = count_parts(book)

    counter = 2

    for chpt in range(counter, part_count + 1):
        if chpt < 11:
            audioname = f"atomic_habits_0{chpt-1}_{speaker}"
        else:
            audioname = f"atomic_habits_{chpt-1}_{speaker}"

        command = f"epub2tts {book} " \
        f"--engine edge " \
        f"--speaker {speaker} " \
        f"--start {chpt} " \
        f"--end {chpt} "  \
        f"--language {lang} " \
        f"--cover ../cover-image.jpg " \
        f"--audioformat m4b " \
        f"--audioname {audioname} " \
        f"--skipfootnotes " \
        f"--skiplinks "

        print(command)
        os.system(command)

        counter += 1
        print(f"Finished chapters {counter}{part_count}!")

