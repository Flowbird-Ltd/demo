# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
from io import BytesIO
from PyPDF2 import PdfFileReader, PdfFileMerger


class PDFMerge(models.Model):
    _name = 'pdf_merge.pdf_merge'

    name = fields.Char("Name")
    document_ids = fields.One2many(comodel_name="pdf_merge.document", inverse_name="merge_id")
    final = fields.Binary(string="Document")

    def process(self):
        # start the merger
        merger = PdfFileMerger()
        for document in self.document_ids:
            # for each document in the one2many append
            merger.append(PdfFileReader(BytesIO(base64.decodebytes(document.document))), import_bookmarks=False)

        # get the output in bytes, encode to 64 bytes and save in file
        output = BytesIO()
        merger.write(output)
        self.final = base64.b64encode(output.getvalue())
        merger.close()


class PDFMergeDocument(models.Model):
    _name = "pdf_merge.document"

    name = fields.Char("Name")
    document = fields.Binary(string="Document")
    merge_id = fields.Many2one(comodel_name="pdf_merge.pdf_merge")
