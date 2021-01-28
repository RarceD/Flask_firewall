import math
from requestAemet import RequestAemet
import datetime


class calculateEto(object):
    """
     For calculating ET0 I need first:
        - Temperatures
        - Humidity
        - Solar Radiation
        - Wind Speed
        - Latitude
        - Height
     - There are 12 necessary values
    """

    def __init__(self):
        # The initial data that we need to start with:
        self.t_med = 15.11
        self.t_medprevious = 14.8
        self.t_max = 22.73
        self.t_min = 8.35
        self.hum_max = 53.4
        self.hum_min = 25.05
        self.hum_med = 41.1
        self.rad_solar = 21.37  # obtein from api
        self.wind_speed = 3.54*3.6  # in km/hour
        self.height = 371.0  # in meters
        self.latitude = 39.8152777

        # Constants:
        self.days = self._get_julian(datetime.datetime.now())
        # If I want to calculate on specific day:
        # self.days = self._get_julian(datetime.datetime(2018,3,18))
        self.rad_net = 0.0
        self.rad_net_short = 0.0
        self.rad_net_long = 0.0
        self.rad_solar_0 = 0.0

    def load_file(self, input_data):
        try: 
            self.t_med = input_data['t_med']
            self.t_medprevious = input_data['t_medprevious']
            self.t_max = input_data['t_max']
            self.t_min = input_data['t_min']
            self.hum_max = input_data['hum_max']
            self.hum_min = input_data['hum_min']
            self.hum_med = input_data['hum_med']
            self.rad_solar = input_data['rad_solar']
            self.wind_speed = input_data['wind_speed']
            self.height = input_data['height']
            self.latitude = input_data['latitude']
            return True
        except:
            return False

    def __repr__(self):
        data = ""
        data += " Tmed - Tmax - Tmin: " + \
            str(self.t_med)+" ! " + str(self.t_max) + \
            " ! " + str(self.t_min)+"\n"
        data += " Hmed - Hmax - Hmin: " + \
            str(self.hum_med)+" ! " + str(self.hum_max) + \
            " ! " + str(self.hum_min)+"\n"
        data += "wind speed: " + str(self.wind_speed)+"\n"
        data += "Height: " + str(self.height)+"\n"
        data += " Solar Radiation: " + str(self.rad_solar) + "\n"
        data += " Solar Radiation_0: " + str(self.rad_solar_0) + " - OK" + "\n"
        data += " Solar Radiation LONG: " + \
            str(self.rad_net_long) + " - OK" "\n"
        data += " Solar Radiation SHORT: " + \
            str(self.rad_net_short) + " - OK" + "\n"
        data += " Solar Radiation NETA: " + str(self.rad_net) + " - OK"+"\n"
        return data

    def get_data(self):
        weather_data = RequestAemet()
        self.t_max, self.t_min, self.t_med, self.hum_max, self.hum_min, self.wind_speed = weather_data.get_weather_params()

    def calc_eto(self):
        # Short solar radiation:
        self.rad_net_short = (1-0.23)*self.rad_solar
        # Extra solar radiation for day periods:
        ra = self._calc_radiation_extra()
        # Solar radiation on cloudy days:
        self.rad_solar_0 = (0.75 + (2*self.height/100000)) * ra
        # Pressure vap
        presure_vap, e_s = self._calc_preasure()
        # Long solar radiation:
        self.rad_net_long = 4.903*10**(-9)*((self.t_max+273.16)**4 + (self.t_min+273.16)**4)/2*(
            0.34-(0.14*presure_vap**0.5))*(1.35*(self.rad_solar/self.rad_solar_0)-0.35)
        self.rad_net = self.rad_net_short - self.rad_net_long
        # Flujo termico de suelo
        thermal_flow = 0.1*(self.t_med-self.t_medprevious)
        # Constante psicrométrica
        gamma, lambda_vap = self._calc_gamma()
        delta = self._calc_delta()
        # Convert to m/s
        self.wind_speed /= 3.6
        # The last operation to get the ET_0:
        num = delta*(self.rad_net - thermal_flow)+(gamma*900 *
                                                   self.wind_speed*lambda_vap*(e_s-presure_vap))/(self.t_med+273.16)
        den = lambda_vap*(delta+gamma*(1+0.34*self.wind_speed))
        et_0 = num/den
        return et_0

    def _calc_radiation_extra(self):
        # Days are on julian days
        distance_earth_sun = 1 + 0.033 * math.cos(((2*math.pi)/365)*self.days)
        # Latitude and logitude on radians:
        self.latitude = math.radians(self.latitude)
        # Solar declination:
        declination = 0.409*math.sin((2*math.pi)/365.0 * self.days - 1.39)
        # Compute solar angle:
        solar_angle = math.acos(-math.tan(self.latitude)*math.tan(declination))
        ra = (24.0*60.0*0.082)/math.pi * distance_earth_sun*(solar_angle*math.sin(self.latitude)
                                                             * math.sin(declination) + math.cos(self.latitude)*math.cos(declination)*math.sin(solar_angle))
        return ra

    def _calc_preasure(self):
        e_max = 0.6108*math.e**((17.27*self.t_max)/(self.t_max+237.3))
        e_min = 0.6108*math.e**((17.27*self.t_min)/(self.t_min+237.3))
        return ((e_max*self.hum_min/100.0)+(e_min*self.hum_max/100))/2, (e_max+e_min)/2

    def _calc_gamma(self):
        # Phicromertric constant:
        c_p = 1.102*10**(-3)
        lambda_vap = 2.501 - (0.002361*self.t_med)
        P = 101.3*((293-0.0065*self.height)/293)**5.26
        gamma = (c_p*P)/(0.622*lambda_vap)
        return gamma, lambda_vap

    def _calc_delta(self):
        # Correlation between temperatura and vapor pressure
        t = (self.t_max + self.t_min)/2
        e_med = 0.6108*math.e**((17.27*t)/(t+237.3))
        return (4098*e_med) / ((self.t_max+self.t_min)/2 + 237.3)**2

    def _get_julian(self, date):
        # Substract the current day to the first day of the year:
        first_day_year = datetime.datetime(date.year, 1, 1)
        julian_day = (date-first_day_year).days + 1
        return julian_day


calc = calculateEto()
print("ET0: ", calc.calc_eto())
# print(calc)
# a = RequestAemet()
# print(a)
