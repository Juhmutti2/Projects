import csv
import os


def ohjeet():
    print(" ")
    print("Ohjelma laskee sijoitustuotot käyttäjältä kysyttävän syötteen mukaan. 30.000 euron raja huomioidaan automaattisesti.") 
    print("Vaihtoehdossa kolme huomioidaan, että 15% osingoista tulee verovapaasti, jolloin tavanomainen pääomavero lasketaan 85%:lle.")
    print("Tulokset voi halutessaan tulostaa ohjelman konsoliin tai tallentaa .csv tiedostoon samaan kansioon, jossa ohjelma sijaitsee. ")
    print("Ohjelma kysyy käyttäjältä tulostuksesta ja tallennuksesta automaattisesti. ")    
    print("Ohjelman nykyinen versio ei huomioi hankintameno-olettamaa, eikä sillä voi laskea osinkoja listaamattomista yhtiöistä.")
    print("Osinkojen sijoittamista uudelleen saman vuoden aikana (esim. kvartaaliosingot) ei nykyisessä versiossa huomioida.")
    print("Versio 1.0")
    print(" ")
    print("1: Ohjeet")
    print("2: Laskee sijoitustuotot verokannoilla 30% ja 34%")
    print("3: Laskee sijoitustuotot osinkoverokannalla 25,5% ja 28,9%")
    print("4: Lopettaa ohjelman.")
    print(" ")

def laske_tuotot(sijoitus):
    paaoma = []
    brutto =[]
    netto = []
    verot = []
    aloitus_summa = int(input('Syötä aloitussumma: '))
    vuodet = int(input('Syötä sijoitusvuodet: '))
    tuottoprosentti = float(input('Syötä tuottoprosentti. Käytä desimaaliin pistettä ".":'))
    tuotto = aloitus_summa

    if sijoitus:
        perusvero = 0.3
        perusveron_maksimi = 9000
        korotettu_vero = 0.34
    else:
        perusvero = 0.255
        perusveron_maksimi = 7650
        korotettu_vero = 0.289

    for i in range(vuodet):
        tuotto = tuotto * ((tuottoprosentti / 100) + 1)
        brutto_summa = tuotto - aloitus_summa  
        paaoma.append(round(tuotto, 2))
        
        if brutto_summa <= 30000:
            vero = brutto_summa * perusvero
        else:
            vero = perusveron_maksimi + ((brutto_summa - 30000) * korotettu_vero)
        brutto.append(round(brutto_summa, 2))
        netto_summa = brutto_summa - vero
        netto.append(round(netto_summa, 2))
        verot.append(round(vero, 2))
        

    return paaoma, brutto, netto, verot, aloitus_summa, vuodet, tuottoprosentti


def tulosta_tulokset(paaoma, brutto, netto, verot, vuodet):
    print('Summat euroja')
    for i in range(vuodet):
        print(f"Vuoden {i + 1} jälkeen Pääoma: {paaoma[i]}, Brutto:{brutto[i]}, Netto: {netto[i]}, Verot: {verot[i]}")
        print()

def tallenna_tulokset(paaoma, brutto, netto, verot, vuodet, aloitus_summa, tuottoprosentti):
    base_filename = 'Sijoitustulokset'
    file_counter = 1
    filename = f'{base_filename}.csv'

    # Ohjelman nykyinen sijaintikansio
    current_directory = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_directory, filename)

    while os.path.isfile(filepath):
        filename = f'{base_filename}{file_counter}.csv'
        filepath = os.path.join(current_directory, filename)
        file_counter += 1

    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        
        writer.writerow([f'Aloitussumma: {aloitus_summa} euroa'])
        writer.writerow([f'Sijoitusvuosia: {vuodet}'])
        writer.writerow([f'Tuottoprosentti: {tuottoprosentti}'])
        writer.writerow(['Alla olevat summat euroja'])
        writer.writerow([]) 
        
        
        for i in range(vuodet):
            writer.writerow([f"Vuoden {i + 1} jälkeen Pääoma: {paaoma[i]}, Brutto: {brutto[i]}, Netto: {netto[i]}, Verot: {verot[i]}"])
            writer.writerow([])

    print(f'Tiedot tallennettu tiedostoon {filepath}')

def main():
    while True:
        valinta = input("Syötä valinta 1 = Ohjeet / 2 = Laske pääomavero / 3 = Laske osinkovero / 4 = Lopeta: ").strip()

        if valinta == '1':
            ohjeet()
        elif valinta == '2':
            sijoitus = True
            paaoma, brutto, netto, verot, aloitus_summa, vuodet, tuottoprosentti = laske_tuotot(sijoitus)
            print_results = input("Haluatko tulostaa tiedot, K/E? ").strip().upper()
            if print_results == 'K':
                tulosta_tulokset(paaoma, brutto, netto, verot, vuodet)
            save_results = input("Haluatko että tulokset tallennetaan, K/E? ").strip().upper()
            if save_results == 'K':
                tallenna_tulokset(paaoma, brutto, netto, verot, vuodet, aloitus_summa, tuottoprosentti)
            else:
                print("Tuloksia ei tallennettu.")
        elif valinta == '3':
            sijoitus=False
            paaoma, brutto, netto, verot, aloitus_summa, vuodet, tuottoprosentti = laske_tuotot(sijoitus)
            print_results = input("Haluatko tulostaa tiedot, K/E? ").strip().upper()
            if print_results == 'K':
                tulosta_tulokset(paaoma, brutto, netto, verot, vuodet)
            save_results = input("Haluatko että tulokset tallennetaan, K/E? ").strip().upper()
            if save_results == 'K':
                tallenna_tulokset(paaoma, brutto, netto, verot, vuodet, aloitus_summa, tuottoprosentti)
            else:
                print("Tuloksia ei tallennettu.")
        elif valinta == '4':
            print("Ohjelma lopetetaan.")
            break
        else:
            print("Virheellinen valinta, yritä uudelleen.")

if __name__ == "__main__":
    main()
