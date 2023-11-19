# Author: Daiki Nomura
# !/usr/local/bin/python3
# coding: utf-8
import locale
import PyPDF2
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from flask import Flask, request, render_template, make_response
from io import BytesIO
from datetime import datetime

app = Flask(__name__, static_folder='./templates')
app.config['JSON_AS_ASCII'] = False
locale.setlocale(locale.LC_TIME, 'Japanese_Japan.UTF-8')

def prepare_response(data):
    response = make_response(data)
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self' https://cdn.jsdelivr.net https://fonts.googleapis.com https://fonts.gstatic.com; style-src: 'self' https://fonts.googleapis.com https://fonts.gstatic.com; font-src: 'self' https://fonts.gstatic.com; img-src: 'self' data:; frame-src: 'self'; script-src 'self' https://cdn.jsdelivr.net https://fonts.googleapis.com https://fonts.gstatic.com unsafe-inline 'nonce-371c39bd8dc29b14542d774a83cc5781f59fd261b492e4cedf841198696d4d7b'; object-src: 'none'; base-uri: 'none'; form-action: self;"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

def is_checked(value):
    if value is None:
        return 'false'
    else:
        return 'true'


@app.route("/")
def start():
    return prepare_response(render_template('index.html'))


@app.route("/report", methods=['POST'])
def report():
    user_grade = request.form.get('grade')
    user_class = request.form.get('class')
    user_number = request.form.get('number')
    student_name = request.form.get('st-name')
    parents_name = request.form.get('pr-name')
    start_date = datetime.strptime(request.form.get('str-date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.form.get('ed-date'), '%Y-%m-%d')
    reason_sel = request.form.get('sel-reason')

    if reason_sel == "myself":
        hospital_name = request.form.get('hospital-name')
        onset_date = datetime.strptime(request.form.get('os-date'), '%Y-%m-%d')

    # make json
    form_data = {
        'grade': user_grade,
        'class': user_class,
        'number': user_number,
        'st-name': student_name,
        'pr-name': parents_name,
        'str-date': start_date,
        'ed-date': end_date,
        'sel-reason': reason_sel,
        'hospital-name': hospital_name if reason_sel == "myself" else None,
        'os-date': onset_date if reason_sel == "myself" else None
    }
    # for PDF making
    pdf_reader = PyPDF2.PdfReader(open('./resource/covid-report.pdf', 'rb'), strict=False)
    pdf_writer = PyPDF2.PdfWriter()
    out_put = BytesIO()
    canv = canvas.Canvas(out_put, pagesize=A4)
    pdfmetrics.registerFont(TTFont('IPAexGothic', './resource/ipaexg.ttf'))
    canv.setFont('IPAexGothic', 12)

    # function for write circle like check
    def check(x, y):
        canv.setLineWidth(2.0)
        canv.circle(x, y, 2.0 * mm, stroke=1, fill=0)

    def write_required():
        # 曜日入れるのはあとで(ここ重要
        canv.drawRightString(151.8 * mm, 240.5 * mm, form_data['grade'])
        canv.drawRightString(163.3 * mm, 240.5 * mm, form_data['class'])
        canv.drawRightString(174.7 * mm, 240.5 * mm, form_data['number'])
        canv.drawString(134.0 * mm, 228.2 * mm, form_data['st-name'])
        canv.drawString(134.0 * mm, 215.2 * mm, form_data['pr-name'])
        canv.drawRightString(68.5 * mm, 176.5 * mm, form_data['str-date'].strftime('%Y'))
        canv.drawRightString(83.1 * mm, 176.5 * mm, form_data['str-date'].strftime('%m'))
        canv.drawRightString(97.9 * mm, 176.5 * mm, form_data['str-date'].strftime('%d'))

        canv.drawString(108 * mm, 176.5 * mm, form_data['str-date'].strftime('%a'))

        canv.drawRightString(135.5 * mm, 176.5 * mm, form_data['ed-date'].strftime('%Y'))
        canv.drawRightString(150.2 * mm, 176.5 * mm, form_data['ed-date'].strftime('%m'))
        canv.drawRightString(164.9 * mm, 176.5 * mm, form_data['ed-date'].strftime('%d'))

        canv.drawString(174.5 * mm, 176.5 * mm, form_data['ed-date'].strftime('%a'))

        reason = form_data['sel-reason']
        if reason == 'myself':
            check(33.8 * mm, 152.4 * mm)
        elif reason == 'medical-care':
            check(41.4 * mm, 133.7 * mm)
        elif reason == 'primary-illness':
            check(41.4 * mm, 127.3 * mm)
        elif reason == 'family':
            check(41.4 * mm, 120.9 * mm)
        elif reason == 'vaccine':
            check(33.8 * mm, 108.1 * mm)

    def write_if_myself():
        canv.drawString(124.0 * mm, 151.2 * mm, form_data['hospital-name'])
        canv.drawRightString(102.3 * mm, 196.0 * mm, form_data['os-date'].strftime('%Y'))
        canv.drawRightString(117.5 * mm, 196.0 * mm, form_data['os-date'].strftime('%m'))
        canv.drawRightString(132.8 * mm, 196.0 * mm, form_data['os-date'].strftime('%d'))
        canv.drawRightString(149.0 * mm, 196.0 * mm, form_data['os-date'].strftime('%a'))

    write_required()
    if form_data['sel-reason'] == 'myself':
        write_if_myself()

    canv.showPage()
    canv.save()
    pdf_input = PyPDF2.PdfReader(out_put)
    pdf_base = pdf_reader.pages[0]
    pdf_enter = pdf_input.pages[0].rotate(180)
    pdf_base.merge_page(pdf_enter)
    pdf_writer.add_page(pdf_base)
    out_put.close()
    new_pdf = BytesIO()
    pdf_writer.write(new_pdf)
    response = prepare_response(new_pdf.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'filename=covid-report.pdf'
    return response

if __name__ == "__main__":
    app.run(debug=True)