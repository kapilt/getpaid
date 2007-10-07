from lxml import etree
from StringIO import StringIO
import upsconstants


class ups_access:
    """Temporary holder for the access info, keep it only if you like!"""
    def __init__(self, access_key, user_id, psswrd):
	self.access_key = access_key
	self.user_id = user_id
	self.psswrd = psswrd

class UpsRatingServiceResponse:
    """An object representing a response from UPS...will contain status/error info and possibly a list of shipments"""

class RatedShipment:
    """A response can send back a list of many shipping options...this is one of them"""

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
	


def CreateAccessRequest( license_number, user_id, psswrd):
    """Generates and returns the etree version of the access request"""
    accessrequest = etree.Element("AccessRequest")
    accessrequest.set("xml:lang", 'en-US')
    etree.SubElement(accessrequest, "AccessLicenseNumber").text = license_number
    etree.SubElement(accessrequest, "UserId").text = user_id
    etree.SubElement(accessrequest, "Password").text = psswrd
    
    #print etree.tostring(accessrequest, pretty_print=True)
    return accessrequest


def CreateServiceRequest(request_option, shipper, shipto, pickup_type_code='01', description = "Rate Shopping"):
    """Generates and returns the etree version of the service request"""

    servicerequest = etree.Element("RatingServiceSelectionRequest")
    request = etree.SubElement(servicerequest, "Request")

    #transaction reference
    trans_reference = etree.SubElement(request, "TransactionReference")
    customercontext = etree.SubElement(trans_reference, "CustomerContext").text = 'Rating and Service'
    xpciversion = etree.SubElement(trans_reference, "XpciVersion").text = "1.0"
    
    etree.SubElement(request, "RequestAction").text = "rate"
    etree.SubElement(request, "RequestOption").text = request_option #'Rate' or 'Shop'
    
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
    if request_option == "Rate":
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
    
    etree.SubElement(package, "Description").text = "Shop"
    package_weight = etree.SubElement(package, "PackageWeight")
    package_weight_unit = etree.SubElement(package_weight, "UnitOfMeasurement")
    etree.SubElement(package_weight_unit, "Code").text = "LBS"
    etree.SubElement(package_weight, "Weight").text = str(23)

    etree.SubElement(shipment, "ShipmentServiceOptions")
    
    return servicerequest



def CreateRequest(ups_user, rate_or_shop, shipper, shipto, pretty=False):
    """Returns the text version of the xml request"""
    accessreq = CreateAccessRequest( ups_user.access_key, ups_user.user_id, ups_user.psswrd)
    servicereq = CreateServiceRequest(rate_or_shop, shipper, shipto)
    xml_text = '<?xml version="1.0"?>' + etree.tostring(accessreq, pretty_print=pretty) + '<?xml version="1.0"?>' + etree.tostring(servicereq, pretty_print=pretty)
    return xml_text

def ParseResponse( tree ):
    """check the etree returned for the status of the request."""
    ups_response = UpsRatingServiceResponse()
    root = tree.getroot()
    ups_response.shipments = []
    if root.tag != "RatingServiceSelectionResponse":
        print 'error...RatingServiceSelectionResponse'
        return
    for elem in root:
        if elem.tag == "Response":
            for child in elem:
                if child.tag == "ResponseStatusCode":
                    ups_response.status_code = child.text
                elif child.tag == "ResponseStatusDescription":
                    ups_response.status_desc = child.text
                elif child.tag == "Error":
                    for child2 in child:
                        if child2.tag == "ErrorSeverity":
                            ups_response.error_severity = child2.text
                        elif child2.tag == "ErrorCode":
                            ups_response.error_code = child2.text
                        elif child2.tag == "ErrorDescription":
                            ups_response.error_desc = child2.text
                        elif child2.tag == "MinimumRetrySeconds":
                            ups_response.minimum_retry_seconds = child2.text
                        elif child2.tag == "ErrorLocation":
                            for child3 in child2:
                                if child3.tag == "ErrorLocationElementName":
                                    ups_response.error_locaction_elem_name = child3.text
                                elif child3.tag == "ErrorLocationElementReference":
                                    ups_response.error_location_elem_ref = child3.text
                                elif child3.tag == "ErrorLocationAttributeName":
                                    ups_response.error_location_atrr_name = child3.text
                        elif child2.tag == "ErrorDigest":
                            ups_response.error_digest = child2.text
        elif elem.tag == "RatedShipment":
            ParseShipment( ups_response.shipments, elem )
    
    PrintResponse( ups_response )

def ParseShipment( shipments, elem ):
    """grab the info for a single shipment within a response, and add that shipment to the list of all shipments"""
    current_shipment = RatedShipment()
    for child in elem:
        if child.tag == "Service":
            for child2 in child:
                if child2.tag == "Code":
                    current_shipment.service_code = child2.text
                elif child2.tag == "Description":
                    current_shipment.service_desc = child2.text
        elif child.tag == "BillingWeight":
            for child2 in child:
                if child2.tag == "UnitOfMeasurement":
                    current_shipment.unit = child2[0].text
                elif child2.tag == "Weight":
                    current_shipment.weight = child2.text
        elif child.tag == "TransportationCharges":
            for child2 in child:
                if child2.tag == "CurrencyCode":
                    current_shipment.transport_charge_currency = child2.text
                elif child2.tag == "MonetaryValue":
                    current_shipment.transport_charge_value = child2.text
        elif child.tag == "ServiceOptionsCharges":
            for child2 in child:
                if child2.tag == "CurrencyCode":
                    current_shipment.service_charge_currency = child2.text
                elif child2.tag == "MonetaryValue":
                    current_shipment.service_charge_value = child2.text
        elif child.tag == "HandlingChargeAmount":
            for child2 in child:
                if child2.tag == "CurrencyCode":
                    current_shipment.handling_charge_currency = child2.text
                elif child2.tag == "MonetaryValue":
                    current_shipment.handling_charge_value = child2.text
        elif child.tag == "TotalCharges":
            for child2 in child:
                if child2.tag == "CurrencyCode":
                    current_shipment.total_charge_currency = child2.text
                elif child2.tag == "MonetaryValue":
                    current_shipment.total_charge_value = child2.text
        elif child.tag == "GuaranteedDaysToDelivery":
            current_shipment.days_to_delivery = child.text
        elif child.tag == "ScheduledDeliveryTime":
            current_shipment.delivery_time = child.text
            
    shipments.append(current_shipment)
    
def PrintResponse( response ):
    print 'Response Status Code: %s' % response.status_code
    print 'Response Status Description: %s' % response.status_desc
    if hasattr( response, 'error_code' ):
        print 'Error...severity: %(severity)s, code: %(code)s, description: %(desc)s' % \
        {'severity' : response.error_severity, 'code' : response.error_code, 'desc' : response.error_desc }
    for shipment in response.shipments:
        print 'Service Code: %s' % shipment.service_code
        if hasattr(shipment, 'service_desc'):
            print 'Service Description %s' % shipment.service_desc
        print 'Shipment unit of measurement: %s' % shipment.unit
        print 'Shipment weight: %s' % shipment.weight
        print 'Currency Code: %s' % shipment.total_charge_currency
        print 'Total Charge: %s' % shipment.total_charge_value
        print 'Days to Delivery: %s' % shipment.days_to_delivery
        print 'Delivery Time: %s' % shipment.delivery_time

if __name__ == '__main__':
    #get your own user info from http://www.ups.com/e_comm_access/gettools_index?loc=en_US
    ups_user = ups_access('AC0D1E830968BAC8', 'godavemon', 'password') #correct/original
    #ups_user = ups_access('AC0D1E830248BAC8', 'godavemon', 'password') #incorrect for testing

    #Example Data
    class user:
	pass
    
    shipper = user()
    shipper.name = "Dave Fowler"
    shipper.phone = "5102928662"
    shipper.AddressLine1 = "120 Pierce St. #6"
    shipper.AddressLine2 = ""
    shipper.city = "San Francisco"
    shipper.state = "CA"
    shipper.postalcode = "94117"
    shipper.countrycode = "US"
    shipper.attentionname = ""
    shipper.faxnumber = ""
    shipper.shippernumber = ""
    
    shipto = user()
    shipto.name = "MakingThings"
    shipto.phone = "4152558329"
    shipto.AddressLine1 = "1020 Mariposa St. #2"
    shipto.AddressLine2 = ""
    shipto.city = "San Francisco"
    shipto.postalcode = "94107"
    shipto.state = "CA"
    shipto.countrycode = "US"
    shipto.attentionname = ""
    shipto.faxnumber = ""
    shipto.shippernumber = ""
    
    request = CreateRequest(ups_user, "Shop", shipper, shipto)

    response = SendRequest( upsconstants.SANDBOX_URL, request ).read()
    
    #print response

    resp = etree.parse( StringIO(response))
    ParseResponse(resp)

    
    
    
    
    

