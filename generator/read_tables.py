from models import CertCategory, Certification, Skill
from datetime import date, datetime as dt
from sqlalchemy import null


def read_certificates(file):
    with open(file, 'r') as certs:
        acc = []

        for row in certs:
            # Transform each table row into a dict
            (lambda name, desc, finish, link, cat: acc.append({
                    'name': name,
                    'category': CertCategory.query.with_entities(CertCategory.id)
                                    .filter_by(name=cat, finish=dt.strptime(finish, '%Y').date()),
                    'finish': dt.strptime(finish, '%Y').date(),
                    'link': link,
                    'description': desc
                }))(*map(lambda i: i.strip(), row.split('\t')))

        return acc


def read_skills(file):
    with open(file, 'r') as skills:
        acc = []

        for row in skills:
            (lambda name, category: acc.append({
                'name': name,
                'category': category
            }))(*map(lambda i: i.strip(), row.split('\t')))

        return acc


def read_societies(file):
    with open(file, 'r') as societies:
        acc = []

        for row in societies:
            (lambda name, start, finish, chapter: acc.append({
                'name': name,
                'start': dt.strptime(start, '%Y').date(),
                'finish': dt.strptime(finish, '%Y').date() if finish else null(),
                'chapter': chapter
            }))(*map(lambda i: i.strip(), row.split('\t')))

        return acc
