from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import pdfquery
from pdfminer.high_level import extract_text



GSAS_PIA_URL = "https://www.gsa.gov/reference/gsa-privacy-program/privacy-impact-assessments-pia"

class Agency:
  def __init__(self):
    '''
    Agency holds the url to the list of PIAs and the scraped PIAs.
    '''
    self.url = GSAS_PIA_URL
    self.pias = []

  def get_pia_urls(self):
    result = requests.get(self.url)
    soup = BeautifulSoup(result.text, 'html.parser')
    for link in soup.find_all('a'): # Find all anchor tags
        href = link.get('href')
        if "/cdnstatic/" in href: # All the PDFs are stored on GSA's cdn.
          full_url = "https://gsa.gov" + href
          pia = PIA(full_url)
          self.pias.append(pia)


class PIA:
  def __init__(self, pdf_url):
    self.pdf_url = pdf_url
    self.pdf_path = None
    self.full_text = None

  def download_pdf(self):
    filename = urlparse(self.pdf_url).path
    filename = filename.split("/")[2] # drop the cdnstatic
    result = requests.get(self.pdf_url)
    self.pdf_path = 'pias/' + filename
    open(self.pdf_path, 'wb').write(result.content)

  def get_full_text(self):
    text = extract_text(self.pdf_path)
    output_file = self.pdf_path.split(".")[0] + ".txt" # replace the .pdf
    with open(output_file, 'w') as text_file:
      text_file.write(text)
    
    self.full_text = text


if __name__ == '__main__':
  agency = Agency()
  agency.get_pia_urls()
  for pia in agency.pias:
    pia.download_pdf()
    pia.get_full_text()
  # agency.pias[0].download_pdf()
  # agency.pias[0].get_full_text()
