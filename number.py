from typing import Dict, Optional

MAXIMUM_GETAL_OM_TE_LATEN_ZIEN = 50
MINIMUM_GETAL_VOOR_OPSLAAN = -1000
MAXIMUM_GETAL_VOOR_OPSLAAN = 1000
MAXIMUM_AANTAL_VIEREN = 5


FORMULES: Dict[int, str] = {}
AANTAL_VIEREN: Dict[int, int] = {}
NIEUWE_FORMULES: Dict[int, str] = {4: "4", 44: "44", 444: "444"}
NIEUWE_AANTAL_VIEREN: Dict[int, int] = {4: 1, 44: 2, 444: 3}


def probeer_plus(getal_1: int, getal_2: int) -> None:
    probeer_getal_toevoegen(getal_1, "+", getal_2, getal_1 + getal_2)


def probeer_min(getal_1: int, getal_2: int) -> None:
    probeer_getal_toevoegen(getal_1, "-", getal_2, getal_1 - getal_2)


def probeer_keer(getal_1: int, getal_2: int) -> None:
    probeer_getal_toevoegen(getal_1, "*", getal_2, getal_1 * getal_2)


def probeer_delen(getal_1: int, getal_2: int) -> None:
    if abs(getal_2) < 1e-9:
        return
    probeer_getal_toevoegen(getal_1, "/", getal_2, getal_1 / getal_2)


def probeer_getal_toevoegen(getal_1, operatie, getal_2, nieuw_getal) -> None:
    if not is_geldig_getal(nieuw_getal):
        return
    heel_getal = probeer_heel_getal_te_maken(nieuw_getal)
    if heel_getal is None:
        return
    nieuw_aantal_vieren = AANTAL_VIEREN[getal_1] + AANTAL_VIEREN[getal_2]
    if nieuw_aantal_vieren >= oud_aantal_vieren(heel_getal):
        return
    formule = f"({FORMULES[getal_1]} {operatie} {FORMULES[getal_2]})"
    # formule = f"({getal_1} {operatie} {getal_2})"
    NIEUWE_FORMULES[heel_getal] = formule
    NIEUWE_AANTAL_VIEREN[heel_getal] = nieuw_aantal_vieren


def oud_aantal_vieren(getal: int) -> int:
    aantal_vieren = NIEUWE_AANTAL_VIEREN.get(getal)
    if aantal_vieren is None:
        aantal_vieren = AANTAL_VIEREN.get(getal)
    if aantal_vieren is None:
        aantal_vieren = MAXIMUM_AANTAL_VIEREN + 1
    return aantal_vieren


def is_geldig_getal(getal: float) -> bool:
    return MINIMUM_GETAL_VOOR_OPSLAAN <= getal <= MAXIMUM_GETAL_VOOR_OPSLAAN


def probeer_heel_getal_te_maken(getal: float) -> Optional[int]:
    heel_getal = int(getal)
    return None if abs(heel_getal - getal) > 1e-9 else heel_getal


def vind_alle_nieuwe_getallen(nieuwe_getal: int) -> None:
    for getal in FORMULES:
        probeer_plus(nieuwe_getal, getal)
        probeer_min(nieuwe_getal, getal)
        probeer_min(getal, nieuwe_getal)
        probeer_keer(nieuwe_getal, getal)
        probeer_delen(nieuwe_getal, getal)
        probeer_delen(getal, nieuwe_getal)


def haal_nieuw_getal_op() -> int:
    minimum_aantal_vieren = min(NIEUWE_AANTAL_VIEREN.values())
    for getal, aantal_vieren in NIEUWE_AANTAL_VIEREN.items():
        if aantal_vieren == minimum_aantal_vieren:
            return getal
    raise Exception("This should not be possible!")


def main() -> None:
    while NIEUWE_FORMULES:
        nieuwe_getal = haal_nieuw_getal_op()
        FORMULES[nieuwe_getal] = NIEUWE_FORMULES.pop(nieuwe_getal)
        AANTAL_VIEREN[nieuwe_getal] = NIEUWE_AANTAL_VIEREN.pop(nieuwe_getal)
        vind_alle_nieuwe_getallen(nieuwe_getal)
    print_formules()


def print_formules(nieuw=False) -> None:
    formules = NIEUWE_FORMULES if nieuw else FORMULES
    aantal_vieren = NIEUWE_AANTAL_VIEREN if nieuw else AANTAL_VIEREN
    for getal in range(1, MAXIMUM_GETAL_OM_TE_LATEN_ZIEN + 1):
        deze_formule = formules.get(getal)
        if deze_formule is None:
            deze_formule = "X"
            dit_aantal_vieren = MAXIMUM_AANTAL_VIEREN
        else:
            dit_aantal_vieren = aantal_vieren[getal]
        vieren = "vieren" if dit_aantal_vieren > 1 else "vier"
        print(f"{getal:3} = {deze_formule:40} ({dit_aantal_vieren} {vieren})")


if __name__ == "__main__":
    main()
