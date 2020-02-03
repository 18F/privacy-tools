import time, csv
import requests
from bs4 import BeautifulSoup

GSA_SORNS_URL = "https://www.gsa.gov/reference/gsa-privacy-program/systems-of-records-privacy-act/system-of-records-notices-sorns-privacy-act"

class Agency:
  def __init__(self):
    '''
    Agency holds the url to the list of SORNs and the gathered SORNs.
    '''
    self.url = GSA_SORNS_URL
    self.sorns = []

  def get_sorn_urls(self):
    result = requests.get(self.url)
    soup = BeautifulSoup(result.text, 'html.parser')
    for link in soup.find_all('a'): # Find all anchor tag's
        if "https://www.federalregister.gov" in link.get('href'):
          sorn = Sorn(link.get('href'))
          self.sorns.append(sorn)

  def get_all_data(self):
    self.get_sorn_urls()
    for sorn in self.sorns:
      time.sleep(0.1)
      sorn.get_all_data()

  def write_all_to_csv(self):
    with open("gsa_sorns.csv", "w") as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow(['System Name', 'URL', 'PII', 'Purpose', 'Retention Policy', 'Routine Uses'])
      for sorn in self.sorns:
        writer.writerow([sorn.system_name, sorn.html_url, sorn.pii, sorn.purpose, sorn.retention, sorn.routine_uses])

class Sorn:
  def __init__(self, html_url):
    self.html_url = html_url
    self.xml_url = self.build_xml_url()
    self.full_xml = None
    self.system_name = None
    self.pii = None
    self.purpose = None
    self.retention = None
    self.routine_uses = None
    
  def build_xml_url(self):
    '''
    transform the html url to the xml url

    Example html and xml urls
    https://www.federalregister.gov/documents/2015/06/04/2015-13701/privacy-act-of-1974-notice-of-an-updated-system-of-records
    https://www.federalregister.gov/documents/full_text/xml/2015/06/04/2015-13701.xml
    '''
    split_url = self.html_url.split("/")
    first_half = "/".join(split_url[0:4])
    second_half = "/".join(split_url[4:8])
    return first_half + "/full_text/xml/" + second_half + ".xml"

  def get_full_xml(self):
    response = requests.get(self.xml_url)
    self.full_xml = response.text
    if response.status_code != 200:
      print("XML url not working: " + self.xml_url)

  def get_sorn_text_after_a_given_heading(self, heading, sorn_attribute):
    '''
    heading is the text we are searching for in the XML. 
    We grab all the text after that heading until we hit the next heading.
    sorn_attribute is where we want to save the scraped text.
    '''

    soup = BeautifulSoup(self.full_xml, 'xml')
    html = u""

    try:
      # Many SORNs have an added space after their heading.
      # We want to match with space or without, so we pass both.
      # We could also regex here.
      headings = [heading, heading + " "]
      for tag in soup.find('HD', text=headings).next_siblings:
        if tag.name == "HD":
          break
        else:
          html += str(tag)
      # put the text back into BS to strip out the xml tags
      new_soup = BeautifulSoup(html, 'html.parser')
      tagless_content = new_soup.get_text().strip()
      setattr(self, sorn_attribute, tagless_content)
    except:
      print("%s not found for %s" % (sorn_attribute, self.xml_url))

  def get_all_data(self):
    self.get_full_xml()
    self.get_system_name()
    self.get_pii()
    self.get_purpose()
    self.get_retention()
    self.get_routine_uses()
    # self.write_to_csv()

  def get_system_name(self):
    self.get_sorn_text_after_a_given_heading("SYSTEM NAME:", "system_name")

  def get_pii(self):
    self.get_sorn_text_after_a_given_heading("CATEGORIES OF RECORDS IN THE SYSTEM:", "pii")

  def get_purpose(self):
    self.get_sorn_text_after_a_given_heading("PURPOSE:", "purpose")

  def get_retention(self):
    self.get_sorn_text_after_a_given_heading("RETENTION AND DISPOSAL:", "retention")

  def get_routine_uses(self):
    header = "ROUTINE USES OF RECORDS MAINTAINED IN THE SYSTEM INCLUDING CATEGORIES OF USERS AND THE PURPOSES OF SUCH USES:"
    self.get_sorn_text_after_a_given_heading(header, "routine_uses")

  def write_to_csv(self):
    with open("gsa_sorns.csv", 'a', newline="") as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow([self.system_name, self.html_url, self.pii, self.purpose, self.retention, self.routine_uses])


if __name__ == '__main__':
  agency = Agency()
  agency.get_all_data()
  agency.write_all_to_csv()
