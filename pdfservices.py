import io
import os
import PyPDF2

class PdfHandeler:
    def __init__(self) -> None:
        pass


def merge_pdfs(api_pdf_data, local_pdf_path, output_pdf_path):
    merger = PyPDF2.PdfMerger()

    # Create a file-like object from the API PDF data
    pdf_like_file = io.BytesIO(api_pdf_data)

    merger.append(pdf_like_file)
    with open(local_pdf_path, 'rb') as local_pdf_file:
        merger.append(local_pdf_file)

    # Write the merged PDF to a new file
    with open(output_pdf_path, 'wb') as output_pdf:
        merger.write(output_pdf)

    merger.close()

    #Delete the original local file PDF
    if os.path.exists(local_pdf_path):
        os.remove(local_pdf_path)

    else:
        print("The cant be deleted beacuse file does not exist.")

