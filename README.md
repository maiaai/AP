# AP

This small API will be performing only GET requests on dpkg packages. Files are either read from local machine (if OS is ubunty/debian) or from specified gist on github.

For use of this API you need to perform next steps:

1. Create virtualenv with Python 3
2. Clone this repo
3. Install requirements: pip install -r requirements.txt
4. The root url is : "http://localhost:{port}/api/packages/"
5. Browsable api is included. To navigate between the packages, type:
  * "http://localhost:{port}/api/packages/" should be used to list all packages.
  * "http://localhost:{port}/api/packages/{package-name}" to get data for the selected package. 

6. Other option is to use Postman or CURL to make requests.
