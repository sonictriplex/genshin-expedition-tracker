import json
import os
import urllib.request

# Vollständige Liste aller Genshin Impact Charaktere mit Fandom-Dateinamen
FANDOM_FILES = {
    # --- Mondstadt ---
    "Albedo": "Character_Albedo_Thumb.png",
    "Amber": "Character_Amber_Thumb.png",
    "Barbara": "Character_Barbara_Thumb.png",
    "Bennett": "Character_Bennett_Thumb.png",
    "Diluc": "Character_Diluc_Thumb.png",
    "Diona": "Character_Diona_Thumb.png",
    "Eula": "Character_Eula_Thumb.png",
    "Fischl": "Character_Fischl_Thumb.png",
    "Jean": "Character_Jean_Thumb.png",
    "Kaeya": "Character_Kaeya_Thumb.png",
    "Klee": "Character_Klee_Thumb.png",
    "Lisa": "Character_Lisa_Thumb.png",
    "Mona": "Character_Mona_Thumb.png",
    "Mika": "Character_Mika_Thumb.png",
    "Noelle": "Character_Noelle_Thumb.png",
    "Razor": "Character_Razor_Thumb.png",
    "Rosaria": "Character_Rosaria_Thumb.png",
    "Sucrose": "Character_Sucrose_Thumb.png",
    "Venti": "Character_Venti_Thumb.png",
    # --- Liyue ---
    "Beidou": "Character_Beidou_Thumb.png",
    "Chongyun": "Character_Chongyun_Thumb.png",
    "Ganyu": "Character_Ganyu_Thumb.png",
    "Gaming": "Character_Gaming_Thumb.png",
    "Hu Tao": "Character_Hu_Tao_Thumb.png",
    "Keqing": "Character_Keqing_Thumb.png",
    "Lanyan": "Character_Lan_Yan_Thumb.png",
    "Ningguang": "Character_Ningguang_Thumb.png",
    "Qiqi": "Character_Qiqi_Thumb.png",
    "Shenhe": "Character_Shenhe_Thumb.png",
    "Xiangling": "Character_Xiangling_Thumb.png",
    "Xianyun": "Character_Xianyun_Thumb.png",
    "Xiao": "Character_Xiao_Thumb.png",
    "Xingqiu": "Character_Xingqiu_Thumb.png",
    "Xinyan": "Character_Xinyan_Thumb.png",
    "Yanfei": "Character_Yanfei_Thumb.png",
    "Yelan": "Character_Yelan_Thumb.png",
    "Yao Yao": "Character_Yaoyao_Thumb.png",
    "Yun Jin": "Character_Yun_Jin_Thumb.png",
    "Zhongli": "Character_Zhongli_Thumb.png",
    # --- Inazuma ---
    "Arataki Itto": "Character_Arataki_Itto_Thumb.png",
    "Chiori": "Character_Chiori_Thumb.png",
    "Gorou": "Character_Gorou_Thumb.png",
    "Kaedehara Kazuha": "Character_Kaedehara_Kazuha_Thumb.png",
    "Kamisato Ayaka": "Character_Kamisato_Ayaka_Thumb.png",
    "Kamisato Ayato": "Character_Kamisato_Ayato_Thumb.png",
    "Kujou Sara": "Character_Kujou_Sara_Thumb.png",
    "Kuki Shinobu": "Character_Kuki_Shinobu_Thumb.png",
    "Kirara": "Character_Kirara_Thumb.png",
    "Raiden Shogun": "Character_Raiden_Shogun_Thumb.png",
    "Sayu": "Character_Sayu_Thumb.png",
    "Sangonomiya Kokomi": "Character_Sangonomiya_Kokomi_Thumb.png",
    "Shikanoin Heizou": "Character_Shikanoin_Heizou_Thumb.png",
    "Thoma": "Character_Thoma_Thumb.png",
    "Yae Miko": "Character_Yae_Miko_Thumb.png",
    "Yoimiya": "Character_Yoimiya_Thumb.png",
    # --- Sumeru ---
    "Alhaitham": "Character_Alhaitham_Thumb.png",
    "Candace": "Character_Candace_Thumb.png",
    "Collei": "Character_Collei_Thumb.png",
    "Cyno": "Character_Cyno_Thumb.png",
    "Dehya": "Character_Dehya_Thumb.png",
    "Dori": "Character_Dori_Thumb.png",
    "Faruzan": "Character_Faruzan_Thumb.png",
    "Kaveh": "Character_Kaveh_Thumb.png",
    "Layla": "Character_Layla_Thumb.png",
    "Nahida": "Character_Nahida_Thumb.png",
    "Nilou": "Character_Nilou_Thumb.png",
    "Sethos": "Character_Sethos_Thumb.png",
    "Tighnari": "Character_Tighnari_Thumb.png",
    "Wanderer": "Character_Wanderer_Thumb.png",
    # --- Fontaine ---
    "Arlecchino": "Character_Arlecchino_Thumb.png",
    "Charlotte": "Character_Charlotte_Thumb.png",
    "Chevreuse": "Character_Chevreuse_Thumb.png",
    "Clorinde": "Character_Clorinde_Thumb.png",
    "Emilie": "Character_Emilie_Thumb.png",
    "Freminet": "Character_Freminet_Thumb.png",
    "Furina": "Character_Furina_Thumb.png",
    "Lynette": "Character_Lynette_Thumb.png",
    "Lyney": "Character_Lyney_Thumb.png",
    "Navia": "Character_Navia_Thumb.png",
    "Neuvillette": "Character_Neuvillette_Thumb.png",
    "Sigewinne": "Character_Sigewinne_Thumb.png",
    "Wriothesley": "Character_Wriothesley_Thumb.png",
    # --- Natlan ---
    "Chasca": "Character_Chasca_Thumb.png",
    "Citlali": "Character_Citlali_Thumb.png",
    "Iansan": "Character_Iansan_Thumb.png",
    "Kachina": "Character_Kachina_Thumb.png",
    "Kinich": "Character_Kinich_Thumb.png",
    "Mavuika": "Character_Mavuika_Thumb.png",
    "Mualani": "Character_Mualani_Thumb.png",
    "Ororon": "Character_Ororon_Thumb.png",
    "Xilonen": "Character_Xilonen_Thumb.png",
    # --- Sonstige ---
    "Aloy": "Character_Aloy_Thumb.png",
    "Traveller": "Character_Traveler_Thumb.png",
}

output_dir = "assets/characters"
os.makedirs(output_dir, exist_ok=True)

print("Starte Download über Fandom MediaWiki API...\n")

success_count = 0
fail_count = 0

for char_name, filename in FANDOM_FILES.items():
  file_path = os.path.join(
      output_dir, f"{char_name.lower().replace(' ', '_')}.png"
  )

  # Überspringen, falls das Bild schon existiert
  if os.path.exists(file_path):
    print(f"➜ [{char_name}] bereits vorhanden")
    success_count += 1
    continue

  api_url = f"https://genshin-impact.fandom.com/api.php?action=query&titles=File:{filename}&prop=imageinfo&iiprop=url&format=json"

  try:
    req = urllib.request.Request(
        api_url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
    )
    with urllib.request.urlopen(req) as resp:
      data = json.loads(resp.read().decode("utf-8"))
      pages = data["query"]["pages"]
      page_id = list(pages.keys())[0]

      if page_id == "-1" or "imageinfo" not in pages[page_id]:
        print(f"✗ [{char_name}] Datei nicht gefunden ({filename})")
        fail_count += 1
        continue

      image_url = pages[page_id]["imageinfo"][0]["url"]

    img_req = urllib.request.Request(
        image_url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
    )
    with (
        urllib.request.urlopen(img_req) as img_resp,
        open(file_path, "wb") as out_file,
    ):
      out_file.write(img_resp.read())

    print(f"✓ [{char_name}] neu gespeichert -> {file_path}")
    success_count += 1

  except Exception as e:
    print(f"✗ [{char_name}] Fehler: {e}")
    fail_count += 1

print(
    f"\nFertig! {success_count} verarbeitet/vorhanden, {fail_count}"
    " Fehlgeschlagen."
)
