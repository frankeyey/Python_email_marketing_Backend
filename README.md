# Python Email Marketing

This project is originally from [pupubird](https://github.com/pupubird). I forked it and implemented a rich text editor from [Basecamp](https://github.com/basecamp) to provide some text formatting on the email content for current use.

I use [Trix](https://github.com/basecamp/trix) as the editor because it provide intuitive UI as well as flexible functionality to programmatically access the editor instance.

However, proper tests are not executed, some error handlings are not implemented yet, some bugs might appear while using the tool. I will try to fix that during my free time (if possible 😂).

Below is the original README.

***

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Contributing](../CONTRIBUTING.md)

## About <a name = "about"></a>

The process of sending custom-made email to every single member is a hassle for me if I do not use existing external service such as MailChimp.

Hence, I am developing this program to make it open source and everyone, anyone can use without paying a single cent.

## Getting Started <a name = "getting_started"></a>

Download or directly clone from github using:

```
git clone https://github.com/pupubird/Email_marketing_backend.git
```

### Prerequisites

This program require Python 3, if you have Scoop with you, install using the command

```bash
scoop install python
```

If you are using MacOS

```bash
brew install python
```

### Installing

Use pip to install all required libraries

```bash
pip install -r requirements.txt
```

## Usage <a name = "usage"></a>

Run the command

```python
python app.py
```
