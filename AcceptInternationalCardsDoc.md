# Introduction #

By default, authorize.net payment gateway does address verification and other checks that may make non-US credit cards or card holders be declined. Read on for more about accepting international cards and the changes you need to make.


# Details #

Does Authorize.Net support international transactions? _From authorize.net FAQ: http://developer.authorize.net/faqs/#7421 for source_

Yes. Merchants can submit transactions to the payment gateway on behalf of non-U.S. customers. To do so, the merchant’s bank account must be with a financial institution located in the United States, and the merchant must be configured to accept the customer’s card type: Visa, MasterCard, American Express, Discover, JCB, Diner’s Club, or EnRoute. The payment gateway will submit the amount of the transaction to the customer’s card issuer, who will then handle all currency conversion to U.S. dollars. Since default Address Verification Service (AVS) settings may cause foreign transactions to be declined, merchants who plan to regularly accept international transactions should make sure that their AVS settings are configured to meet their business needs.

How to set your gateway to accept international cards: _note: you will incur additional risk of fraudulent charges by doing this; you accept this and any other risks that may result by making these changes. we are not advising you to do this, just providing you information on how to_

  * Log in to https://account.authorize.net/
  * Click on "Settings" (under "Account" on the left side)
  * Click on "Address Verification Service" under "Security Settings"
  * Unclick the following three boxes: Non US Card Issuing Bank (G), AVS is not supported by card issuing bank (S), Address information for cardholder is unavailable (U).
