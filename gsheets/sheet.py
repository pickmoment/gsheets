class Sheet():
    def __init__(self, client, doc_id, title, sheet_id):
        self.__client = client
        self.__doc_id = doc_id
        self.title = title
        self.sheet_id = sheet_id
        self.headers = {}
        self.rows = []
    
    def read(self, has_headers=True, cell_range=''):
        range_text = [self.title]
        if cell_range:
            range_text.append(cell_range)
        result = self.__client.values().get(spreadsheetId=self.__doc_id, range='!'.join(range_text)).execute()
        data = result.get('values', [])
        self.headers = {} if not data else {d: i for i, d in enumerate(data[0])} if has_headers else {}
        self.rows = [] if not data else data[1:] if has_headers else data
        self.__last_row = len(self.rows) + 1
        self.__last_col = len(self.headers) if self.headers else len(self.rows[0]) if self.rows else 1
        return self
    
    def write(self, cell_range='', is_raw=False):
        range_text = [self.title]
        value_option = 'RAW' if is_raw else 'USER_ENTERED'
        values = []
        if self.headers:
            values.append(list(self.headers.keys()))
        values += self.rows
        
        if self.__last_row > len(values):
            col_size = len(self.headers) if self.headers else self.__last_col
            null_row = ['' for i in range(col_size)]
            for i in range(self.__last_row - len(values)):
                values.append(null_row)
        
        if len(values) > 0 and self.__last_col > len(values[0]):
            col_diff = self.__last_col - len(values[0])
            for val in values:
                for i in range(col_diff):
                    val.append('')
        
        body = {
            'values': values
        }
        if cell_range:
            range_text.append(cell_range)
        result = self.__client.values().update(spreadsheetId=self.__doc_id, range='!'.join(range_text), valueInputOption=value_option, body=body).execute()

    def get(self, row, col):
        if (type(col) is str):
            col = self.headers[col]
        return self.rows[row][col]
    
    def set(self, row, col, value):
        if (type(col) is str):
            col = self.headers[col]
        self.rows[row][col] = value
    
    def add(self, values):
        row = []
        if type(values) is dict:
            for key in self.headers.keys():
                row.append(values.get(key, ''))
        else:
            if self.headers:
                for i, key in enumerate(self.headers.keys()):
                    row.append(values[i])
            else:
                row = values
        self.rows.append(row)

    def remove(self, index):
        del self.rows[index]
        
    def set_headers(self, headers):
        if self.rows:
            if len(self.rows[0]) != len(headers):
                raise Exception('headers has invalid length')
        self.headers = {h: i for i, h in enumerate(headers)}