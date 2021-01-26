import math
from requestAemet import RequestAemet
import datetime


class calculateEto(object):
    """
     For calculating ET0 I need first:
     - Aemet values:
        - T_max
        - T_min
        - Hum
        - 
     - Long radiation - x
    """

    def __init__(self):
        self.t_med = 15.0
        self.t_medprevious = 0.0
        self.t_max = 20.0
        self.t_min = 10.0
        self.rad_net = 0.0
        self.rad_net_short = 0.0
        self.rad_net_long = 0.0
        self.rad_net_wave_no_cloud = 0.0
        self.albedo = 0.23
        self.rad_solar = 0.0  # obtein from api
        self.rad_solar_0 = 0.1
        self.height = 800.0  # in meters
        self.hum_max = 0.0
        self.hum_min = 0.0
        self.hum_med = 0.0
        self.c_p = 1.102*10**(-3)
        self.height = 860.0  # in meters

        self.presure_atm = 1020.0
        self.latitude = 42.34
        self.days = self.get_julian(datetime.datetime.now())
        self.wind_speed = 8  # in km/hour

    def __repr__(self):
        data = ""
        data += "Tmed - Tmax - Tmin: " + \
            str(self.t_med)+" ! " + str(self.t_max) + \
            " ! " + str(self.t_min)+"\n"
        data += "Hmed - Hmax - Hmin: " + \
            str(self.hum_med)+" ! " + str(self.hum_max) + \
            " ! " + str(self.hum_min)+"\n"
        data += "wind speed: " + str(self.wind_speed)+"\n"
        data += "Height: " + str(self.height)+"\n"
        return data

    def get_data(self):
        weather_data = RequestAemet()
        self.t_max, self.t_min, self.t_med, self.hum_max, self.hum_min, self.wind_speed = weather_data.get_weather_params()

    def calc_eto(self):
        # get rad solar from api:
        self.rad_solar = self.get_rad_solar()
        self.rad_net_short = (1-self.albedo)*self.rad_solar
        self.rad_net_wave_no_cloud = (
            0.75 + (2*self.height/100000))*self.calc_radiation_extra()
        presure_vap, e_s = self.calc_preasure()
        self.rad_net_long = (4.903*10**(-9/2))*1.35*((self.rad_solar/self.rad_solar_0)-0.35)*(
            0.34-0.14*presure_vap**0.5)*((self.t_max+273.0)**4 + (self.t_min+273.0)**4)
        self.rad_net = self.rad_net_long - self.rad_net_short

        thermal_flow = 0.1*(self.t_med-self.t_medprevious)
        gamma, lambda_vap = self.calc_gamma()
        delta = self.calc_delta()
        self.wind_speed /= 3.6  # Convert to m/s

        # The last operation to get the ET_0:
        num = delta*(self.rad_net - thermal_flow)+((gamma*900*self.wind_speed) /
                                                   (self.t_med+273.16))*lambda_vap*(e_s-presure_vap)
        den = delta+lambda_vap*(1+0.34*self.wind_speed)
        et_0 = 1/lambda_vap * num/den
        # print(self.wind_speed)
        return et_0

    def get_rad_solar(self):
        return 0.1

    def calc_radiation_extra(self):
        # days are on julian days
        distance_earth_sun = 1 + 0.033 * math.cos(((2*math.pi)/365)*self.days)
        # Latitude and logitude on radians:
        #Convert latitude in º to radians
        self.latitude = math.radians(self.latitude)
        # Solar declination:
        declination = 0.409*math.sin((2*math.pi)/365.0 * self.days - 1.39)
        # Compute solar angle:
        solar_angle = math.acos(-math.tan(self.latitude)*math.tan(declination))

        ra = (24.0*60.0*0.082)/math.pi * distance_earth_sun * distance_earth_sun*(solar_angle*math.sin(self.latitude)
                                                                                  * math.sin(declination) + math.cos(self.latitude)*math.cos(declination)*math.sin(solar_angle))
        return ra

    def calc_preasure(self):
        # HR: relative humidity
        e_max = 0.6108*math.e**((17.27*self.t_max)/(self.t_max+237.3))
        e_min = 0.6108*math.e**((17.27*self.t_min)/(self.t_min+237.3))
        return (e_max*self.hum_min/100.0)+(e_min*self.hum_max)/200, (e_max+e_min)/2

    def calc_gamma(self):
        lambda_vap = 2.501 - (0.002361*self.t_med)
        P = 101.3*((293-0.0065*self.height)/293)**5.26
        gamma = (self.c_p*P)/(0.622*lambda_vap)
        return gamma, lambda_vap

    def calc_delta(self):
        t = (self.t_max + self.t_min)/2
        e_med = 0.6108*math.e**((17.27*t)/(t+237.3))
        return (4098*e_med) / ((self.t_max+self.t_min)/237.3)**2

    def get_julian(self, date):
        # Substract the current day to the first day of the year:
        first_day_year = datetime.datetime(date.year, 1, 1)
        julian_day = (date-first_day_year).days + 1
        return julian_day


calc = calculateEto()
print(calc)
calc.get_data()
print(calc)
print(calc.calc_eto())
# a = RequestAemet()
# print(a)
