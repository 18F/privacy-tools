# DevOps for Privacy Offices

### We envision a future in which the public can easily understand how and why personally identifiable information gets collected by government agencies. 

To get there, we're working with federal privacy offices and structuring data from PDFed privacy-related compliance documents. By structuring data, we're equipping privacy offices with the ability to more quickly search through these documents, reducing unnecessary manual practices and laying a foundation for them to more easily collaborate with engineering teams.

This project is funded by [10x](https://10x.gsa.gov/).

Our phase three work is happening in partnership with [the GSA's Privacy Office](https://www.gsa.gov/reference/gsa-privacy-program).


<!--- # DevOps for Privacy Offices

### We envision a future in which the public can easily understand how and why personally identifiable information gets collected by government agencies. 

This project is funded by [10x](https://10x.gsa.gov/).

## Project Description

**DevOps for Privacy Offices** phase three aims to bring privacy compliance documentation back to life by reducing unnecessary manual practices across privacy offices in the federal government and increasing the public’s access to this important information.

<!--
### What we believe this model can achieve

- **New Search Capabilities:** A dashboard that enables Privacy Officers to search all their privacy compliance documents at once, easing their administrative burden and freeing up their time to focus on other activities.

- **Speed up Compliance:** Program teams completing compliance paperwork will be able to see the important elements of PIAs from the beginning, and can use the structured data when drafting PIAs.

- **More Context for risk assessment:** It will allow privacy offices to adopt new and more efficient ways to assess and compare the risk level of their systems from a single vantage point.

- **Reduce scope of breaches:** Retention policies that mandate when data will be deleted, reduce the impact of breaches when they happen. Our dashboard will aid enforcement of those retention policies, by making them easy to find and understand for the Privacy Officers, the system owners, and the public.

- **Increased accuracy:** Program Teams will be able to easily see their current level of compliance. The dashboard will quickly let them know what PII they said they collect, why, for how long, and how it can be shared.

## Partner with us
If you are a privacy officer or work in a privacy office and are interested in making your agency's SORNs and PIAs available on our system, we want to hear from you. Please send an e-mail to privacy_devops@gsa.gov.

--->

## Install

The scraping code is written in Python and runs locally. We recommend creating a virtual environment using virtualenv to install and manage the required Python libraries. Run these commands in the repository directory on your machine to create a local virtual environment, start it, and then install all requirements.

```
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Scraping Data

Running `python sorn_scraper.py` does the following:
- Fetches the contents of the [page](https://www.gsa.gov/reference/gsa-privacy-program/systems-of-records-privacy-act/system-of-records-notices-sorns-privacy-act) where GSA publishes links and descriptions of System of Records Notices (SORNs)
- Scrapes the unique SORN identifiers contained in each federalregister.gov url and crafts url for the XML version of the full text document
- Downloads those XML files and parses them to get the text from specific sections of the document:
  - System Name
  - PII
  - Purpose
  - Retention Policy
  - Routine Uses
  - Document Title
- Outputs text from these fields into a local .csv file called `gsa_sorns.csv` with one row per system.


