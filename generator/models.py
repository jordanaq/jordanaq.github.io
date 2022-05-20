from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null, Integer, String, Date, ForeignKey
from typing import Dict
from functools import reduce


# Create a SQLAlchemy object to hold and derive models
db = SQLAlchemy()


# The semester object is a wrapper for a semester name and an object describing that semester's classes
class Semester:
    def __init__(self, name, classes):
        self.name = name
        self.classes = classes

    def __repr__(self):
        return f'{self.name}' + reduce(lambda x, y: x+y, ('\n\t' + i.__repr__() for i in self.classes))


# Table to hold 'school' objects
class School(db.Model):
    __tablename__ = 'school'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(128), nullable=False, unique=True)
    start = db.Column(Date, nullable=False)
    finish = db.Column(Date, nullable=True)
    description = db.Column(String(1024), nullable=True)

    # semesters returns a list containing semester objects for each semester of classes at School object self
    def semesters(self):
        ret = []

        # Append a Semester object containing the semester's name and the list of all classes that semester
        for i in Classes.query.with_entities(Classes.term).filter_by(school_id=self.id).group_by(Classes.term).all():
            ret.append(Semester(i.term,
                                Classes.query.filter_by(school_id=self.id,
                                                        term=i.term).order_by(Classes.name.asc()).all()))

        return ret

    # Returns all programs associated with School object self
    def programs(self):
        return Program.query.filter_by(school_id=self.id).all()

    def __repr__(self):
        return f'{self.id}:{self.name}:{self.start}:{self.finish}:{self.description}'

    # Takes a Dict as an argument and adds a new School object using data from this dict
    @staticmethod
    def insert_value(value: Dict):
        if School.query.filter_by(name=value.get('name')).first() is None:
            db.session.add(School(name=value.get('name'),
                                  start=value.get('start', null()), finish=value.get('finish', null()),
                                  description=value.get('description', null())))

    # Returns all schools in descending attendance date order
    @staticmethod
    def get_all():
        return School.query.order_by(School.start.desc()).all()


# Table to hold programs taken at a School
class Program(db.Model):
    __tablename__ = 'program'
    school_id = db.Column(Integer, ForeignKey(School.id), primary_key=True)
    name = db.Column(String(512), primary_key=True)

    def __repr__(self):
        return f'{self.school_id}:{self.name}'

    # Takes a Dict as an argument and adds a new Program object using data from this dict
    @staticmethod
    def insert_value(value: Dict):
        if Program.query.filter_by(school_id=value.get('school_id'), name=value.get('name')).first() is None:
            db.session.add(Program(school_id=value.get('school_id'), name=value.get('name')))


# Table to hold 'class' objects
class Classes(db.Model):
    __tablename__ = 'classes'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(128), nullable=False)
    term = db.Column(String(128), nullable=False)
    school_id = db.Column(Integer, ForeignKey(School.id), nullable=False)

    def __repr__(self):
        return f'{self.id}:{self.name}:{self.term}:{self.school_id}'

    # Takes a Dict as an argument and adds a new class object using data from this dict
    @staticmethod
    def insert_value(value: Dict):
        if i := Classes.query.filter_by(name=value.get('name'), term=value.get('term'),
                                        school_id=value.get('school_id')).first() is None:
            db.session.add(Classes(name=value.get('name'), term=value.get('term', null()),
                                   school_id=value.get('school_id', null())))


# Table that holds categories of certifications
class CertCategory(db.Model):
    __tablename__ = 'cert_category'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(128), nullable=False,)
    link = db.Column(String(512), nullable=True)
    finish = db.Column(Date, nullable=False)
    db.UniqueConstraint(name, finish)

    # Returns an object containing certifications corresponding to self.id
    def items(self):
        return Certification.query.filter_by(category=self.id).order_by(Certification.name).all()

    def __repr__(self):
        return f'{self.id}:{self.name}:{self.link}:{self.finish}'

    # Takes a Dict as an argument and adds a new CertCategory object using data from this dict
    @staticmethod
    def insert_value(value: Dict):
        if CertCategory.query.filter_by(name=value.get('name'), finish=value.get('finish')).first() is None:
            db.session.add(CertCategory(name=value.get('name'), link=value.get('link', null()),
                                        finish=value.get('finish', null())))

    # Returns all CertCategory rows in order of ascending id number
    @staticmethod
    def get_all():
        return CertCategory.query.order_by(CertCategory.id.asc()).all()


# Table to hold the different certifications
class Certification(db.Model):
    __tablename__ = 'certification'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(128), nullable=False)
    category = db.Column(Integer, ForeignKey(CertCategory.id), nullable=False)
    finish = db.Column(Date, nullable=False)
    link = db.Column(String(512), nullable=True)
    description = db.Column(String(1024), nullable=True)

    def __repr__(self):
        return f'{self.id}:{self.name}:{self.category}:{self.finish}:{self.link}:{self.description}'

    # Takes a Dict as an argument and adds a new Certification object using data from this dict
    @staticmethod
    def insert_value(value: Dict):
        if Certification.query.filter_by(name=value.get('name'), finish=value.get('finish')).first() is None:
            db.session.add(Certification(name=value.get('name'), category=value.get('category'),
                                         finish=value.get('finish'), link=value.get('link', null()),
                                         description=value.get('description', null())))


class SkillCategory:
    # Constructor using an object with a parameter called category
    def __init__(self, val):
        self.name = val.category

        # Populate the items property with all corresponding rows in the Skill table
        self.items = Skill.query.filter_by(category=val.category).order_by(Skill.name).all()

    @staticmethod
    def get_all():
        return map(SkillCategory, Skill.query.with_entities(Skill.category).group_by(Skill.category).all())

    # Return a string representation for the SkillCategory object
    def __repr__(self):
        ret = self.name + ':'

        for i in self.items:
            ret += f', {i.name}'

        return ret


# Table to hold different skills
class Skill(db.Model):
    name = db.Column(String(256), primary_key=True)
    category = db.Column(String(128), primary_key=True)

    def __repr__(self):
        return f'{self.category}:{self.name}'

    # Takes a Dict as an argument and adds a new Skill object using data from this dict
    @staticmethod
    def insert_value(value: Dict):
        if Skill.query.filter_by(name=value.get('name'), category=value.get('category')).first() is None:
            db.session.add(Skill(name=value.get('name'), category=value.get('category')))


# Table to hold different academic/professional societies
class Society(db.Model):
    __tablename__ = 'society'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(128), nullable=False)
    start = db.Column(Date, nullable=False)
    finish = db.Column(Date, nullable=True)
    chapter = db.Column(String(512), nullable=True)

    def __repr__(self):
        return f'{self.id}:{self.name}:{self.chapter}:{self.start}:{self.finish}'

    # Takes a Dict as an argument and adds a new Society object using data from this dict
    @staticmethod
    def insert_value(value: Dict):
        if Society.query.filter_by(name=value.get('name'), start=value.get('start')).first() is None:
            db.session.add(Society(name=value.get('name'), start=value.get('start', null()),
                                   finish=value.get('finish', null()), chapter=value.get('chapter', null())))

    # Returns an object containing all Society rows in order of ascending name
    @staticmethod
    def get_all():
        return Society.query.order_by(Society.name.asc()).all()
