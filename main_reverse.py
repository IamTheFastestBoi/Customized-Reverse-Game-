import pygame
import sys

# oyunun pygame arayuzu yapay zeka ile yapildi .

class OyunMotoru:
    def __init__(self , oyunTahtasi , oyuncuPC , oyuncuInsan):
        self.oyuncuPC = oyuncuPC
        self.oyuncuInsan = oyuncuInsan
        self.oyunTahtasi = oyunTahtasi
        self.hakem = Hakem(oyunTahtasi)
        self.zeka = Zeka(-1 , oyunTahtasi=self.oyunTahtasi)
        pygame.init()
        self.KARE_BOYUTU = 80 
        self.GENISLIK = self.KARE_BOYUTU * 8
        self.YUKSEKLIK = self.KARE_BOYUTU * 8
        self.ekran = pygame.display.set_mode((self.GENISLIK, self.YUKSEKLIK))
        pygame.display.set_caption("Serbest Yerleşim Reversi")
        self.RENK_ZEMIN = (34, 139, 34) 
        self.RENK_CIZGI = (0, 0, 0)     
        self.RENK_INSAN = (0, 0, 0)     
        self.RENK_PC = (255, 255, 255)
    def draw_board(self):
        self.ekran.fill(self.RENK_ZEMIN) 
        
    
        for i in range(9):
            pygame.draw.line(self.ekran, self.RENK_CIZGI, (0, i * self.KARE_BOYUTU), (self.GENISLIK, i * self.KARE_BOYUTU), 2)
            pygame.draw.line(self.ekran, self.RENK_CIZGI, (i * self.KARE_BOYUTU, 0), (i * self.KARE_BOYUTU, self.YUKSEKLIK), 2)
            
        
        for i in range(8):
            for j in range(8):
                kare_degeri = self.oyunTahtasi.oyunTahtasi[i][j]
                
                merkez_x = j * self.KARE_BOYUTU + self.KARE_BOYUTU // 2
                merkez_y = i * self.KARE_BOYUTU + self.KARE_BOYUTU // 2
                yaricap = self.KARE_BOYUTU // 2 - 5
                
                if kare_degeri == 1:
                    pygame.draw.circle(self.ekran, self.RENK_INSAN, (merkez_x, merkez_y), yaricap)
                elif kare_degeri == -1:
                    pygame.draw.circle(self.ekran, self.RENK_PC, (merkez_x, merkez_y), yaricap)
        pygame.display.flip() 
    def hamleYap_Oyuncu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    fare_x, fare_y = event.pos
                    self.Oyuncu_inputHamle_y = fare_x // self.KARE_BOYUTU
                    self.Oyuncu_inputHamle_x = fare_y // self.KARE_BOYUTU
                    
                    if 0 <= self.Oyuncu_inputHamle_x < 8 and 0 <= self.Oyuncu_inputHamle_y < 8:
                        return (self.Oyuncu_inputHamle_x, self.Oyuncu_inputHamle_y)

    def hamleYap_PC(self , x, y):
        self.PC_inputHamle_x = x
        self.PC_inputHamle_y = y
        return (self.PC_inputHamle_x , self.PC_inputHamle_y)
    def hamleKontrol_Oyuncu(self):
        if self.oyunTahtasi.oyunTahtasi[self.Oyuncu_inputHamle_x][self.Oyuncu_inputHamle_y] == 0:
            return True
        else:
            return False
    def hamleKontrol_PC(self):
        if self.oyunTahtasi.oyunTahtasi[self.PC_inputHamle_x][self.PC_inputHamle_y] == 0:
            return True
        else:
            return False    
    def oyunmotoru(self):
        while True:
            self.draw_board()
            while True:
                self.hamleYap_Oyuncu()
                if self.hamleKontrol_Oyuncu() == True:
                    self.oyunTahtasi.oyunTahtasi[self.Oyuncu_inputHamle_x][self.Oyuncu_inputHamle_y] = 1
                    self.hakem.reverse(self.Oyuncu_inputHamle_x , self.Oyuncu_inputHamle_y , 1) 
                    break
                else:
                    print("Geçersiz hamle! Lütfen tekrar deneyin.")
                    continue
            self.draw_board()
            print("PC dusunuyor...")
            pc_hedef_x, pc_hedef_y = self.zeka.calculate_best_move()
            if pc_hedef_x is not None and pc_hedef_y is not None:
                self.hamleYap_PC(pc_hedef_x, pc_hedef_y)
                if self.hamleKontrol_PC() == True:
                    print(f"PC hamlesi: ({self.PC_inputHamle_x}, {self.PC_inputHamle_y})")
                    self.oyunTahtasi.oyunTahtasi[self.PC_inputHamle_x][self.PC_inputHamle_y] = -1
                    self.hakem.reverse(self.PC_inputHamle_x, self.PC_inputHamle_y, -1)
            else:
                print("PC için geçerli bir hamle bulunamadı.")
                break
            bos_var, insan_skor, pc_skor = self.oyunTahtasi.skor_ve_bitis_kontrol()
            if not bos_var:
                print(f"\nOyun Bitti! Tahta tamamen doldu.")
                print(f"Senin Skorun (X): {insan_skor}")
                print(f"Bilgisayarın Skoru (O): {pc_skor}")
                if insan_skor > pc_skor:
                    print("Tebrikler, Kazandın! 🏆")
                elif pc_skor > insan_skor:
                    print("Bilgisayar Kazandı! 🤖")
                else:
                    print("Oyun Berabere! 🤝")
                break


class Hakem:    
    def __init__(self , oyunTahtasi):
        self.oyunTahtasi = oyunTahtasi
        self.vectors = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)]
        self.oyuncu = 1
        self.pc = -1
    def reverse(self , x , y , currentPlayer):
        otherPlayer = currentPlayer * -1
        for dx , dy in self.vectors:
            temporaryList = []
            vectorX = x + dx
            vectorY = y + dy
            while 0 <= vectorX < 8 and 0 <= vectorY < 8:
                checked_value = self.oyunTahtasi.oyunTahtasi[vectorX][vectorY]
                if checked_value == otherPlayer:
                    temporaryList.append((vectorX , vectorY))
                    vectorX += dx
                    vectorY += dy
                elif checked_value == currentPlayer:
                    if len(temporaryList) > 0:
                        for reverseX , reverseY in temporaryList:
                            self.oyunTahtasi.oyunTahtasi[reverseX][reverseY] = currentPlayer
                    break
                else:
                    break

class Zeka:
    def __init__(self, pc_renk , oyunTahtasi):
        self.pc_renk = pc_renk
        self.oyuncu = pc_renk * -1
        self.oyunTahtasi = oyunTahtasi
        self.puan_haritasi = [
            [ 100, -20,  10,   5,   5,  10, -20,  100],
            [ -20, -50,  -2,  -2,  -2,  -2, -50, -20],
            [  10,  -2,  -1,  -1,  -1,  -1,  -2,   10],
            [   5,  -2,  -1,  -1,  -1,  -1,  -2,    5],
            [   5,  -2,  -1,  -1,  -1,  -1,  -2,    5],
            [  10,  -2,  -1,  -1,  -1,  -1,  -2,   10],
            [ -20, -50,  -2,  -2,  -2,  -2, -50, -20],
            [ 100, -20,  10,   5,   5,  10, -20,  100]
        ]
    def virtual_calculation(self , i , j):
        vectors = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)]
        count_of_reversed = 0
        for dx , dy in vectors:
            temporaryReverse = 0
            vectorX = i + dx
            vectorY = j + dy
            while 0 <= vectorX < 8 and 0 <= vectorY < 8:
                checked_value = self.oyunTahtasi.oyunTahtasi[vectorX][vectorY]
                if checked_value == self.oyuncu:
                    temporaryReverse += 1
                    vectorX += dx
                    vectorY += dy
                elif checked_value == self.pc_renk:
                    if temporaryReverse > 0:
                        count_of_reversed += temporaryReverse
                    break
                else:
                    break
        return count_of_reversed
    def calculate_best_move(self):
        self.update_map()
        best_score = -9999
        best_move = ( None , None)
        for i in range(8):
            for j in range(8):
                if self.oyunTahtasi.oyunTahtasi[i][j] == 0:
                    score = self.puan_haritasi[i][j] 
                    reverse_points = self.virtual_calculation(i , j)* 10
                    total_score = score + reverse_points
                    if total_score > best_score:
                        best_score = total_score
                        best_move = (i , j)
        return best_move
    def update_map(self):
        if self.oyunTahtasi.oyunTahtasi[0][0] == self.pc_renk:
            self.puan_haritasi[0][1] = 20
            self.puan_haritasi[1][0] = 20
            self.puan_haritasi[1][1] = 30 

        if self.oyunTahtasi.oyunTahtasi[0][7] == self.pc_renk:
            self.puan_haritasi[0][6] = 20
            self.puan_haritasi[1][7] = 20
            self.puan_haritasi[1][6] = 30

        if self.oyunTahtasi.oyunTahtasi[7][0] == self.pc_renk:
            self.puan_haritasi[6][0] = 20
            self.puan_haritasi[7][1] = 20
            self.puan_haritasi[6][1] = 30 

        if self.oyunTahtasi.oyunTahtasi[7][7] == self.pc_renk:
            self.puan_haritasi[7][6] = 20
            self.puan_haritasi[6][7] = 20
            self.puan_haritasi[6][6] = 30

class OyunTahtasi:
    def __init__(self):
        self.oyunTahtasi = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
    def initialize_board(self):
        print("\n 0 1 2 3 4 5 6 7")
        for i in range(8):
            row = str(i) + " "
            for j in range(8):
                if self.oyunTahtasi[i][j] == 1:
                    row += "X "
                elif self.oyunTahtasi[i][j] == -1:
                    row += "O "
                else:
                    row += ". "
            print(row)
        print("-" * 20)
    def skor_ve_bitis_kontrol(self):
        bos_yer_var = False
        insan_puan = 0
        pc_puan = 0
        
        for i in range(8):
            for j in range(8):
                if self.oyunTahtasi[i][j] == 0:
                    bos_yer_var = True
                elif self.oyunTahtasi[i][j] == 1:
                    insan_puan += 1
                elif self.oyunTahtasi[i][j] == -1:
                    pc_puan += 1
                    
        return bos_yer_var, insan_puan, pc_puan

if __name__ == "__main__":
    tahta = OyunTahtasi()
    motor = OyunMotoru(tahta, oyuncuPC=-1, oyuncuInsan=1)
    print("Oyun Başladı!")
    motor.oyunmotoru()




# Bir sınıfı (class) çağırıp ondan bir nesne (object) yarattığın anda, o şey dünyaya tam takım bir paket olarak gelir. Yani sen self.hakem = Hakem(...) dediğinde, o Hakem senin Motor'unun içine şu üç şeyi çantasına koyup gelir:
# Kendi Değişkenleri (Nesneleri): Örneğin self.vectors, self.oyuncu gibi kendi hafızasında tuttuğu veriler.
# Kendi Yetenekleri (Fonksiyonları): Örneğin reverse() ve update_map() gibi yapabildiği özel işler.
# Kendi Kuralları (Parametre İstekleri): Hakem, "Benim reverse yeteneğimi kullanacaksan reverse yetenegime zorunlu olarak x, y, currentPlayer vereceksin, yoksa çalışmam!" kuralını (imzasını) da yanında getirir ve senden bunu harfiyen talep eder.