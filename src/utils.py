import random
from src.config import setup_parameters

def get_checkin_time_counter():
    return random.expovariate(1.0 / setup_parameters['CHECKIN_TIME']['counter'])

def get_checkin_time_kiosk():
    return random.expovariate(1.0 / setup_parameters['CHECKIN_TIME']['kiosk'])

def get_security_time():
    return random.expovariate(1.0 / setup_parameters['SECURITY_TIME'])

def get_immigration_time():
    return random.expovariate(1.0 / setup_parameters['IMMIGRATION_TIME'])
