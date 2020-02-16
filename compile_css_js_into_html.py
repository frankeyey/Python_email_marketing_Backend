import os
import re
ROOT = "./public"


def main():
    files = os.listdir(ROOT)

    htmls = []
    for file_name in files:
        if '.html' in file_name:
            htmls.append(file_name)
    for html in htmls:
        for file_name in files:
            insert_into_html(file_name, html)
        print("________________________")


def insert_into_html(file_name, html):
    name1 = file_name.split(".")[0]
    name2 = html.split(".")[0]

    if name1 != name2:  # return if its not the same
        return

    tag, target = "", ""

    if 'css' in file_name:
        tag = "style"
        target = "</head>"
    elif 'js' in file_name:
        tag = "script"
        target = "</body>"
    elif 'html' in file_name:
        return

    with open(ROOT+"/"+file_name, 'r') as f:
        output = ""
        for line in f.readlines():
            output += line
        output_template = f"<{tag}>{output}</{tag}>"

        print(file_name, html)
        with open(ROOT+"/"+html, 'r') as g:
            html_string = ""
            for line in g.readlines():
                html_string += line

            index_head = html_string.index(target)
            html_string = html_string[:index_head] + \
                output_template + html_string[index_head:]

            with open(ROOT+"/"+html, 'w') as h:
                h.writelines(html_string)


if __name__ == "__main__":
    main()