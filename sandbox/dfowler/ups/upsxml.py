from lxml import etree
from StringIO import StringIO

#build the Access Request

#destination url

class ups_access:
    """Temporary holder for the access info, keep it only if you like!"""
    def __init__(self, access_key, user_id, psswrd):
	self.access_key = access_key
	self.user_id = user_id
	self.psswrd = psswrd


def SendRequest(url, request):
    from urllib2 import Request, urlopen, URLError
    req = Request(url, request)
    response = ''
    try:
	response = urlopen(req)
    except URLError, e:
	if hasattr(e, 'reason'):
	    print 'We failed to reach a server.'
	    print 'Reason: ', e.reason
	elif hasattr(e, 'code'):
	    print 'The server couldn\'t fulfill the request.'
	    print 'Error code: ', e.code
    else:
	pass #Everything went through

    return response
	


def GetAccessRequest( license_number, user_id, psswrd):
    """Generates and returns the etree version of the access request"""
    accessrequest = etree.Element("AccessRequest")
    accessrequest.set("xml:lang", 'en-US')
    etree.SubElement(accessrequest, "AccessLicenseNumber").text = license_number
    etree.SubElement(accessrequest, "UserId").text = user_id
    etree.SubElement(accessrequest, "Password").text = psswrd
    
    #print etree.tostring(accessrequest, pretty_print=True)
    return accessrequest


def GetServiceRequest(request_option, shipper, shipto, pickup_type_code='01', description = "Rate Shopping"):
    """Generates and returns the etree version of the service request"""

    servicerequest = etree.Element("RatingServiceSelectionRequest")
    request = etree.SubElement(servicerequest, "Request")

    #transaction reference
    trans_reference = etree.SubElement(request, "TransactionReference")
    customercontext = etree.SubElement(trans_reference, "CustomerContext").text = 'Rating and Service'
    xpciversion = etree.SubElement(trans_reference, "XpciVersion").text = "1.0"
    
    etree.SubElement(request, "RequestAction").text = "Rate"
    etree.SubElement(request, "RequestOption").text = request_option #Rate or Shop
    
    #pickup type
    pickup_types = { '01': 'daily pickup', '03': 'customer counter', '06': 'one time pickup', '07': 'on call air', '11':'suggested retail rates', '19':'letter center', '20':'air service center' }

    pickuptype = etree.SubElement(servicerequest, "PickupType")
    etree.SubElement(pickuptype, "Code").text = pickup_type_code
    etree.SubElement(pickuptype, "Description").text = pickup_types[pickup_type_code]
    
    #Shipment
    shipment = etree.SubElement(servicerequest, "Shipment")
    
    etree.SubElement(shipment, "Description").text = description

    #shipment - shipper
    shipment_shipper = etree.SubElement(shipment, "Shipper")

    etree.SubElement(shipment_shipper, "Name").text = shipper.name
    etree.SubElement(shipment_shipper, "AttentionName")
    etree.SubElement(shipment_shipper, "TaxIdentificationNumber")
    etree.SubElement(shipment_shipper, "PhoneNumber")
    etree.SubElement(shipment_shipper, "FaxNumber")
    etree.SubElement(shipment_shipper, "ShipperNumber")

    shipper_address = etree.SubElement(shipment_shipper, "Address")
    etree.SubElement(shipper_address, "AddressLine1").text = shipper.AddressLine1
    etree.SubElement(shipper_address, "AddressLine2").text = shipper.AddressLine2
    etree.SubElement(shipper_address, "AddressLine3")
    etree.SubElement(shipper_address, "City").text = shipper.city
    etree.SubElement(shipper_address, "StateProvinceCode").text = shipper.state
    etree.SubElement(shipper_address, "PostalCode").text = shipper.postalcode
    etree.SubElement(shipper_address, "CountryCode").text = shipper.countrycode

    #shipment - shipto    
    shipment_shipto = etree.SubElement(shipment, "ShipTo")
    etree.SubElement(shipment_shipto, "CompanyName")
    etree.SubElement(shipment_shipto, "AttentionName")
    etree.SubElement(shipment_shipto, "PhoneNumber")
    etree.SubElement(shipment_shipto, "Name").text = shipto.name
    shipto_address = etree.SubElement(shipment_shipto, "Address")
    etree.SubElement(shipto_address, "AddressLine1").text = shipto.AddressLine1
    etree.SubElement(shipto_address, "AddressLine2").text = shipto.AddressLine2
    etree.SubElement(shipto_address, "AddressLine3")

    
    etree.SubElement(shipto_address, "City").text = shipto.city
    etree.SubElement(shipto_address, "State").text = shipto.state
    etree.SubElement(shipto_address, "PostalCode").text = shipto.postalcode
    etree.SubElement(shipto_address, "CountryCode").text = shipto.countrycode


    #shipment - shipfrom (same as shipper)
    shipment_shipfrom = etree.SubElement(shipment, "ShipFrom")
    
    etree.SubElement(shipment_shipfrom, "CompanyName")
    etree.SubElement(shipment_shipfrom, "AttentionName").text = shipper.name
    etree.SubElement(shipment_shipfrom, "PhoneNumber")
    etree.SubElement(shipment_shipfrom, "FaxNumber")
    
    shipfrom_address = etree.SubElement(shipment_shipfrom, "Address")
    etree.SubElement(shipfrom_address, "AddressLine1").text = shipper.AddressLine1
    etree.SubElement(shipfrom_address, "AddressLine2").text = shipper.AddressLine2
    etree.SubElement(shipfrom_address, "AddressLine3")
    etree.SubElement(shipfrom_address, "City").text = shipper.city
    etree.SubElement(shipfrom_address, "StateProvinceCode").text = shipper.state
    etree.SubElement(shipfrom_address, "PostalCode").text = shipper.postalcode
    etree.SubElement(shipfrom_address, "CountryCode").text = shipper.countrycode
    
    #Service Code
    shipment_service = etree.SubElement(shipment, "Service")
    etree.SubElement(shipment_service, "Code").text = str(65)
    

    #payment information
    payment = etree.SubElement(shipment, "PaymentInformation")
    prepaid = etree.SubElement(shipment, "Prepaid")

    #Package Information
    package = etree.SubElement(shipment, "Package")
    package_type = etree.SubElement(package, "PackagingType")
    etree.SubElement(package_type, "Code").text = '04'
    etree.SubElement(package_type, "Description").text = "UPS 25KG Box"
    
    etree.SubElement(package, "Description").text = "Rate"
    package_weight = etree.SubElement(package, "PackageWeight")
    package_weight_unit = etree.SubElement(package_weight, "UnitOfMeasurement")
    etree.SubElement(package_weight_unit, "Code").text = "KGS"
    etree.SubElement(package_weight, "Weight").text = str(23)

    etree.SubElement(shipment, "ShipmentServiceOptions")
    
    return servicerequest



def GetRequest(ups_user, rate_or_shop, shipper, shipto, pretty=False):
    """Returns the text version of the xml request"""
    accessreq = GetAccessRequest( ups_user.access_key, ups_user.user_id, ups_user.psswrd)
    servicereq = GetServiceRequest(rate_or_shop, shipper, shipto)
    xml_text = '<?xml version="1.0"?>' + etree.tostring(accessreq, pretty_print=pretty) + '<?xml version="1.0"?>' + etree.tostring(servicereq, pretty_print=pretty)
    
    return xml_text


#start 

if __name__ == '__main__':
    #get your own user info from http://www.ups.com/e_comm_access/gettools_index?loc=en_US
    ups_user = ups_access('AC0D1E830968BAC8', 'godavemon', 'password')

    #Example Data
    class user:
	pass
    
    shipper = user()
    shipper.name = "Dave Fowler"
    shipper.phone = "3057449002"
    shipper.AddressLine1 = "Southam Rd"
    shipper.AddressLine2 = ""
    shipper.city = "Dunchurch"
    shipper.state = "Warwickshire"
    shipper.postalcode = "CV226PD"
    shipper.countrycode = "GB"
    shipper.attentionname = ""
    shipper.faxnumber = ""
    shipper.shippernumber = ""
    
    shipto = user()
    shipto.name = "Belgium"
    shipto.phone = "4568193849"
    shipto.AddressLine1 = "5, rue de la Bataille"
    shipto.AddressLine2 = ""
    shipto.city = "Neufchateau"
    shipto.postalcode = "6840"
    shipto.state = ""
    shipto.countrycode = "BE"
    shipto.attentionname = ""
    shipto.faxnumber = ""
    shipto.shippernumber = ""
    
    request = GetRequest(ups_user, "Rate", shipper, shipto)
    
    #url's for ups.  Use the testing one for testing purposes, then switch to the implementation!
    testing_url = 'https://wwwcie.ups.com/ups.app/xml/Rate'
    implementation_url = 'https://www.ups.com/ups.app/xml/Rate'

    response = SendRequest( testing_url, request).read()
    
    #print response

    resp = etree.parse( StringIO(response))
    
    
    
    
    

