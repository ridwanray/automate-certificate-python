from io import BytesIO

from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def add_text_to_certificate_template(input_pdf, output_pdf):
    pdf_reader = PdfReader(input_pdf)
    pdf_writer = PdfWriter()

    # Access the first page
    page = pdf_reader.pages[0]

    # Create a BytesIO buffer to store the overlay
    packet = BytesIO()
    canvas_obj = canvas.Canvas(packet)

    custom_font_path = "PinyonScript-Regular.ttf"  
    pdfmetrics.registerFont(TTFont('PinyonScript-Regular', custom_font_path))

    # Set font and size
    font_name = "PinyonScript-Regular"
    font_size = 45
    canvas_obj.setFont(font_name, font_size)
    canvas_obj.setFillColorRGB(1.0, 0.84, 0.0)

    # Draw the name on the template
    canvas_obj.drawString(280, 268, "Anas Ridwan")
    # canvas_obj.drawString(500, 268, "Anas Ridwan")
    canvas_obj.save()
    packet.seek(0)

    # Merge the overlay with the certificate
    overlay_reader = PdfReader(packet)
    overlay_page = overlay_reader.pages[0]
    page.merge_page(overlay_page)
    pdf_writer.add_page(page)

    # Add remaining pages without modification
    for page in pdf_reader.pages[1:]:
        pdf_writer.add_page(page)

    # Write the final output to a new PDF
    with open(output_pdf, 'wb') as output_file:
        pdf_writer.write(output_file)
      
    print("Certificate Completed!")
      

add_text_to_certificate_template("template.pdf", "output.pdf")
