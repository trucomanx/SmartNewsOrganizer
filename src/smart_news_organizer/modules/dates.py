from dateutil import parser

def normalizar_data(data_str):
    try:
        dt = parser.parse(data_str)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(f"Erro ao converter data: {data_str} -> {e}")
        return data_str
        
def get_datetime(data):
    try:
        return parser.parse(data.published)
    except Exception:
        return parser.parse("1900-01-01 00:00:00") 
