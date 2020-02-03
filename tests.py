import unittest
from unittest.mock import patch, mock_open
from sorn_scraper import Agency, Sorn

class TestClasses(unittest.TestCase):
  SORN_HTML_URL = "https://www.federalregister.gov/documents/2009/06/03/E9-12951/privacy-act-of-1974-notice-of-updated-systems-of-records"
  MOCK_XML = """
      <PRIACT>
        <HD SOURCE="HD1">GSA/GOVT-4</HD>
        <HD SOURCE="HD2">SYSTEM NAME:</HD>
        <P>Contracted Travel Services Program.</P>
        <HD SOURCE="HD2">SYSTEM LOCATION:</HD>

        <HD SOURCE="HD2">CATEGORIES OF RECORDS IN THE SYSTEM:</HD>
        <P>Social Security Number; employee identification number;</P>
        <HD SOURCE="HD2">AUTHORITIES FOR MAINTENANCE:</HD>

        <HD SOURCE="HD2">PURPOSE:</HD>
        <P>To establish a comprehensive beginning-to-end travel services system containing information ...</P>
        <HD SOURCE="HD2">ROUTINE USES OF THE SYSTEM RECORDS:</HD>

        <HD SOURCE="HD2">RETENTION AND DISPOSAL:</HD>
        <P>Records kept by a Federal agency are maintained ...</P>
        <HD SOURCE="HD2">SYSTEM MANAGER AND ADDRESS:</HD>

        <HD SOURCE="HD1">ROUTINE USES OF RECORDS MAINTAINED IN THE SYSTEM INCLUDING CATEGORIES OF USERS AND THE PURPOSES OF SUCH USES:</HD>
        <P>a. A record of any case in which ...</P>
        <HD SOURCE="HD1">POLICIES AND PRACTICES FOR STORING, RETRIEVING, ACCESSING, RETAINING, AND DISPOSING OF RECORDS IN THE SYSTEM:</HD>
      </PRIACT>
    """

  def test_get_sorn_urls(self):
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
      agency.get_sorn_urls()
      
    self.assertTrue(len(agency.sorns) == 2)
    self.assertEqual(agency.sorns[0].html_url, self.SORN_HTML_URL)
    self.assertEqual(agency.sorns[1].html_url, second_sorn_url)


  def test_build_xml_url(self):
    expected_xml_url = "https://www.federalregister.gov/documents/full_text/xml/2009/06/03/E9-12951.xml"
    sorn = Sorn(self.SORN_HTML_URL)
    self.assertEqual(sorn.xml_url, expected_xml_url)


  def test_get_full_xml(self):
    with patch('requests.get') as mock_get:
      mock_get.return_value.text = self.MOCK_XML
      mock_get.return_value.status_code = 200

      sorn = Sorn(self.SORN_HTML_URL)
      sorn.get_full_xml()
    
    self.assertEqual(sorn.full_xml, self.MOCK_XML)


  def test_get_sorn_text_after_a_given_heading(self):
    sorn = Sorn(self.SORN_HTML_URL)
    sorn.full_xml = self.MOCK_XML

    sorn.get_sorn_text_after_a_given_heading("SYSTEM NAME:", "system_name")

    self.assertEqual(sorn.system_name, "Contracted Travel Services Program.")


  def test_sorn_get_system_name(self):
    sorn = Sorn(self.SORN_HTML_URL)
    sorn.full_xml = self.MOCK_XML

    sorn.get_system_name()

    self.assertEqual(sorn.system_name, "Contracted Travel Services Program.")


  def test_sorn_get_pii(self):
    sorn = Sorn(self.SORN_HTML_URL)
    sorn.full_xml = self.MOCK_XML

    sorn.get_pii()

    self.assertEqual(sorn.pii, "Social Security Number; employee identification number;")


  def test_sorn_get_purpose(self):
    sorn = Sorn(self.SORN_HTML_URL)
    sorn.full_xml = self.MOCK_XML

    sorn.get_purpose()

    self.assertEqual(sorn.purpose, "To establish a comprehensive beginning-to-end travel services system containing information ...")


  def test_sorn_get_retention(self):
    sorn = Sorn(self.SORN_HTML_URL)
    sorn.full_xml = self.MOCK_XML

    sorn.get_retention()

    self.assertEqual(sorn.retention, "Records kept by a Federal agency are maintained ...")


  def test_sorn_get_routine_uses(self):
    sorn = Sorn(self.SORN_HTML_URL)
    sorn.full_xml = self.MOCK_XML

    sorn.get_routine_uses()

    self.assertEqual(sorn.routine_uses, "a. A record of any case in which ...")


  def test_agency_write_all_to_csv(self):
    agency = Agency()

    with patch("builtins.open") as mock_file:
      with patch('csv.writer') as mock_csv:
        agency.write_all_to_csv()

        mock_file.assert_called_with('gsa_sorns.csv', 'w')


  def test_sorn_write_to_csv(self):
    sorn = Sorn(self.SORN_HTML_URL)
    sorn.full_xml = self.MOCK_XML
    sorn.get_system_name()
    sorn.get_pii()
    sorn.get_purpose()
    sorn.get_retention()
    sorn.get_routine_uses()

    with patch("builtins.open") as mock_file:
      with patch('csv.writer') as mock_csv:
        sorn.write_to_csv()

        mock_file.assert_called_with('gsa_sorns.csv', 'a', newline='')
        full_csv_row = [
          'Contracted Travel Services Program.',
          'https://www.federalregister.gov/documents/2009/06/03/E9-12951/privacy-act-of-1974-notice-of-updated-systems-of-records',
          'Social Security Number; employee identification number;',
          'To establish a comprehensive beginning-to-end travel services system containing information ...',
          'Records kept by a Federal agency are maintained ...',
          'a. A record of any case in which ...'
          ]
        mock_csv.return_value.writerow.assert_called_once_with(full_csv_row)


if __name__ == '__main__':
    unittest.main()
