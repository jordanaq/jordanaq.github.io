# jordanaq.github.io

This is the repository for my personal site, hosted at jordan.github.io.

This repo contains the files for the staic webpage and the code used to generate it.



## index.html

This file contains the page displayed whenever someone navigates to the website's address. In this case, it simply redirects the user to **build/resume.html**



## build

This directory contains all the static elements built by *Flask Freezer*. 



## generator

This directory contains the application, page templates, and static files used by both the application and webpage.

The application is based on *Flask* and *SQLAlchemy*. It ties into a PostgreSQL database deployed locally.

The templates use *jinja2* and allow for additional pages being added in the future.
