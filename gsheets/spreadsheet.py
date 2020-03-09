from .sheet import Sheet

class SpreadSheet():
    def __init__(self, client, doc_id,):
        self.__client = client
        self.doc_id = doc_id
        self.__metadata = self.__client.get(spreadsheetId=self.doc_id).execute()
        self.title = self.__metadata.get('properties', {}).get('title', '')
        self.sheets = [Sheet(self.__client, self.doc_id, s.get('properties', {}).get('title', 'Sheet1'), s.get('properties', {}).get('sheetId', '')) for s in self.__metadata.get('sheets', [])]
        
    def add_sheet(self, title):
        body = {
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': title
                    }
                }
            }]
        }
        result = self.__client.batchUpdate(spreadsheetId=self.doc_id, body=body).execute()
        props = result.get('replies', {})[0].get('addSheet', {}).get('properties', {})
        sheet = Sheet(self.__client, self.doc_id, props.get('title', ''), props.get('sheetId', ''))
        self.sheets.append(sheet)
        return sheet
        
    def remove_sheet(self, sheet):
        body = {
            'requests': [{
                'deleteSheet': {
                    'sheetId': sheet.sheet_id
                }
            }]
        }
        self.__client.batchUpdate(spreadsheetId=self.doc_id, body=body).execute()
        self.sheets.remove(sheet)

    def get_sheet(self, title):
        return next((sheet for sheet in self.sheets if sheet.title == title), None)
        