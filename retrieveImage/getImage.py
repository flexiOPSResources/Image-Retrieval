import logging
import requests
import json
import time

#FCO endpoint
ENDPOINT="https://cp.sd1.flexiant.net:4442/"

MAX_NO_ATTEMPTS = 5
WAIT_TIME = 30

#Global variable which will be programatically set to contain the generated image UUID
image_uuid = ""

#Method used to generate an authentication token for a user
def getToken(endpoint, username, cust_uuid, password):
    tokenURL = "%srest/user/current/authentication" % endpoint
    apiUserName = username + "/" + cust_uuid
    tokenPayload = {'automaticallyRenew': 'True'}
    tokenRequest = requests.get(tokenURL, params=tokenPayload,
                                auth=(apiUserName, password))

    retry = True
    count = 1

    #Attempt the authentication request a specified number of times before giving up
    while ((count <= MAX_NO_ATTEMPTS) and (retry == True)):

        tokenRequest = requests.get(tokenURL, params=tokenPayload,
                                    auth=(apiUserName, password))
        #Token returned correctly
        if tokenRequest.ok:
            token = tokenRequest.content
            tokenObj = json.loads(token)
            return tokenObj['publicToken']

        #Server busy - retry
        if (tokenRequest.status_code == 429):
            print "Server busy - received 429 response, wait and retry. Attempt number: ", count
            time.sleep(WAIT_TIME)
            count = count + 1
        else:
            #Server connection error
            raise Exception("Failed contacting %s with %s (%s)" % (
                tokenURL, tokenRequest.reason, tokenRequest.status_code))

    #Max number of attempts to contact server reached, failure
    if ((retry == True) and (count == MAX_NO_ATTEMPTS)):
        raise Exception("HTTP 429 ERROR, Maximum unsuccessful attempts made to send request to the server")

def rest_post_image(auth_parms):

    #Parameters needed to fetch/create image on platform
    resourceURL = ""
    createURL = ENDPOINT + "rest/user/current/resources/image"

    vdcUUID = "b7e36320-c08a-377d-8f7a-b9df06bca358"
    productoUUID = "3660d322-9d4e-3ff7-a3bd-7b6dc635b3da"
    imageName = "pythontestimage"
    clusterUUID = "e92bb306-72cd-33a2-a952-908db2f47e98"
    default_user = "ubuntu"
    gen_password = True
    make_image = True
    size = 20

    fetchParameters = {
        "url" : resourceURL,
        "makeImage" : make_image,
        "defaultUserName" : default_user,
        "genPassword" : gen_password,
    }

    skeletonImage = {
        "productOfferUUID" : productoUUID,
        "resourceName" : imageName,
        "vdcUUID" : vdcUUID,
        "clusterUUID" : clusterUUID,
        "size" : size,
    }

    resourceData = {
        "fetchParameters" : fetchParameters,
        "skeletonImage" : skeletonImage,
    }

    payload = resourceData

    print(payload)
    payload_as_string = json.JSONEncoder().encode(payload)

    # Need to set the content type, because if we don't the payload is just silently ignored
    headers = {'content-type': 'application/json'}
    result = rest_submit_postrequest(createURL, payload_as_string, headers, auth_parms,False)
    return result

#Method used for handling the post request of the data to the platform API
def rest_submit_postrequest(theURL, payload, headers, auth_parms):
    retry = True
    count = 1

    #Attempt the request a specified number of times
    while ((count <= MAX_NO_ATTEMPTS) and (retry == True)):
        res = requests.post(theURL, payload, auth=(auth_parms['token'], ''), headers=headers)
        print("==============================================================")
        print "Request submitted, response URL and contents:"
        print(res.url)
        print res.content
        print("HTTP response code: ", res.status_code)

        #Collect the newly generated image uuid which can be used in future calls
        jsonContent = json.loads(res.content)
        global image_uuid
        image_uuid = jsonContent["itemUUID"]

        # Status 202 (Accepted) indicates success
        if ((res.status_code == 202) or (res.status_code == 200)):
            response = json.loads(res.content)
            retry = False
            return response

        #Server busy
        if (res.status_code == 429):
            print "Server busy - received 429 response, wait and retry. Attempt number: ", count
            time.sleep(WAIT_TIME)
            count = count + 1
        else:
            # Something else went wrong. Pick out the status code and message
            response = json.loads(res.content)
            retry = False
            return ""
        print("==============================================================")

    if ((retry == True) and (count == MAX_NO_ATTEMPTS)):
        print "HTTP 429 ERROR, Maximum unsuccessful attempts made to send request to the server"
        # print(response['message'] + " (error code: " + response['errorCode'] + ")")

    return ""

#Method used to call the various methods needed to fetch and create the image
def imagePull():

    #Authentication parameters
    username = ""
    customer_uuid = ""
    password = ""

    token = getToken("https://cp.sd1.flexiant.net/", username,
                     customer_uuid, password)

    auth = dict(endpoint="https://cp.sd1.flexiant.net/", token=token)
    auth_parms = auth
    rest_post_image(auth_parms)

imagePull()
