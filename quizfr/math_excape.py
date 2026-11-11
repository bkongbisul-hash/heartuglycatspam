import random
import sys
import pygame


pygame.init()
pygame.mixer.init()


info = pygame.display.Info()
LEBAR, TINGGI = info.current_w, info.current_h
layar = pygame.display.set_mode((LEBAR, TINGGI), pygame.FULLSCREEN)
pygame.display.set_caption("Math Escape Challenge")

# Warna
PUTIH = (255, 255, 255)
HITAM = (0, 0, 0)
HIJAU = (46, 204, 113)
MERAH = (231, 76, 60)
KUNING = (241, 196, 15)


font_soal = pygame.font.SysFont("Arial", 48, bold=True)
font_sub = pygame.font.SysFont("Arial", 28)


try:
  gambar_raw = pygame.image.load("quizfr/plankton.png")
  gambar = pygame.transform.scale(gambar_raw, (120, 120))
except Exception:
  gambar = pygame.Surface((120, 120))
  gambar.fill(KUNING)

# --- LOAD BACKGROUND IMAGE ---
try:
  bg_raw = pygame.image.load("quizfr/spongebobcreep.png")
  background_img = pygame.transform.scale(bg_raw, (LEBAR, TINGGI))
except Exception:
  background_img = None

# --- SISTEM MULTI-SPAWN GAMBAR ---
daftar_gambar = []
MAX_GAMBAR = 250  
WAKTU_SPAWN = 1000  
waktu_terakhir_spawn = pygame.time.get_ticks()


def spawn_gambar_baru():
  if len(daftar_gambar) < MAX_GAMBAR:
    x = random.randint(50, max(50, LEBAR - 170))
    y = random.randint(50, max(50, TINGGI - 170))
    vx = random.choice([-7, -6, 6, 7])
    vy = random.choice([-7, -6, 6, 7])
    daftar_gambar.append({"x": x, "y": y, "vx": vx, "vy": vy})


# Masukkan 1 gambar pertama saat awal program berjalan
spawn_gambar_baru()

try:
  pygame.mixer.music.load("quizfr/planktonsong.mp3")
  pygame.mixer.music.play(-1)  # -1 artinya putar terus tanpa henti (looping)
except Exception:
  pass


# 4. Fungsi Generator Soal Matematika
def buat_soal():
  op = random.choice(["+", "-", "*"])
  if op == "+":
    a, b = random.randint(5, 50), random.randint(5, 50)
    ans = a + b
  elif op == "-":
    a = random.randint(10, 50)
    b = random.randint(1, a)
    ans = a - b
  else:  # Perkalian mudah
    a, b = random.randint(2, 9), random.randint(2, 9)
    ans = a * b
  return f"{a} {op} {b} = ?", str(ans)


# Variabel Status Game
soal_teks, jawaban_benar = buat_soal()
input_user = ""
skor_benar = 0
target_skor = 5
pesan_status = "Jawab 5 soal dengan benar untuk keluar!"
warna_pesan = PUTIH

# 5. Main Game Loop
clock = pygame.time.Clock()
running = True

while running:
  clock.tick(60)  # 60 FPS
  waktu_sekarang = pygame.time.get_ticks()

  # Cek pewaktu untuk menambah gambar baru setiap 1 detik
  if waktu_sekarang - waktu_terakhir_spawn >= WAKTU_SPAWN:
    spawn_gambar_baru()
    waktu_terakhir_spawn = waktu_sekarang

  # Event Handling
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pass

    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_RETURN:
        # Cek Jawaban saat tekan Enter
        if input_user.strip() == jawaban_benar:
          skor_benar += 1
          pesan_status = f"BENAR! ({skor_benar}/{target_skor})"
          warna_pesan = HIJAU
          if skor_benar >= target_skor:
            running = False  # Keluar dari loop / menang!
          else:
            soal_teks, jawaban_benar = buat_soal()
        else:
          skor_benar = 0  # Reset jika salah!
          pesan_status = "SALAH! Skor di-reset ke 0. Coba lagi!"
          warna_pesan = MERAH
          soal_teks, jawaban_benar = buat_soal()

        input_user = ""

      elif event.key == pygame.K_BACKSPACE:
        input_user = input_user[:-1]
      else:
        # Hanya menerima angka dan minus
        if event.unicode.isdigit() or event.unicode == "-":
          input_user += event.unicode

  # Pergerakan semua gambar yang aktif (memantul di dinding layar)
  for item in daftar_gambar:
    item["x"] += item["vx"]
    item["y"] += item["vy"]

    if item["x"] <= 0 or item["x"] + 120 >= LEBAR:
      item["vx"] *= -1
    if item["y"] <= 0 or item["y"] + 120 >= TINGGI:
      item["vy"] *= -1

  # Render Visual (Background)
  if background_img:
    layar.blit(background_img, (0, 0))
  else:
    layar.fill((50, 50, 50))  # Warna abu-abu cadangan jika gambar bg tidak ketemu

  # Gambar semua karakter yang ada di daftar
  for item in daftar_gambar:
    layar.blit(gambar, (item["x"], item["y"]))

  # Tampilan Interface (Kotak UI Soal)
  kotak_ui = pygame.Rect(LEBAR // 2 - 300, TINGGI // 2 - 180, 600, 360)
  pygame.draw.rect(layar, (30, 30, 30), kotak_ui, border_radius=15)
  pygame.draw.rect(layar, PUTIH, kotak_ui, width=3, border_radius=15)

  # Teks Header & Status
  txt_status = font_sub.render(pesan_status, True, warna_pesan)
  layar.blit(txt_status, txt_status.get_rect(center=(LEBAR // 2, TINGGI // 2 - 130)))

  # Teks Soal
  txt_soal = font_soal.render(soal_teks, True, KUNING)
  layar.blit(txt_soal, txt_soal.get_rect(center=(LEBAR // 2, TINGGI // 2 - 50)))

  # Kotak Input Jawaban
  kotak_input = pygame.Rect(LEBAR // 2 - 150, TINGGI // 2 + 20, 300, 60)
  pygame.draw.rect(layar, PUTIH, kotak_input, border_radius=10)
  txt_input = font_soal.render(input_user, True, HITAM)
  layar.blit(txt_input, txt_input.get_rect(center=kotak_input.center))

  # Petunjuk Tekan Enter
  txt_hint = font_sub.render("Ketik angka lalu tekan ENTER", True, (150, 150, 150))
  layar.blit(txt_hint, txt_hint.get_rect(center=(LEBAR // 2, TINGGI // 2 + 120)))

  pygame.display.flip()

# Stop audio dan keluar setelah berhasil
pygame.mixer.music.stop()
pygame.quit()
sys.exit()