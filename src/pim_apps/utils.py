import csv
import os
import tempfile
import zipfile

import pandas as pd
os.environ['A2C_BASE_URL']="https://api.api2cart.com/"

os.environ['PIM_APP_BASE_URL']="https://pim-apps.unbxd.io/pim/"
os.environ['PIM_BASE_URL']="https://pim.unbxd.io/"
os.environ['PEPPERX_URL']="https://pim.unbxd.io/pepperx/"

os.environ['QA_PIM_APP_BASE_URL']="http://pimqa-apps.unbxd.io/pim/"
os.environ['QA_PIM_BASE_URL']="http://pimqa.unbxd.io/"
os.environ['QA_PEPPERX_URL']="https://pimqa.unbxd.io/pepperx/"



def get_pim_app_domain():

    env = os.environ['PEPPERX_ENV']
    url = os.environ['PIM_APP_BASE_URL'] if env == "PROD" else os.environ['QA_PIM_APP_BASE_URL']
    print(f" {env} ---- {url} ")
    return url


def get_pim_domain():
    env = os.environ['PEPPERX_ENV']
    url = os.environ['PIM_BASE_URL'] if env == "PROD" else os.environ['QA_PIM_BASE_URL']
    print(f" {env} ---- {url} ")
    return url


def get_a2c_domain():
    return os.environ['A2C_BASE_URL']


def get_pepperx_domain():
    env = os.environ['PEPPERX_ENV']
    url =  os.environ['PEPPERX_URL'] if env == "PROD" else os.environ['QA_PEPPERX_URL']
    print(f" {env} ---- {url} ")
    return url

def write_csv_file(data, delimiter="\t", filename="IndexedExport.csv"):

    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=delimiter)
        csvwriter.writerows(data)
    return filename

class FileParser(object):
    def load(self ,url):
        self.url = url
        self.file_type = url.split(".")[-1]
        print("The URL file type is : ", self.file_type)
        method_name ='parse_' +self.file_type
        method =getattr(self ,method_name ,lambda :'Invalid')
        return method()

    def infer_schema(self):
        self.df.info()
        self.columns = list(self.df.columns.values.tolist())
        print("List of all columns are : ", self.columns)
        print("##### Pandas inferred Schema")
        pandas_schema = self.df.columns.to_series().groupby(self.df.dtypes).groups
        print(pandas_schema)

    def parse_xlsx(self):
        return self.parse_excel()

    def parse_xlsm(self):
        return self.parse_xlsm()

    def parse_xls(self):
        return self.parse_excel()

    def parse_csv(self):
        df = pd.read_csv(self.url, sep=",", header=0)

    def parse_zip(self):
        zip = zipfile.ZipFile('filename.zip')

        # available files in the container
        print(zip.namelist())
        zip.open(zip.namelist()[0])

    def parse_tsv(self):
        df = pd.read_csv(self.url, sep="\t", header=0)

    def parse_json(self):
        df = pd.read_json(self.url)

    #         https://www.dataquest.io/blog/python-json-tutorial/
    # def parse_xml(self):
    #     xml2df = XML2DataFrame(self.url)
    #     self.df = xml2df.process_data()

    def parse_txt(self):
        df = pd.read_csv(self.url, sep=" ")

    def parse_tsv(self):
        df = pd.read_csv(self.url, sep="\t", header=0)

    def parse_excel(self):
        xls = pd.ExcelFile(self.url)
        # Now you can list all sheets in the file
        sheets = xls.sheet_names;
        print("Sheets present in excel file are : ", sheets)
        self.df = pd.read_excel(xls, sheets[0])
        return self.infer_schema()

    def parse_xlsm(self):
        print("Pasring Amazon File in xlsm format")
        xls = pd.ExcelFile(self.url)
        # Now you can list all sheets in the file
        # sheets = xls.sheet_names;
        # enum_value_rules = pd.read_excel(xls, sheet_name="Valid Values")
        # # valid_enum_values = pd.read_excel(xls, sheet_name="Valid Values", header=1)
        # properties_list = pd.read_excel(xls, sheet_name="Data Definitions", header=1)
        # properties_template = pd.read_excel(xls, sheet_name="Template", header=0)
        return xls
