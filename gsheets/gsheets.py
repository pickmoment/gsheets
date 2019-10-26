from googleapiclient.discovery import build
from .spreadsheet import SpreadSheet

class GSheets():
    def __init__(self, creds):
        self.__client = build('sheets', 'v4', credentials=creds).spreadsheets()
        
    def open(self, doc_id):
        return SpreadSheet(self.__client, doc_id)
    
    def create(self, title):
        spreadsheet = {
            'properties': {
                'title': title
            }
        }
        result = self.__client.create(body=spreadsheet, fields='spreadsheetId').execute()
        return result.get('spreadsheetId', '')