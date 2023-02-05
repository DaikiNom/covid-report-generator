# Author: @09_Aimer
# !/usr/local/bin/python3
# coding: utf-8
import os
from os.path import dirname, join
import sys
import json
import locale
import PyPDF2
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from flask import Flask, abort, request, render_template, make_response
from io import BytesIO
from datetime import date, datetime

app = Flask(__name__, static_folder='./templates')
app.config['JSON_AS_ASCII'] = False
locale.setlocale(locale.LC_ALL, 'ja_JP.UTF-8')


def is_checked(value):
    if value is None:
        return 'false'
    else:
        return 'true'


@app.route("/")
def start():
    return render_template("index.html", name='name')


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
        onset_date = datetime.strptime(request.form.get('os-date'), '%Y-%m-%d')
        was_fever = is_checked(request.form.get('fever'))
        if was_fever == 'true':
            fever_temp = request.form.get('temperature')
            fever_period = request.form.get('period')
        else:
            fever_temp = ""
            fever_period = ""
        was_boredom = is_checked(request.form.get('boredom'))
        was_dyspnea = is_checked(request.form.get('dyspnea'))
        was_dysgeusia = is_checked(request.form.get('dysgeusia'))
        was_cough = is_checked(request.form.get('cough'))
        was_sore_throat = is_checked(request.form.get('sore-throat'))
        if is_checked(request.form.get('chbox-otsym')) == 'true':
            was_other = request.form.get('other-symptom')
        else:
            was_other = ""
    else:
        onset_date = ""
        was_fever = ""
        fever_temp = ""
        fever_period = ""
        was_boredom = ""
        was_dyspnea = ""
        was_dysgeusia = ""
        was_cough = ""
        was_sore_throat = ""
        was_other = ""

    if reason_sel == "other":
        reason_other = request.form.get('other-reason')
    else:
        reason_other = ""

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
        'onset-date': onset_date,
        'fever': was_fever,
        'temperature': fever_temp,
        'period': fever_period,
        'boredom': was_boredom,
        'dyspnea': was_dyspnea,
        'dysgeusia': was_dysgeusia,
        'cough': was_cough,
        'sore-throat': was_sore_throat,
        'other-symptom': was_other,
        'other-reason': reason_other
    }
    # for PDF making
    pdf_reader = PyPDF2.PdfReader(open('./resource/covid-report.pdf', 'rb'), strict=False)
    pdf_writer = PyPDF2.PdfWriter()
    out_put = BytesIO()
    canv = canvas.Canvas(out_put, pagesize=A4)
    pdfmetrics.registerFont(TTFont('IPAexGothic', './resource/ipaexg.ttf'))
    canv.setFont('IPAexGothic', 12)

    # function for write check
    def check(x, y):
        canv.drawString(x, y, '◯')

    def write_required():
        # 曜日入れるのはあとで(ここ重要
        canv.drawRightString(154.02 * mm, 223.35 * mm, form_data['grade'])
        canv.drawRightString(164.64 * mm, 223.35 * mm, form_data['class'])
        canv.drawRightString(175.35 * mm, 223.35 * mm, form_data['number'])
        canv.drawString(136.70 * mm, 209.3 * mm, form_data['st-name'])
        canv.drawString(136.70 * mm, 195.8 * mm, form_data['pr-name'])
        canv.drawRightString(62 * mm, 146.5 * mm, form_data['str-date'].strftime('%Y'))
        canv.drawRightString(76 * mm, 146.5 * mm, form_data['str-date'].strftime('%m'))
        canv.drawRightString(90.75 * mm, 146.5 * mm, form_data['str-date'].strftime('%d'))

        canv.drawString(99 * mm, 146.5 * mm, form_data['str-date'].strftime('%a'))

        canv.drawRightString(128.34 * mm, 146.5 * mm, form_data['ed-date'].strftime('%Y'))
        canv.drawRightString(142.75 * mm, 146.5 * mm, form_data['ed-date'].strftime('%m'))
        canv.drawRightString(157.25 * mm, 146.5 * mm, form_data['ed-date'].strftime('%d'))

        canv.drawString(165.5 * mm, 146.5 * mm, form_data['ed-date'].strftime('%a'))

        reason = form_data['sel-reason']
        if reason == 'myself':
            check(27.3 * mm, 125.3 * mm)
        elif reason == 'family':
            check(27.3 * mm, 90.5 * mm)
        elif reason == 'prevention':
            check(27.3 * mm, 81.25 * mm)
        elif reason == 'other':
            check(27.3 * mm, 74.25 * mm)

    def write_if_myself():
        canv.drawRightString(85. * mm, 167.5 * mm, form_data['onset-date'].strftime('%Y'))
        canv.drawRightString(106 * mm, 167.5 * mm, form_data['onset-date'].strftime('%m'))
        canv.drawRightString(124 * mm, 167.5 * mm, form_data['onset-date'].strftime('%d'))

        canv.drawString(134 * mm, 167.5 * mm, form_data['onset-date'].strftime('%a'))

        if form_data['fever'] == 'true':
            check(34.3 * mm, 118.4 * mm)
            canv.drawRightString(58.74 * mm, 118.79 * mm, form_data['temperature'])
            canv.drawRightString(77.22 * mm, 118.79 * mm, form_data['period'])
        if form_data['boredom'] == 'true':
            check(111.17 * mm, 118.4 * mm)
        if form_data['dyspnea'] == 'true':
            check(34.3 * mm, 111.5 * mm)
        if form_data['dysgeusia'] == 'true':
            check(111.17 * mm, 111.5 * mm)
        if form_data['cough'] == 'true':
            check(34.3 * mm, 104.5 * mm)
        if form_data['sore-throat'] == 'true':
            check(111.17 * mm, 104.5 * mm)
        if form_data['other-symptom'] != '':
            check(34.3 * mm, 97.5 * mm)
            canv.drawString(52.34 * mm, 97.24 * mm, form_data['other-symptom'])

    def write_if_other():
        canv.drawString(52 * mm, 74.15 * mm, form_data['other-reason'])

    write_required()
    if form_data['sel-reason'] == 'myself':
        write_if_myself()
    elif form_data['sel-reason'] == 'other':
        write_if_other()

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
    response = make_response(new_pdf.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=covid-report.pdf'
    return response


if __name__ == '__main__':
    app.run(debug=True)
