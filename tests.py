import unittest
from sorn_scraper import Agency, Sorn
from unittest.mock import patch

class TestClasses(unittest.TestCase):
  SORN_HTML_URL = "https://www.federalregister.gov/documents/2009/06/03/E9-12951/privacy-act-of-1974-notice-of-updated-systems-of-records"

  def test_get_sorns(self):
    # setup fixture data
    second_sorn_url = "https://www.federalregister.gov/documents/2008/04/25/E8-8883/privacy-act-of-1974-notice-of-updated-systems-of-records"
    # add these test urls into the mock_response
    mock_html_response = """
        <tr>
          <td><strong><a href=%s id="externalLink" title="">GSA/GOVT-4</a></strong></td>
          <td><strong>Contracted Travel Services Program (E-TRAVEL)</strong></td>
          <td><strong>June 3, 2009</strong></td>
        </tr>
        <tr>
          <td><strong><a href=%s id="externalLink" title="">GSA/GOVT-6</a></strong></td>
          <td><strong>GSA SmartPay Purchase Charge Card Program</strong></td>
          <td><strong>April 25, 2008</strong></td>
        </tr>""" % (self.SORN_HTML_URL, second_sorn_url)

    with patch('requests.get') as mock_get:
      # return fixture data
      mock_get.return_value.text = mock_html_response
      agency = Agency()
      agency.get_sorns()
      
    self.assertTrue(len(agency.sorns) == 2)
    self.assertEqual(agency.sorns[0].html_url, self.SORN_HTML_URL)
    self.assertEqual(agency.sorns[1].html_url, second_sorn_url)


  def test_build_xml_url(self):
    expected_xml_url = "https://www.federalregister.gov/documents/full_text/xml/2009/06/03/E9-12951.xml"
    sorn = Sorn(self.SORN_HTML_URL)
    self.assertEqual(sorn.xml_url, expected_xml_url)


  def test_sorn_get_title(self):
    mock_xml = """
      <PRIACT>
        <HD SOURCE="HD1">GSA/GOVT-4</HD>
        <HD SOURCE="HD2">SYSTEM NAME:</HD>
        <P>Contracted Travel Services Program.</P>
        <HD SOURCE="HD2">SYSTEM LOCATION:</HD>
      </PRIACT>
    """
    with patch('requests.get') as mock_get:
      mock_get.return_value.text = mock_xml

      sorn = Sorn(self.SORN_HTML_URL)
      sorn.get_title()

    self.assertEqual(sorn.title, "Contracted Travel Services Program.")


  def test_sorn_get_pii(self):
    mock_xml = """
      <PRIACT>
        <HD SOURCE="HD2">CATEGORIES OF RECORDS IN THE SYSTEM:</HD>
        <P>Social Security Number; employee identification number;</P>
        <HD SOURCE="HD2">AUTHORITIES FOR MAINTENANCE:</HD>
      </PRIACT>
    """
    with patch('requests.get') as mock_get:
      mock_get.return_value.text = mock_xml

      sorn = Sorn(self.SORN_HTML_URL)
      sorn.get_pii()
      

    self.assertEqual(sorn.pii, "Social Security Number; employee identification number;")


  def test_sorn_get_purpose(self):
    mock_xml = """
      <PRIACT>
        <HD SOURCE="HD2">PURPOSE:</HD>
        <P>To establish a comprehensive beginning-to-end travel services system containing information ...</P>
        <HD SOURCE="HD2">ROUTINE USES OF THE SYSTEM RECORDS:</HD>
      </PRIACT>
    """
    with patch('requests.get') as mock_get:
      mock_get.return_value.text = mock_xml

      sorn = Sorn(self.SORN_HTML_URL)
      sorn.get_purpose()

    self.assertEqual(sorn.purpose, "To establish a comprehensive beginning-to-end travel services system containing information ...")

if __name__ == '__main__':
    unittest.main()