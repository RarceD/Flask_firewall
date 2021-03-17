import datetime
import json
from datetime import timedelta


class Cropstages(object):
    def __init__(self):
        self.seedtime = self._get_julian(datetime.datetime.now())
        self.stage_days = []
        self.depths = []
        self.kc =0
        self.depths_radicualar =0
        self.depths_suelo =0
        self.stone_percentage =0
        self.precipitation_day =0
        self.efective_precipitation_day =0
        self.iHD_initial =0
        self.radiocular_ =0
        self.et0 =0
        self.cred_rad =0
        self.nap =0

    def load_file(self, file):
        try:
            with open(file) as json_file:
                data = json.load(json_file)
                # I get the DD/MM/YYYY format so I convert to datetime:
                self.seedtime = list(data['seedtime'].split("/"))
                self.seedtime = datetime.datetime(
                    2000 + int(self.seedtime[2]), int(self.seedtime[1]), int(self.seedtime[0]))
                # Get the julians days in a list:
                self.seedtime = self._get_julian(self.seedtime)
                self.stage_days = data['stage_days']
                days_julians = []
                previous_s = 0
                for s in self.stage_days:
                    previous_s += s
                    days_julians.append(self._get_julian(
                        self.seedtime + timedelta(days=previous_s)))
                self.stage_days = days_julians.copy()
                # The kc provided by the client:
                self.kc = data['kc']
                self.depths_radicualar = data['depths_radicualar']
                self.depths_suelo = data['depths_suelo']
                self.stone_percentage = data['stone_percentage']
                self.precipitation_day = data['precipitation_day']
                self.efective_precipitation_day = data['efective_precipitation_day']
                self.iHD_initial = data['iHD_initial']
                self.radiocular_ = data['radiocular_']
                self.et0 = data['et0']
                self.cred_rad = data['cred_rad']
                self.nap = data['nap']
                self.crop = data['crop']
                return True
        except:
            return False

    def __repr__(self):
        data_inside = ""
        data_inside += "Seedtime: " + str(self.seedtime) + "\n"
        data_inside += "Kc: " + str(self.kc) + "\n"
        data_inside += "Stage_days: " + str(self.stage_days) + "\n"
        data_inside += "Depths_radicualar: " + \
            str(self.depths_radicualar) + "\n"
        return data_inside

    def solve(self):
        # The first eta is the first day etc.
        eta = 0
        efective_precipitation = self.precipitation_day * \
            self.efective_precipitation_day/100
        fc = 0  # i don't have the fc
        water_balance_rad = self.iHD_initial / \
            (100*fc*(1-self.stone_percentage)*1000*self.depths_radicualar[0])
        wp = 0  # i don't have it and don't even know what it is.
        pr = 0
        cred_rad = 0
        eta_num = water_balance_rad+efective_precipitation + \
            self.precipitation_day+cred_rad * \
            (wp*(1-self.stone_percentage)*pr*1000)

        eta_den = (1-self.nap)/((1-self.stone_percentage)*(fc-wp)*pr*1000)
        # The following ta
        return eta_num/eta_den

    def _calc_evo(self, stage, prev_evo):
        # TODO: Let's make any sense---
        if stage == 0:
            if self.seedtime < stage_days[0]:
                return 0
            else:
                return stage_days[0]
        if stage == 1:
            return prev_evo
        elif self.seedtime < stage_days[1]:
            return
        elif self.seedtime < stage_days[1]:
            pass

    def _get_julian(self, date):
        # Substract the current day to the first day of the year:
        first_day_year = datetime.datetime(date.year, 1, 1)
        julian_day = (date-first_day_year).days + 1
        return julian_day





cropstages = Cropstages()
if (cropstages.load_file('data/cropstages.json')):
    print(cropstages)
