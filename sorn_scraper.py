# import sys, time
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


class Sorn:
  def __init__(self, html_url):
    self.html_url = html_url
    self.xml_url = self.build_xml_url()
    self.full_xml = str
    self.title = str
    self.pii = str
    self.purpose = str
    
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

  def get_title(self):
    soup = BeautifulSoup(self.full_xml, 'xml')
    html = u""
    for tag in soup.find('HD', text="SYSTEM NAME:").next_siblings:
      if tag.name == "HD":
        break
      else:
        html += str(tag)
    new_soup = BeautifulSoup(html, 'xml')
    self.title = new_soup.get_text()
    
  def get_pii(self):
    soup = BeautifulSoup(self.full_xml, 'xml')
    html = u""
    for tag in soup.find('HD', text="CATEGORIES OF RECORDS IN THE SYSTEM:").next_siblings:
      if tag.name == "HD":
        break
      else:
        html += str(tag)

    new_soup = BeautifulSoup(html, 'html.parser') # html is working when xml was not
    self.pii = new_soup.get_text().strip()

  def get_purpose(self):
    soup = BeautifulSoup(self.full_xml, 'xml')
    html = u""
    try:
      for tag in soup.find('HD', text="PURPOSE:").next_siblings:
        if tag.name == "HD":
          break
        else:
          html += str(tag)

      new_soup = BeautifulSoup(html, 'html.parser') # html is working when xml was not
      self.purpose = new_soup.get_text().strip()
    except:
      print("Purpose not found for %s" % self.xml_url)





  # def validate_all_xml_urls(self):
  #   for xml_url in self.sorns_xml_urls:
  #     response = requests.get(xml_url)
  #     time.sleep(0.1)
  #     if response.status_code != 200:
  #       print("Ruh roh: " + xml_url)

if __name__ == '__main__':
  agency = Agency()
  agency.get_sorn_urls()
  agency.sorns[0].get_full_xml()
  agency.sorns[0].get_title()
  # agency.sorns[0].get_pii()
  # agency.sorns[0].get_purpose()
  print(agency.sorns[0].title)
