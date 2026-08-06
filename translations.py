# --- ZENTRALES SPRACH- UND ÜBERSETZUNGSSYSTEM ---

CURRENT_LANGUAGE = "Deutsch"

TRANSLATIONS = {
    "English": {
        # General & App
        "app_title": "Genshin Impact Tracker",
        "theme": "Theme:",
        "language": "Language / Sprache:",
        "sys_settings": "System Settings",
        "autostart": "Start with System (Autostart)",
        "close_behavior": "Window Close Behavior (✕):",
        "close_tray": "Minimize to System Tray",
        "close_exit": "Exit Application Completely",
        "exp_finished": "The expedition of {char} has finished!",
        "exp_complete_title": "Expedition Complete",
        "tray_running": "Running in background.",
        "tray_open": "Open Tracker",
        "tray_quit": "Quit",

        # Navigation Tooltips & Main Titles
        "nav_expeditions": "Expeditions",
        "nav_journal": "Teyvat Journal",
        "nav_crafting": "Crafting Calculator",
        "nav_wishes": "Wish & Pity Counter",
        "nav_resin": "Resin Planner",
        "nav_bosses": "Weekly Boss Tracker",
        "nav_team": "Team & Farming Goals",
        "nav_settings": "Settings",

        "title_expeditions": "Active Expeditions",
        "title_journal": "Teyvat Journal & HQ Operations",
        "title_crafting": "Alchemy & Crafting Bench Calculator",
        "title_wishes": "Wish & Pity Savings Counter",
        "title_resin": "Original Resin Overflow & Cap Planner",
        "title_bosses": "Weekly Boss Discount & Claim Tracker",
        "title_team": "Team Building & Farming Goals",
        "title_settings": "Settings & Preferences",

        # Regions
        "reg_mondstadt": "Mondstadt",
        "reg_liyue": "Liyue",
        "reg_inazuma": "Inazuma",
        "reg_sumeru": "Sumeru",
        "reg_fontaine": "Fontaine",
        "reg_natlan": "Natlan",

        # Common Actions & Buttons
        "start_new": "+ Start New Expedition",
        "limit_reached": "Limit Reached ({count}/5 Expeditions)",
        "ready": "READY!",
        "running": "Running",
        "claim_reward": "Claim Reward",
        "cancel": "Cancel",
        "confirm": "OK",
        "delete": "Delete",
        "edit": "Edit",
        "save": "Save",

        # Resources
        "res_mora": "Mora",
        "res_ores": "Ores (Iron & Crystal)",
        "res_meat": "Meat & Fowl",
        "res_plants": "Ingredients & Plants",
        "res_fish": "Fish",

        # Crafting Calculator
        "craft_title": "🧪 Alchemy & Crafting Bench Calculator",
        "craft_passive": "Crafting Passive (Char Bonus):",
        "craft_passive_none": "None (Standard 3:1)",
        "craft_passive_double": "Sucrose / Albedo (10% Chance for 2x Product)",
        "craft_passive_refund": "Mona / Xingqiu (25% Chance to Refund Material)",
        "craft_inventory": "CURRENT INVENTORY:",
        "craft_t1": "🟢 Tier 1 (Green / 2★):",
        "craft_t2": "🔵 Tier 2 (Blue / 3★):",
        "craft_t3": "🟣 Tier 3 (Purple / 4★):",
        "craft_summary": "CRAFTING SUMMARY & OUTPUT",
        "craft_out_t2": "🔵 Total Blue Materials (3★): <b>{total}</b> <span style='color: #aaa;'>(+ {crafted} crafted)</span>",
        "craft_out_t3": "🟣 Max Purple Materials (4★): <b>{total}</b> <span style='color: #aaa;'>(+ {crafted} crafted)</span>",
        "craft_mora": "💰 Estimated Crafting Cost: <b style='color: {color};'>{mora:,} Mora</b>",

        # Dialogs
        "dlg_add_title": "New Expedition",
        "dlg_char": "Character:",
        "dlg_region": "Region:",
        "dlg_resource": "Resource:",
        "dlg_duration": "Duration:",
        "dlg_dur_4h": "4 Hours",
        "dlg_dur_8h": "8 Hours",
        "dlg_dur_12h": "12 Hours",
        "dlg_dur_20h": "20 Hours (Standard)",
        "dlg_dur_3h_bonus": "3 Hours (Bonus 4h)",
        "dlg_dur_6h_bonus": "6 Hours (Bonus 8h)",
        "dlg_dur_9h_bonus": "9 Hours (Bonus 12h)",
        "dlg_dur_15h_bonus": "15 Hours (Bonus 20h)",
        "dlg_start": "Start",
        "dlg_resin_title": "Adjust Original Resin",
        "dlg_current_resin": "Current Resin:",
        "dlg_save": "Save",
        "dlg_settings_title": "⚙️ Settings",
        "dlg_edit_time_title": "Adjust Time ({char})",
        "dlg_remaining_time": "Remaining Time:",

        # Teyvat Journal
        "jnl_title": "📖 Teyvat Travel Journal & Checklists",
        "jnl_ar": "Adventure Rank (AR):",
        "jnl_ar_tooltip": "Unlocks features based on your Adventure Rank.",
        "jnl_commissions": "DAILY COMMISSIONS",
        "jnl_katheryne": "🎁 Katheryne",
        "jnl_bosses_rot": "WEEKLY BOSSES & ROTATION",
        "jnl_boss_num": "Boss #{num}",
        "jnl_pot_title": "SERENITEA POT (UNLOCKED AT AR 28)",
        "jnl_pot_resin": "Transient Resin",
        "jnl_pot_books": "XP/Books",
        "jnl_pot_arte": "Artifact Coins",
        "jnl_trans_title": "PARAMETRIC TRANSFORMER (UNLOCKED AT AR 31)",
        "jnl_trans_btn": "Use Now (7d)",
        "jnl_art_title": "ARTIFACT ROUTE (UNLOCKED AT AR 45)",
        "jnl_art_btn": "Route Finished",
        "jnl_art_ready": "Ready to Farm!",
        "jnl_endgame_title": "ENDGAME STARS (UNLOCKED AT AR 45)",
        "jnl_abyss": "Abyss:",
        "jnl_theater": "Theater:",
        "jnl_rot_mon_thu": "Mon / Thu: Freedom, Prosperity, Transience, Admonition, Equity, Contention",
        "jnl_rot_tue_fri": "Tue / Fri: Resistance, Diligence, Elegance, Ingenuity, Justice, Kindling",
        "jnl_rot_wed_sat": "Wed / Sat: Ballad, Gold, Light, Praxis, Order, Conflict",
        "jnl_rot_sun": "🌟 Sunday: All Talent Domains Open!",

        # Resin Planner
        "resin_title": "⚡ Original Resin Overflow & Cap Planner",
        "resin_current": "Current Resin Amount:",
        "resin_summary": "RESIN REGENERATION SUMMARY",
        "resin_full_status": "⚡ Status: <b style='color: #ff5555;'>RESIN IS FULL (MAX CAP)!</b>",
        "resin_cap_time_full": "Exact Full Cap Time: <b>Already Capped</b>",
        "resin_warning_full": "Warning Trigger: <b>Overlapping Capacity</b>",
        "resin_time_to_full": "⏳ Time to Full (200/200): <b style='color: {color};'>{hours}h {minutes}m</b>",
        "resin_cap_timestamp": "📅 Exact Full Cap Time: <b>{time_str}</b>",
        "resin_warning_time": "🔔 Warning Time (30m Before Cap): <b style='color: {color};'>{time_str}</b>",
        "resin_progress_format": "{current} / 200 Resin",

        # Team Goals & Talent Books
        "team_title": "🎯 Team Building & Material Farming Goals",
        "team_char_header": "TEAM CHARACTER",
        "team_mat_header": "TALENT BOOK GOAL",
        "team_sum_title": "WEEKLY DOMAIN FARMING SCHEDULE",
        "team_mon_thu": "📅 <b>Mon / Thu:</b> {txt}",
        "team_tue_fri": "📅 <b>Tue / Fri:</b> {txt}",
        "team_wed_sat": "📅 <b>Wed / Sat:</b> {txt}",
        "team_sun": "📅 Sunday: All Talent Domains Open!",
        "team_none": "None",
        "book_freedom": "Freedom",
        "book_resistance": "Resistance",
        "book_ballad": "Ballad",
        "book_prosperity": "Prosperity",
        "book_diligence": "Diligence",
        "book_gold": "Gold",
        "book_transience": "Transience",
        "book_elegance": "Elegance",
        "book_light": "Light",
        "book_admonition": "Admonition",
        "book_ingenuity": "Ingenuity",
        "book_praxis": "Praxis",
        "book_equity": "Equity",
        "book_justice": "Justice",
        "book_order": "Order",
        "book_contention": "Contention",
        "book_kindling": "Kindling",
        "book_conflict": "Conflict",
        "days_mon_thu_sun": "(Mon/Thu/Sun)",
        "days_tue_fri_sun": "(Tue/Fri/Sun)",
        "days_wed_sat_sun": "(Wed/Sat/Sun)",

        # Weekly Bosses
        "boss_title": "🐲 Weekly Boss Discount Tracker (Half Resin)",
        "boss_slots_title": "WEEKLY 50% RESIN DISCOUNTS (3/3 AVAILABLE)",
        "boss_discount_slot": "Discount Slot {num} (30 Resin)",
        "boss_header": "DEFEATED WEEKLY BOSSES THIS WEEK:",
        "boss_rem_disc": "⚡ Remaining Half-Resin Discounts: <b style='color: {color};'>{rem} / 3</b>",
        "boss_saved_resin": "💰 Resin Saved This Week: <b style='color: {color};'>{saved} Resin</b> <span style='color: #aaa;'>(Equivalates to {hours} hours regen time)</span>",

        # Widgets / HQ
        "hq_title": "OPERATIONS HQ",
        "hq_next_title": "NEXT ARRIVAL",
        "hq_no_active": "No active expeditions",
        "hq_next_in": "{char} in {h:02d}:{m:02d}:{s:02d}",
        "hq_reset_title": "DAILY RESET (04:00)",
        "hq_resin_title": "RESIN COUNTER",
        "hq_claim_all": "Claim All Ready",
        "hq_ready_count": "{count} Ready to claim!",
        "hq_resin_full": "{max} / {max} (FULL!)",
        "hq_resin_countdown": "{current} / {max} (Full in {h:02d}h {m:02d}m)",
        "hq_reset_countdown": "In {h:02d}h {m:02d}m",

        # Wishes & Banner
        "wish_title": "🌠 Wish & Pity Savings Counter",
        "banner_title": "⏳ Current Event Wish Ends In:",
        "banner_loading": "Loading banner time...",
        "banner_ended": "Banner ended / New banner active!",
        "banner_countdown_format": "{days} Days, {hours:02d}:{minutes:02d}:{seconds:02d} Hrs.",
        "wish_current_pity": "Current Pity (Wishes since last 5★):",
        "wish_guaranteed": "Next 5★ is Guaranteed (Lost last 50/50)",
        "wish_primos": "💎 Primogems Owned:",
        "wish_fates": "💫 Intertwined Fates Owned:",
        "wish_summary_title": "PITY & SAVINGS SUMMARY",
        "wish_total_pulls": "💫 Total Available Pulls: <b style='color: {color};'>{total} Wishes</b> <span style='color: #aaa;'>(From {primos} primos + {fates} fates)</span>",
        "wish_soft_pity": "🎯 Wishes to Soft Pity (75): <b>{val}</b>",
        "wish_hard_pity": "🛡️ Wishes to Hard Pity (90): <b>{val}</b>",
        "wish_status_guaranteed": "✨ Target Status: <b style='color: #55ff55;'>GUARANTEED 5★ Character</b>",
        "wish_status_5050": "🎲 Target Status: <b style='color: #ffaa00;'>50/50 Chance</b>",
    },
    "Deutsch": {
        # General & App
        "app_title": "Genshin Impact Tracker",
        "theme": "Design:",
        "language": "Sprache / Language:",
        "sys_settings": "Systemeinstellungen",
        "autostart": "Mit System starten (Autostart)",
        "close_behavior": "Verhalten beim Schließen (✕):",
        "close_tray": "In den System-Tray minimieren",
        "close_exit": "Anwendung komplett beenden",
        "exp_finished": "Die Expedition von {char} ist abgeschlossen!",
        "exp_complete_title": "Expedition Beendet",
        "tray_running": "Läuft im Hintergrund.",
        "tray_open": "Tracker öffnen",
        "tray_quit": "Beenden",

        # Navigation Tooltips & Main Titles
        "nav_expeditions": "Expeditionen",
        "nav_journal": "Teyvat Tagebuch",
        "nav_crafting": "Alchemie-Rechner",
        "nav_wishes": "Gebete-Zähler",
        "nav_resin": "Harz-Planer",
        "nav_bosses": "Boss-Tracker",
        "nav_team": "Team-Ziele",
        "nav_settings": "Einstellungen",

        "title_expeditions": "Aktive Expeditionen",
        "title_journal": "Teyvat Tagebuch & HQ Operationen",
        "title_crafting": "Alchemie & Werkbank Rechner",
        "title_wishes": "Gebete & Pity Zähler",
        "title_resin": "Ursprüngliches Harz Planer",
        "title_bosses": "Wöchentlicher Boss Tracker",
        "title_team": "Team-Aufbau & Farming Ziele",
        "title_settings": "Einstellungen & Optionen",

        # Regionen
        "reg_mondstadt": "Mondstadt",
        "reg_liyue": "Liyue",
        "reg_inazuma": "Inazuma",
        "reg_sumeru": "Sumeru",
        "reg_fontaine": "Fontaine",
        "reg_natlan": "Natlan",

        # Common Actions & Buttons
        "start_new": "+ Neue Expedition starten",
        "limit_reached": "Limit erreicht ({count}/5 Expeditionen)",
        "ready": "BEREIT!",
        "running": "Läuft",
        "claim_reward": "Belohnung holen",
        "cancel": "Abbrechen",
        "confirm": "OK",
        "delete": "Löschen",
        "edit": "Bearbeiten",
        "save": "Speichern",

        # Resources
        "res_mora": "Mora",
        "res_ores": "Erze (Eisen & Kristall)",
        "res_meat": "Fleisch & Geflügel",
        "res_plants": "Zutaten & Pflanzen",
        "res_fish": "Fisch",

        # Crafting Calculator
        "craft_title": "🧪 Alchemie & Werkbank-Rechner",
        "craft_passive": "Herstellungs-Passiv (Charakter-Bonus):",
        "craft_passive_none": "Keiner (Standard 3:1)",
        "craft_passive_double": "Sucrose / Albedo (10% Chance auf 2x Produkt)",
        "craft_passive_refund": "Mona / Xingqiu (25% Chance auf Material-Rückerstattung)",
        "craft_inventory": "AKTUELLER INVENTARBESTAND:",
        "craft_t1": "🟢 Rang 1 (Grün / 2★):",
        "craft_t2": "🔵 Rang 2 (Blau / 3★):",
        "craft_t3": "🟣 Rang 3 (Violett / 4★):",
        "craft_summary": "HERSTELLUNGSERGEBNIS & AUSBEUTE",
        "craft_out_t2": "🔵 Gesamt Blaue Materialien (3★): <b>{total}</b> <span style='color: #aaa;'>(+ {crafted} hergestellt)</span>",
        "craft_out_t3": "🟣 Max. Violette Materialien (4★): <b>{total}</b> <span style='color: #aaa;'>(+ {crafted} hergestellt)</span>",
        "craft_mora": "💰 Geschätzte Herstellungskosten: <b style='color: {color};'>{mora:,} Mora</b>",

        # Dialogs
        "dlg_add_title": "Neue Expedition",
        "dlg_char": "Charakter:",
        "dlg_region": "Region:",
        "dlg_resource": "Ressource:",
        "dlg_duration": "Dauer:",
        "dlg_dur_4h": "4 Stunden",
        "dlg_dur_8h": "8 Stunden",
        "dlg_dur_12h": "12 Stunden",
        "dlg_dur_20h": "20 Stunden (Standard)",
        "dlg_dur_3h_bonus": "3 Stunden (Bonus 4h)",
        "dlg_dur_6h_bonus": "6 Stunden (Bonus 8h)",
        "dlg_dur_9h_bonus": "9 Stunden (Bonus 12h)",
        "dlg_dur_15h_bonus": "15 Stunden (Bonus 20h)",
        "dlg_start": "Starten",
        "dlg_resin_title": "Ursprüngliches Harz anpassen",
        "dlg_current_resin": "Aktuelles Harz:",
        "dlg_save": "Speichern",
        "dlg_settings_title": "⚙️ Einstellungen",
        "dlg_edit_time_title": "Zeit anpassen ({char})",
        "dlg_remaining_time": "Restzeit:",

        # Teyvat Journal
        "jnl_title": "📖 Teyvat Tagebuch & Checklisten",
        "jnl_ar": "Abenteuerstufe (AR):",
        "jnl_ar_tooltip": "Schaltet Funktionen basierend auf deiner Abenteuerstufe frei.",
        "jnl_commissions": "TÄGLICHE KOPFGELDER",
        "jnl_katheryne": "🎁 Katheryne",
        "jnl_bosses_rot": "WÖCHENTLICHE BOSSES & ROTATION",
        "jnl_boss_num": "Boss #{num}",
        "jnl_pot_title": "KANNENREICH (FREIGESCHALTET AB AR 28)",
        "jnl_pot_resin": "Flüchtiges Harz",
        "jnl_pot_books": "EP-Bücher",
        "jnl_pot_arte": "Artefakt-Münzen",
        "jnl_trans_title": "PARAMETRISCHER TRANSFORMATOR (FREIGESCHALTET AB AR 31)",
        "jnl_trans_btn": "Jetzt nutzen (7d)",
        "jnl_art_title": "ARTEFAKT-ROUTE (FREIGESCHALTET AB AR 45)",
        "jnl_art_btn": "Route beendet",
        "jnl_art_ready": "Bereit zum Farmen!",
        "jnl_endgame_title": "ENDGAME-STERNE (FREIGESCHALTET AB AR 45)",
        "jnl_abyss": "Gewundener Abgrund:",
        "jnl_theater": "Theater:",
        "jnl_rot_mon_thu": "Mo / Do: Freiheit, Wohlstand, Vergänglichkeit, Ermahnung, Gerechtigkeit, Anfechtung",
        "jnl_rot_tue_fri": "Di / Fr: Beständigkeit, Fleiß, Eleganz, Einfallsreichtum, Ordnung, Entzündung",
        "jnl_rot_wed_sat": "Mi / Sa: Poesie, Gold, Licht, Praxis, Mahnung, Konflikt",
        "jnl_rot_sun": "🌟 Sonntag: Alle Talent-Sphären geöffnet!",

        # Resin Planner
        "resin_title": "⚡ Ursprüngliches Harz & Überlauf-Planer",
        "resin_current": "Aktueller Harzbestand:",
        "resin_summary": "HARZ-REGENERATIONS-ÜBERSICHT",
        "resin_full_status": "⚡ Status: <b style='color: #ff5555;'>HARZ IST VOLL (MAXIMUM ERREICHT)!</b>",
        "resin_cap_time_full": "Exakte Voll-Zeit: <b>Bereits voll</b>",
        "resin_warning_full": "Warn-Auslöser: <b>Bereits überschritten</b>",
        "resin_time_to_full": "⏳ Zeit bis Maximum (200/200): <b style='color: {color};'>{hours} Std. {minutes} Min.</b>",
        "resin_cap_timestamp": "📅 Exakte Voll-Zeit: <b>{time_str}</b>",
        "resin_warning_time": "🔔 Warn-Zeit (30 Min. vor Maximum): <b style='color: {color};'>{time_str}</b>",
        "resin_progress_format": "{current} / 200 Harz",

        # Team Goals & Talent Books
        "team_title": "🎯 Team-Ziele & Material-Farming",
        "team_char_header": "TEAM-CHARAKTER",
        "team_mat_header": "TALENTBUCH-ZIEL",
        "team_sum_title": "WÖCHENTLICHER PHÄNOLOGISCHER PLAN",
        "team_mon_thu": "📅 <b>Mo / Do:</b> {txt}",
        "team_tue_fri": "📅 <b>Di / Fr:</b> {txt}",
        "team_wed_sat": "📅 <b>Mi / Sa:</b> {txt}",
        "team_sun": "📅 Sonntag: Alle Talent-Sphären geöffnet!",
        "team_none": "Keine",
        "book_freedom": "Freiheit",
        "book_resistance": "Beständigkeit",
        "book_ballad": "Poesie",
        "book_prosperity": "Wohlstand",
        "book_diligence": "Fleiß",
        "book_gold": "Gold",
        "book_transience": "Vergänglichkeit",
        "book_elegance": "Eleganz",
        "book_light": "Licht",
        "book_admonition": "Ermahnung",
        "book_ingenuity": "Einfallsreichtum",
        "book_praxis": "Praxis",
        "book_equity": "Gerechtigkeit",
        "book_justice": "Ordnung",
        "book_order": "Mahnung",
        "book_contention": "Anfechtung",
        "book_kindling": "Entzündung",
        "book_conflict": "Konflikt",
        "days_mon_thu_sun": "(Mo/Do/So)",
        "days_tue_fri_sun": "(Di/Fr/So)",
        "days_wed_sat_sun": "(Mi/Sa/So)",

        # Weekly Bosses
        "boss_title": "🐲 Wöchentlicher Boss-Rabatt-Tracker (Halbes Harz)",
        "boss_slots_title": "WÖCHENTLICHE 50% HARZ-RABATTE (3/3 VERFÜGBAR)",
        "boss_discount_slot": "Discount Slot {num} (30 Harz)",
        "boss_header": "DIESE WOCHE BESIEGTE WÖCHENTLICHE BOSSE:",
        "boss_rem_disc": "⚡ Verbleibende Halbharz-Rabatte: <b style='color: {color};'>{rem} / 3</b>",
        "boss_saved_resin": "💰 Diese Woche gespartes Harz: <b style='color: {color};'>{saved} Harz</b> <span style='color: #aaa;'>(Entspricht {hours} Stunden Regenerationszeit)</span>",

        # Widgets / HQ
        "hq_title": "OPERATIONS-HQ",
        "hq_next_title": "NÄCHSTE ANKUNFT",
        "hq_no_active": "Keine aktiven Expeditionen",
        "hq_next_in": "{char} in {h:02d}:{m:02d}:{s:02d}",
        "hq_reset_title": "TÄGLICHER RESET (04:00)",
        "hq_resin_title": "HARZ-ZÄHLER",
        "hq_claim_all": "Alle fertigen abholen",
        "hq_ready_count": "{count} bereit zum Abholen!",
        "hq_resin_full": "{max} / {max} (VOLL!)",
        "hq_resin_countdown": "{current} / {max} (Voll in {h:02d}h {m:02d}m)",
        "hq_reset_countdown": "In {h:02d}h {m:02d}m",

        # Wishes & Banner
        "wish_title": "🌠 Gebete- & Pity-Sparplan",
        "banner_title": "⏳ Aktuelles Aktionsgebet endet in:",
        "banner_loading": "Lade Banner-Zeit...",
        "banner_ended": "Banner beendet / Neues Banner aktiv!",
        "banner_countdown_format": "{days} Tage, {hours:02d}:{minutes:02d}:{seconds:02d} Std.",
        "wish_current_pity": "Aktuelles Pity (Gebete seit letztem 5★):",
        "wish_guaranteed": "Nächster 5★ ist garantiert (letzten 50/50 verloren)",
        "wish_primos": "💎 Vorherrschende Urgesteine:",
        "wish_fates": "💫 Vorherbestimmte Schicksale:",
        "wish_summary_title": "PITY- & SPARPLAN-ÜBERSICHT",
        "wish_total_pulls": "💫 Gesamte verfügbare Gebete: <b style='color: {color};'>{total} Gebete</b> <span style='color: #aaa;'>(Aus {primos} Urgestein + {fates} Schicksalen)</span>",
        "wish_soft_pity": "🎯 Gebete bis Soft Pity (75): <b>{val}</b>",
        "wish_hard_pity": "🛡️ Gebete bis Hard Pity (90): <b>{val}</b>",
        "wish_status_guaranteed": "✨ Zielstatus: <b style='color: #55ff55;'>GARANTIERTER 5★-Charakter</b>",
        "wish_status_5050": "🎲 Zielstatus: <b style='color: #ffaa00;'>50/50-Chance</b>",
    },
}


def set_language(lang_name: str):
    global CURRENT_LANGUAGE
    if lang_name in TRANSLATIONS:
        CURRENT_LANGUAGE = lang_name


def get_language() -> str:
    return CURRENT_LANGUAGE


def tr(key: str, **kwargs) -> str:
    """Zentrale Übersetzungsfunktion für alle Python-Module"""
    text = TRANSLATIONS.get(CURRENT_LANGUAGE, {}).get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            pass
    return text


def get_resources_list():
    """Gibt die übersetzte Ressourcen-Liste zurück"""
    return [
        tr("res_mora"),
        tr("res_ores"),
        tr("res_meat"),
        tr("res_plants"),
        tr("res_fish"),
    ]


def get_regions_list():
    """Gibt die übersetzten Regionen-Namen zurück"""
    return [
        tr("reg_mondstadt"),
        tr("reg_liyue"),
        tr("reg_inazuma"),
        tr("reg_sumeru"),
        tr("reg_fontaine"),
        tr("reg_natlan"),
    ]


def get_translated_book_title(book_key: str, days_key: str) -> str:
    """Kombiniert Talentbuch-Name und Tage-Suffix dynamisch"""
    return f"{tr(book_key)} {tr(days_key)}"