from basepokemon import BasePokemon, BaseMove, Type

class Pokemon(BasePokemon):
    def __init__(self):
        BasePokemon.__init__(self)
        # Has to sum to 100
        self.spend_hp(0)
        self.spend_attack(99)
        self.spend_defence(1)
        self.add_move(Shoot())

        self.set_type(Type.EARTH)

    def get_name(self):
        return "Earthander"

    def choose_move(self, enemy):
        return self.get_move_by_name("Shoot")

class Shoot(BaseMove):
    def __init__(self):
        BaseMove.__init__(self)
        self.choose_uses(5)
        self.set_type(Type.EARTH)

    def get_name(self):
        return "Shoot"
