from coderack import Coderack
from randomness import Randomness
from slipnet import Slipnet
from temperature import Temperature
from workspace import Workspace


class Reporter(object):
    """Do-nothing base class for defining new reporter types"""
    def report_answer(self, answer):
        pass

    def report_coderack(self, coderack):
        pass

    def report_slipnet(self, slipnet):
        pass

    def report_temperature(self, temperature):
        pass

    def report_workspace(self, workspace):
        pass


class Copycat(object):
    def __init__(self, rng_seed=None, reporter=None):
        self.coderack = Coderack(self)
        self.random = Randomness(rng_seed)
        self.slipnet = Slipnet()
        self.temperature = Temperature()
        self.workspace = Workspace(self)
        self.reporter = reporter or Reporter()

    def mainLoop(self, lastUpdate):
        currentTime = self.coderack.codeletsRun
        self.temperature.tryUnclamp(currentTime)
        # Every 15 codelets, we update the workspace.
        if currentTime >= lastUpdate + 15:
            self.workspace.updateEverything()
            self.coderack.updateCodelets()
            self.slipnet.update(self.random)
            self.temperature.update(self.workspace.getUpdatedTemperature())
            lastUpdate = currentTime
            self.reporter.report_slipnet(self.slipnet)
        self.coderack.chooseAndRunCodelet()
        self.reporter.report_coderack(self.coderack)
        self.reporter.report_temperature(self.temperature)
        self.reporter.report_workspace(self.workspace)
        return lastUpdate

    def runTrial(self):
        """Run a trial of the copycat algorithm"""
        self.coderack.reset()
        self.slipnet.reset()
        self.temperature.reset()
        self.workspace.reset()
        lastUpdate = float('-inf')
        while self.workspace.finalAnswer is None:
            lastUpdate = self.mainLoop(lastUpdate)
        answer = {
            'answer': self.workspace.finalAnswer,
            'temp': self.temperature.last_unclamped_value,
            'time': self.coderack.codeletsRun,
        }
        self.reporter.report_answer(answer)
        return answer

    def run(self, initial, modified, target, iterations):
        self.workspace.resetWithStrings(initial, modified, target)
        answers = {}
        for i in range(iterations):
            answer = self.runTrial()
            d = answers.setdefault(answer['answer'], {
                'count': 0,
                'sumtemp': 0,
                'sumtime': 0
            })
            d['count'] += 1
            d['sumtemp'] += answer['temp']
            d['sumtime'] += answer['time']

        for answer, d in answers.items():
            d['avgtemp'] = d.pop('sumtemp') / d['count']
            d['avgtime'] = d.pop('sumtime') / d['count']
        return answers

    def run_forever(self, initial, modified, target):
        self.workspace.resetWithStrings(initial, modified, target)
        while True:
            self.runTrial()
