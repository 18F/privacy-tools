import unittest
from sorn_scraper import Agency, Sorn
from unittest.mock import patch

class TestClasses(unittest.TestCase):

  def test_get_sorns(self):
    # setup fixture data
    first_sorn_url = "https://www.federalregister.gov/documents/2009/06/03/E9-12951/privacy-act-of-1974-notice-of-updated-systems-of-records"
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
        </tr>""" % (first_sorn_url, second_sorn_url)

    with patch('requests.get') as mock_get:
      # return fixture data
      mock_get.return_value.text = mock_html_response
      agency = Agency()
      agency.get_sorns()
      
    self.assertTrue(len(agency.sorns) == 2)
    self.assertEqual(agency.sorns[0].html_url, first_sorn_url)
    self.assertEqual(agency.sorns[1].html_url, second_sorn_url)


  def test_build_xml_url(self):
    html_url = "https://www.federalregister.gov/documents/2009/06/03/E9-12951/privacy-act-of-1974-notice-of-updated-systems-of-records"
    expected_xml_url = "https://www.federalregister.gov/documents/full_text/xml/2009/06/03/E9-12951.xml"
    sorn = Sorn(html_url)
    self.assertEqual(sorn.xml_url, expected_xml_url)


if __name__ == '__main__':
    unittest.main()