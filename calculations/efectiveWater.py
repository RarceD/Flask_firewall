
class Efective_water(object):
    def __init__(self):
        #INPUTS:
        self.initial_water_percentage = 10 #HD initial  
        self.fc = 1
        self.wp = 1
        ## crop db
        ## group naps

        self.efective_water = 0
    
    def solve(self):
        rad_balance = self._calc_rad_balance()
        efective_water_num =  rad_balance - 1

    def _calc_rad_balance(self, first_day):
        balance = 0
        if first_day:
            balance = self.initial_water_percentage /(100)
        else:
            balance = self.initial_water_percentage /(100)
        return 0
