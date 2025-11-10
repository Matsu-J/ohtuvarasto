from varasto import Varasto

def lisaa_tavarat(mehua, olutta):
    print("Mehu setterit:")
    print("Lisätään 50.7")
    mehua.lisaa_varastoon(50.7)

    print("Olut setterit:")
    print("Lisätään 4.7")
    olutta.lisaa_varastoon(50.7)


def ota_tavaraa(mehua, olutta):
    print(f"Mehuvarasto: {mehua}")
    print("Otetaan 3.14")
    mehua.ota_varastosta(3.14)
    print(f"Mehuvarasto: {mehua}")

    print(f"Olutvarasto: {olutta}")
    print("Otetaan 3.14")
    olutta.ota_varastosta(1.11)
    print(f"Olutvarasto: {olutta}")

def hae_varastot(mehua, olutta):
    print("Olut getterit:")
    print(f"saldo = {olutta.saldo}")
    print(f"tilavuus = {olutta.tilavuus}")
    print(f"paljonko_mahtuu = {olutta.paljonko_mahtuu()}")
    print("Mehu getterit:")
    print(f"saldo = {mehua.saldo}")
    print(f"tilavuus = {mehua.tilavuus}")
    print(f"paljonko_mahtuu = {mehua.paljonko_mahtuu()}")

def virheellinen_varasto():
    print("Virhetilanteita:")
    print("Varasto(-100.0);")
    huono = Varasto(-100.0)
    print(huono)

    print("Varasto(100.0, -50.7)")
    huono = Varasto(100.0, -50.7)
    print(huono)

def virheellinen_ottaminen(mehua, olutta):
    print(f"Olutvarasto: {olutta}")
    print("olutta.ota_varastosta(1000.0)")
    saatiin = olutta.ota_varastosta(1000.0)
    print(f"saatiin {saatiin}\nOlutvarasto: {olutta}")

    print(f"Mehuvarasto: {mehua}")
    print("mehua.otaVarastosta(-32.9)")
    saatiin = mehua.ota_varastosta(-32.9)
    print(f"saatiin {saatiin}\nMehuvarasto: {mehua}")

def virheellinen_lisaaminen(mehua, olutta):
    print(f"Olutvarasto: {olutta}")
    print("olutta.lisaa_varastoon(1000.0)")
    olutta.lisaa_varastoon(1000.0)
    print(f"Olutvarasto: {olutta}")

    print(f"Mehuvarasto: {mehua}")
    print("mehua.lisaa_varastoon(-666.0)")
    mehua.lisaa_varastoon(-666.0)
    print(f"Mehuvarasto: {mehua}")

def main():
    mehua = Varasto(100.0)
    olutta = Varasto(100.0, 20.2)

    print(f"Luonnin jälkeen:\nMehuvarasto: {mehua}\nOlutvarasto: {olutta}")

    lisaa_tavarat(mehua, olutta)
    ota_tavaraa(mehua, olutta)
    hae_varastot(mehua, olutta)
    virheellinen_varasto()
    virheellinen_lisaaminen(mehua, olutta)
    virheellinen_ottaminen(mehua, olutta)


if __name__ == "__main__":
    main()
