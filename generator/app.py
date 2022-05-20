from flask import Flask, render_template
from models import School, CertCategory, SkillCategory, Society, db
from populate import populate_tables


# Create the Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = f'{input("Secret Key: ")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure the database URI with input username and password
app.config['SQLALCHEMY_DATABASE_URI'] =\
    f'postgresql://{input("DB User: ")}:{input("DB Password: ")}@localhost:5432/my_info'

# Initialize the database with the Flask app
db.app = app
db.init_app(app)

# Create all the models as tables in the database
# db.create_all()


# Create the template to be rendered at /resume
@app.route('/resume.html')
def home():
    # Populate the tables with data hard coded or in tsv files if in debug
    if app.debug:
        populate_tables()

    # Render and return the html for index
    return render_template('resume.html',
                           # Describe the webpage
                           description='Jordan Quinn\'s Resume. Contains information on '
                                       'schooling, certification, skills, and societies.',

                           # Retrieve Schools
                           schools=School.get_all(),

                           # Retrieve the categories of certifications in creation order
                           certificates=CertCategory.get_all(),

                           # Pass a all categories of skills
                           expertise=SkillCategory.get_all(),

                           # Pass all societies
                           societies=Society.get_all())


# Run the server in debug mode
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=3000)
