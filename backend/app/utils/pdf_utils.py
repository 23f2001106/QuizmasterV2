from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
import io
import os

# Jinja2 setup
template_env = Environment(
    loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '..', 'templates'))
)

def generate_pdf_from_template(template_name, context):
    """
    Renders HTML template and converts it to PDF.
    """
    template = template_env.get_template(template_name)
    html_out = template.render(context)
    result = io.BytesIO()
    pisa_status = pisa.CreatePDF(html_out, dest=result)

    if pisa_status.err:
        raise Exception('Error generating PDF')

    pdf_bytes = result.getvalue()
    result.close()
    return pdf_bytes