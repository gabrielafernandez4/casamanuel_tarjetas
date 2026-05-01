import qrcode
import os

base_url = "https://acasamanuel.onrender.com/cliente/"

for i in range (1,401):
    id_cliente=str(i).zfill(3)

    url = base_url + id_cliente

    qr = qrcode.make(url)

    qr.save(f"qrs/cliente_{id_cliente}.png")

print("400 QR generados correctamente")