from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import pdfquery
from pdfminer.high_level import extract_text
import time, re, pdb, glob, csv



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

  def load_local_pias_from_txt(self):
    txts = glob.glob('pias/*.txt')
    for txt_path in txts:
      pia = PIA(txt_path=txt_path)
      self.pias.append(pia)

  def write_all_to_csv(self):
    with open("gsa_pias.csv", "w") as f:
      writer = csv.writer(f)
      writer.writerow(['System Name', 'Authority'])
      for pia in self.pias:
        writer.writerow([pia.system_name, pia.authority])

class PIA:
  def __init__(self, pdf_url=None, pdf_path=None, txt_path=None):
    self.pdf_url = pdf_url
    self.pdf_path = pdf_path
    self.txt_path = txt_path
    self.full_text = None
    self.system_name = None
    self.authority = None

  def download_pdf(self):
    filename = urlparse(self.pdf_url).path
    filename = filename.split("/")[2] # drop the cdnstatic
    self.pdf_path = 'pias/' + filename
    result = requests.get(self.pdf_url)
    with open(self.pdf_path, 'wb') as f:
      f.write(result.content)

  def get_text_from_pdf(self):
    self.txt_path = self.pdf_path.split(".")[0] + ".txt" # replace the .pdf
    self.full_text = extract_text(self.pdf_path)
    with open(self.txt_path, 'w') as f:
      f.write(self.full_text)

  def get_text_from_txt(self):
    with open(self.txt_path) as f:
      self.full_text = f.read()

  def get_system_name(self):
    # Two different regex patterns run in order to ge the most complete set of system names. 
    words_after_system_names = "January|February|March|April|May|June|July|August|September|October|November|December|Privacy|\d+/"
    pattern_one = "(.*?)(?=%s)" %(words_after_system_names)
    pattern_two = "(?<=Assessment)(.*?)(?=%s)" %(words_after_system_names)
    match = re.search(pattern_one, self.full_text, flags=re.IGNORECASE | re.DOTALL)
    self.system_name = match.group(1).replace('\n','').strip()

    if not self.system_name:
      match = re.search(pattern_two, self.full_text, flags=re.IGNORECASE | re.DOTALL)
    self.system_name = match.group(1).replace('\n','').strip()

  def get_authority(self):
    pattern_just_cfr = "(\d+\s+(CFR|U\.S\.C\.|U\.S\. Code § |USC § )\s*\d+\.*\d+)"
    pattern_full_authority = "1\.2.+?\?+?(.+)?1\.3"
    match = re.search(pattern_just_cfr, self.full_text, flags=re.DOTALL)
    try:
      self.authority = match.group(1).replace("\n","")
    except:
      pass

    # if not self.authority:
    #   match = re.search(pattern_full_authority, self.full_text, flags=re.DOTALL)
    # try:
    #   self.authority = match.group(1).replace("\n","")
    # except:
    #   pass


if __name__ == '__main__':
  agency = Agency()
  agency.load_local_pias_from_txt()
  for pia in agency.pias:
    pia.get_text_from_txt()
    pia.get_system_name()
    pia.get_authority()
  agency.write_all_to_csv()
    