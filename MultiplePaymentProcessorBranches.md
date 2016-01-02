# Brandon's Changes #

Here are the raw commands to see what Brandon changed in each module in the process of creating his branch.

svn diff -r 2895:HEAD https://getpaid.googlecode.com/svn/Products.PloneGetPaid/branches/brandon-no-overrides

svn diff -r 2895:HEAD https://getpaid.googlecode.com/svn/getpaid.core/branches/brandon-no-overrides

svn diff -r 2895:HEAD https://getpaid.googlecode.com/svn/getpaid.googlecheckout/branches/brandon-no-overrides

svn diff -r 2895:HEAD
https://getpaid.googlecode.com/svn/getpaid.nullpayment/branches/brandon-no-overrides

# Kapil's Diffs #

Kapil used bzr to check out the branches from Subversion and generate some diffs to see what each branch had done to Products.PloneGetPaid.

http://kapilt.com/files/brandon-no-overrides.txt

http://kapilt.com/files/multipaymentprocessors.txt

# Comments on the code #

Kapil noted that the multiplepaymentprocessors branch stores some of its settings by using the "self.context.portal\_properties" mechanism from Zope 2. This means that his branch moves GetPaid from using a single, modern, Zope 3 mechanism for saving and retrieving its settings — calling getToolByName() — to using two different mechanisms, which means that some settings for GetPaid will be stored in one place, and all of its other settings in another.