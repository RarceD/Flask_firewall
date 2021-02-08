class Cropstages(object):
    def __init__ (self):
        self.seedtime = str()
        self.stage_days = []
        self.depths = []
    def calc_eta(self):
        #The first eta is the first day etc.
        