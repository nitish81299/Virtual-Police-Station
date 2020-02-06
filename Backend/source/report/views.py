from django.shortcuts import render
from django.http import HttpResponse, FileResponse
import io
from .models import Report
from .forms import ReportForm
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from easy_pdf.views import PDFTemplateView
import os


def report_create_view(request):
    form = ReportForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        victim = form.cleaned_data['victim']
        fathers_name = form.cleaned_data['fathers_name']
        address = form.cleaned_data['address']
        email = form.cleaned_data['email']
        aadhaar_number = form.cleaned_data['aadhaar_number']
        contact = form.cleaned_data['contact']
        category_of_crime = form.cleaned_data['category_of_crime']
        place_of_crime = form.cleaned_data['place_of_crime']
        data_time_of_crime = form.cleaned_data['date_time_of_crime']
        description = form.cleaned_data['description']
        other_details = form.cleaned_data['other_details']
        r = Report(victim=victim, fathers_name=fathers_name, address=address, email=email, aadhaar_number=aadhaar_number, contact=contact, category_of_crime=category_of_crime, place_of_crime=place_of_crime, description=description, other_details=other_details)
        r.save()
        return render(request, "report/done.html", context)
    return render(request, "report/create.html", context)


def pdf_view(request):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    # get objects from db
    can.drawString(171, 652, "Delhi")   #location
    can.drawString(500, 652, "Date here") #date
    can.drawString(90,600,"This section will have all the complaints details.")    #complaint details
    can.drawString(90,470,"This is for the description")    #description
    can.drawString(90,370,"Other neccessary details here")  #other details
    can.save()


    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    path = os.getcwd()

    output_file_path = path + "/content/media/"
    existing_pdf = PdfFileReader(open(output_file_path+'report_structure.pdf', "rb"))
    output = PdfFileWriter()


    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)


    outputStream = open(output_file_path+"destination.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
    return FileResponse(open(output_file_path+"destination.pdf", "rb"), as_attachment=True, filename='hello.pdf')


class PDFView(PDFTemplateView):
    template_name = 'report/done.html'
    base_url =  '../content/media'
    download_filename = 'report_structure.pdf'

    def get_context_data(self, **kwargs):
        return super(PDFView, self).get_context_data(
            pagesize='A4',
            title='Hi there!',
            **kwargs
        )