from collections import defaultdict
from dataclasses import dataclass

from .IndexedItem import IndexedItem


@dataclass
class PkmSpecies(IndexedItem):
    @property
    def is_glitch(self) -> bool:
        return self.index > 0x01B7 or 0x00FB < self.index < 0x0115


pkm_species = defaultdict(
    lambda: PkmSpecies(index=0x01B8, name="??????????"),
    {
        pkm_species.index: pkm_species
        for pkm_species in (
            PkmSpecies(index=0x0000, name="??????????"),
            PkmSpecies(index=0x0001, name="Bulbasaur"),
            PkmSpecies(index=0x0002, name="Ivysaur"),
            PkmSpecies(index=0x0003, name="Venusaur"),
            PkmSpecies(index=0x0004, name="Charmander"),
            PkmSpecies(index=0x0005, name="Charmeleon"),
            PkmSpecies(index=0x0006, name="Charizard"),
            PkmSpecies(index=0x0007, name="Squirtle"),
            PkmSpecies(index=0x0008, name="Wartortle"),
            PkmSpecies(index=0x0009, name="Blastoise"),
            PkmSpecies(index=0x000A, name="Caterpie"),
            PkmSpecies(index=0x000B, name="Metapod"),
            PkmSpecies(index=0x000C, name="Butterfree"),
            PkmSpecies(index=0x000D, name="Weedle"),
            PkmSpecies(index=0x000E, name="Kakuna"),
            PkmSpecies(index=0x000F, name="Beedrill"),
            PkmSpecies(index=0x0010, name="Pidgey"),
            PkmSpecies(index=0x0011, name="Pidgeotto"),
            PkmSpecies(index=0x0012, name="Pidgeot"),
            PkmSpecies(index=0x0013, name="Rattata"),
            PkmSpecies(index=0x0014, name="Raticate"),
            PkmSpecies(index=0x0015, name="Spearow"),
            PkmSpecies(index=0x0016, name="Fearow"),
            PkmSpecies(index=0x0017, name="Ekans"),
            PkmSpecies(index=0x0018, name="Arbok"),
            PkmSpecies(index=0x0019, name="Pikachu"),
            PkmSpecies(index=0x001A, name="Raichu"),
            PkmSpecies(index=0x001B, name="Sandshrew"),
            PkmSpecies(index=0x001C, name="Sandslash"),
            PkmSpecies(index=0x001D, name="Nidoran♀"),
            PkmSpecies(index=0x001E, name="Nidorina"),
            PkmSpecies(index=0x001F, name="Nidoqueen"),
            PkmSpecies(index=0x0020, name="Nidoran♂"),
            PkmSpecies(index=0x0021, name="Nidorino"),
            PkmSpecies(index=0x0022, name="Nidoking"),
            PkmSpecies(index=0x0023, name="Clefairy"),
            PkmSpecies(index=0x0024, name="Clefable"),
            PkmSpecies(index=0x0025, name="Vulpix"),
            PkmSpecies(index=0x0026, name="Ninetales"),
            PkmSpecies(index=0x0027, name="Jigglypuff"),
            PkmSpecies(index=0x0028, name="Wigglytuff"),
            PkmSpecies(index=0x0029, name="Zubat"),
            PkmSpecies(index=0x002A, name="Golbat"),
            PkmSpecies(index=0x002B, name="Oddish"),
            PkmSpecies(index=0x002C, name="Gloom"),
            PkmSpecies(index=0x002D, name="Vileplume"),
            PkmSpecies(index=0x002E, name="Paras"),
            PkmSpecies(index=0x002F, name="Parasect"),
            PkmSpecies(index=0x0030, name="Venonat"),
            PkmSpecies(index=0x0031, name="Venomoth"),
            PkmSpecies(index=0x0032, name="Diglett"),
            PkmSpecies(index=0x0033, name="Dugtrio"),
            PkmSpecies(index=0x0034, name="Meowth"),
            PkmSpecies(index=0x0035, name="Persian"),
            PkmSpecies(index=0x0036, name="Psyduck"),
            PkmSpecies(index=0x0037, name="Golduck"),
            PkmSpecies(index=0x0038, name="Mankey"),
            PkmSpecies(index=0x0039, name="Primeape"),
            PkmSpecies(index=0x003A, name="Growlithe"),
            PkmSpecies(index=0x003B, name="Arcanine"),
            PkmSpecies(index=0x003C, name="Poliwag"),
            PkmSpecies(index=0x003D, name="Poliwhirl"),
            PkmSpecies(index=0x003E, name="Poliwrath"),
            PkmSpecies(index=0x003F, name="Abra"),
            PkmSpecies(index=0x0040, name="Kadabra"),
            PkmSpecies(index=0x0041, name="Alakazam"),
            PkmSpecies(index=0x0042, name="Machop"),
            PkmSpecies(index=0x0043, name="Machoke"),
            PkmSpecies(index=0x0044, name="Machamp"),
            PkmSpecies(index=0x0045, name="Bellsprout"),
            PkmSpecies(index=0x0046, name="Weepinbell"),
            PkmSpecies(index=0x0047, name="Victreebel"),
            PkmSpecies(index=0x0048, name="Tentacool"),
            PkmSpecies(index=0x0049, name="Tentacruel"),
            PkmSpecies(index=0x004A, name="Geodude"),
            PkmSpecies(index=0x004B, name="Graveler"),
            PkmSpecies(index=0x004C, name="Golem"),
            PkmSpecies(index=0x004D, name="Ponyta"),
            PkmSpecies(index=0x004E, name="Rapidash"),
            PkmSpecies(index=0x004F, name="Slowpoke"),
            PkmSpecies(index=0x0050, name="Slowbro"),
            PkmSpecies(index=0x0051, name="Magnemite"),
            PkmSpecies(index=0x0052, name="Magneton"),
            PkmSpecies(index=0x0053, name="Farfetchd"),
            PkmSpecies(index=0x0054, name="Doduo"),
            PkmSpecies(index=0x0055, name="Dodrio"),
            PkmSpecies(index=0x0056, name="Seel"),
            PkmSpecies(index=0x0057, name="Dewgong"),
            PkmSpecies(index=0x0058, name="Grimer"),
            PkmSpecies(index=0x0059, name="Muk"),
            PkmSpecies(index=0x005A, name="Shellder"),
            PkmSpecies(index=0x005B, name="Cloyster"),
            PkmSpecies(index=0x005C, name="Gastly"),
            PkmSpecies(index=0x005D, name="Haunter"),
            PkmSpecies(index=0x005E, name="Gengar"),
            PkmSpecies(index=0x005F, name="Onix"),
            PkmSpecies(index=0x0060, name="Drowzee"),
            PkmSpecies(index=0x0061, name="Hypno"),
            PkmSpecies(index=0x0062, name="Krabby"),
            PkmSpecies(index=0x0063, name="Kingler"),
            PkmSpecies(index=0x0064, name="Voltorb"),
            PkmSpecies(index=0x0065, name="Electrode"),
            PkmSpecies(index=0x0066, name="Exeggcute"),
            PkmSpecies(index=0x0067, name="Exeggutor"),
            PkmSpecies(index=0x0068, name="Cubone"),
            PkmSpecies(index=0x0069, name="Marowak"),
            PkmSpecies(index=0x006A, name="Hitmonlee"),
            PkmSpecies(index=0x006B, name="Hitmonchan"),
            PkmSpecies(index=0x006C, name="Lickitung"),
            PkmSpecies(index=0x006D, name="Koffing"),
            PkmSpecies(index=0x006E, name="Weezing"),
            PkmSpecies(index=0x006F, name="Rhyhorn"),
            PkmSpecies(index=0x0070, name="Rhydon"),
            PkmSpecies(index=0x0071, name="Chansey"),
            PkmSpecies(index=0x0072, name="Tangela"),
            PkmSpecies(index=0x0073, name="Kangaskhan"),
            PkmSpecies(index=0x0074, name="Horsea"),
            PkmSpecies(index=0x0075, name="Seadra"),
            PkmSpecies(index=0x0076, name="Goldeen"),
            PkmSpecies(index=0x0077, name="Seaking"),
            PkmSpecies(index=0x0078, name="Staryu"),
            PkmSpecies(index=0x0079, name="Starmie"),
            PkmSpecies(index=0x007A, name="Mr. Mime"),
            PkmSpecies(index=0x007B, name="Scyther"),
            PkmSpecies(index=0x007C, name="Jynx"),
            PkmSpecies(index=0x007D, name="Electabuzz"),
            PkmSpecies(index=0x007E, name="Magmar"),
            PkmSpecies(index=0x007F, name="Pinsir"),
            PkmSpecies(index=0x0080, name="Tauros"),
            PkmSpecies(index=0x0081, name="Magikarp"),
            PkmSpecies(index=0x0082, name="Gyarados"),
            PkmSpecies(index=0x0083, name="Lapras"),
            PkmSpecies(index=0x0084, name="Ditto"),
            PkmSpecies(index=0x0085, name="Eevee"),
            PkmSpecies(index=0x0086, name="Vaporeon"),
            PkmSpecies(index=0x0087, name="Jolteon"),
            PkmSpecies(index=0x0088, name="Flareon"),
            PkmSpecies(index=0x0089, name="Porygon"),
            PkmSpecies(index=0x008A, name="Omanyte"),
            PkmSpecies(index=0x008B, name="Omastar"),
            PkmSpecies(index=0x008C, name="Kabuto"),
            PkmSpecies(index=0x008D, name="Kabutops"),
            PkmSpecies(index=0x008E, name="Aerodactyl"),
            PkmSpecies(index=0x008F, name="Snorlax"),
            PkmSpecies(index=0x0090, name="Articuno"),
            PkmSpecies(index=0x0091, name="Zapdos"),
            PkmSpecies(index=0x0092, name="Moltres"),
            PkmSpecies(index=0x0093, name="Dratini"),
            PkmSpecies(index=0x0094, name="Dragonair"),
            PkmSpecies(index=0x0095, name="Dragonite"),
            PkmSpecies(index=0x0096, name="Mewtwo"),
            PkmSpecies(index=0x0097, name="Mew"),
            PkmSpecies(index=0x0098, name="Chikorita"),
            PkmSpecies(index=0x0099, name="Bayleef"),
            PkmSpecies(index=0x009A, name="Meganium"),
            PkmSpecies(index=0x009B, name="Cyndaquil"),
            PkmSpecies(index=0x009C, name="Quilava"),
            PkmSpecies(index=0x009D, name="Typhlosion"),
            PkmSpecies(index=0x009E, name="Totodile"),
            PkmSpecies(index=0x009F, name="Croconaw"),
            PkmSpecies(index=0x00A0, name="Feraligatr"),
            PkmSpecies(index=0x00A1, name="Sentret"),
            PkmSpecies(index=0x00A2, name="Furret"),
            PkmSpecies(index=0x00A3, name="Hoothoot"),
            PkmSpecies(index=0x00A4, name="Noctowl"),
            PkmSpecies(index=0x00A5, name="Ledyba"),
            PkmSpecies(index=0x00A6, name="Ledian"),
            PkmSpecies(index=0x00A7, name="Spinarak"),
            PkmSpecies(index=0x00A8, name="Ariados"),
            PkmSpecies(index=0x00A9, name="Crobat"),
            PkmSpecies(index=0x00AA, name="Chinchou"),
            PkmSpecies(index=0x00AB, name="Lanturn"),
            PkmSpecies(index=0x00AC, name="Pichu"),
            PkmSpecies(index=0x00AD, name="Cleffa"),
            PkmSpecies(index=0x00AE, name="Igglybuff"),
            PkmSpecies(index=0x00AF, name="Togepi"),
            PkmSpecies(index=0x00B0, name="Togetic"),
            PkmSpecies(index=0x00B1, name="Natu"),
            PkmSpecies(index=0x00B2, name="Xatu"),
            PkmSpecies(index=0x00B3, name="Mareep"),
            PkmSpecies(index=0x00B4, name="Flaaffy"),
            PkmSpecies(index=0x00B5, name="Ampharos"),
            PkmSpecies(index=0x00B6, name="Bellossom"),
            PkmSpecies(index=0x00B7, name="Marill"),
            PkmSpecies(index=0x00B8, name="Azumarill"),
            PkmSpecies(index=0x00B9, name="Sudowoodo"),
            PkmSpecies(index=0x00BA, name="Politoed"),
            PkmSpecies(index=0x00BB, name="Hoppip"),
            PkmSpecies(index=0x00BC, name="Skiploom"),
            PkmSpecies(index=0x00BD, name="Jumpluff"),
            PkmSpecies(index=0x00BE, name="Aipom"),
            PkmSpecies(index=0x00BF, name="Sunkern"),
            PkmSpecies(index=0x00C0, name="Sunflora"),
            PkmSpecies(index=0x00C1, name="Yanma"),
            PkmSpecies(index=0x00C2, name="Wooper"),
            PkmSpecies(index=0x00C3, name="Quagsire"),
            PkmSpecies(index=0x00C4, name="Espeon"),
            PkmSpecies(index=0x00C5, name="Umbreon"),
            PkmSpecies(index=0x00C6, name="Murkrow"),
            PkmSpecies(index=0x00C7, name="Slowking"),
            PkmSpecies(index=0x00C8, name="Misdreavus"),
            PkmSpecies(index=0x00C9, name="Unown"),
            PkmSpecies(index=0x00CA, name="Wobbuffet"),
            PkmSpecies(index=0x00CB, name="Girafarig"),
            PkmSpecies(index=0x00CC, name="Pineco"),
            PkmSpecies(index=0x00CD, name="Forretress"),
            PkmSpecies(index=0x00CE, name="Dunsparce"),
            PkmSpecies(index=0x00CF, name="Gligar"),
            PkmSpecies(index=0x00D0, name="Steelix"),
            PkmSpecies(index=0x00D1, name="Snubbull"),
            PkmSpecies(index=0x00D2, name="Granbull"),
            PkmSpecies(index=0x00D3, name="Qwilfish"),
            PkmSpecies(index=0x00D4, name="Scizor"),
            PkmSpecies(index=0x00D5, name="Shuckle"),
            PkmSpecies(index=0x00D6, name="Heracross"),
            PkmSpecies(index=0x00D7, name="Sneasel"),
            PkmSpecies(index=0x00D8, name="Teddiursa"),
            PkmSpecies(index=0x00D9, name="Ursaring"),
            PkmSpecies(index=0x00DA, name="Slugma"),
            PkmSpecies(index=0x00DB, name="Magcargo"),
            PkmSpecies(index=0x00DC, name="Swinub"),
            PkmSpecies(index=0x00DD, name="Piloswine"),
            PkmSpecies(index=0x00DE, name="Corsola"),
            PkmSpecies(index=0x00DF, name="Remoraid"),
            PkmSpecies(index=0x00E0, name="Octillery"),
            PkmSpecies(index=0x00E1, name="Delibird"),
            PkmSpecies(index=0x00E2, name="Mantine"),
            PkmSpecies(index=0x00E3, name="Skarmory"),
            PkmSpecies(index=0x00E4, name="Houndour"),
            PkmSpecies(index=0x00E5, name="Houndoom"),
            PkmSpecies(index=0x00E6, name="Kingdra"),
            PkmSpecies(index=0x00E7, name="Phanpy"),
            PkmSpecies(index=0x00E8, name="Donphan"),
            PkmSpecies(index=0x00E9, name="Porygon2"),
            PkmSpecies(index=0x00EA, name="Stantler"),
            PkmSpecies(index=0x00EB, name="Smeargle"),
            PkmSpecies(index=0x00EC, name="Tyrogue"),
            PkmSpecies(index=0x00ED, name="Hitmontop"),
            PkmSpecies(index=0x00EE, name="Smoochum"),
            PkmSpecies(index=0x00EF, name="Elekid"),
            PkmSpecies(index=0x00F0, name="Magby"),
            PkmSpecies(index=0x00F1, name="Miltank"),
            PkmSpecies(index=0x00F2, name="Blissey"),
            PkmSpecies(index=0x00F3, name="Raikou"),
            PkmSpecies(index=0x00F4, name="Entei"),
            PkmSpecies(index=0x00F5, name="Suicune"),
            PkmSpecies(index=0x00F6, name="Larvitar"),
            PkmSpecies(index=0x00F7, name="Pupitar"),
            PkmSpecies(index=0x00F8, name="Tyranitar"),
            PkmSpecies(index=0x00F9, name="Lugia"),
            PkmSpecies(index=0x00FA, name="Ho-Oh"),
            PkmSpecies(index=0x00FB, name="Celebi"),
            PkmSpecies(index=0x00FC, name="?"),
            PkmSpecies(index=0x00FD, name="?"),
            PkmSpecies(index=0x00FE, name="?"),
            PkmSpecies(index=0x00FF, name="?"),
            PkmSpecies(index=0x0100, name="?"),
            PkmSpecies(index=0x0101, name="?"),
            PkmSpecies(index=0x0102, name="?"),
            PkmSpecies(index=0x0103, name="?"),
            PkmSpecies(index=0x0104, name="?"),
            PkmSpecies(index=0x0105, name="?"),
            PkmSpecies(index=0x0106, name="?"),
            PkmSpecies(index=0x0107, name="?"),
            PkmSpecies(index=0x0108, name="?"),
            PkmSpecies(index=0x0109, name="?"),
            PkmSpecies(index=0x010A, name="?"),
            PkmSpecies(index=0x010B, name="?"),
            PkmSpecies(index=0x010C, name="?"),
            PkmSpecies(index=0x010D, name="?"),
            PkmSpecies(index=0x010E, name="?"),
            PkmSpecies(index=0x010F, name="?"),
            PkmSpecies(index=0x0110, name="?"),
            PkmSpecies(index=0x0111, name="?"),
            PkmSpecies(index=0x0112, name="?"),
            PkmSpecies(index=0x0113, name="?"),
            PkmSpecies(index=0x0114, name="?"),
            PkmSpecies(index=0x0115, name="Treecko"),
            PkmSpecies(index=0x0116, name="Grovyle"),
            PkmSpecies(index=0x0117, name="Sceptile"),
            PkmSpecies(index=0x0118, name="Torchic"),
            PkmSpecies(index=0x0119, name="Combusken"),
            PkmSpecies(index=0x011A, name="Blaziken"),
            PkmSpecies(index=0x011B, name="Mudkip"),
            PkmSpecies(index=0x011C, name="Marshtomp"),
            PkmSpecies(index=0x011D, name="Swampert"),
            PkmSpecies(index=0x011E, name="Poochyena"),
            PkmSpecies(index=0x011F, name="Mightyena"),
            PkmSpecies(index=0x0120, name="Zigzagoon"),
            PkmSpecies(index=0x0121, name="Linoone"),
            PkmSpecies(index=0x0122, name="Wurmple"),
            PkmSpecies(index=0x0123, name="Silcoon"),
            PkmSpecies(index=0x0124, name="Beautifly"),
            PkmSpecies(index=0x0125, name="Cascoon"),
            PkmSpecies(index=0x0126, name="Dustox"),
            PkmSpecies(index=0x0127, name="Lotad"),
            PkmSpecies(index=0x0128, name="Lombre"),
            PkmSpecies(index=0x0129, name="Ludicolo"),
            PkmSpecies(index=0x012A, name="Seedot"),
            PkmSpecies(index=0x012B, name="Nuzleaf"),
            PkmSpecies(index=0x012C, name="Shiftry"),
            PkmSpecies(index=0x012D, name="Nincada"),
            PkmSpecies(index=0x012E, name="Ninjask"),
            PkmSpecies(index=0x012F, name="Shedinja"),
            PkmSpecies(index=0x0130, name="Taillow"),
            PkmSpecies(index=0x0131, name="Swellow"),
            PkmSpecies(index=0x0132, name="Shroomish"),
            PkmSpecies(index=0x0133, name="Breloom"),
            PkmSpecies(index=0x0134, name="Spinda"),
            PkmSpecies(index=0x0135, name="Wingull"),
            PkmSpecies(index=0x0136, name="Pelipper"),
            PkmSpecies(index=0x0137, name="Surskit"),
            PkmSpecies(index=0x0138, name="Masquerain"),
            PkmSpecies(index=0x0139, name="Wailmer"),
            PkmSpecies(index=0x013A, name="Wailord"),
            PkmSpecies(index=0x013B, name="Skitty"),
            PkmSpecies(index=0x013C, name="Delcatty"),
            PkmSpecies(index=0x013D, name="Kecleon"),
            PkmSpecies(index=0x013E, name="Baltoy"),
            PkmSpecies(index=0x013F, name="Claydol"),
            PkmSpecies(index=0x0140, name="Nosepass"),
            PkmSpecies(index=0x0141, name="Torkoal"),
            PkmSpecies(index=0x0142, name="Sableye"),
            PkmSpecies(index=0x0143, name="Barboach"),
            PkmSpecies(index=0x0144, name="Whiscash"),
            PkmSpecies(index=0x0145, name="Luvdisc"),
            PkmSpecies(index=0x0146, name="Corphish"),
            PkmSpecies(index=0x0147, name="Crawdaunt"),
            PkmSpecies(index=0x0148, name="Feebas"),
            PkmSpecies(index=0x0149, name="Milotic"),
            PkmSpecies(index=0x014A, name="Carvanha"),
            PkmSpecies(index=0x014B, name="Sharpedo"),
            PkmSpecies(index=0x014C, name="Trapinch"),
            PkmSpecies(index=0x014D, name="Vibrava"),
            PkmSpecies(index=0x014E, name="Flygon"),
            PkmSpecies(index=0x014F, name="Makuhita"),
            PkmSpecies(index=0x0150, name="Hariyama"),
            PkmSpecies(index=0x0151, name="Electrike"),
            PkmSpecies(index=0x0152, name="Manectric"),
            PkmSpecies(index=0x0153, name="Numel"),
            PkmSpecies(index=0x0154, name="Camerupt"),
            PkmSpecies(index=0x0155, name="Spheal"),
            PkmSpecies(index=0x0156, name="Sealeo"),
            PkmSpecies(index=0x0157, name="Walrein"),
            PkmSpecies(index=0x0158, name="Cacnea"),
            PkmSpecies(index=0x0159, name="Cacturne"),
            PkmSpecies(index=0x015A, name="Snorunt"),
            PkmSpecies(index=0x015B, name="Glalie"),
            PkmSpecies(index=0x015C, name="Lunatone"),
            PkmSpecies(index=0x015D, name="Solrock"),
            PkmSpecies(index=0x015E, name="Azurill"),
            PkmSpecies(index=0x015F, name="Spoink"),
            PkmSpecies(index=0x0160, name="Grumpig"),
            PkmSpecies(index=0x0161, name="Plusle"),
            PkmSpecies(index=0x0162, name="Minun"),
            PkmSpecies(index=0x0163, name="Mawile"),
            PkmSpecies(index=0x0164, name="Meditite"),
            PkmSpecies(index=0x0165, name="Medicham"),
            PkmSpecies(index=0x0166, name="Swablu"),
            PkmSpecies(index=0x0167, name="Altaria"),
            PkmSpecies(index=0x0168, name="Wynaut"),
            PkmSpecies(index=0x0169, name="Duskull"),
            PkmSpecies(index=0x016A, name="Dusclops"),
            PkmSpecies(index=0x016B, name="Roselia"),
            PkmSpecies(index=0x016C, name="Slakoth"),
            PkmSpecies(index=0x016D, name="Vigoroth"),
            PkmSpecies(index=0x016E, name="Slaking"),
            PkmSpecies(index=0x016F, name="Gulpin"),
            PkmSpecies(index=0x0170, name="Swalot"),
            PkmSpecies(index=0x0171, name="Tropius"),
            PkmSpecies(index=0x0172, name="Whismur"),
            PkmSpecies(index=0x0173, name="Loudred"),
            PkmSpecies(index=0x0174, name="Exploud"),
            PkmSpecies(index=0x0175, name="Clamperl"),
            PkmSpecies(index=0x0176, name="Huntail"),
            PkmSpecies(index=0x0177, name="Gorebyss"),
            PkmSpecies(index=0x0178, name="Absol"),
            PkmSpecies(index=0x0179, name="Shuppet"),
            PkmSpecies(index=0x017A, name="Banette"),
            PkmSpecies(index=0x017B, name="Seviper"),
            PkmSpecies(index=0x017C, name="Zangoose"),
            PkmSpecies(index=0x017D, name="Relicanth"),
            PkmSpecies(index=0x017E, name="Aron"),
            PkmSpecies(index=0x017F, name="Lairon"),
            PkmSpecies(index=0x0180, name="Aggron"),
            PkmSpecies(index=0x0181, name="Castform"),
            PkmSpecies(index=0x0182, name="Volbeat"),
            PkmSpecies(index=0x0183, name="Illumise"),
            PkmSpecies(index=0x0184, name="Lileep"),
            PkmSpecies(index=0x0185, name="Cradily"),
            PkmSpecies(index=0x0186, name="Anorith"),
            PkmSpecies(index=0x0187, name="Armaldo"),
            PkmSpecies(index=0x0188, name="Ralts"),
            PkmSpecies(index=0x0189, name="Kirlia"),
            PkmSpecies(index=0x018A, name="Gardevoir"),
            PkmSpecies(index=0x018B, name="Bagon"),
            PkmSpecies(index=0x018C, name="Shelgon"),
            PkmSpecies(index=0x018D, name="Salamence"),
            PkmSpecies(index=0x018E, name="Beldum"),
            PkmSpecies(index=0x018F, name="Metang"),
            PkmSpecies(index=0x0190, name="Metagross"),
            PkmSpecies(index=0x0191, name="Regirock"),
            PkmSpecies(index=0x0192, name="Regice"),
            PkmSpecies(index=0x0193, name="Registeel"),
            PkmSpecies(index=0x0194, name="Kyogre"),
            PkmSpecies(index=0x0195, name="Groudon"),
            PkmSpecies(index=0x0196, name="Rayquaza"),
            PkmSpecies(index=0x0197, name="Latias"),
            PkmSpecies(index=0x0198, name="Latios"),
            PkmSpecies(index=0x0199, name="Jirachi"),
            PkmSpecies(index=0x019A, name="Deoxys"),
            PkmSpecies(index=0x019B, name="Chimecho"),
            PkmSpecies(index=0x019C, name="Pokémon Egg"),
            PkmSpecies(index=0x019D, name="Unown"),
            PkmSpecies(index=0x019E, name="Unown"),
            PkmSpecies(index=0x019F, name="Unown"),
            PkmSpecies(index=0x01A0, name="Unown"),
            PkmSpecies(index=0x01A1, name="Unown"),
            PkmSpecies(index=0x01A2, name="Unown"),
            PkmSpecies(index=0x01A3, name="Unown"),
            PkmSpecies(index=0x01A4, name="Unown"),
            PkmSpecies(index=0x01A5, name="Unown"),
            PkmSpecies(index=0x01A6, name="Unown"),
            PkmSpecies(index=0x01A7, name="Unown"),
            PkmSpecies(index=0x01A8, name="Unown"),
            PkmSpecies(index=0x01A9, name="Unown"),
            PkmSpecies(index=0x01AA, name="Unown"),
            PkmSpecies(index=0x01AB, name="Unown"),
            PkmSpecies(index=0x01AC, name="Unown"),
            PkmSpecies(index=0x01AD, name="Unown"),
            PkmSpecies(index=0x01AE, name="Unown"),
            PkmSpecies(index=0x01AF, name="Unown"),
            PkmSpecies(index=0x01B0, name="Unown"),
            PkmSpecies(index=0x01B1, name="Unown"),
            PkmSpecies(index=0x01B2, name="Unown"),
            PkmSpecies(index=0x01B3, name="Unown"),
            PkmSpecies(index=0x01B4, name="Unown"),
            PkmSpecies(index=0x01B5, name="Unown"),
            PkmSpecies(index=0x01B6, name="Unown"),
            PkmSpecies(index=0x01B7, name="Unown"),
        )
    },
)
