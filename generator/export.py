from flask_frozen import Freezer
from app import app


# Set the directory for the static webpage output to the build directory in the project root
app.config['FREEZER_DESTINATION'] = '../build'

# Create a Freezer object for the resume app
freezer = Freezer(app)

if __name__ == '__main__':
    # Freeze the webpage as a static app
    freezer.freeze()
