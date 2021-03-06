import json
import os
import requests
import sys

from operator import itemgetter, attrgetter

REST_API="http://node43.princeton.vicci.org:8000/xos/"
USERS_API = REST_API + "users/"

username = sys.argv[1]
password = sys.argv[2]

opencloud_auth=(username, password)

admin_auth=("scott@onlab.us", "letmein")

print "users I can see:"
r = requests.get(USERS_API + "?email=%s" % username, auth=opencloud_auth)
for user in r.json():
    print "  ", user["email"]

myself = r.json()[0]

if myself["phone"] == "123":
    myself["phone"] = "456"
else:
    myself["phone"] = "123"

r = requests.put(USERS_API + str(myself["id"]) +"/", data=myself, auth=opencloud_auth)
if r.status_code == 200:
    print "I updated my phone to", myself["phone"]
else:
    print "I failed to update my phone"

if myself["is_admin"] == True:
    myself["is_admin"] = False
else:
    myself["is_admin"] = True

r = requests.put(USERS_API + str(myself["id"]) +"/", data=myself, auth=opencloud_auth)
if r.status_code == 200:
    print "I updated my is_admin to", myself["is_admin"]
else:
    print "I failed to update my is_admin"

r = requests.get(USERS_API + "?email=jhh@cs.arizona.edu", auth=opencloud_auth)
if len(r.json())>0:
    print "I was able to read jhh@cs.arizona.edu"
else:
    print "I was not able to read jhh@cs.arizona.edu"

# get john's record using admin, so we can try to update it
r = requests.get(USERS_API + "?email=jhh@cs.arizona.edu", auth=admin_auth)
if len(r.json())>0:
    print "Admin was able to read jhh@cs.arizona.edu"
    jhh = r.json()[0]
else:
    print "ADmin was not able to read jhh@cs.arizona.edu"
    jhh = None

if jhh:
    # try to update john's user record
    r = requests.put(USERS_API + str(jhh["id"]) + "/", data=jhh, auth=opencloud_auth)
    if r.status_code == 200:
        print "I was able to update user", str(jhh["id"])
    else:
        print "I was not able to update user", str(jhh["id"])




