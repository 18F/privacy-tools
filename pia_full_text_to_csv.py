import glob, csv

'''
This file will create a large .csv containing the full text of all of the PIAs.
You'll need to first get the full text of each PIA by running the `pia_scraper.py`
Once the `pias` folder is full of text files, you can run this to generate `pias/pia-full-text-search.csv`
'''

if __name__ == '__main__':
  pia_text_files = glob.glob("pias/*.txt")
  with open("pias/pia-full-text-search.csv", "w") as full_text_file:
    csv_writer = csv.writer(full_text_file)
    id = 0
    csv_writer.writerow(["id", "system name", "full text"]) # headers
    for file_path in pia_text_files:
      system_name = file_path.split("/")[1].split(".")[0]
      full_text = open(file_path).read()
      id =+ 1
      csv_writer.writerow([id, system_name, full_text])
