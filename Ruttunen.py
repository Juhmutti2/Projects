import pygame
import random
import os

pygame.init()

nayton_leveys, nayton_korkeus = 1200, 600
pistealue_leveys = 200
pelialue_leveys = nayton_leveys - pistealue_leveys
pelialue_korkeus = nayton_korkeus
naytto = pygame.display.set_mode((nayton_leveys, nayton_korkeus))
pygame.display.set_caption("Ruttunen Pelastaa")
kello = pygame.time.Clock()

MUSTA = (0, 0, 0)
VALKOINEN = (255, 255, 255)
PUNAINEN = (255, 0, 0)
KELTAINEN = (255, 255, 0)
VIHREA = (0, 255, 0)
ORANSSI = (255, 165, 0)
PINKKI = (255, 192, 203)
VIOLETTI = (148, 0, 211)
TURKOOSI = (64, 224, 208)
HARMAA = (128, 128, 128)
taustavari = MUSTA

base_dir = os.path.dirname(os.path.abspath(__file__))
kuva_dir = os.path.join(base_dir, 'Kuvat')
aani_dir = os.path.join(base_dir, 'Äänet')

robo_imgs = [
    pygame.image.load(os.path.join(kuva_dir, 'robo_1.png')),
    pygame.image.load(os.path.join(kuva_dir, 'robo_2.png')),
    pygame.image.load(os.path.join(kuva_dir, 'robo_3.png')),
    pygame.image.load(os.path.join(kuva_dir, 'robo_4.png')),
    pygame.image.load(os.path.join(kuva_dir, 'robo_5.png')),
    pygame.image.load(os.path.join(kuva_dir, 'robo_6.png')),
    pygame.image.load(os.path.join(kuva_dir, 'robo_7.png')),
    pygame.image.load(os.path.join(kuva_dir, 'robo_8.png')),
    pygame.image.load(os.path.join(kuva_dir, 'robo_9.png')),
    pygame.image.load(os.path.join(kuva_dir, 'robo_10.png'))
]
ammus_img= pygame.image.load(os.path.join(kuva_dir, 'laser.png'))
#bfg_img = pygame.image.load(os.path.join(base_dir, 'bfg.png'))

# Surface
vihollinen_img = pygame.Surface((50, 50))
vihollinen_img.fill(PUNAINEN)
valiloppari_img = pygame.Surface((70, 70))
valiloppari_img.fill(VIOLETTI)
vikaloppari_img = pygame.Surface((70, 70))
vikaloppari_img.fill(TURKOOSI)
bfg_img = pygame.Surface((50, 50))
bfg_img.fill(HARMAA)
#explosion_img=pygame.image.load(os.path.join(base_dir, 'explosion.png'))
#rajahdys=explosion_img

# Alkuarvot
pelaaja_sijainti = [pelialue_leveys // 2, pelialue_korkeus - 60]
pelaaja_suunta = 'seisoo'  # Suunta ('seisoo', 'vasen', 'oikea')
animaatio_indeksi = 0
vihollinen_sijainti = [pelialue_leveys // 2, 60]
ammukset = []
viholliset = [[vihollinen_sijainti[0], vihollinen_sijainti[1], 0]]
valiloppari = None
vikaloppari = None
bfg = None
bfg_ajastin = 0
bfg_count = 0 
pisteet = 0
fontti = pygame.font.Font(None, 36)
robotti_lkm = 0
vikaloppari_lkm=0
vihollisen_pudotusnopeus = 2
animaatio_vasemmalle = robo_imgs[:5]
animaatio_oikealle = robo_imgs[5:]

BRRR_TEKSTI_AJASTIN = pygame.USEREVENT + 2
brrr_teksti = ""
brrr_teksti_ajastin_aktiivinen = False

OSUMA_TEKSTI_AJASTIN = pygame.USEREVENT + 4
osuma_teksti = ""
osuma_teksti_ajastin_aktiivinen = False

BFG_TEKSTI_AJASTIN = pygame.USEREVENT + 6
bfg_teksti = ""
bfg_teksti_ajastin_aktiivinen = False

intro_text = [
    "Ohita intro painamalla välilyöntiä.",
    "Jonkin aikaa sitten läheisessä kaupungissa Robotti Ruttunen vietti kovaa elämää.",
    "\"Sä et tiedä mitä tää on, sul ei oo hajuu, jos sul ois säki tekisit näin\" tuumi Ruttunen,",
    "tehdessään kioskimurtoja öljyrahojen toivossa.",
    "Sitten eräänä aamuna Ruttunen huomasi lievästi järkyttyneenä,", 
    "että taivaalta alkoi putoilla inhoja, punaisia neliöitä.",
    "Onneksi Ruttusella oli vielä luotto-pystykorva edellisestä mähinästä.", 
    "\"Aika potkia persusta ja jauhaa purkkaa... Eikä mulla oo yhtään purkkaa\".",
    "Tehtävänäsi on auttaa Ruttusta pelastamaan ainakin lähikaupunki,", 
    "mahdollisesti loppupäivä sekä koko maailma."
]
intro_font = pygame.font.Font(None, 24)
intro_text_surfaces = [intro_font.render(line, True, VALKOINEN) for line in intro_text]
intro_text_y = nayton_korkeus

def lataa_aanet():
    pygame.mixer.init()
    osuma_aani_path = [os.path.join(aani_dir, f"explosion{i}.wav") for i in range(1, 5)]
    osuma_aani = [pygame.mixer.Sound(path) for path in osuma_aani_path]
    bfg_aani_path = os.path.join(aani_dir, "bfg.wav")
    bfg_aani = pygame.mixer.Sound(bfg_aani_path)
    duke_aani_path = os.path.join(aani_dir, "duke.wav")
    duke_aani = pygame.mixer.Sound(duke_aani_path)
    intro_aani_path = os.path.join(aani_dir, "intro.wav")
    intro_aani = pygame.mixer.Sound(intro_aani_path)
    xcom_aani_path = os.path.join(aani_dir, "xcom.wav")
    xcom_aani = pygame.mixer.Sound(xcom_aani_path)
    sor1_aani_path = os.path.join(aani_dir, "sor1.wav")
    sor1_aani = pygame.mixer.Sound(sor1_aani_path)
    sor2_aani_path = os.path.join(aani_dir, "sor2.wav")
    sor2_aani = pygame.mixer.Sound(sor2_aani_path)
    sor3_aani_path = os.path.join(aani_dir, "sor3.wav")
    sor3_aani = pygame.mixer.Sound(sor3_aani_path)
    sor4_aani_path = os.path.join(aani_dir, "sor4.wav")
    sor4_aani = pygame.mixer.Sound(sor4_aani_path)
    
    return osuma_aani, bfg_aani, duke_aani, intro_aani, xcom_aani, sor1_aani, sor2_aani, sor3_aani, sor4_aani

osuma_aani, bfg_aani, duke_aani, intro_aani, xcom_aani, sor1_aani, sor2_aani, sor3_aani, sor4_aani = lataa_aanet()

def lataa_parhaat_pisteet():
    try:
        with open("parhaat_pisteet.txt", "r") as tiedosto:
            parhaat_pisteet = [rivi.strip().split(",") for rivi in tiedosto.readlines()]
            parhaat_pisteet = [(nimi, int(pisteet)) for nimi, pisteet in parhaat_pisteet]
    except FileNotFoundError:
        parhaat_pisteet = []
    return parhaat_pisteet

def tallenna_parhaat_pisteet(parhaat_pisteet):
    with open("parhaat_pisteet.txt", "w") as tiedosto:
        for nimi, pisteet in parhaat_pisteet:
            tiedosto.write(f"{nimi},{pisteet}\n")

def nayta_pisteiden_syotto(pisteet):
    syotto_fontti = pygame.font.Font(None, 36)
    nimi = ""
    syotto_valmis = False

    while not syotto_valmis:
        naytto.fill(MUSTA)
        teksti = syotto_fontti.render(f"Syötä nimesi (pisteet: {pisteet}): {nimi}", True, VALKOINEN)
        naytto.blit(teksti, (nayton_leveys // 2 - teksti.get_width() // 2, nayton_korkeus // 2))
        pygame.display.flip()

        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                pygame.quit()
                exit()
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_RETURN:
                    syotto_valmis = True
                elif tapahtuma.key == pygame.K_BACKSPACE:
                    nimi = nimi[:-1]
                else:
                    nimi += tapahtuma.unicode
    return nimi

parhaat_pisteet = lataa_parhaat_pisteet()

def liikuta_pelaajaa():
    global pelaaja_suunta, animaatio_indeksi
    keys = pygame.key.get_pressed()
    nopeus = 5
    if keys[pygame.K_LEFT] and pelaaja_sijainti[0] > 0: 
        pelaaja_sijainti[0] -= nopeus
        pelaaja_suunta = 'vasen'
    elif keys[pygame.K_RIGHT] and pelaaja_sijainti[0] < pelialue_leveys - 50: 
        pelaaja_sijainti[0] += nopeus
        pelaaja_suunta = 'oikea'
    else:
        pelaaja_suunta = 'seisoo'
        animaatio_indeksi = 0

def piirra_pelaaja():
    global animaatio_indeksi
    korjattu_sijainti = [pelaaja_sijainti[0], pelaaja_sijainti[1] - 61]  # Korjaa sijaintia ylöspäin noin puolet pelaajan korkeudesta joka on 123
    if pelaaja_suunta == 'seisoo':
        naytto.blit(animaatio_vasemmalle[0], korjattu_sijainti)
    elif pelaaja_suunta == 'vasen':
        naytto.blit(animaatio_vasemmalle[animaatio_indeksi // 5], korjattu_sijainti)
        animaatio_indeksi = (animaatio_indeksi + 1) % (len(animaatio_vasemmalle) * 5)
    elif pelaaja_suunta == 'oikea':
        naytto.blit(animaatio_oikealle[animaatio_indeksi // 5], korjattu_sijainti)
        animaatio_indeksi = (animaatio_indeksi + 1) % (len(animaatio_oikealle) * 5)

def ammu(suunta):
    global brrr_teksti, brrr_teksti_ajastin_aktiivinen
    if suunta == "ylös":
        ammukset.append([pelaaja_sijainti[0] + 15, pelaaja_sijainti[1], suunta])
    elif suunta == "vasen":
        ammukset.append([pelaaja_sijainti[0], pelaaja_sijainti[1] + 20, suunta])
    elif suunta == "oikea":
        ammukset.append([pelaaja_sijainti[0] + 30, pelaaja_sijainti[1] + 20, suunta])
    pygame.time.set_timer(BRRR_TEKSTI_AJASTIN, 500)  
    brrr_teksti = "Pystykorva goes BRRR"
    brrr_teksti_ajastin_aktiivinen = True

def paivita_ammukset():
    global pisteet, valiloppari, vikaloppari, bfg, bfg_count, bfg_teksti, bfg_ajastin, bfg_teksti_ajastin_aktiivinen
    poistettavat_ammukset = []

    # Kaikki tarkistettavat kohteet
    kohteet = [{'obj': vikaloppari, 'rect': pygame.Rect(vikaloppari[0], vikaloppari[1], 70, 70), 'pisteet': 20}] if vikaloppari else []
    kohteet += [{'obj': valiloppari, 'rect': pygame.Rect(valiloppari[0], valiloppari[1], 70, 70), 'pisteet': 10}] if valiloppari else []
    kohteet +=[{'obj': bfg, 'rect': pygame.Rect(bfg[0], bfg[1], 50, 50), 'pisteet': 1}] if bfg else []
    kohteet += [{'obj': vihollinen, 'rect': pygame.Rect(vihollinen[0], vihollinen[1], 50, 50), 'pisteet': 1} for vihollinen in viholliset]
 

    for ammus in ammukset:
        if ammus[2] == "ylös":
            ammus[1] -= 10  
        elif ammus[2] == "vasen":
            ammus[0] -= 10  
        elif ammus[2] == "oikea":
            ammus[0] += 10  
        if ammus[1] < 0 or ammus[0] < 0 or ammus[0] > pelialue_leveys:
            poistettavat_ammukset.append(ammus)
            continue
        
        ammus_rect = pygame.Rect(ammus[0], ammus[1], 20, 10)
        for kohde in kohteet:
            if ammus_rect.colliderect(kohde['rect']):
                poistettavat_ammukset.append(ammus)
                if kohde['obj'] == vikaloppari:
                    vikaloppari[2] -= 1
                    if vikaloppari[2] <= 0:
                        vikaloppari = None
                        random.choice(osuma_aani).play()
                        pisteet += kohde['pisteet'] 
                elif kohde['obj'] == valiloppari:
                    valiloppari[2] -= 1
                    if valiloppari[2] <= 0:
                        valiloppari = None 
                        random.choice(osuma_aani).play() 
                        pisteet += kohde['pisteet']
                elif kohde['obj'] == bfg: 
                    bfg_count += 1
                    bfg = None                   
                    random.choice(osuma_aani).play()
                    pisteet += kohde['pisteet']
                    pygame.time.set_timer(BFG_TEKSTI_AJASTIN, 1000)
                    bfg_teksti = "Pee äf gee, kylläpä kyllä"
                    bfg_teksti_ajastin_aktiivinen = True
                else:
                    viholliset.remove(kohde['obj'])
                    random.choice(osuma_aani).play() 
                    pisteet += kohde['pisteet']
                break

    for ammus in poistettavat_ammukset:
        if ammus in ammukset:
            ammukset.remove(ammus)

def vaihda_tasomusiikki(uusi_musiikki):
    global tasomusiikit
    if tasomusiikit:
        tasomusiikit.stop()
    tasomusiikit = uusi_musiikki
    tasomusiikit.play(loops=-1)

def luo_objekti():
    global robotti_lkm,vikaloppari_lkm, vihollisen_pudotusnopeus, taustavari, peli_kaynnissa, valiloppari, vikaloppari, bfg, bfg_ajastin
    x = random.randint(0, pelialue_leveys - 50)
    viholliset.append([x, 0, 0])
    robotti_lkm += 1

    if robotti_lkm == 20: 
        vihollisen_pudotusnopeus += 0.2
        taustavari = KELTAINEN
        xcom_aani.stop()
        vaihda_tasomusiikki(sor1_aani)
    elif robotti_lkm %30==0 and not bfg:
        bfg = [x,0, 0]
        bfg_ajastin = pygame.time.get_ticks() + 5000
    elif robotti_lkm %50==0 and not valiloppari:
        valiloppari = [x, 0, 10]  
    elif robotti_lkm == 40:
        vihollisen_pudotusnopeus += 0.25
        taustavari = VIHREA
        vaihda_tasomusiikki(sor2_aani)
    elif robotti_lkm == 60:
        vihollisen_pudotusnopeus += 0.25
        taustavari = ORANSSI
        vaihda_tasomusiikki(sor3_aani)
    elif robotti_lkm == 80:
        vihollisen_pudotusnopeus += 0.25
        taustavari = PINKKI
        vaihda_tasomusiikki(sor4_aani)
    elif robotti_lkm > 120 and  vikaloppari_lkm==0:
        vihollisen_pudotusnopeus += 0.1
        vikaloppari = [x, 0, 20]  
        vikaloppari_lkm+=1

def paivita_viholliset():
    global peli_kaynnissa, robotti_lkm, osuma_teksti, osuma_teksti_ajastin_aktiivinen, bfg
    pelaajan_leveys = 33
    pelaajan_korkeus = 123  # Korjattu korkeus
    pelaaja_rect = pygame.Rect(pelaaja_sijainti[0], pelaaja_sijainti[1], pelaajan_leveys, pelaajan_korkeus)


    kohteet = [{'obj': vikaloppari, 'rect': pygame.Rect(vikaloppari[0], vikaloppari[1], 70, 134), 'koko': 70}] if vikaloppari else []
    kohteet += [{'obj': valiloppari, 'rect': pygame.Rect(valiloppari[0], valiloppari[1], 70, 134), 'koko': 70}] if valiloppari else []
    kohteet += [{'obj': bfg, 'rect': pygame.Rect(bfg[0], bfg[1], 50, 114), 'koko': 50}] if bfg else []
    kohteet += [{'obj': vihollinen, 'rect': pygame.Rect(vihollinen[0], vihollinen[1], 50, 114), 'koko': 50} for vihollinen in viholliset]

    
    for kohde in kohteet:
        obj = kohde['obj']
        rect = kohde['rect']
        koko = kohde['koko']

        if obj[1] < pelialue_korkeus - koko:
            obj[1] += vihollisen_pudotusnopeus
        else:
            if obj[2] == 0:
                obj[2] = random.choice([-2, 2])
            obj[0] += obj[2]
            if obj[0] < 0 or obj[0] > pelialue_leveys - koko:
                obj[2] = -obj[2]

        if pelaaja_rect.colliderect(rect):
            osuma_tekstit = ["Autsista", "Argh", "Nyt sattui Ruttusta leukaan"]
            osuma_teksti = random.choice(osuma_tekstit)
            pygame.time.set_timer(OSUMA_TEKSTI_AJASTIN, 500)
            osuma_teksti_ajastin_aktiivinen = True
            peli_kaynnissa = False

    if robotti_lkm > 120 and not vikaloppari:
        peli_kaynnissa = False

def nayta_intro():
    global intro_text_y
    naytto.fill(MUSTA)
    for i, line_surface in enumerate(intro_text_surfaces):
        naytto.blit(line_surface, (20, intro_text_y + i * 30))
    intro_text_y -= 0.5
    pygame.display.flip()
    kello.tick(60)

def nayta_valikko():
    naytto.fill(MUSTA)
    otsikko_fontti = pygame.font.Font(None, 72)
    valikko_fontti = pygame.font.Font(None, 48)
    otsikko_teksti = otsikko_fontti.render("Ruttunen Pelastaa", True, VALKOINEN)
    naytto.blit(otsikko_teksti, (nayton_leveys // 2 - otsikko_teksti.get_width() // 2, nayton_korkeus // 4))

    valinnat = ["1. Käynnistä peli", "2. Ohjeet", "3. Parhaat pisteet", "4. Lopeta peli"]
    valikko_rects = []
    for i, valinta in enumerate(valinnat):
        valinta_teksti = valikko_fontti.render(valinta, True, VALKOINEN)
        rect = valinta_teksti.get_rect(center=(nayton_leveys // 2, nayton_korkeus // 2 + i * 50))
        naytto.blit(valinta_teksti, rect)
        valikko_rects.append(rect)

    pygame.display.flip()
    return valikko_rects

def nayta_ohjeet():
    naytto.fill(MUSTA)
    ohje_fontti = pygame.font.Font(None, 36)
    ohjeet = [
        "Ohjeet:",
        "1. Liiku vasemmalle ja oikealle nuolinäppäimillä.",
        "2. Ammu ylöspäin painamalla välilyöntiä.",
        "3. Ammu vasemmalle painamalla shift + välilyönti.",
        "4. Ammu oikealle painamalla ctrl + välilyönti.",
        "5. Kerää BFG ampumalla harmaata vihollista. Kylvä tuhoa painamalla b:tä.",
        "6. Väistä vihollisia ja ammu niitä saadaksesi pisteitä.",
        "7. Käytössäsi on kehitysversio. Välipomo on violetti (10 osumaa) ja loppuvastus on pinkki (20 osumaa). "
        "8. Peli on kehitysvaiheessa grafiikoiden osalta. Pelitoiminnot, äänet, musiikit, tekstit, pelitapahtumat ja muu ohjelman toiminta on tarkoitettua. Vaikeusastetta ei ole säädetty, peli on helpohko."
    ]
    for i, ohje in enumerate(ohjeet):
        ohje_teksti = ohje_fontti.render(ohje, True, VALKOINEN)
        naytto.blit(ohje_teksti, (20, 50 + i * 40))

    poistu_nappi = pygame.Rect(nayton_leveys // 2 - 50, nayton_korkeus - 100, 100, 50)
    pygame.draw.rect(naytto, VALKOINEN, poistu_nappi)
    poistu_teksti = ohje_fontti.render("Poistu", True, MUSTA)
    naytto.blit(poistu_teksti, (nayton_leveys // 2 - poistu_teksti.get_width() // 2, nayton_korkeus - 90))

    pygame.display.flip()

    while True:
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                pygame.quit()
                exit()
            if tapahtuma.type == pygame.MOUSEBUTTONDOWN and tapahtuma.button == 1:
                if poistu_nappi.collidepoint(tapahtuma.pos):
                    return

def nayta_parhaat_pisteet():
    naytto.fill(MUSTA)
    pisteet_fontti = pygame.font.Font(None, 36)
    otsikko_teksti = pisteet_fontti.render("Parhaat pisteet", True, VALKOINEN)
    naytto.blit(otsikko_teksti, (nayton_leveys // 2 - otsikko_teksti.get_width() // 2, 50))

    for i, (nimi, pisteet) in enumerate(parhaat_pisteet):
        pisteet_teksti = pisteet_fontti.render(f"{i + 1}. {nimi} - {pisteet}", True, VALKOINEN)
        naytto.blit(pisteet_teksti, (nayton_leveys // 2 - pisteet_teksti.get_width() // 2, 100 + i * 40))

    poistu_nappi = pygame.Rect(nayton_leveys // 2 - 50, nayton_korkeus - 100, 100, 50)
    pygame.draw.rect(naytto, VALKOINEN, poistu_nappi)
    poistu_teksti = pisteet_fontti.render("Poistu", True, MUSTA)
    naytto.blit(poistu_teksti, (nayton_leveys // 2 - poistu_teksti.get_width() // 2, nayton_korkeus - 90))

    pygame.display.flip()

    while True:
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                pygame.quit()
                exit()
            if tapahtuma.type == pygame.MOUSEBUTTONDOWN and tapahtuma.button == 1:
                if poistu_nappi.collidepoint(tapahtuma.pos):
                    return

def paavalikko():
    intro_aani.play(loops=-1)
    while True:
        valikko_rects = nayta_valikko()
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                intro_aani.stop()
                pygame.quit()
                exit()
            if tapahtuma.type == pygame.MOUSEBUTTONDOWN and tapahtuma.button == 1:
                for i, rect in enumerate(valikko_rects):
                    if rect.collidepoint(tapahtuma.pos):
                        if i == 0:
                            intro_aani.stop()
                            xcom_aani.play(loops=-1)
                            return True
                        elif i == 1:
                            nayta_ohjeet()
                        elif i == 2:
                            nayta_parhaat_pisteet()
                        elif i == 3:
                            pygame.quit()
                            exit()
        kello.tick(60)

# Pelisilmukka
while True:
    peli_kaynnissa = paavalikko()
    intro_kaynnissa = peli_kaynnissa

    vihollinen_ajastin = 0
    pelaaja_sijainti = [pelialue_leveys // 2, pelialue_korkeus - 60]
    viholliset.clear()
    ammukset.clear()
    pisteet = 0
    robotti_lkm = 0
    vikaloppari_lkm = 0
    vihollisen_pudotusnopeus = 2
    taustavari = MUSTA
    valiloppari = None
    vikaloppari = None
    bfg = None
    bfg_ajastin = 0
    bfg_count = 0

    tasomusiikit = None

    while peli_kaynnissa or intro_kaynnissa:
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                pygame.quit()
                exit()
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_SPACE:
                    if intro_kaynnissa:
                        intro_kaynnissa = False
                    else:
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_LSHIFT]:
                            ammu("vasen")
                        elif keys[pygame.K_LCTRL]:
                            ammu("oikea")
                        else:
                            ammu("ylös")
                elif tapahtuma.key == pygame.K_b and bfg_count > 0:
                    bfg_aani.play()
                    bfg_count -= 1
                    viholliset.clear()
                    valiloppari = None
                    vikaloppari = None
                    duke_aani.play()
                if not peli_kaynnissa and tapahtuma.key == pygame.K_RETURN:
                    intro_kaynnissa = False
            if tapahtuma.type == BRRR_TEKSTI_AJASTIN:
                brrr_teksti = ""
                pygame.time.set_timer(BRRR_TEKSTI_AJASTIN, 0)
                brrr_teksti_ajastin_aktiivinen = False
            if tapahtuma.type == OSUMA_TEKSTI_AJASTIN:
                osuma_teksti = ""
                pygame.time.set_timer(OSUMA_TEKSTI_AJASTIN, 0)
                osuma_teksti_ajastin_aktiivinen = False
            if tapahtuma.type == BFG_TEKSTI_AJASTIN:
                bfg_teksti = ""
                pygame.time.set_timer(BFG_TEKSTI_AJASTIN, 0)
                bfg_teksti_ajastin_aktiivinen = False

        if intro_kaynnissa:
            nayta_intro()
            if intro_text_y + len(intro_text_surfaces) * 30 < 0:
                intro_kaynnissa = False
        elif peli_kaynnissa:
            naytto.fill(taustavari)
            paivita_ammukset()
            paivita_viholliset()

            vihollinen_ajastin += 1 #Konffaa vaikeusaste
            if vihollinen_ajastin > 100:
                luo_objekti()
                vihollinen_ajastin = 0

            pelialue = pygame.Surface((pelialue_leveys, pelialue_korkeus))
            pelialue.fill(taustavari)
            pistealue = pygame.Surface((pistealue_leveys, nayton_korkeus))
            pistealue.fill(VALKOINEN)

            # PIIRROT SEURAA
            for vihollinen in viholliset:
                pelialue.blit(vihollinen_img, (vihollinen[0], vihollinen[1]))

            if valiloppari:
                pelialue.blit(valiloppari_img, (valiloppari[0], valiloppari[1]))

            if vikaloppari:
                pelialue.blit(vikaloppari_img, (vikaloppari[0], vikaloppari[1]))

            if bfg and pygame.time.get_ticks() <= bfg_ajastin:
                pelialue.blit(bfg_img, (bfg[0], bfg[1]))
            else:
                bfg = None

            for ammus in ammukset:
                pelialue.blit(ammus_img, (ammus[0], ammus[1]))
            #PIIRROT LOPPU

            piste_teksti = fontti.render(f"Pisteet: {pisteet}", True, MUSTA)
            pistealue.blit(piste_teksti, (10, 10))

            bfg_maara = fontti.render(f"BFG: {bfg_count}", True, MUSTA)
            pistealue.blit(bfg_maara, (10, 50))

            if brrr_teksti:
                brrr_teksti_surface = fontti.render(brrr_teksti, True, VALKOINEN)
                pelialue.blit(brrr_teksti_surface, (pelaaja_sijainti[0] + 60, pelaaja_sijainti[1] - 10))

            if osuma_teksti:
                osuma_teksti_surface = fontti.render(osuma_teksti, True, VALKOINEN)
                pelialue.blit(osuma_teksti_surface, (pelaaja_sijainti[0] + 60, pelaaja_sijainti[1] - 30))

            if bfg_teksti:
                bfg_teksti_surface = fontti.render(bfg_teksti, True, VALKOINEN)
                pelialue.blit(bfg_teksti_surface, (pelaaja_sijainti[0] + 60, pelaaja_sijainti[1] - 50))

            if not peli_kaynnissa:
                if robotti_lkm <= 20 and xcom_aani.get_num_channels() > 0:
                    xcom_aani.stop()
                if robotti_lkm > 120 and vikaloppari_lkm > 0 and not vikaloppari:
                    lopetus_teksti = "Voitit pelin"
                else:
                    lopetus_teksti = "Hävisit pelin"
                lopetus_surface = fontti.render(lopetus_teksti, True, VALKOINEN)
                pelialue.blit(lopetus_surface, (pelialue_leveys // 2 - 100, pelialue_korkeus // 2))

                ok_nappi = pygame.Rect(pelialue_leveys // 2 - 50, pelialue_korkeus // 2 + 50, 100, 50)
                pygame.draw.rect(pelialue, VALKOINEN, ok_nappi)
                ok_teksti = fontti.render("OK", True, MUSTA)
                pelialue.blit(ok_teksti, (pelialue_leveys // 2 - ok_teksti.get_width() // 2, pelialue_korkeus // 2 + 60))

                naytto.blit(pelialue, (0, 0))
                naytto.blit(pistealue, (pelialue_leveys, 0))
                piirra_pelaaja()
                pygame.display.flip()

                peli_paattynyt = True
                while peli_paattynyt:
                    for tapahtuma in pygame.event.get():
                        if tapahtuma.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        if tapahtuma.type == pygame.MOUSEBUTTONDOWN and tapahtuma.button == 1:
                            if ok_nappi.collidepoint(tapahtuma.pos):
                                peli_paattynyt = False
                if len(parhaat_pisteet) < 10 and pisteet > parhaat_pisteet[-1][1]:
                    nimi = nayta_pisteiden_syotto(pisteet)
                    parhaat_pisteet.append((nimi, pisteet))
                    parhaat_pisteet.sort(key=lambda x: x[1], reverse=True)
                    parhaat_pisteet = parhaat_pisteet[:10]
                    tallenna_parhaat_pisteet(parhaat_pisteet)
                if tasomusiikit:
                    tasomusiikit.stop()
            else:
                naytto.blit(pelialue, (0, 0))
                naytto.blit(pistealue, (pelialue_leveys, 0))
                liikuta_pelaajaa()
                piirra_pelaaja()
                pygame.display.flip()
                kello.tick(60)