from models import School, Program, Classes, CertCategory, Certification, Skill, Society, db
from typing import List
from read_tables import *


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
    """The rows for School, Program, Class, and CertCategory have been hard-coded. This will be fixed in the future"""

    # Populate the school table
    insert_values(School, read_schools('static/schools.tsv'))

    # Populate the Program table
    insert_values(Program, read_programs('static/programs.tsv'))

    # Populate the Classes table
    insert_values(Classes, read_classes('static/classes.tsv'))

    # Populate the cert_category table
    insert_values(CertCategory, read_certcategory('static/certcategory.tsv'))

    # Populate the Certification table using the values in the certificates tsv file
    insert_values(Certification, read_certificates('static/certificates.tsv'))

    # Populate the Skill table using the values in the skills tsv file
    insert_values(Skill, read_skills('static/skills.tsv'))

    # Populate the Society table using the values in the societies tsv file
    insert_values(Society, read_societies('static/societies.tsv'))
