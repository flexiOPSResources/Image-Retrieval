# Image-Retrieval
Python script used to programatically retrieve an image from a URL, and then import it to the Flexiant Cloud Orchestration platform.

Inside the rest_post_image method in the getImage.py file, various parameters will need to be set.  These include:

**resourceURL** (the URL of the image which is to be imported into the system)
**vdcUUID** (the UUID of the VDC which the image will belong to)
**productoUUID** (the product offer UUID of the disk which will house the new image)
**imageName** (the name which will be assigned to the new image)
**clusteruuid** (the UUID of the cluster which the image will belong to)
**default_user** (the default username which will be set on the image (optional))
**gen_password** (boolean value specifying if a password should be generated for the image)
**size** (the size of the disk which will contain the image)

As part of the imagePull() method (also in getImage.py), authentication parameters are required to be set to generate an authentication token for the API request.  These parameters are:

**username** (the username of the customer)
**customer_uuid** (the UUID assigned to the customers account)
**password** (the password used to access the customer account)

Once these parameters have been set correctly, the script can be executed to retrieve and import an image from a URL into the FCO platform.


