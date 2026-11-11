import sys
import cv2
import pygame


pygame.init()
pygame.mixer.init()


info = pygame.display.Info()
LEBAR, TINGGI = info.current_w, info.current_h
layar = pygame.display.set_mode((LEBAR, TINGGI), pygame.FULLSCREEN)
pygame.display.set_caption("Face Cam Backsound Challenge")


PUTIH = (255, 255, 255)
HITAM = (0, 0, 0)
HIJAU = (46, 204, 113)
font_teks = pygame.font.SysFont("Arial", 36, bold=True)


cap = cv2.VideoCapture(0)


try:
  pygame.mixer.music.load("youuu/beauty.mp3")  
  pygame.mixer.music.play(-1)  
except Exception as e:
  print("Gagal memutar musik:", e)

# Main Game Loop
clock = pygame.time.Clock()
running = True

while running:
  clock.tick(60)  # 60 FPS

  # frame kamera laptop
  ret, frame = cap.read()
  
  # Variabel surface untuk frame kamera
  frame_surface = None
  if ret and frame is not None:
    # efek cermin
    frame = cv2.flip(frame, 1)
    
    # frame video kamera agar pas menutupi layar
    frame = cv2.resize(frame, (LEBAR, TINGGI))
    
    # Konversi format warna dari OpenCV (BGR) ke RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    frame_rgb = cv2.transpose(frame_rgb)
    
    frame_surface = pygame.surfarray.make_surface(frame_rgb)

  # Event Handling (Tombol untuk keluar program, misal tekan ESC)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.KEYDOWN:
      # Tekan tombol ESC (Escape) di keyboard untuk keluar dari kamera & musik
      if event.key == pygame.K_ESCAPE:
        running = False

  if frame_surface is not None:
    layar.blit(frame_surface, (0, 0))  
  else:
    layar.fill(HITAM)

  teks_info = font_teks.render(
      "Kamera Aktif! Tekan 'ESC' di keyboard untuk keluar.", True, HIJAU
  )

  pygame.draw.rect(
      layar, (0, 0, 0), (LEBAR // 2 - 350, 30, 700, 50), border_radius=10
  )
  pygame.draw.rect(
      layar, PUTIH, (LEBAR // 2 - 350, 30, 700, 50), width=2, border_radius=10
  )
  layar.blit(teks_info, teks_info.get_rect(center=(LEBAR // 2, 55)))

  pygame.display.flip()


cap.release()
pygame.mixer.music.stop()
pygame.quit()
sys.exit()