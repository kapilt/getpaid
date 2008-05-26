##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import os
import httplib
import urllib
from xml.dom import minidom
import md5
import zc.creditcard
import zc.ssl

class TransactionResult(object):
    def __init__(self, response):
        doc = minidom.parse(response)

        self.response_code = \
            doc.getElementsByTagName('resultCode')[0].childNodes[0].data
        self.response = {'Ok': 'approved', 'Error': 'error',
                        }[self.response_code]
        self.response_reason_code = \
            doc.getElementsByTagName('code')[0].childNodes[0].data
        self.response_reason = \
            doc.getElementsByTagName('text')[0].childNodes[0].data
        TESTING_PREFIX = '(TESTMODE) '
        if self.response_reason.startswith(TESTING_PREFIX):
            self.test = True
            self.response_reason = self.response_reason[len(TESTING_PREFIX):]
        else:
            self.test = False
        if self.response_code == 'Ok':
            self.trans_id = \
                doc.getElementsByTagName('subscriptionId')[0].childNodes[0].data
        self.card_type = None

class ARBConnection(object):
    header = u'<?xml version="1.0" encoding="utf-8"?>'
    footer = u''
    authentication = """\
<merchantAuthentication>
    <name>%s</name>
    <transactionKey>%s</transactionKey>
</merchantAuthentication>"""
    schedule = """\
<paymentSchedule>
  <interval>
    <length>%s</length>
    <unit>%s</unit>
  </interval>
  <startDate>%s</startDate>
  <totalOccurrences>%s</totalOccurrences>
  <trialOccurrences>%s</trialOccurrences>
</paymentSchedule>"""
    payment = """\
<payment>
  <creditCard>
    <cardNumber>%s</cardNumber>
    <expirationDate>%s</expirationDate>
  </creditCard>
</payment>"""
    billto = """\
<billTo>
  <firstName>%s</firstName>
  <lastName>%s</lastName>
</billTo>"""

    def __init__(self, server, login, key, salt=None, timeout=None):
        self.server = server
        self.login = login
        self.salt = salt
        self.timeout = timeout
        self.key = key
        self.authentication = self.authentication % (self.login, self.key)


    def sendTransaction(self, xml):
        if self.server.startswith('localhost:'):
            server, port = self.server.split(':')
            conn = httplib.HTTPConnection(server, port)
        else:
            conn = zc.ssl.HTTPSConnection(self.server,
                                          timeout=self.timeout,
                                          cert_file=os.path.join(os.path.dirname(__file__),
                                                                 'cert.pem'))
        conn.putrequest('POST', '/xml/v1/request.api')
        conn.putheader('content-type', 'text/xml')
        conn.putheader('content-length', len(xml))
        conn.endheaders()
        conn.send(xml)

        response = conn.getresponse()
        result = TransactionResult(response)

        return result

    def createSubscriptionRequest(self, **kws):
        """
        """

        xml = self.header
        xml += """
<ARBCreateSubscriptionRequest xmlns="AnetApi/xml/v1/schema/AnetApiSchema.xsd">"""
        xml += self.authentication
        xml += """
<refId>%s</refId>
<subscription>"""  % (kws.get('invoice_num', ''))
        if kws.get('invoice_num', ''):
            xml += "<name>%s</name>" % kws.get('invoice_num', '')
        xml += self.schedule % (kws.get('length', 0),
                                kws.get('unit', 'months'),
                                kws.get('start_date', ''),
                                kws.get('total_occurrences', 0),
                                kws.get('trial_occurrences', 0))
        xml += """
<amount>%s</amount>
<trialAmount>%s</trialAmount>""" % (kws.get('amount', 0),
                                    kws.get('trial_amount', 0))

        xml += self.payment % (kws.get('card_num', ''),
                               kws.get('exp_date', ''))
        xml += self.billto % (kws.get('first_name', ''),
                              kws.get('last_name', ''))
        xml += """
</subscription>
</ARBCreateSubscriptionRequest>"""
        xml += self.footer
        return xml

    def updateSubscriptionRequest(self, **kws):
        """
        """
        xml = self.header

        xml += self.footer
        return xml

    def cancelSubscriptionRequest(self, **kws):
        """
        """
        xml = self.header

        xml += self.footer
        return xml

#class ARBPaymentSchedule(object):
#
#   SCHEDULE_DATE_FORMAT = "yyyy-MM-dd"
#
#   interval_length = 0
#   subscription_unit = "days" # days | months
#   start_date = None
#   total_occurrences = 0
#   trial_occurrences = 0
#
#   def getIntervaLength(self):
#      return interval_length
#
#   def setIntervalLength(self, interval_length):
#      self.interval_length = interval_length;
#
#   def getStartDate(self):
#      return start_date
#
#   def setStartDate(self, date):
#      self.start_date = date
#
#   def setStartDate(self,start_date):
#      self.start_date = start_date
#
#   def getSubscriptionUnit(self):
#      return subscription_unit
#
#   def setSubscriptionUnit(self, subscription_unit):
#      self.subscription_unit = subscription_unit
#
#   def getTotalOccurrences(self):
#      return total_occurrences
#
#   def setTotalOccurrences(self, total_occurrences):
#      self.total_occurrences = total_occurrences
#
#   def getTrialOccurrences(self):
#      return trial_occurrences
#
#   def setTrialOccurrences(self, trial_occurrences):
#      self.trial_occurrences = trial_occurrences;

class ARBProcessor(object):
    def __init__(self, server, login, key, salt=None, timeout=None):
        self.connection = ARBConnection(
            server, login, key, salt, timeout)

    def create(self, **kws):
        """
        """
        if not isinstance(kws['amount'], basestring):
            raise ValueError('amount must be a string')

        request = self.connection.createSubscriptionRequest(**kws)
        result = self.connection.sendTransaction(request)
        # get the card_type
        card_num = kws.get('card_num')
        if card_num is not None and len(card_num) >= 4:
            card_type = zc.creditcard.identifyCreditCardType(card_num[:4], len(card_num))
            result.card_type = card_type

        return result

    def update(self, **kws):
        """
        """
        request = self.connection.updateSubscriptionRequest(**kws)
        result = self.connection.sendTransaction(request)

    def cancel(self, **kws):
        """
        """
        request = self.connection.cancelSubscriptionRequest(**kws)
        result = self.connection.sendTransaction(request)
