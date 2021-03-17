import datetime
import json
from datetime import timedelta
from databaseinteractions import DatabaseInteractions
import math


class Cropstages(object):
    def __init__(self):
        self.seedtime = self._get_julian(datetime.datetime.now())
        self.stage_days = []
        self.depths = []
        self.kc = 0
        self.depths_radicualar = 0
        self.depths_suelo = 0
        self.stone_percentage = 0
        self.precipitation_day = 0
        self.efective_precipitation_day = 0
        self.iHD_initial = 0
        self.radiocular_ = 0
        self.et0 = 0
        self.cred_rad = 0
        self.nap = 0
        self.crop = "Girasol"
        self.texture = "Arcilloso"
        
        self.fc = 0
        self.wp = 0
        self.ep  = 0
               

        self.efective_prec_percentage = 0  # porcentaje de precipitación efectivo
        self.efective_riego_percentage = 0  # porcentaje de riego efectivo
        self.precipitation = 0  # lluvia que cae, obtenido de las estaciones
        self.irrigation = 12  # mm de riego

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

    def calc_eta(self):

        # The first eta is the first day etc.
        efective_precipitation = self.precipitation_day * \
            self.efective_precipitation_day/100
        # obtein the fc and wp from the database:
        db = DatabaseInteractions()
        crop_params = db.get_parameters_plot(self.texture)
        self.fc, self.wp, self.ep = crop_params['fc'], crop_params['wp'], crop_params['ep']
        crop_params = db.get_nap_parameters_crop(self.crop)
        nap_a, nap_b, nap_c = crop_params['naps_abc'][0],  crop_params['naps_abc'][1],  crop_params['naps_abc'][2]
        self.kc = crop_params['kcs_list']

        etm = self.et0 * float(self.kc[0])
        NAP = (1-nap_a)/(1+nap_b*math.exp(-nap_c * etm))

        pr = 1
        # water_balance_rad = self.iHD_initial / \
        #     (100*self.fc*(1-self.stone_percentage)
        #      * 1000*self.depths_radicualar[0])
        water_balance_rad = 1
        cred_rad = 0
        eta_num = water_balance_rad+efective_precipitation + \
            self.precipitation_day+cred_rad * \
            (self.wp*(1-self.stone_percentage)*pr*1000)

        eta_den = (1-self.nap)/((1-self.stone_percentage)
                                * (self.fc-self.wp)*pr*1000)
        self.eta = eta_num / eta_den

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

    def get_water_util(self, first_day):

        # INPUTS:
        radicular_depht = 1
        radicular_balace_day = 21
        radicular_balace_first_day = 3
        water_util_num = 0
        water_util_den = (self.fc*(1-self.stone_percentage))*1000*radicular_depht - \
            (self.wp*(1-self.stone_percentage))*1000*radicular_depht

        # It change if is the first day or not:
        if first_day:
            water_util_num = (radicular_balace_day - (self.wp(1-self.stone_percentage))
                              * 1000*radicular_depht)*100
        else:
            water_util_num = (radicular_balace_first_day - (self.wp(1-self.stone_percentage))
                              * 1000*radicular_depht)*100

    def _calc_radicular_balance(self, first_day, HD, radicular_depht):
        radicular_balance_first_stage = 0
        radicular_balance = 0
        radicular_balance_prev = 0
        eta = self._cal_inputs()
        inputs = 0

        if first_day:
            radicular_balance = HD / \
                (100*self.fc*(1-self.stone_percentage)*1000*radicular_balance_first_stage)
        else:
            if (radicular_balance_prev + inputs - eta) > radicular_depht:
                paradicular_balance = radicular_depht * \
                    self.fc * (1-self.stone_percentage) * 100
            else:
                paradicular_balance = radicular_depht * \
                    self.wp * (1-self.stone_percentage) * 100

    def _cal_inputs(self):
        pe = self.efective_prec_percentage * self.precipitation / 100
        riego_neto = self.irrigation * (1-self.efective_riego_percentage)/100
        radicular_growth = 0  # Es cero porque me sale de los cojones
        inputs = pe + riego_neto + radicular_growth
        return inputs
