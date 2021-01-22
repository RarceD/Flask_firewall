import math


class calculateEto(object):
    """
     For calculating ET0 I need first:
     - Short_radiation - x
     - Long radiation - x
    """

    def __init__(self):
        self.t_med_ = 0.0
        self.t_med_previous = 0.0
        self.t_max = 0.0
        self.t_min = 0.0
        self.rad_net = 0.0
        self.rad_net_short = 0.0
        self.rad_net_long = 0.0
        self.rad_net_wave_no_cloud = 0.0
        self.albedo = 0.23
        self.rad_solar = 0.0  # obtein from api
        self.rad_solar_0 = 0.1
        self.presure_vap = 0.0
        self.height = 0.0
        self.hum_max = 0.0
        self.hum_min = 0.0

    def calc_eto(self):
        # get rad solar from api:
        self.rad_solar = self.ger_rad_solar()
        self.rad_net_short = (1-self.albedo)*self.rad_solar
        self.rad_net_wave_no_cloud = (
            0.75 + (2*self.height/100000))*calc_radiation_extra(self.days, self.latitude)
        self.presure_vap = self.calc_preasure(self.t_max, self.t_min, self.hum_max,self.hum_min)
        self.rad_net_long = (4.903*10**(-9.0/2.0))*1.35*((self.rad_solar/self.rad_solar_0)-0.35)*(
            0.34-0.14*self.presure_vap**0.5)*((self.t_max+273.0)**4 + (self.t_min+273.0)**4)
        self.rad_net = self.rad_net_long - self.rad_net_short

        thermal_flow = 0.1*(self.t_med-self.t_med_previous)
        ## TODO
        gamma = (1.103*10**(-3)*self.presure_atm)
        print(self.rad_net_long)
        return self.rad_net_long

    def ger_rad_solar(self):
        return 0.1

    def calc_radiation_extra(self, days, latitude):
        # days are on julian days
        distance_earth_sun = 1 + 0.033 * math.cos(((2*math.pi)/365)*days)
        # Latitude and logitude on radians:
        latitude = math.radians(latitude)
        # Solar declination:
        declination = 0.409*math.sin((2*math.pi)/365.0 * days - 1.39)
        # Compute solar angle:
        solar_angle = math.acos(-math.tan(latitude)*math.tan(declination))

        ra = (24.0*60.0*0.082)/math.pi * distance_earth_sun * distance_earth_sun*(solar_angle*math.sin(latitude)
                                                                                  * math.sin(declination) + math.cos(latitude)*math.cos(declination)*math.sin(solar_angle))
        return ra

    def calc_preasure(self, t_max, t_min, hum_max,hum_min):
        # HR: relative humidity
        e_max = 0.6108*math.e**((17.27*t_max)/(t_max+237.3))
        e_min = 0.6108*math.e**((17.27*t_min)/(t_min+237.3))
        return (e_max*hum_min/100.0)+(e_min*hum_max)/200


calc = calculateEto()

calc.calc()
print(10**(4))
print(math.pi)
