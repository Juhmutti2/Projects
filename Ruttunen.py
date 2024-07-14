import pygame
import random
import os

class Peli:
    def __init__(self):
        pygame.init()
        self.nayton_leveys, self.nayton_korkeus = 1200, 600
        self.pistealue_leveys = 200
        self.pelialue_leveys = self.nayton_leveys - self.pistealue_leveys
        self.pelialue_korkeus = self.nayton_korkeus
        self.naytto = pygame.display.set_mode((self.nayton_leveys, self.nayton_korkeus))
        pygame.display.set_caption("Ruttunen Pelastaa")
        self.kello = pygame.time.Clock()

        self.MUSTA = (0, 0, 0)
        self.VALKOINEN = (255, 255, 255)
        self.PUNAINEN = (255, 0, 0)
        self.KELTAINEN = (255, 255, 0)
        self.VIHREA = (0, 255, 0)
        self.ORANSSI = (255, 165, 0)
        self.PINKKI = (255, 192, 203)
        self.VIOLETTI = (148, 0, 211)
        self.TURKOOSI = (64, 224, 208)
        self.HARMAA = (128, 128, 128)
        self.taustavari = self.MUSTA

        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.kuva_dir = os.path.join(self.base_dir, 'Kuvat')
        self.aani_dir = os.path.join(self.base_dir, 'Äänet')

        self.robo_imgs = [pygame.image.load(os.path.join(self.kuva_dir, f'robo_{i}.png')) for i in range(1, 11)]
        self.ammus_img = pygame.image.load(os.path.join(self.kuva_dir, 'laser.png'))
        self.vihollinen_img = self.create_surface(50, 50, self.PUNAINEN)
        self.valiloppari_img = self.create_surface(70, 70, self.VIOLETTI)
        self.vikaloppari_img = self.create_surface(70, 70, self.TURKOOSI)
        self.bfg_img = self.create_surface(50, 50, self.HARMAA)

        self.animaatio_vasemmalle = self.robo_imgs[:5]
        self.animaatio_oikealle = self.robo_imgs[5:]

        self.pelaaja = Pelaaja(self.pelialue_leveys // 2, self.pelialue_korkeus - 60, self.animaatio_vasemmalle, self.animaatio_oikealle)
        self.viholliset = []
        self.ammukset = []
        self.bfg = None
        self.valiloppari = None
        self.vikaloppari = None
        self.bfg_ajastin = 0
        self.bfg_count = 0
        self.pisteet = 0

        self.fontti = pygame.font.Font(None, 36)
        self.robotti_lkm = 0
        self.vikaloppari_lkm = 0
        self.vihollisen_pudotusnopeus = 2

        self.BRRR_TEKSTI_AJASTIN = pygame.USEREVENT + 2
        self.brrr_teksti = ""
        self.brrr_teksti_ajastin_aktiivinen = False

        self.OSUMA_TEKSTI_AJASTIN = pygame.USEREVENT + 4
        self.osuma_teksti = ""
        self.osuma_teksti_ajastin_aktiivinen = False

        self.BFG_TEKSTI_AJASTIN = pygame.USEREVENT + 6
        self.bfg_teksti = ""
        self.bfg_teksti_ajastin_aktiivinen = False

        self.intro_text = [
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
        self.intro_font = pygame.font.Font(None, 24)
        self.intro_text_surfaces = [self.intro_font.render(line, True, self.VALKOINEN) for line in self.intro_text]
        self.intro_text_y = self.nayton_korkeus

        self.osuma_aani, self.bfg_aani, self.duke_aani, self.intro_aani, self.xcom_aani, self.sor1_aani, self.sor2_aani, self.sor3_aani, self.sor4_aani = self.lataa_aanet()

    def create_surface(self, width, height, color):
        surface = pygame.Surface((width, height))
        surface.fill(color)
        return surface

    def lataa_aanet(self):
        pygame.mixer.init()
        base_dir = self.aani_dir
        osuma_aani_path = [os.path.join(base_dir, f"explosion{i}.wav") for i in range(1, 5)]
        osuma_aani = [pygame.mixer.Sound(path) for path in osuma_aani_path]
        bfg_aani = pygame.mixer.Sound(os.path.join(base_dir, "bfg.wav"))
        duke_aani = pygame.mixer.Sound(os.path.join(base_dir, "duke.wav"))
        intro_aani = pygame.mixer.Sound(os.path.join(base_dir, "intro.wav"))
        xcom_aani = pygame.mixer.Sound(os.path.join(base_dir, "xcom.wav"))
        sor1_aani = pygame.mixer.Sound(os.path.join(base_dir, "sor1.wav"))
        sor2_aani = pygame.mixer.Sound(os.path.join(base_dir, "sor2.wav"))
        sor3_aani = pygame.mixer.Sound(os.path.join(base_dir, "sor3.wav"))
        sor4_aani = pygame.mixer.Sound(os.path.join(base_dir, "sor4.wav"))

        return osuma_aani, bfg_aani, duke_aani, intro_aani, xcom_aani, sor1_aani, sor2_aani, sor3_aani, sor4_aani

    def lataa_parhaat_pisteet(self):
        try:
            with open("parhaat_pisteet.txt", "r") as tiedosto:
                parhaat_pisteet = [rivi.strip().split(",") for rivi in tiedosto.readlines()]
                parhaat_pisteet = [(nimi, int(pisteet)) for nimi, pisteet in parhaat_pisteet]
        except FileNotFoundError:
            parhaat_pisteet = []
        return parhaat_pisteet

    def tallenna_parhaat_pisteet(self, parhaat_pisteet):
        with open("parhaat_pisteet.txt", "w") as tiedosto:
            for nimi, pisteet in parhaat_pisteet:
                tiedosto.write(f"{nimi},{pisteet}\n")

    def nayta_pisteiden_syotto(self, pisteet):
        syotto_fontti = pygame.font.Font(None, 36)
        nimi = ""
        syotto_valmis = False

        while not syotto_valmis:
            self.naytto.fill(self.MUSTA)
            teksti = syotto_fontti.render(f"Syötä nimesi (pisteet: {pisteet}): {nimi}", True, self.VALKOINEN)
            self.naytto.blit(teksti, (self.nayton_leveys // 2 - teksti.get_width() // 2, self.nayton_korkeus // 2))
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

    def liikuta_pelaajaa(self):
        keys = pygame.key.get_pressed()
        nopeus = 5
        pelaaja = self.pelaaja
        pelialue_leveys = self.pelialue_leveys
        if keys[pygame.K_LEFT] and pelaaja.x > 0:
            pelaaja.liiku(-nopeus, 0)
        elif keys[pygame.K_RIGHT] and pelaaja.x < pelialue_leveys - pelaaja.leveys:
            pelaaja.liiku(nopeus, 0)
        else:
            pelaaja.seisoo()

    def ammu(self, suunta):
        pelaaja = self.pelaaja
        ammus_img = self.ammus_img
        ammukset = self.ammukset
        BRRR_TEKSTI_AJASTIN = self.BRRR_TEKSTI_AJASTIN
        if suunta == "ylös":
            ammukset.append(Ammus(pelaaja.x + 15, pelaaja.y, suunta, ammus_img))
        elif suunta == "vasen":
            ammukset.append(Ammus(pelaaja.x, pelaaja.y + 20, suunta, ammus_img))
        elif suunta == "oikea":
            ammukset.append(Ammus(pelaaja.x + 30, pelaaja.y + 20, suunta, ammus_img))
        pygame.time.set_timer(BRRR_TEKSTI_AJASTIN, 500)
        self.brrr_teksti = "Pystykorva goes BRRR"
        self.brrr_teksti_ajastin_aktiivinen = True

    def paivita_ammukset(self):
        poistettavat_ammukset = []
        kohteet = []
        vikaloppari = self.vikaloppari
        valiloppari = self.valiloppari
        bfg = self.bfg
        viholliset = self.viholliset
        osuma_aani = self.osuma_aani
        if vikaloppari:
            kohteet.append({'obj': vikaloppari, 'rect': pygame.Rect(vikaloppari[0], vikaloppari[1], 70, 70), 'pisteet': 20})
        if valiloppari:
            kohteet.append({'obj': valiloppari, 'rect': pygame.Rect(valiloppari[0], valiloppari[1], 70, 70), 'pisteet': 10})
        if bfg:
            kohteet.append({'obj': bfg, 'rect': pygame.Rect(bfg[0], bfg[1], 50, 50), 'pisteet': 1})
        for vihollinen in viholliset:
            kohteet.append({'obj': vihollinen, 'rect': pygame.Rect(vihollinen[0], vihollinen[1], 50, 50), 'pisteet': 1})

        for ammus in self.ammukset:
            ammus.paivita()
            if ammus.tuhottu:
                poistettavat_ammukset.append(ammus)
                continue

            for kohde in kohteet:
                if ammus.rect.colliderect(kohde['rect']):
                    poistettavat_ammukset.append(ammus)
                    obj = kohde['obj']
                    if obj == vikaloppari:
                        vikaloppari[2] -= 1
                        if vikaloppari[2] <= 0:
                            self.vikaloppari = None
                            random.choice(osuma_aani).play()
                            self.pisteet += kohde['pisteet']
                    elif obj == valiloppari:
                        valiloppari[2] -= 1
                        if valiloppari[2] <= 0:
                            self.valiloppari = None
                            random.choice(osuma_aani).play()
                            self.pisteet += kohde['pisteet']
                    elif obj == bfg:
                        self.bfg_count += 1
                        self.bfg = None
                        random.choice(osuma_aani).play()
                        self.pisteet += kohde['pisteet']
                        pygame.time.set_timer(self.BFG_TEKSTI_AJASTIN, 1000)
                        self.bfg_teksti = "Pee äf gee, kylläpä kyllä"
                        self.bfg_teksti_ajastin_aktiivinen = True
                    else:
                        viholliset.remove(obj)
                        random.choice(osuma_aani).play()
                        self.pisteet += kohde['pisteet']
                    break

        for ammus in poistettavat_ammukset:
            if ammus in self.ammukset:
                self.ammukset.remove(ammus)

    def paivita_viholliset(self):
        pelaaja = self.pelaaja
        pelaaja_rect = pygame.Rect(pelaaja.x, pelaaja.y, 33, 123)
        pelialue_leveys = self.pelialue_leveys
        pelialue_korkeus = self.pelialue_korkeus
        vihollisen_pudotusnopeus = self.vihollisen_pudotusnopeus
        kohteet = []
        vikaloppari = self.vikaloppari
        valiloppari = self.valiloppari
        bfg = self.bfg
        viholliset = self.viholliset

        if vikaloppari:
            kohteet.append({'obj': vikaloppari, 'rect': pygame.Rect(vikaloppari[0], vikaloppari[1], 70, 134), 'koko': 70})
        if valiloppari:
            kohteet.append({'obj': valiloppari, 'rect': pygame.Rect(valiloppari[0], valiloppari[1], 70, 134), 'koko': 70})
        if bfg:
            kohteet.append({'obj': bfg, 'rect': pygame.Rect(bfg[0], bfg[1], 50, 114), 'koko': 50})
        for vihollinen in viholliset:
            kohteet.append({'obj': vihollinen, 'rect': pygame.Rect(vihollinen[0], vihollinen[1], 50, 114), 'koko': 50})

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
                self.osuma_teksti = random.choice(["Autsista", "Argh", "Nyt sattui Ruttusta leukaan"])
                pygame.time.set_timer(self.OSUMA_TEKSTI_AJASTIN, 500)
                self.osuma_teksti_ajastin_aktiivinen = True
                self.peli_kaynnissa = False

        if self.robotti_lkm > 120 and not self.vikaloppari:
            self.peli_kaynnissa = False

    def nayta_intro(self):
        naytto = self.naytto
        intro_text_surfaces = self.intro_text_surfaces
        intro_text_y = self.intro_text_y
        naytto.fill(self.MUSTA)
        for i, line_surface in enumerate(intro_text_surfaces):
            naytto.blit(line_surface, (20, intro_text_y + i * 30))
        self.intro_text_y -= 0.5
        pygame.display.flip()
        self.kello.tick(60)

    def nayta_valikko(self):
        naytto = self.naytto
        nayton_leveys = self.nayton_leveys
        nayton_korkeus = self.nayton_korkeus
        MUSTA = self.MUSTA
        VALKOINEN = self.VALKOINEN
        otsikko_fontti = pygame.font.Font(None, 72)
        valikko_fontti = pygame.font.Font(None, 48)
        otsikko_teksti = otsikko_fontti.render("Ruttunen Pelastaa", True, VALKOINEN)
        naytto.fill(MUSTA)
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

    def nayta_ohjeet(self):
        naytto = self.naytto
        nayton_leveys = self.nayton_leveys
        nayton_korkeus = self.nayton_korkeus
        MUSTA = self.MUSTA
        VALKOINEN = self.VALKOINEN
        ohje_fontti = pygame.font.Font(None, 36)
        ohjeet = [
            "Ohjeet:",
            "1. Liiku vasemmalle ja oikealle nuolinäppäimillä.",
            "2. Ammu ylöspäin painamalla välilyöntiä.",
            "3. Ammu vasemmalle painamalla shift + välilyönti.",
            "4. Ammu oikealle painamalla ctrl + välilyönti.",
            "5. Kerää BFG ampumalla harmaata vihollista. Kylvä tuhoa painamalla b:tä.",
            "6. Väistä vihollisia ja ammu niitä saadaksesi pisteitä. Välipomo on violetti (10 osumaa),",
            "loppuvastus on pinkki (20 osumaa).",
            "7. Käytössäsi on kehitysversio. Olemassa olevat toiminnot, tapahtumat, äänet, musiikit sekä tekstit",
            "ovat tarkoitettuja. Peliin on tarkoitus lisätä myöhemmin ominaisuuksia.", 
            "Vaikeusastetta ei ole säädetty, peli on helpohko."
        ]
        
        naytto.fill(MUSTA)
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

    def nayta_parhaat_pisteet(self):
        naytto = self.naytto
        nayton_leveys = self.nayton_leveys
        nayton_korkeus = self.nayton_korkeus
        MUSTA = self.MUSTA
        VALKOINEN = self.VALKOINEN
        pisteet_fontti = pygame.font.Font(None, 36)
        otsikko_teksti = pisteet_fontti.render("Parhaat pisteet", True, VALKOINEN)
        naytto.fill(MUSTA)
        naytto.blit(otsikko_teksti, (nayton_leveys // 2 - otsikko_teksti.get_width() // 2, 50))

        for i, (nimi, pisteet) in enumerate(self.lataa_parhaat_pisteet()):
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

    def paavalikko(self):
        intro_aani = self.intro_aani
        intro_aani.play(loops=-1)
        kello = self.kello
        while True:
            valikko_rects = self.nayta_valikko()
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
                                self.xcom_aani.play(loops=-1)
                                return True
                            elif i == 1:
                                self.nayta_ohjeet()
                            elif i == 2:
                                self.nayta_parhaat_pisteet()
                            elif i == 3:
                                pygame.quit()
                                exit()
            kello.tick(60)

    def luo_objekti(self):
        x = random.randint(0, self.pelialue_leveys - 50)
        robotti_lkm = self.robotti_lkm
        viholliset = self.viholliset
        if robotti_lkm == 20:
            self.vihollisen_pudotusnopeus += 0.2
            self.taustavari = self.KELTAINEN
            self.xcom_aani.stop()
            self.vaihda_tasomusiikki(self.sor1_aani)
        elif robotti_lkm %30== 0 and self.robotti_lkm !=0 and not self.bfg:
            self.bfg = [x, 0, 0]
            self.bfg_ajastin = pygame.time.get_ticks() + 5000
        elif robotti_lkm % 50 == 0 and self.robotti_lkm !=0 and not self.valiloppari:
            self.valiloppari = [x, 0, 10]
        elif robotti_lkm == 40:
            self.vihollisen_pudotusnopeus += 0.25
            self.taustavari = self.VIHREA
            self.vaihda_tasomusiikki(self.sor2_aani)
        elif robotti_lkm == 60:
            self.vihollisen_pudotusnopeus += 0.25
            self.taustavari = self.ORANSSI
            self.vaihda_tasomusiikki(self.sor3_aani)
        elif robotti_lkm == 80:
            self.vihollisen_pudotusnopeus += 0.25
            self.taustavari = self.PINKKI
            self.vaihda_tasomusiikki(self.sor4_aani)
        elif robotti_lkm > 120 and self.vikaloppari_lkm == 0 and not self.vikaloppari:
            self.vihollisen_pudotusnopeus += 0.1
            self.vikaloppari = [x, 0, 20]
            self.vikaloppari_lkm += 1
        else:
            viholliset.append([x, 0, 0])
        self.robotti_lkm += 1

    def vaihda_tasomusiikki(self, uusi_musiikki):
        if hasattr(self, 'tasomusiikit') and self.tasomusiikit:
            self.tasomusiikit.stop()
        self.tasomusiikit = uusi_musiikki
        self.tasomusiikit.play(loops=-1)

    def suorita(self):
        naytto = self.naytto
        fontti = self.fontti
        pelialue_leveys = self.pelialue_leveys
        pelialue_korkeus = self.pelialue_korkeus
        pistealue_leveys = self.pistealue_leveys
        while True:
            self.peli_kaynnissa = self.paavalikko()
            self.intro_kaynnissa = self.peli_kaynnissa

            vihollinen_ajastin = 0
            self.pelaaja = Pelaaja(pelialue_leveys // 2, pelialue_korkeus - 60, self.animaatio_vasemmalle, self.animaatio_oikealle)
            self.viholliset.clear()
            self.ammukset.clear()
            self.pisteet = 0
            self.robotti_lkm = 0
            self.vikaloppari_lkm = 0
            self.vihollisen_pudotusnopeus = 2
            self.taustavari = self.MUSTA
            self.valiloppari = None
            self.vikaloppari = None
            self.bfg = None
            self.bfg_ajastin = 0
            self.bfg_count = 0

            self.tasomusiikit = None

            while self.peli_kaynnissa or self.intro_kaynnissa:
                for tapahtuma in pygame.event.get():
                    if tapahtuma.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if tapahtuma.type == pygame.KEYDOWN:
                        if tapahtuma.key == pygame.K_SPACE:
                            if self.intro_kaynnissa:
                                self.intro_kaynnissa = False
                            else:
                                keys = pygame.key.get_pressed()
                                if keys[pygame.K_LSHIFT]:
                                    self.ammu("vasen")
                                elif keys[pygame.K_LCTRL]:
                                    self.ammu("oikea")
                                else:
                                    self.ammu("ylös")
                        elif tapahtuma.key == pygame.K_b and self.bfg_count > 0:
                            self.bfg_aani.play()
                            self.bfg_count -= 1
                            self.viholliset.clear()
                            self.valiloppari = None
                            self.vikaloppari = None
                            self.duke_aani.play()
                        if not self.peli_kaynnissa and tapahtuma.key == pygame.K_RETURN:
                            self.intro_kaynnissa = False
                    if tapahtuma.type == self.BRRR_TEKSTI_AJASTIN:
                        self.brrr_teksti = ""
                        pygame.time.set_timer(self.BRRR_TEKSTI_AJASTIN, 0)
                        self.brrr_teksti_ajastin_aktiivinen = False
                    if tapahtuma.type == self.OSUMA_TEKSTI_AJASTIN:
                        self.osuma_teksti = ""
                        pygame.time.set_timer(self.OSUMA_TEKSTI_AJASTIN, 0)
                        self.osuma_teksti_ajastin_aktiivinen = False
                    if tapahtuma.type == self.BFG_TEKSTI_AJASTIN:
                        self.bfg_teksti = ""
                        pygame.time.set_timer(self.BFG_TEKSTI_AJASTIN, 0)
                        self.bfg_teksti_ajastin_aktiivinen = False

                if self.intro_kaynnissa:
                    self.nayta_intro()
                    if self.intro_text_y + len(self.intro_text_surfaces) * 30 < 0:
                        self.intro_kaynnissa = False
                elif self.peli_kaynnissa:
                    naytto.fill(self.taustavari)
                    self.paivita_ammukset()
                    self.paivita_viholliset()

                    vihollinen_ajastin += 1  # Konffaa vaikeusaste
                    if vihollinen_ajastin > 100:
                        self.luo_objekti()
                        vihollinen_ajastin = 0

                    pelialue = pygame.Surface((pelialue_leveys, pelialue_korkeus))
                    pelialue.fill(self.taustavari)
                    pistealue = pygame.Surface((pistealue_leveys, self.nayton_korkeus))
                    pistealue.fill(self.VALKOINEN)

                    # PIIRROT SEURAA
                    for vihollinen in self.viholliset:
                        pelialue.blit(self.vihollinen_img, (vihollinen[0], vihollinen[1]))

                    if self.valiloppari:
                        pelialue.blit(self.valiloppari_img, (self.valiloppari[0], self.valiloppari[1]))

                    if self.vikaloppari:
                        pelialue.blit(self.vikaloppari_img, (self.vikaloppari[0], self.vikaloppari[1]))

                    if self.bfg and pygame.time.get_ticks() <= self.bfg_ajastin:
                        pelialue.blit(self.bfg_img, (self.bfg[0], self.bfg[1]))
                    else:
                        self.bfg = None

                    for ammus in self.ammukset:
                        pelialue.blit(self.ammus_img, (ammus.x, ammus.y))
                    # PIIRROT LOPPU

                    piste_teksti = fontti.render(f"Pisteet: {self.pisteet}", True, self.MUSTA)
                    pistealue.blit(piste_teksti, (10, 10))

                    bfg_maara = fontti.render(f"BFG: {self.bfg_count}", True, self.MUSTA)
                    pistealue.blit(bfg_maara, (10, 50))

                    if self.brrr_teksti:
                        brrr_teksti_surface = fontti.render(self.brrr_teksti, True, self.VALKOINEN)
                        pelialue.blit(brrr_teksti_surface, (self.pelaaja.x + 60, self.pelaaja.y - 10))

                    if self.osuma_teksti:
                        osuma_teksti_surface = fontti.render(self.osuma_teksti, True, self.VALKOINEN)
                        pelialue.blit(osuma_teksti_surface, (self.pelaaja.x + 60, self.pelaaja.y - 30))

                    if self.bfg_teksti:
                        bfg_teksti_surface = fontti.render(self.bfg_teksti, True, self.VALKOINEN)
                        pelialue.blit(bfg_teksti_surface, (self.pelaaja.x + 60, self.pelaaja.y - 50))

                    if not self.peli_kaynnissa:
                        if self.robotti_lkm <= 20 and self.xcom_aani.get_num_channels() > 0:
                            self.xcom_aani.stop()
                        if self.robotti_lkm > 120 and self.vikaloppari_lkm > 0 and not self.vikaloppari:
                            lopetus_teksti = "Voitit pelin"
                        else:
                            lopetus_teksti = "Hävisit pelin"
                        lopetus_surface = fontti.render(lopetus_teksti, True, self.VALKOINEN)
                        pelialue.blit(lopetus_surface, (pelialue_leveys // 2 - 100, pelialue_korkeus // 2))

                        ok_nappi = pygame.Rect(pelialue_leveys // 2 - 50, pelialue_korkeus // 2 + 50, 100, 50)
                        pygame.draw.rect(pelialue, self.VALKOINEN, ok_nappi)
                        ok_teksti = fontti.render("OK", True, self.MUSTA)
                        pelialue.blit(ok_teksti, (pelialue_leveys // 2 - ok_teksti.get_width() // 2, pelialue_korkeus // 2 + 60))

                        naytto.blit(pelialue, (0, 0))
                        naytto.blit(pistealue, (pelialue_leveys, 0))
                        self.pelaaja.piirra(naytto)
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
                        parhaat_pisteet = self.lataa_parhaat_pisteet()
                        if len(parhaat_pisteet) < 10 or self.pisteet > parhaat_pisteet[-1][1]:
                            nimi = self.nayta_pisteiden_syotto(self.pisteet)
                            parhaat_pisteet.append((nimi, self.pisteet))
                            parhaat_pisteet.sort(key=lambda x: x[1], reverse=True)
                            parhaat_pisteet = parhaat_pisteet[:10]
                            self.tallenna_parhaat_pisteet(parhaat_pisteet)
                        if self.tasomusiikit:
                            self.tasomusiikit.stop()
                    else:
                        naytto.blit(pelialue, (0, 0))
                        naytto.blit(pistealue, (pelialue_leveys, 0))
                        self.liikuta_pelaajaa()
                        self.pelaaja.piirra(naytto)
                        pygame.display.flip()
                        self.kello.tick(60)

class Pelaaja:
    def __init__(self, x, y, animaatio_vasemmalle, animaatio_oikealle):
        self.x = x
        self.y = y
        self.leveys = 33
        self.korkeus = 123
        self.suunta = 'seisoo'
        self.animaatio_vasemmalle = animaatio_vasemmalle
        self.animaatio_oikealle = animaatio_oikealle
        self.animaatio_indeksi = 0

    def liiku(self, dx, dy):
        self.x += dx
        self.y += dy
        self.suunta = 'vasen' if dx < 0 else 'oikea'

    def seisoo(self):
        self.suunta = 'seisoo'
        self.animaatio_indeksi = 0

    def piirra(self, naytto):
        if self.suunta == 'seisoo':
            naytto.blit(self.animaatio_vasemmalle[0], (self.x, self.y - 61))
        elif self.suunta == 'vasen':
            naytto.blit(self.animaatio_vasemmalle[self.animaatio_indeksi // 5], (self.x, self.y - 61))
            self.animaatio_indeksi = (self.animaatio_indeksi + 1) % (len(self.animaatio_vasemmalle) * 5)
        elif self.suunta == 'oikea':
            naytto.blit(self.animaatio_oikealle[self.animaatio_indeksi // 5], (self.x, self.y - 61))
            self.animaatio_indeksi = (self.animaatio_indeksi + 1) % (len(self.animaatio_oikealle) * 5)

class Ammus:
    def __init__(self, x, y, suunta, kuva):
        self.x = x
        self.y = y
        self.suunta = suunta
        self.kuva = kuva
        self.tuhottu = False
        self.rect = pygame.Rect(self.x, self.y, 20, 10)

    def paivita(self):
        if self.suunta == "ylös":
            self.y -= 10
        elif self.suunta == "vasen":
            self.x -= 10
        elif self.suunta == "oikea":
            self.x += 10
        if self.y < 0 or self.x < 0 or self.x > 1200 - 200:   
            self.tuhottu = True
        self.rect = pygame.Rect(self.x, self.y, 20, 10)

    def piirra(self, naytto):
        naytto.blit(self.kuva, (self.x, self.y))

def main():
    peli = Peli()
    peli.suorita()

if __name__ == "__main__":
    main()
