"""
Test data for the unit tests
"""

HOME_PAGE_TEXT = """

<!DOCTYPE html>
<html class="fsvs" lang="en">

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

    <link rel='stylesheet' href='assets/css/fonts.css'>
    <link rel='stylesheet' href='assets/css/sss.css'>
    <script src='assets/js/modernizr-2.6.2-min.js'></script>
    <script src='assets/js/modernizr-2.6.2-min.js/'></script>
  </head>
  <body>

  <ul class="main-menu main-menu-slide">
    <li><a href="books.html">Books</a></li>
    <li><a href="/music.html/">Music</a></li>
    <li><a href="http://test-page.com/contact.html">Contact</a></li>
    <li><a href="shopping">shop</a></li>
    <li><a href="../previous.html">Contact</a></li>
    <li><a href="/buy">Buy a book</a></li>
    <li><a href="/buy/">Buy a book duplicate</a></li>
    <li><a href="/zipped.zip">zip</a></li>
    <li><a href="/image.jpeg">image</a></li>
    <li><a href="http://external-page.com/">external page</a></li>
  </ul>
  </body>
</html>

"""

URLS = {
    'BUY_PAGE_TEXT' : 'http://test-page.com/buy',
    'SHOP_PAGE_TEXT' : 'http://test-page.com/shopping',
    'HOME_PAGE_SIMPLE' : 'http://test-page.com',
    'HOME_PAGE_TEXT' : 'http://test-page.com',
}