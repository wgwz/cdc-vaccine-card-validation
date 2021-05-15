# COVID-19 CDC Vaccination Card Validation

This repository contains a script that can be used to validate images
of CDC issued vaccination cards. The script was designed to read in a
list of files in a particular directory, and attempt to validate whether
or not the image contains a valid CDC issued card.

The check only validates if the "COVID-19 Vaccination Record Card" text
at the top of CDC cards is present. It does not validate any other
features of the card such as the persons name or whether or not the
person has received both dosages. It could perhaps be extended to do
that but it will take some work.

This repository is MIT Licensed, and given the importance of this
problem I wanted to share it. That said, there are real data privacy
concerns that come along with using a service like AWS Textract and
those should be taken into consideration.

# Validation? Not really..

The script here does not actually validate the card. It's a bit of a
misnomer for me to name it as such. All that the script concludes is
that it found the "COVID-19 Vaccination Record Card" text somewhere in
the image. Therefore as it stands, the validation provided in this repo
could easily be cheated if someone were to print out a piece of paper
with the same text printed on it. So this repo really provides a
ground-level starting point for the validation of these cards. It is a
crude check, which might be helpful in certain situations.

# How it works?

This is a very simple script, it was a proof-of-concept. It is not
running in production. Given a directory, it will find all the images in
the directory and attempt to submit those images for processing by AWS
Textract. It will print out a list of those that were valid or too large
to be processed by AWS Textract.

```
$ python3 -m venv venv
$ . venv/bin/activate
(venv) $ pip install -r requirements.txt 
(venv) $ python validate.py
Image: X143A2818_1 (1).jpg is too large to process with AWS Textract
Image: X143A2818_1.jpg is too large to process with AWS Textract
Image: image_55415491.JPG is Valid Vaccine Card
Image: image_67155969.JPG is Valid Vaccine Card
```

Here is the specific [API reference][4] that the code uses.

# Prerequisites

* You need to have followed the `boto3` installation guide.
* This means you need valid AWS credentials.
* Those AWS credentials need permissions to AWS Textract.

# AWS Textract

This script relies on the AWS Textract service to do the OCR. At the
time of writing the AWS Textract service offers a cheap, and high
quality service. Currently is $1.50/1000 pages processed.

There are some [limitations to be aware of with AWS Textract][3]. Most
importantly is that at the time of writing the service only accepts
images up to 10MB in size.

The script in this repository takes that into account, but does not do
anything to solve that problem. If the script finds some image that is
too large to process with AWS Textract, it just skips that file.

Another important limitation is that you can only use JPG/PNG files with
AWS Textract. Obviously any production application will need to take
these things into account.

# Data Privacy

Simply put, be aware of how AWS uses the data you process with AWS
Textract. See the "Data Privacy" section of the [FAQs][1]. They will use
the data you upload to make the service better. That may or may not be
acceptable for you and your company.

# Productionizing

You might want to [tune the connection and read timeouts][2] for boto.

[1]: https://aws.amazon.com/textract/faqs/
[2]: https://botocore.amazonaws.com/v1/documentation/api/latest/reference/config.html#botocore-config
[3]: https://docs.aws.amazon.com/textract/latest/dg/limits.html
[4]: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.detect_document_text
