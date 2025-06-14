from typing import IO

from rich.align import Align
from rich.columns import Columns
from rich.console import Console, RenderableType
from rich.panel import Panel
from rich.table import Table

from ..data import IndexedItem
from .bytes_handling import NumberByteSize, format_bytes, format_hex
from .Pkm import PcPkm


def pkm(pkm: PcPkm, output: IO[str]) -> None:
    overall = box(
        "Overall information",
        col(
            label("Personality value"),
            format_hex(pkm.personality_value, byte_size=4),
        ),
        col(
            label("Original trainer ID"),
            format_hex(pkm.original_trainer_id, byte_size=4),
        ),
        col(label("Substructure order"), pkm.substructure_order.value.upper()),
        col(
            label("Substructure encryption key"),
            format_hex(pkm.substructure_encryption_key, byte_size=4),
        ),
        col(label("Nickname"), format_bytes(pkm.nickname)),
        col(label("Language"), format_hex(pkm.language, byte_size=1)),
        col(
            label("Bad egg?"),
            "[red bold]True[/]" if pkm.is_bad_egg else "[green bold]False[/]",
        ),
        col(label("Original trainer name"), format_bytes(pkm.original_trainer_name)),
        col(label("Markings"), format_hex(pkm.markings, byte_size=1)),
        col(label("Checksum"), format_hex(pkm.checksum, byte_size=4)),
    )

    growth = box(
        "Growth",
        col(label("Species"), print_indexed_item(pkm.growth.species, byte_size=2)),
        col(label("Held item"), print_indexed_item(pkm.growth.held_item, byte_size=2)),
        col(label("Experience"), format_hex(pkm.growth.experience, byte_size=4)),
        col(
            label("PP bonuses"),
            f"{" - ".join(map(str, pkm.growth.pp_ups))} ({format_hex(pkm.growth.pp_ups_byte, byte_size=1)})",
        ),
        col(label("Friendship"), format_hex(pkm.growth.friendship, byte_size=1)),
    )

    attacks = box(
        "Attacks",
        col(label("Move 1"), print_indexed_item(pkm.attacks.move1, byte_size=2)),
        col(label("Move 2"), print_indexed_item(pkm.attacks.move2, byte_size=2)),
        col(label("Move 3"), print_indexed_item(pkm.attacks.move3, byte_size=2)),
        col(label("Move 4"), print_indexed_item(pkm.attacks.move4, byte_size=2)),
        col(label("PP 1"), format_hex(pkm.attacks.pp1, byte_size=1)),
        col(label("PP 2"), format_hex(pkm.attacks.pp2, byte_size=1)),
        col(label("PP 3"), format_hex(pkm.attacks.pp3, byte_size=1)),
        col(label("PP 4"), format_hex(pkm.attacks.pp4, byte_size=1)),
    )

    evs_and_conditions = box(
        "Evs and conditions",
        col(label("HP EVs"), format_hex(pkm.evs_and_conditions.hp_evs, byte_size=1)),
        col(
            label("Attack EVs"),
            format_hex(pkm.evs_and_conditions.atk_evs, byte_size=1),
        ),
        col(
            label("Defense EVs"),
            format_hex(pkm.evs_and_conditions.def_evs, byte_size=1),
        ),
        col(
            label("Speed EVs"),
            format_hex(pkm.evs_and_conditions.speed_evs, byte_size=1),
        ),
        col(
            label("Special Attack EVs"),
            format_hex(pkm.evs_and_conditions.sp_atk_evs, byte_size=1),
        ),
        col(
            label("Special Defense EVs"),
            format_hex(pkm.evs_and_conditions.sp_def_evs, byte_size=1),
        ),
        col(
            label("Coolness"),
            format_hex(pkm.evs_and_conditions.coolness, byte_size=1),
        ),
        col(
            label("Beauty"),
            format_hex(pkm.evs_and_conditions.beauty, byte_size=1),
        ),
        col(
            label("Cuteness"),
            format_hex(pkm.evs_and_conditions.cuteness, byte_size=1),
        ),
        col(
            label("Smartness"),
            format_hex(pkm.evs_and_conditions.smartness, byte_size=1),
        ),
        col(
            label("Thoughness"),
            format_hex(pkm.evs_and_conditions.toughness, byte_size=1),
        ),
        col(
            label("Feel"),
            format_hex(pkm.evs_and_conditions.feel, byte_size=1),
        ),
    )

    pkrs = box(
        "Pokérus",
        col(
            row(
                col(
                    label("Days left"),
                    format_hex(pkm.misc.prks_days_left, byte_size=1),
                ),
                col(
                    label("Strain"),
                    format_hex(pkm.misc.pkrs_strain, byte_size=1),
                ),
                wrapping=False,
            ),
            Align(format_hex(pkm.misc.pkrs_byte, byte_size=1), align="center"),
            gap=1,
        ),
    )
    origins = box(
        "Origins",
        col(
            row(
                col(label("Original trainer gender"), pkm.misc.original_trainer_gender),
                col(
                    label("Caught Poké Ball"),
                    format_hex(pkm.misc.caught_poke_ball, byte_size=1),
                ),
                col(
                    label("Game of origin"),
                    format_hex(pkm.misc.game_of_origin, byte_size=1),
                ),
                col(label("Level met"), format_hex(pkm.misc.level_met, byte_size=1)),
            ),
            Align(format_hex(pkm.misc.origin, byte_size=2), align="center"),
            gap=1,
        ),
    )
    ivs_egg_ability_panel = box(
        "IVs, egg and ability",
        col(
            row(
                col(label("HP IVs"), format_hex(pkm.misc.hp_ivs, byte_size=1)),
                col(label("Attack IVs"), format_hex(pkm.misc.atk_ivs, byte_size=1)),
                col(label("Defense IVs"), format_hex(pkm.misc.def_ivs, byte_size=1)),
                col(label("Speed IVs"), format_hex(pkm.misc.speed_ivs, byte_size=1)),
                col(
                    label("Special Attack IVs"),
                    format_hex(pkm.misc.sp_atk_ivs, byte_size=1),
                ),
                col(
                    label("Special Defense IVs"),
                    format_hex(pkm.misc.sp_def_ivs, byte_size=1),
                ),
                col(label("Is egg?"), str(pkm.misc.is_egg)),
                col(label("Ability"), str(pkm.misc.ability)),
            ),
            Align(format_hex(pkm.misc.ivs_egg_ability, byte_size=4), align="center"),
            gap=1,
        ),
    )

    misc = box(
        "Misc",
        col(
            row(
                pkrs,
                col(
                    label("Met location"),
                    print_indexed_item(pkm.misc.met_location, byte_size=1),
                ),
                origins,
                wrapping=False,
            ),
            ivs_egg_ability_panel,
        ),
    )

    layout = Table.grid(padding=(1, 1))
    layout.add_row(overall, growth)
    layout.add_row(attacks, evs_and_conditions)

    console = Console(file=output)
    console.print(layout, misc)


def print_indexed_item(item: IndexedItem, *, byte_size: NumberByteSize) -> str:
    return f"{'[red bold]GLITCH[/] ' if item.is_glitch else ''}{item.name} ({format_hex(item.index, byte_size=byte_size)})"


def box(title: str, *items: RenderableType) -> RenderableType:
    renderable = items[0] if len(items) == 1 else row(*items)
    return Panel(renderable=renderable, title=title, expand=False)


def col(*items: RenderableType, gap: int = 0) -> RenderableType:
    column = Table.grid(padding=(gap, 0))
    for item in items:
        column.add_row(item)
    return column


def row(*items: RenderableType, gap: int = 3, wrapping: bool = True) -> RenderableType:
    padding = (1, gap)
    if wrapping:
        return Columns(items, padding=padding)
    row = Table.grid(padding=padding)
    row.add_row(*items)
    return row


def label(text: str) -> str:
    return f"[bold]{text}[/]"
