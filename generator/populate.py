from models import School, Program, Classes, CertCategory, Certification, Skill, Society, db
from typing import List
from datetime import date
from read_tables import read_certificates, read_skills, read_societies


# Inserts a list of values into a table
def insert_values(table, values: List):
    # Iterates through each row in the values table
    for row in values:
        # Call the table's static insert_value function on each row
        table.insert_value(row)

    # Try to commit the inserts, otherwise rollback the changes and re-raise the exception
    try:
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        print(ex)
        db.session.close()
        raise ex


# populate_tables populates the database if the values have not already been added
def populate_tables():
    """The rows for School, Program, Classes, and CertCategory have been hard-coded. This will be fixed in the future"""

    # Populate the school table
    insert_values(School, [
            {
                'id': 0, 'name': 'Slippery Rock University',
                'start': date(2018, 7, 1),
                'finish': date(2022, 5, 1),
                'description': 'GPA: 4.0, Attended twice: Fall 2018-Spring 2019, Winter 2021-Spring 2022'
            },
            {
                'name': 'Pitt Community College',
                'start': date(2021, 1, 1),
                'finish': date(2022, 12, 1),
                'description': 'GPA: 4.0, Dean\'s List Spring 2021, Summer 2021, Fall 2021, Spring 2022'
            },
            {
                'name': 'Rochester Institute of Technology',
                'start': date(2022, 7, 1),
            },
    ])

    # Variables to hold strings corresponding to each semester
    fa_18, sp_19, w_21, sp_21, su_21, fa_21, sp_22, fa_22 = 'Fall 2018', 'Spring 2019', 'Winter 2021', \
                                                            'Spring 2021', 'Summer 2021', 'Fall 2021', \
                                                            'Spring 2022', 'Fall 2022'
    # Create variable to hold the relevant school id
    sru_id, pitt_id, rit_id = (School.query.filter_by(name=i).first().id for i in ['Slippery Rock University',
                                                                                   'Pitt Community College',
                                                                                   'Rochester Institute of Technology'])

    # Populate the Program table
    insert_values(Program, [
        {'school_id': rit_id, 'name': 'B.S. Computer Science'},
        {'school_id': pitt_id, 'name': 'A.A.S. Information Technology: Computer Programming and Development'},
        {'school_id': pitt_id, 'name': 'Data Reporting and Analytics Certificate'},
        {'school_id': pitt_id, 'name': 'C# Programming Certificate'},
        {'school_id': pitt_id, 'name': 'JAVA Programming Certificate'}
    ])

    # Populate the Classes table
    insert_values(Classes, [
            # Insert classes for 'PittCC'
            # Insert classes for 'Spring 2021' at 'PittCC'
            {'name': 'C# Programming', 'term': sp_21, 'school_id': pitt_id},
            {'name': 'Network & Security Foundation', 'term': sp_21, 'school_id': pitt_id},
            {'name': 'Simulation and Game Development Programming', 'term': sp_21, 'school_id': pitt_id},
            {'name': 'Web, Programming, and Databases', 'term': sp_21, 'school_id': pitt_id},
            {'name': 'Information Systems Business Concepts', 'term': sp_21, 'school_id': pitt_id},
            {'name': 'Art Appreciation', 'term': sp_21, 'school_id': pitt_id},

            # Insert classes for 'Summer 2021' at 'PittCC'
            {'name': 'College Student Success', 'term': su_21, 'school_id': pitt_id},
            {'name': 'Introduction to Computers', 'term': su_21, 'school_id': pitt_id},
            {'name': 'C++ Programming', 'term': su_21, 'school_id': pitt_id},
            {'name': 'Professional Practices in IT', 'term': su_21, 'school_id': pitt_id},

            # Insert classes for 'Fall 2021' at 'PittCC'
            {'name': 'Computing Fundamentals I', 'term': fa_21, 'school_id': pitt_id},
            {'name': 'JAVA Programming', 'term': fa_21, 'school_id': pitt_id},
            {'name': 'Systems Analysis & Design', 'term': fa_21, 'school_id': pitt_id},
            {'name': 'Advanced C# Programming', 'term': fa_21, 'school_id': pitt_id},
            {'name': 'Project Management', 'term': fa_21, 'school_id': pitt_id},
            {'name': 'Linux/UNIX Single User', 'term': fa_21, 'school_id': pitt_id},

            # Insert classes for 'Spring 2022' at 'PittCC'
            {'name': 'Python Programming', 'term': sp_22, 'school_id': pitt_id},
            {'name': 'Advanced JAVA Programming', 'term': sp_22, 'school_id': pitt_id},
            {'name': 'Database Concepts', 'term': sp_22, 'school_id': pitt_id},
            {'name': 'Programming Capstone Project', 'term': sp_22, 'school_id': pitt_id},
            {'name': 'Spreadsheets', 'term': sp_22, 'school_id': pitt_id},
            {'name': 'Introduction to Ethics', 'term': sp_22, 'school_id': pitt_id},

            # Insert classes for 'Fall 2022' at 'PittCC'
            {'name': 'Database Programming I', 'term': fa_22, 'school_id': pitt_id},


            # Insert classes for 'SRU'
            # Insert classes for 'Fall 2018' at 'SRU'
            {'name': 'Calculus II', 'term': fa_18, 'school_id': sru_id},
            {'name': 'Programming Principles', 'term': fa_18, 'school_id': sru_id},

            # Insert classes for 'Spring 2019 at 'SRU'
            {'name': 'Chinese 101', 'term': sp_19, 'school_id': sru_id},
            {'name': 'Interactive Multimedia 2', 'term': sp_19, 'school_id': sru_id},

            # Insert classes for 'Winter 2021' at 'SRU'
            {'name': 'Introduction Chemistry I', 'term': w_21, 'school_id': sru_id},

            # Insert classes for 'Spring 2021' at 'SRU'
            {'name': 'University Physics 1 with Lab', 'term': sp_22, 'school_id': sru_id}


            # Insert classes for 'RIT'
    ])

    # Populate the cert_category table
    insert_values(CertCategory, [
            {
                'name': 'Educative\'s Python for Programmers', 'finish': date(2021, 1, 1), 'path': True,
                'link': 'https://www.educative.io/verify-certificate/r0w3pLtnXYkROnNJKix5ZOjgZmB5u6'
            },
            {
                'name': 'Educative\'s C++ for Programmers', 'finish': date(2021, 1, 1), 'path': True,
                'link': 'https://www.educative.io/verify-certificate/MjprXLCk4EXXB07yKIR7EoQKEq07IZ'
            },
            {
                'name': 'DartmouthX and IMTx\'s C Programming with Linux', 'finish': date(2021, 1, 1), 'path': True,
                'link': 'https://credentials.edx.org/credentials/c938fe5ee3934afd99900886df70f473/'
            },

            # Create categories for oracle academy courses
            {'name': 'Oracle Academy', 'finish': date(2022, 1, 1)},

            # Create categories for educative courses
            {'name': 'Educative Course Certificates: Programming Strategies', 'finish': date(2022, 1, 1)},
            {'name': 'Educative Course Certificates: Programming Languages', 'finish': date(2021, 1, 1)},
            {'name': 'Educative Course Certificates: Functional Programming', 'finish': date(2021, 1, 1)},
            {'name': 'Educative Course Certificates: Miscellaneous', 'finish': date(2021, 1, 1)},
            {'name': 'Educative Course Certificates: Miscellaneous', 'finish': date(2022, 1, 1)},
    ])

    # Populate the Certification table using the values in the certificates tsv file
    insert_values(Certification, read_certificates('static/certificates.tsv'))

    # Populate the Skill table using the values in the skills tsv file
    insert_values(Skill, read_skills('static/skills.tsv'))

    # Populate the Society table using the values in the societies tsv file
    insert_values(Society, read_societies('static/societies.tsv'))
