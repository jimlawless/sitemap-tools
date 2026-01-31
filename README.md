# sitemap-tools

These are just a couple of simple scripts that accept a text file containing a list of URL's that generate either a sitemap_index.xml file or a sitemap.xml file.  You'll have to installs the **requests** library ...

    pip install requests

...in order for these to work.  Each script tests the URL with a HEAD request to attain the appropriate datestamp.  If the file date is not returned in a header, the current date (in GMT) will be substituted.
