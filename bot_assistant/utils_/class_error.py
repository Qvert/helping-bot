class IntNotText(ValueError):
    pass


class UncorrectedInputCity(Exception):
    pass


class NoTimeUser(IntNotText):
    pass


class DontWritePlan(UncorrectedInputCity):
    pass