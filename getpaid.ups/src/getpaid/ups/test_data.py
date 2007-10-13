class ups_access:
    """Temporary holder for the access info, keep it only if you like!"""
    def __init__(self, access_key, user_id, psswrd):
	self.access_key = access_key
	self.user_id = user_id
	self.psswrd = psswrd

ups_user = ups_access('AC0D1E830968BAC8', 'godavemon', 'password') #correct/original
ups_user_badpassword = ups_access('AC0D1E830968BAC8', 'godavemon', 'garbage')
ups_user_badkey = ups_access('garbage', 'godavemon', 'password')
ups_user_badname = ups_access('AC0D1E830968BAC8', 'garbage', 'password')

class Shipper:
    pass

class ShipTo:
    pass

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

shipto = ShipTo()
shipto.name = "Test ShipTo"
shipto.phone = "4152558329"
shipto.AddressLine1 = "1020 Mariposa St."
shipto.AddressLine2 = ""
shipto.city = "San Francisco"
shipto.postalcode = "94107"
shipto.state = "CA"
shipto.countrycode = "US"
shipto.attentionname = ""
shipto.faxnumber = ""
shipto.shippernumber = ""