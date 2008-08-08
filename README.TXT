On August 8th 2009, I [lucielejard] am doing the svn refactor of getpaid.

Everything is going to be moved one level up.
For more information, see http://code.google.com/p/getpaid/wiki/svnrefactor.

If you have the following error when doing svn up in your buildout:

svn: REPORT request failed on '/svn/!svn/vcc/default'
svn: Target path does not exist

Do the following:
 * if you are using the anonymous buildout:
svn switch http://getpaid.googlecode.com/svn/getpaid-anonymous-buildout/trunk/

 * if you are not using the anonymous buildout:
svn switch https://getpaid.googlecode.com/svn/getpaid.buildout/trunk/