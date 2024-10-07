import json

import sys

import os


EXTENSION = ".ipynb"  # 향후 유연하게 변경 가능



def addseqnum(notestring: str) -> str:

    noteobj = json.loads(notestring)

    cells = noteobj["cells"]  # list


    for seq, cell in enumerate(cells, start=1):

        metadata = cell["metadata"] if "metadata" in cell else dict()

        tags = metadata["tags"] if "tags" in metadata else list()


        tag_count = tags.count(str(seq))

        if tag_count == 0:

            tags.append(str(seq))

        elif tag_count > 1:

            first_index = tags.index(str(seq))

            tags = [

                tag for i, tag in enumerate(tags) if tag != str(seq) or i == first_index

            ]


        metadata["tags"] = tags

        cell["metadata"] = metadata


    return json.dumps(noteobj, indent=2)



def process_file(path: str):

    try:

        with open(path, "r") as f:

            original_content = f.read()

            tagged = addseqnum(original_content)


        if tagged != original_content:

            with open(path, "w") as f:

                f.write(tagged)

            print(f"Processed: {path}")

        else:

            print(f"No changes: {path}")


    except Exception as e:

        print(f"Error processing {path}: {e}")



def main():

    if len(sys.argv) <= 1:

        return


    directory = sys.argv[1]


    if not os.path.isdir(directory):

        print(f"Error: {directory} is not a valid directory.")

        return

    ipynb_files = [

        os.path.join(root, filename)

        for root, _, files in os.walk(directory)

        for filename in files

        if filename.endswith(EXTENSION)

    ]


    for file_path in ipynb_files:

        process_file(file_path)

        print(f"Processed: {file_path}")



if __name__ == "__main__":

    main()


