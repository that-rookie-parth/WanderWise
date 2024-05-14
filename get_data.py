import os

from bs4 import BeautifulSoup


def main():
    files = os.listdir("./content/")
    for file in files:
        with open(f"./content/{file}") as f:
            html = f.read()
            soup = BeautifulSoup(html, "lxml")
            content = soup.text
            text = content.split("\n")
            text = list(filter(lambda x: len(x.strip()) > 0, text))
            text = "\n".join(text)
            print(text)

        break


if __name__ == "__main__":
    main()
