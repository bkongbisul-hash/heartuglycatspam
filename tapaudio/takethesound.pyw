import random
import time
from plyer import notification
import pygame

# Daftar pesan atau teka-teki lucu yang akan muncul secara acak
pesan_kreatif = [
    {
        "title": "💡 Reminder Santai",
        "message": "Udah ngopi belum? Jangan lupa istirahat sejenak!",
    },
    {
        "title": "👾 Interupsi Sistem",
        "message": "Halo! Cuma mau ngecek apakah kamu masih fokus atau malah melamun.",
    },
    {
        "title": "🚀 Teka-teki Kilat",
        "message": (
            "Kenapa programmer suka pakai baju dingin? Karena Windows-nya"
            " kebuka!"
        ),
    },
    {
        "title": "✨ Motivasi Mini",
        "message": (
            "Kode error itu wajar, yang nggak wajar itu kalau menyerah sebelum"
            " ngopi."
        ),
    },
]


def putar_suara_pendek():
  """Fungsi opsional untuk memutar suara (pastikan ada file 'notif.mp3' di folder yang sama,

  atau bagian ini bisa dikomentari jika tidak butuh suara).
  """
  try:
    pygame.mixer.init()
    pygame.mixer.music.load("tapaudio/fartsound.mp3")  # Ganti dengan path file audio kamu
    pygame.mixer.music.play()
  except Exception:
    # Jika file suara tidak ada, program tetap berjalan tanpa error
    pass


def main_loop():
  # Program akan berjalan terus di background
  while True:
    # Tentukan jeda waktu acak antara 15 sampai 30 menit (dalam detik)
    # Untuk pengujian awal, bisa diubah jadi lebih cepat (misal: 10 - 20 detik)
    waktu_tunggu = random.randint(4, 10)
    time.sleep(waktu_tunggu)

    # Pilih pesan secara acak dari daftar
    pilihan = random.choice(pesan_kreatif)

    # Tampilkan notifikasi sistem
    notification.notify(
        title=pilihan["title"],
        message=pilihan["message"],
        app_name="Desktop Companion",
        timeout=5,  # Notifikasi otomatis hilang setelah 5 detik
    )

    # Putar efek suara (jika ada)
    putar_suara_pendek()


if __name__ == "__main__":
  # Jalankan loop utama
  try:
    main_loop()
  except KeyboardInterrupt:
    # Program berhenti jika dihentikan secara manual dari Task Manager / IDE
    pass