import smtplib
import ssl
import tornado
import authenticate
import csv
import base64
import template_converter
import zipfile
import io
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from markdown2 import Markdown

markdowner = Markdown(extras=["break-on-newline"])

class sendEmailsHandler(tornado.web.RequestHandler):
    def post(self):
        config = authenticate.Config.getInstance()
        server = config.Server
        sender_email = config.Email

        if not sender_email:
            self.set_status(400)
            self.write({"status": 400})
            return

        subject = self.get_body_argument('subject_field')
        self.csv_file = self.get_csv_file()
        # get all rows
        rows = self.get_csv_file()
        rows = rows[1:]
        for row in rows:
            row = row.split(',')
            text, html = self.message_generator(row)
            receiver_email = row[int(self.get_csv_column_index('email'))]
            cc_email = row[int(self.get_csv_column_index('cc'))]
            status = self.send_email(server, sender_email,
                                     receiver_email, cc_email, subject, text, html, row=row)
            if not status:
                break
        print("Done")
        self.set_status(200)
        self.write("Done")

    def get_csv_file(self):
        # open the csv file, save in self
        if self.request.files.get('targets_csv', False):
            csv_file = self.request.files['targets_csv'][0]['body'].decode(
                'utf-8').splitlines()

            return csv_file
        self.write('csv file missing')

    def get_csv_column_index(self, column_name):
        # get csv column header
        column_name = column_name.lower()
        if not hasattr(self, 'columns'):
            self.columns = self.csv_file[0].split(',')
            self.columns = {column.lower(): index for index,
                            column in enumerate(self.columns)}
        if type(self.columns.get(column_name, False)) == int:
            return self.columns[column_name]
        else:
            self.write(f'{column_name} does not exists')

    def get_csv_column(self):
        return self.csv_file[0].split(',')

    def message_generator(self, row):
        # yield message and receiver email (convert from template, return the output message)
        template = self.get_body_argument('content_field')
        
        # text = template_converter.convert_into_text
        text = ""
        html_content = markdowner.convert(template)
        html = template_converter.convert_into_html(
            template=html_content, data=row, columns=self.get_csv_column(), media_files=self.request.files)
        return (text, html)

    def attach_media(self, message, **kwargs):
        if kwargs['media_files'].get('media', False):
            for i in range(len(kwargs['media_files']['media'])):
                # set attachment mime and file name, the image type is png
                contenttype = kwargs["media_files"]["media"][i]["content_type"]
                contenttype = contenttype.split("/")
                mime = MIMEBase(
                    contenttype[0], contenttype[1], filename=kwargs['media_files']['media'][i]['filename'])
                # add required header data:
                mime.add_header('Content-Disposition',
                                'attachment', filename=kwargs['media_files']['media'][i]['filename'])
                mime.add_header('X-Attachment-Id', str(i))
                cid = kwargs['media_files']['media'][i]['filename'].replace(
                    " ", "")
                mime.add_header(
                    'Content-ID',  f"<{cid}>")
                # read attachment file content into the MIMEBase object
                mime.set_payload(kwargs['media_files']['media'][i]['body'])
                # encode with base64
                encode_base64(mime)
                # add MIMEBase object to MIMEMultipart object
                message.attach(mime)

    def attach_custom_attachments(self, message, row, **kwargs):
        # 1. Get matching parameter
        # 2. Extract zip
        # 3. See which file match
        # 4. Attach

        if kwargs['zip_file'].get('custom-attachment', False):
            for i in range(len(kwargs['zip_file']['custom-attachment'])):
                # convert into file-like object
                bytefile = io.BytesIO(
                    kwargs['zip_file']['custom-attachment'][i]['body'])

                matching_parameter = self.get_body_argument('selected_header')
                csv_file = self.get_csv_file()
                index = self.get_csv_column_index(matching_parameter)

                # replace all '/' character
                matching = row[index].replace("/", "")
                with zipfile.ZipFile(bytefile, 'r') as zip_ref:

                    # get all file names in the zip
                    zip_namelist = zip_ref.namelist()
                    # remove the extension and '/' character
                    namelist = [name.split(".")[0].replace("/", "")
                                for name in zip_namelist]

                    for j in range(len(namelist)):
                        if matching == namelist[j]:  # attach custom attachments

                            contenttype = kwargs['zip_file']['custom-attachment'][i]["content_type"]
                            contenttype = contenttype.split("/")

                            cid = zip_namelist[j].replace(" ", "")
                            mime = MIMEBase(
                                contenttype[0], contenttype[1], filename=zip_namelist[j])
                            # add required header data:
                            mime.add_header('Content-Disposition',
                                            'attachment', filename=cid)
                            mime.add_header('X-Attachment-Id', str(j))
                            mime.add_header(
                                'Content-ID',  f"<{cid}>")

                            # read attachment file content into the MIMEBase object
                            # only extract the matching file into payload
                            mime.set_payload(zip_ref.read(zip_namelist[j]))

                            # encode with base64
                            encode_base64(mime)

                            # add MIMEBase object to MIMEMultipart object
                            message.attach(mime)
                            print("Added attachment:", zip_namelist[j])
                            return

    def send_email(self, server, sender_email, receiver_email, cc_email, subject, text, html, **kwargs):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Cc"] = cc_email

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)
        self.attach_media(message, media_files=self.request.files)
        self.attach_custom_attachments(
            message, kwargs['row'], zip_file=self.request.files)

        print(f"Sending to: {receiver_email}")
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
        return True
