class ups_access:
    """Temporary holder for the access info, keep it only if you like!"""
    def __init__(self, access_key, user_id, psswrd):
	self.access_key = access_key
	self.user_id = user_id
	self.password = psswrd

ups_user = ups_access('AC0D1E830968BAC8', 'godavemon', 'password') #correct/original
ups_user_badpassword = ups_access('AC0D1E830968BAC8', 'godavemon', 'garbage')
ups_user_badkey = ups_access('garbage', 'godavemon', 'password')
ups_user_badname = ups_access('AC0D1E830968BAC8', 'garbage', 'password')

access = ups_access( "FC1B98E48809DF48", "638WE3", "ups4me.")

class ShipmentOption:
    pass
    
class Shipper:
    pass

class ShipTo:
    pass

class ContactInfo:
    pass

shipment = ShipmentOption()
shipment.request_option = "Shop"
shipment.pickup_type = 'Letter Center'
shipment.weight_unit = 'LBS'
shipment.weight = "3"

shipper = Shipper()
shipper.name = "Test Shipper"
shipper.phone = "5102928662"
shipper.AddressLine1 = "120 Pierce St."
shipper.AddressLine2 = ""
shipper.city = "San Francisco"
shipper.state = "CA"
shipper.postalcode = "94117"
shipper.countrycode = "US"
shipper.attentionname = ""
shipper.faxnumber = ""
shipper.shippernumber = ""

shipto_contact = ContactInfo()
shipto_contact.name = "Test ShipTo"
shipto_contact.phone_number = "4152558329"

shipto = ShipTo()
shipto.name = "Test ShipTo"
shipto.phone = "4152558329"
shipto.ship_first_line = "1418 W Street NW"
shipto.ship_second_line = ""
shipto.ship_city = "Washington"
shipto.ship_postal_code = "20007"
shipto.ship_state = "DC"
shipto.ship_country = "US"
