import sys, time
import requests
from bs4 import BeautifulSoup

class AgencySorns:
  def __init__(self, url):
    '''
    Give it a url of a agency's list of SORNs.
    '''
    self.url = url
    self.sorns = []

  def get_sorns(self):
    result = requests.get(self.url)
    soup = BeautifulSoup(result.text, 'html.parser')
    for link in soup.find_all('a'): # It helps to find all anchor tag's
        if "https://www.federalregister.gov" in link.get('href'):
          sorn = Sorn(link.get('href'))
          self.sorns.append(sorn)


class Sorn:
  def __init__(self, html_url):
    self.html_url = html_url
    self.xml_url = self.build_xml_url()
    #self.pii = str

    
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

  def fetch_pii(self):
    '''
    Just testing for now
    ISO-8859-1
    ''' 
    result = requests.get(self.xml_url)
    converted_result = result.text.encode('utf8')
    print(converted_result)
    # soup = BeautifulSoup(converted_result, 'lxml')
    # print(soup)

  # def validate_all_xml_urls(self):
  #   for xml_url in self.sorns_xml_urls:
  #     response = requests.get(xml_url)
  #     time.sleep(0.1)
  #     if response.status_code != 200:
  #       print("Ruh roh: " + xml_url)

if __name__ == '__main__':
  agency_sorns = AgencySorns(sys.argv[1])
  agency_sorns.get_sorns()
  # for sorn in agency_sorns.sorns:
  # print(sorn.xml_url)

  agency_sorns.sorns[0].fetch_pii()
