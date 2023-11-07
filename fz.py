import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

print("Heloo World")
#variabel input
permintaan = ctrl.Antecedent(np.arange(0, 6001, 1),'permintaan')
persediaan = ctrl.Antecedent(np.arange(0, 601, 1),'persediaan')

#variabel output
produksi = ctrl.Consequent(np.arange(0, 7001, 1), 'produksi')

#fungsi keanggotaan permintaaan
permintaan['turun'] = fuzz.trapmf(permintaan.universe, [-1,0, 500, 6000])
permintaan['naik'] = fuzz.trapmf(permintaan.universe, [500, 6000, 6000, 6001])

#fungsi keanggotaan persediaan
persediaan['sedikit'] = fuzz.trapmf(persediaan.universe, [-1, 0, 100, 600])
persediaan['banyak'] = fuzz.trapmf(persediaan.universe, [100, 600, 600, 601])

#fungsi keanggotaan produksi
produksi['berkurang'] = fuzz.trapmf(produksi.universe, [-1, 0, 2000, 7000])
produksi['bertambah'] = fuzz.trapmf(produksi.universe, [2000, 7000, 7000, 7001])

#rule
r1= ctrl.Rule(permintaan['turun'] & persediaan['banyak'], produksi['berkurang'])
r2= ctrl.Rule(permintaan['turun'] & persediaan['sedikit'], produksi['berkurang'])
r3= ctrl.Rule(permintaan['naik'] & persediaan['banyak'], produksi['bertambah'])
r4= ctrl.Rule(permintaan['naik'] & persediaan['sedikit'], produksi['bertambah'])

# Membuat sistem kontrol
sistem_pakar = ctrl.ControlSystem([r1,r2,r3,r4])

# Membuat simulasi sistem pakar
analisis_produksi = ctrl.ControlSystemSimulation(sistem_pakar)

# Memasukkan data permintaan dan persediaan
permintaan_input = int(input("Masukkan jumlah permintaan : "))
persediaan_input = int(input("Masukkan jumlah persediaan : "))

# Melakukan inferensi
analisis_produksi.input['permintaan'] = permintaan_input
analisis_produksi.input['persediaan'] = persediaan_input
analisis_produksi.compute()

# Mendapatkan output
banyak_produksi = analisis_produksi.output['produksi']

# Menampilkan hasil analisis
print(f"Hasil Analisis banyak produksi yang dibutuhkan: {banyak_produksi:.2f}")

plt.figure(1)
plt.plot(permintaan.universe, fuzz.trapmf(permintaan.universe, [-1,0, 500, 6000]), 'b', linewidth=1.5, label='turun')
plt.plot(permintaan.universe, fuzz.trapmf(permintaan.universe, [500, 6000, 7000, 7001]), 'g', linewidth=1.5, label='naik')
plt.title('Fungsi Keanggotaan Himpunan Fuzzy "permintaan"')
plt.ylabel('Derajat Keanggotaan')
plt.xlabel('jumlah permintaan')
plt.legend()
plt.show()
plt.figure(2)
plt.plot(persediaan.universe, fuzz.trapmf(persediaan.universe, [-1, 0, 100, 600]), 'b', linewidth=1.5, label='sedikit')
plt.plot(persediaan.universe, fuzz.trapmf(persediaan.universe, [100, 600, 1000, 1001]), 'g', linewidth=1.5, label='banyak')
plt.title('Fungsi Keanggotaan Himpunan Fuzzy "persediaan"')
plt.ylabel('Derajat Keanggotaan')
plt.xlabel('jumlah persediaan')
plt.legend()
plt.show()
plt.figure(3)
plt.plot(produksi.universe, fuzz.trapmf(produksi.universe, [-1, 0, 2000, 7000]), 'b', linewidth=1.5, label='berkurang')
plt.plot(produksi.universe, fuzz.trapmf(produksi.universe, [2000, 7000, 8000, 8001]), 'g', linewidth=1.5, label='bertambah')
plt.title('Fungsi Keanggotaan Himpunan Fuzzy "produksi"')
plt.ylabel('Derajat Keanggotaan')
plt.xlabel('jumlah produksi')
plt.legend()
plt.show()
produksi.view(sim=analisis_produksi)