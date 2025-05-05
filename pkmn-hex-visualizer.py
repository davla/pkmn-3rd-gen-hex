import sys
from dataclasses import dataclass

from rich.console import Console

Console.write = lambda self, *args: self.print(*args, end=" ")
console = Console()


def main(args=None):
    file_name = args[1]

    with open(file_name, "rb") as file:
        bytes = file.read()

    substructures = Substructures.from_bytes(bytes)
    print_overall(bytes, substructures.order)
    console.print("")

    print_growth(substructures.growth)
    console.print("")

    print_attacks(substructures.attacks)
    console.print("")

    print_evs(substructures.evs)
    console.print("")

    print_misc(substructures.misc)
    console.print("")


@dataclass
class Substructures:
    order: str
    growth: bytes
    attacks: bytes
    evs: bytes
    misc: bytes

    ORDER = {
        0: "GAEM",
        1: "GAME",
        2: "GEAM",
        3: "GEMA",
        4: "GMAE",
        5: "GMEA",
        6: "AGEM",
        7: "AGME",
        8: "AEGM",
        9: "AEMG",
        10: "AMGE",
        11: "AMEG",
        12: "EGAM",
        13: "EGMA",
        14: "EAGM",
        15: "EAMG",
        16: "EMGA",
        17: "EMAG",
        18: "MGAE",
        19: "MGEA",
        20: "MAGE",
        21: "MAEG",
        22: "MEGA",
        23: "MEAG",
    }

    @classmethod
    def from_bytes(cls, bytes):
        order = cls.ORDER[bytes[0] % 24]
        return cls(
            order,
            growth=cls.get_substructure_at(bytes, order.index("G")),
            attacks=cls.get_substructure_at(bytes, order.index("A")),
            evs=cls.get_substructure_at(bytes, order.index("E")),
            misc=cls.get_substructure_at(bytes, order.index("M")),
        )

    @classmethod
    def get_substructure_at(cls, bytes, index):
        start_index = 32 + index * 12
        return bytes[start_index : start_index + 12]


def print_overall(bytes, substructure_order):
    PID_COLOR = "red"
    TID_COLOR = "cyan"
    SID_COLOR = "yellow"
    BAD_EGG_COLOR = "green"

    misc_flags = format_bits(bytes[19])

    console.rule("Overall data")
    console.write(f"[{PID_COLOR}]{format_bytes(bytes[0:4])}[/]")
    console.write(f"[{TID_COLOR}]{format_bytes(bytes[4:6])}[/]")
    console.print(f"[{SID_COLOR}]{format_bytes(bytes[6:8])}[/]")
    console.print(format_bytes(bytes[8:16]))
    console.print(format_bytes(bytes[16:19]))
    console.print(misc_flags[1:], end="")
    console.print(f"[{BAD_EGG_COLOR}]{misc_flags[0]}[/]")

    console.print(f"Substructure order: {substructure_order}")

    console.print("")
    print_legend_line("PID", PID_COLOR)
    print_legend_line("TID", TID_COLOR)
    print_legend_line("SID", SID_COLOR)
    print_legend_line("Bad egg", BAD_EGG_COLOR)


def print_growth(bytes):
    SPECIES_COLOR = "red"
    HELD_ITEM_COLOR = "cyan"
    EXP_COLOR = "yellow"
    PP_1_COLOR = "green"
    PP_2_COLOR = "orange1"
    PP_3_COLOR = "purple"
    PP_4_COLOR = "yellow2"
    FRIENDSHIP_COLOR = "green4"

    console.rule("Growth")
    console.write(f"[{SPECIES_COLOR}]{format_bytes(bytes[0:2])}[/]")
    console.print(f"[{HELD_ITEM_COLOR}]{format_bytes(bytes[2:4])}[/]")
    console.print(f"[{EXP_COLOR}]{format_bytes(bytes[4:8])}[/]")

    pps = format_bits(bytes[8])
    console.write(f"[{PP_1_COLOR}]{pps[0:2]}[/]")
    console.write(f"[{PP_2_COLOR}]{pps[2:4]}[/]")
    console.write(f"[{PP_3_COLOR}]{pps[4:6]}[/]")
    console.print(f"[{PP_4_COLOR}]{pps[6:8]}[/]")

    console.write(f"[{FRIENDSHIP_COLOR}]{format_bytes([bytes[9]])}[/]")
    console.print(format_bytes(bytes[10:]))

    console.print("")
    print_legend_line("Species", SPECIES_COLOR)
    print_legend_line("Held item", HELD_ITEM_COLOR)
    print_legend_line("Experience", EXP_COLOR)
    print_legend_line("PP 1", PP_1_COLOR)
    print_legend_line("PP 2", PP_2_COLOR)
    print_legend_line("PP 3", PP_3_COLOR)
    print_legend_line("PP 4", PP_4_COLOR)
    print_legend_line("Friendship", FRIENDSHIP_COLOR)


def print_attacks(bytes):
    MOVE_1_COLOR = "green"
    MOVE_2_COLOR = "red"
    MOVE_3_COLOR = "cyan"
    MOVE_4_COLOR = "purple"

    PP_1_COLOR = "dark_goldenrod"
    PP_2_COLOR = "green4"
    PP_3_COLOR = "yellow"
    PP_4_COLOR = "deep_sky_blue1"

    console.rule("Attacks")
    console.write(f"[{MOVE_1_COLOR}]{format_bytes(bytes[0:2])}[/]")
    console.write(f"[{MOVE_2_COLOR}]{format_bytes(bytes[2:4])}[/]")
    console.write(f"[{MOVE_3_COLOR}]{format_bytes(bytes[4:6])}[/]")
    console.print(f"[{MOVE_4_COLOR}]{format_bytes(bytes[6:8])}[/]")

    console.write(f"[{PP_1_COLOR}]{format_bytes([bytes[8]])}[/]")
    console.write(f"[{PP_2_COLOR}]{format_bytes([bytes[9]])}[/]")
    console.write(f"[{PP_3_COLOR}]{format_bytes([bytes[10]])}[/]")
    console.print(f"[{PP_4_COLOR}]{format_bytes([bytes[11]])}[/]")

    console.print("")
    print_legend_line("Move 1", MOVE_1_COLOR)
    print_legend_line("Move 2", MOVE_2_COLOR)
    print_legend_line("Move 3", MOVE_3_COLOR)
    print_legend_line("Move 4", MOVE_4_COLOR)
    print_legend_line("PP 1", PP_1_COLOR)
    print_legend_line("PP 2", PP_2_COLOR)
    print_legend_line("PP 3", PP_3_COLOR)
    print_legend_line("PP 4", PP_4_COLOR)


def print_evs(bytes):
    HP_COLOR = "salmon1"
    ATK_COLOR = "yellow2"
    DEF_COLOR = "dark_red"
    SPE_COLOR = "sea_green2"
    SPATK_COLOR = "magenta2"
    SPDEF_COLOR = "pale_turquoise1"

    console.rule("Evs")
    console.write(f"[{HP_COLOR}]{format_bytes([bytes[0]])}[/]")
    console.write(f"[{ATK_COLOR}]{format_bytes([bytes[1]])}[/]")
    console.write(f"[{DEF_COLOR}]{format_bytes([bytes[2]])}[/]")
    console.write(f"[{SPE_COLOR}]{format_bytes([bytes[3]])}[/]")
    console.write(f"[{SPATK_COLOR}]{format_bytes([bytes[4]])}[/]")
    console.print(f"[{SPDEF_COLOR}]{format_bytes([bytes[5]])}[/]")

    console.print(format_bytes(bytes[5:]))

    console.print("")
    print_legend_line("HP EV", HP_COLOR)
    print_legend_line("Attack EV", ATK_COLOR)
    print_legend_line("Defense EV", DEF_COLOR)
    print_legend_line("Speed EV", SPE_COLOR)
    print_legend_line("Special Attack EV", SPATK_COLOR)
    print_legend_line("Special Defense EV", SPDEF_COLOR)


def print_misc(bytes):
    PKRS_STRAIN_COLOR = "turquoise4"
    PKRS_DAYS_COLOR = "thistle1"
    MET_LOCATION_COLOR = "gold3"

    OT_GENDER_COLOR = "pale_green3"
    BALL_COLOR = "slate_blue1"
    GAME_COLOR = "red"
    LEVEL_COLOR = "blue"

    HP_COLOR = "salmon1"
    ATK_COLOR = "yellow2"
    DEF_COLOR = "dark_red"
    SPE_COLOR = "sea_green2"
    SPATK_COLOR = "magenta2"
    SPDEF_COLOR = "pale_turquoise1"

    EGG_COLOR = "orchid"
    ABILITY_COLOR = "yellow"

    console.rule("Misc")

    pkrs = format_bits(bytes[0])
    console.write(f"[{PKRS_STRAIN_COLOR}]{pkrs[4:8]}[/]")
    console.print(f"[{PKRS_DAYS_COLOR}]{pkrs[0:4]}[/]")

    console.print(f"[{MET_LOCATION_COLOR}]{format_bytes([bytes[1]])}[/]")

    origins = "".join(map(format_bits, bytes[2:4]))
    console.print(
        f"[{OT_GENDER_COLOR}]{origins[15]}[/][{BALL_COLOR}]{origins[11:15]}[/][{GAME_COLOR}]{origins[7:11]}[/][{LEVEL_COLOR}]{origins[0:7]}[/]"
    )

    iv_egg_ability = "".join(map(format_bits, bytes[4:8]))
    console.print(
        f"[{DEF_COLOR}]{iv_egg_ability[10:15]}[/][{ATK_COLOR}]{iv_egg_ability[5:10]}[/][{HP_COLOR}]{iv_egg_ability[0:5]}[/]"
    )
    console.print(
        f"[{SPDEF_COLOR}]{iv_egg_ability[25:30]}[/][{SPATK_COLOR}]{iv_egg_ability[20:25]}[/][{SPE_COLOR}]{iv_egg_ability[15:20]}[/]"
    )
    console.print(
        f"[{ABILITY_COLOR}]{iv_egg_ability[31]}[/][{EGG_COLOR}]{iv_egg_ability[30]}[/]"
    )

    console.print(format_bytes(bytes[8:12]))

    console.print("")
    print_legend_line("Pkrs strain", PKRS_STRAIN_COLOR)
    print_legend_line("Pkrs days", PKRS_DAYS_COLOR)
    print_legend_line("Met location", MET_LOCATION_COLOR)
    print_legend_line("OT gender", OT_GENDER_COLOR)
    print_legend_line("Ball", BALL_COLOR)
    print_legend_line("Game of origin", GAME_COLOR)
    print_legend_line("Level met", LEVEL_COLOR)
    print_legend_line("HP IV", HP_COLOR)
    print_legend_line("Attack IV", ATK_COLOR)
    print_legend_line("Defense IV", DEF_COLOR)
    print_legend_line("Speed IV", SPE_COLOR)
    print_legend_line("Special Attack IV", SPATK_COLOR)
    print_legend_line("Special Defense IV", SPDEF_COLOR)
    print_legend_line("Egg", EGG_COLOR)
    print_legend_line("Ability", ABILITY_COLOR)


def format_bytes(bytes):
    return " ".join(f"{b:02X}" for b in bytes)


def format_bits(byte):
    return f"{byte:08b}"[::-1]


def print_legend_line(label, color):
    console.print(f"[underline]{label}[/]: [{color}]■■■■[/]")


if __name__ == "__main__":
    main(sys.argv)
