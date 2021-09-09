from functools import reduce

class UtilityFunctions:

    @staticmethod
    def powerset(s):
        ps = lambda s: reduce(lambda P, x: P + [subset | {x} for subset in P], s, [set()])
        return ps(s)