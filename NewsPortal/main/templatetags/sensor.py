from django import template
 
register = template.Library()
 

list_sensor = ['qwert', 'qwert12'] # Список запрещенной лексики


def multiple_replace(value, list_sensor):
    """Функция будет заменять запрещенную лексику на ***

    Args:
        value (str): фильтруемое значение
        list_sensor (list): список запрещенной лексики

    Returns:
        str: [description]
    """
    for word in list_sensor:
        value = value.replace(word, '***')
    
    return value
    

 
@register.filter(name='Sensor')  
def sensor(value):
    if filter(lambda x: x in value, list_sensor):
        return multiple_replace(value, list_sensor)
