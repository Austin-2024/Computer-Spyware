
# Post deployment backdoor 

This is a simple python backdoor that opens a Flask webserver and listens for connections on all interfaces.

It allows you to send and run commands on the target machine, and take screenshots of the target machines screen and view them on the webserver.


## Deployment

Steps to deploy the project:

1. Install **all** files
2. Make sure all files are in the same directory/folder
3. Place the ***index.html*** file in a new folder called ***templates***
4. Place the ***styles.css*** file in a new folder called ***static***
5. Run the ***client.py*** file


## Dependencies

Python 3 or higher

`pip install Flask`
`pip install Flask-Cors`


