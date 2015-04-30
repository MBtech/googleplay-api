#!/usr/bin/python

# Do not remove
GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None

import sys
from pprint import pprint
import getpass
from config import *
from googleplay import GooglePlayAPI
from helpers import sizeof_fmt

if (len(sys.argv) < 2):
    print "Usage: %s packagename [filename, password]"
    print "Download an app."
    print "If filename is not present, will write to packagename.apk."
    print "If password is not present, user will be prompted for one"
    sys.exit(0)

packagename = sys.argv[1]

if ((len(sys.argv) >= 3) and (len(sys.argv)<5)):
    filename = sys.argv[2]
    google_pass = sys.argv[3]
elif (len(sys.argv)<3):
    filename = packagename + ".apk"
    google_pass = getpass.getpass()
else:
    print "Usage: %s packagename filename, password]"
    print "Download an app."
    print "If filename is not present, will write to packagename.apk."
    print "If password is not present, user will be prompted for one"
    sys.exit(0)

# Connect
api = GooglePlayAPI(ANDROID_ID)
api.login(GOOGLE_LOGIN, google_pass, AUTH_TOKEN)

# Get the version code and the offer type from the app details
m = api.details(packagename)
doc = m.docV2
vc = doc.details.appDetails.versionCode
ot = doc.offer[0].offerType

# Download
print "Downloading %s..." % sizeof_fmt(doc.details.appDetails.installationSize),
data = api.download(packagename, vc, ot)
open(filename, "wb").write(data)
print "Done"

