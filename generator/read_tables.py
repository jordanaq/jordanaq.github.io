from models import CertCategory
from datetime import datetime as dt
from sqlalchemy import null


# Read certificate categories from the file designated by path 'file'
def read_certcategory(file):
    with open(file, 'r') as categories:
        acc = []

        # Iterate through each row in the file, using a lambda to convert each row into a dictionary and append to acc
        for row in categories:
            (lambda name, path, link, finish: acc.append({
                'name': name,
                'path': bool(int(path)),
                'link': link if link else null(),
                'finish': dt.strptime(finish, '%Y').date(),
            }))(*map(lambda i: i.strip(), row.split('\t')))  # Strip each field before passing to the lambda

        return acc


# Read certificates from the file designated by path 'file'
def read_certificates(file):
    # Open the file for reading
    with open(file, 'r') as certs:
        acc = []

        # Iterate through each row in the file, using a lambda to convert each row into a dictionary and append to acc
        for row in certs:
            # Transform each table row into a dict
            (lambda name, desc, finish, link, cat: acc.append({
                    'name': name,
                    # Determine the appropriate CertCategory.id by querying based off the name in the cat column
                    'category': CertCategory.query.with_entities(CertCategory.id)
                                    .filter_by(name=cat, finish=dt.strptime(finish, '%Y').date()),
                    'finish': dt.strptime(finish, '%Y').date(),
                    'link': link,
                    'description': desc
                }))(*map(lambda i: i.strip(), row.split('\t')))     # Strip each field before passing to the lambda

        return acc


# Read skills from the file designated by path 'file'
def read_skills(file):
    # Open the file for reading
    with open(file, 'r') as skills:
        acc = []

        # Iterate through each row in the file, using a lambda to convert each row into a dictionary and append to acc
        for row in skills:
            (lambda name, category: acc.append({
                'name': name,
                'category': category
            }))(*map(lambda i: i.strip(), row.split('\t')))     # Strip each field before passing to the lambda

        return acc


# Read societies from the file designated by path 'file'
def read_societies(file):
    # Open the file for reading
    with open(file, 'r') as societies:
        acc = []

        # Iterate through each row in the file, using a lambda to convert each row into a dictionary and append to acc
        for row in societies:
            (lambda name, start, finish, chapter: acc.append({
                'name': name,
                'start': dt.strptime(start, '%Y').date(),
                'finish': dt.strptime(finish, '%Y').date() if finish else null(),
                'chapter': chapter
            }))(*map(lambda i: i.strip(), row.split('\t')))     # Strip each field before passing to the lambda

        return acc


# Read schools from the file designated by path 'file'
def read_schools(file):
    with open(file, 'r') as schools:
        acc = []

        # Iterate through each row in the file, using a lambda to convert each row into a dictionary and append to acc
        for row in schools:
            (lambda name, start, finish='', description='': acc.append({
                'name': name,
                'start': dt.strptime(start, '%m/%d/%Y').date(),
                'finish': dt.strptime(finish, '%m/%d/%Y').date() if finish else null(),
                'description': description if description else null()
            }))(*map(lambda i: i.strip(), row.split('\t')))  # Strip each field before passing to the lambda

        return acc


# Read programs from the file designated by path 'file'
def read_programs(file):
    with open(file, 'r') as programs:
        acc = []

        # Iterate through each row in the file, using a lambda to convert each row into a dictionary and append to acc
        for row in programs:
            (lambda name, school: acc.append({
                'name': name,
                'school': school
            }))(*map(lambda i: i.strip(), row.split('\t')))  # Strip each field before passing to the lambda

        return acc


# Read classes from the file designated by path 'file'
def read_classes(file):
    with open(file, 'r') as classes:
        acc = []

        # Iterate through each row in the file, using a lambda to convert each row into a dictionary and append to acc
        for row in classes:
            (lambda name, term, school: acc.append({
                'name': name,
                'term': term,
                'school': school
            }))(*map(lambda i: i.strip(), row.split('\t')))  # Strip each field before passing to the lambda

        return acc
