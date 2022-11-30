from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from io import BytesIO
from zipfile import ZipFile
import base64
import os


def encode_image(file):
    '''' encode image as base64 string to be embedded in pdf export'''
    if file:
        try:
            with open(file.path, "rb") as image_file:
                return {
                    'data': base64.b64encode(image_file.read()).decode(),
                    'url': file.url,
                    'title': os.path.basename(image_file.name)
                }
        except:
            pass
    return {}


def render_to_pdf(container, template, context, request):
    html_content = render_to_string(template, context, request=request)
    HTML(string=html_content,
         base_url=request.build_absolute_uri("/")[-1]).write_pdf(container)
    return container


def render_file_as_pdf(template, context, request):
    container = BytesIO()
    return render_to_pdf(container, template, context, request)


def render_response_as_pdf(template, context, request, filename):
    '''generate pdf content from template and return API response'''
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(
        filename)
    return render_to_pdf(response, template, context, request)


def render_response_as_zip(files, title):
    s = BytesIO()
    zf = ZipFile(s, "w")

    for f in files:
        try:
            if hasattr(f, "path"):
                fdir, fname = os.path.split(f.path)
                zip_path = os.path.join(title, fname)
                zf.write(f.path, zip_path)
            else:
                zf.writestr(os.path.join(title, f.name), f.getvalue())
        except:
            pass
    zf.close()

    response = HttpResponse(s.getvalue(),
                            content_type="application/x-zip-compressed")
    response['Content-Disposition'] = 'attachment; filename="{}.zip"'.format(
        title)
    return response
