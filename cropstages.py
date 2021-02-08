import datetime
import json
from datetime import timedelta


class Cropstages(object):
    def __init__(self):
        self.seedtime = self._get_julian(datetime.datetime.now())
        self.stage_days = []
        self.depths = []

    def load_file(self, file):
        with open(file) as json_file:
            data = json.load(json_file)
            # I get the DD/MM/YYYY format so I convert to datetime:
            self.seedtime = list(data['seedtime'].split("/"))
            self.seedtime = datetime.datetime(
                2000 + int(self.seedtime[2]), int(self.seedtime[1]), int(self.seedtime[0]))
            # Get the julians days in a list:
            julian_init_day = self._get_julian(self.seedtime)
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

    def __repr__(self):
        data_inside = ""
        data_inside += "Seedtime: " + str(self.seedtime) + "\n"
        data_inside += "Kc: " + str(self.kc) + "\n"
        data_inside += "Stage_days: " + str(self.stage_days) + "\n"
        data_inside += "Depths_radicualar: " + \
            str(self.depths_radicualar) + "\n"
        return data_inside

    def _calc_eta(self):
        # The first eta is the first day etc.

        # The following ta
        pass

    def _calc_evo(self):
        if self.seedtime < stage_days[0]:
            return 0
        elif self.seedtime < stage_days[1]:
            return stage_days[0]
        elif self.seedtime < stage_days[1]:
            pass

    def _get_julian(self, date):
        # Substract the current day to the first day of the year:
        first_day_year = datetime.datetime(date.year, 1, 1)
        julian_day = (date-first_day_year).days + 1
        return julian_day


cropstages = Cropstages()
cropstages.load_file('data/cropstages.json')
print(cropstages)
