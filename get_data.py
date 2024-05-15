import os
from bs4 import BeautifulSoup
from fpdf import FPDF

def convert_to_pdf(text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    encoded_text = text.encode("latin-1", "replace").decode("latin-1")
    pdf.multi_cell(0, 10, txt=encoded_text)
    pdf.output(f"./output/{filename}.pdf")

def main():
    # Create output folder if it doesn't exist
    os.makedirs("./output", exist_ok=True)

    files = os.listdir("./content/")
    for file in files:
        with open(f"./content/{file}") as f:
            html = f.read()
            soup = BeautifulSoup(html, "lxml")
            content = soup.text
            text = content.split("\n")
            text = list(filter(lambda x: len(x.strip()) > 0, text))
            text = "\n".join(text)
            
            # Extract filename without extension
            filename = os.path.splitext(file)[0]

            # Convert text to PDF
            convert_to_pdf(text, filename)

            print(f"PDF generated for {filename}.")

            # break

if __name__ == "__main__":
    main()
