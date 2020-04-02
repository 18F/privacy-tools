import unittest
from unittest.mock import patch

from pia_scraper import Agency, PIA

class PiaTests(unittest.TestCase):
  GSAS_PIA_URL = "https://www.gsa.gov/reference/gsa-privacy-program/privacy-impact-assessments-pia"

  def test_agency(self):
    agency = Agency()

    self.assertEqual(agency.url, self.GSAS_PIA_URL)

  def test_get_urls(self):
    mock_html_response = """
      <h2>PIA Systems</h2><table class="stripedTable stripe" width="100%">
      <tbody>
        <tr>
          <th>System Title</th>
          <th>Acronym/Short Name</th>
          <th style="width: 18%;">Date </th>
        </tr>
        <tr>
          <td>Ancillary Financial Applications (AFA)</td>
          <td><a href="/cdnstatic/Ancillary_Financial_Applications_AFA_PIA.pdf" title="Ancillary Financial Applications (AFA)">AFA</a><span> [PDF - 80 KB]</span></td>
          <td>Aug 2017</td>
        </tr>"""

    agency = Agency()
    with patch('requests.get') as mock_get:
      # return fixture data
      mock_get.return_value.text = mock_html_response
      agency.get_pia_urls()

    self.assertEqual(agency.pias[0].pdf_url, "https://gsa.gov/cdnstatic/Ancillary_Financial_Applications_AFA_PIA.pdf")

  def test_download_pdf(self):
    pia = PIA("https://gsa.gov/cdnstatic/Ancillary_Financial_Applications_AFA_PIA.pdf")
    with patch('requests.get') as mock_get:
      # return fixture data
      with open('tests/fixtures/fixture.pdf', "rb") as f:
        fixture_content = f.read()
      mock_get.return_value.content = fixture_content
      pia.download_pdf()

      self.assertEqual(pia.pdf_path, 'pias/Ancillary_Financial_Applications_AFA_PIA.pdf')

  def get_text_from_pdf(self):
    pia = PIA(pdf_path = "tests/fixtures/fixture.pdf")

    pia.get_text_from_pdf()
    self.assertEqual(pia.txt_path, "tests/fixtures/fixture.txt")
    self.assertTrue("Privacy Impact Assessment (PIA)" in pia.full_text)

  def test_get_system_name(self):
    pia = PIA(txt_path = "tests/fixtures/fixture.txt")
    pia.get_text_from_txt()

    pia.get_system_name()
    self.assertTrue("Ancillary Financial Applications" in pia.system_name)

  def test_get_authority(self):
    pia = PIA(txt_path = "tests/fixtures/fixture.txt")
    pia.get_text_from_txt()

    pia.get_authority()
    self.assertTrue("8 CFR 1232.7002" in pia.authority)

if __name__ == '__main__':
    unittest.main()
