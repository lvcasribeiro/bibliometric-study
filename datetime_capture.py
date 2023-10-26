from datetime import timedelta, datetime, date

# Função para captura de data e horário correntes:
def captura_data_e_horario():
    # Data:
    data = date.today()
    data = data.strftime('%d-%m-%Y')

    # Horário:
    hora = datetime.now().hour
    minuto = datetime.now().minute
    segundo = datetime.now().second

    str_datetime = f'{hora}-{minuto}-{segundo}_{data}'
    

    return str_datetime
