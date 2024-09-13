import PyPDF2
import requests

# Download the PDF file
url = "https://www.scss.tcd.ie/~tfernand/FP/OLD/allenFinState.pdf"
response = requests.get(url)

# Save the PDF file
with open('allenFinState.pdf', 'wb') as file:
    file.write(response.content)

# Open the PDF file in binary mode
with open('allenFinState.pdf', 'rb') as file:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfFileReader(file)

    # Get the total number of pages in the PDF
    num_pages = pdf_reader.numPages

    # Iterate through each page and extract the text
    for page in range(num_pages):
        # Get the page object
        pdf_page = pdf_reader.getPage(page)
        
        # Extract the text from the page
        text = pdf_page.extractText()

        # Print the extracted text
        print(f"Page {page+1}:")
        print(text)
        print("\n")
