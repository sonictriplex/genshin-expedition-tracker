package com.mediamatrix.genshintracker

object AppTranslations {
    private val en = mapOf(
        // Main Activity / Tracker
        "app_name" to "Genshin Tracker",
        "nav_tracker" to "Tracker",
        "nav_journal" to "Journal",
        "nav_crafting" to "Crafting",
        "nav_wishes" to "Wishes",
        "nav_resin" to "Resin",
        "nav_bosses" to "Bosses",
        "nav_goals" to "Goals",
        "hq_title" to "OPERATIONS HQ",
        "next_arrival" to "NEXT ARRIVAL",
        "ready_claim" to "Ready to claim!",
        "no_expeditions" to "No active expeditions",
        "daily_reset" to "DAILY RESET (04:00)",
        "resin_counter" to "RESIN COUNTER",
        "claim_all" to "Claim All Ready",
        "start_new" to "+ Start New Expedition",
        "limit_reached" to "Limit Reached",
        "ready" to "READY!",
        "running" to "Running",
        "claim_reward" to "Claim Reward",
        "language" to "Language / Sprache:",
        "in" to "in",
        "full" to "FULL!",
        "full_in" to "Full in",

        // Screens: Teyvat Journal
        "journal_title" to "📖 Teyvat Journal & Checklists",
        "daily_comm" to "DAILY COMMISSIONS",
        "katheryne_bonus" to "🎁 Katheryne Bonus Reward",
        "weekly_bosses" to "WEEKLY BOSSES & ROTATION",
        "sunday_talent" to "🌟 Sunday: All Talent Domains Open!",
        "teapot" to "SERENITEA POT (UNLOCKED AT AR 28)",
        "transient_resin" to "Transient Resin",
        "heros_wit" to "Hero's Wit/Books",
        "artifact_exp" to "Artifact Unction/Exp",
        "parametric" to "PARAMETRIC TRANSFORMER (AR 31)",
        "use_now" to "Use Now (7d)",
        "artifact_route" to "ARTIFACT ROUTE (AR 45)",
        "ready_farm" to "Ready to Farm!",
        "route_finished" to "Route Finished",
        "endgame_stars" to "ENDGAME STARS (AR 45)",
        "abyss" to "Abyss:",
        "theater" to "Theater:",

        // Screens: Crafting
        "crafting_title" to "🧪 Alchemy & Crafting Calculator",
        "crafting_passive" to "Crafting Passive:",
        "none" to "None",
        "sucrose_passive" to "Sucrose (2x)",
        "mona_passive" to "Mona (Refund)",
        "tier1" to "🟢 Tier 1 (Green / 2★)",
        "tier2" to "🔵 Tier 2 (Blue / 3★)",
        "tier3" to "🟣 Tier 3 (Purple / 4★)",
        "crafting_summary" to "CRAFTING SUMMARY",
        "total_blue" to "Total Blue Materials (3★):",
        "max_purple" to "Max Purple Materials (4★):",
        "est_cost" to "Estimated Cost:",

        // Screens: Wishes
        "wish_title" to "🌠 Wish & Pity Savings Counter",
        "current_pity" to "Current Pity (0-89)",
        "next_guaranteed" to "Next 5★ is Guaranteed",
        "primos_owned" to "Primogems Owned",
        "fates_owned" to "Intertwined Fates Owned",
        "pity_summary" to "PITY & SAVINGS SUMMARY",
        "total_pulls" to "Total Available Pulls:",
        "to_soft" to "Wishes to Soft Pity (75):",
        "to_hard" to "Wishes to Hard Pity (90):",
        "status_guar" to "✨ Status: GUARANTEED 5★",
        "status_5050" to "🎲 Status: 50/50 Chance",

        // Screens: Resin Planner
        "resin_planner_title" to "⚡ Resin Overflow & Cap Planner",
        "calc_regen" to "CALCULATE REGEN TIME",
        "target_resin" to "Target Resin Amount",
        "time_from_zero" to "Time from 0 to",

        // Screens: Boss Tracker
        "boss_title" to "🐲 Weekly Boss Discount Tracker",
        "discounts_avail" to "50% RESIN DISCOUNTS",
        "discount_slot" to "Discount Slot",
        "resin_saved" to "Resin Saved:",
        "defeated_bosses" to "DEFEATED BOSSES THIS WEEK:",

        // Screens: Team Goals
        "goals_title" to "🎯 Team Building & Material Farming Goals",
        "team_char" to "TEAM CHARACTER",
        "talent_goal" to "TALENT BOOK GOAL",
        "schedule_title" to "WEEKLY DOMAIN FARMING SCHEDULE",
        "mon_thu" to "Mon / Thu:",
        "tue_fri" to "Tue / Fri:",
        "wed_sat" to "Wed / Sat:",
        "sun_all" to "Sunday: All Talent Domains Open!"
    )

    private val de = mapOf(
        // Main Activity / Tracker
        "app_name" to "Genshin Tracker",
        "nav_tracker" to "Expeditionen",
        "nav_journal" to "Tagebuch",
        "nav_crafting" to "Alchemie",
        "nav_wishes" to "Gebete",
        "nav_resin" to "Harz",
        "nav_bosses" to "Bosse",
        "nav_goals" to "Ziele",
        "hq_title" to "HAUPTQUARTIER",
        "next_arrival" to "NÄCHSTE ANKUNFT",
        "ready_claim" to "Bereit zum Einsammeln!",
        "no_expeditions" to "Keine aktiven Expeditionen",
        "daily_reset" to "TÄGLICHER RESET (04:00)",
        "resin_counter" to "HARZ-ZÄHLER",
        "claim_all" to "Alle Einsammeln",
        "start_new" to "+ Neue Expedition",
        "limit_reached" to "Limit erreicht",
        "ready" to "BEREIT!",
        "running" to "Läuft",
        "claim_reward" to "Belohnung holen",
        "language" to "Sprache / Language:",
        "in" to "in",
        "full" to "VOLL!",
        "full_in" to "Voll in",

        // Screens: Teyvat Journal
        "journal_title" to "📖 Teyvat Tagebuch & Checklisten",
        "daily_comm" to "TÄGLICHE MISSIONEN",
        "katheryne_bonus" to "🎁 Katheryne Bonus-Belohnung",
        "weekly_bosses" to "WÖCHENTLICHE BOSSE",
        "sunday_talent" to "🌟 Sonntag: Alle Talent-Sphären offen!",
        "teapot" to "KANNE DER VERGÄNGLICHKEIT (AB AR 28)",
        "transient_resin" to "Flüchtiges Harz",
        "heros_wit" to "Eines Helden Weisheit",
        "artifact_exp" to "Artefakt-EP (Weihsal)",
        "parametric" to "PARAMETRISCHER WANDLER (AR 31)",
        "use_now" to "Jetzt nutzen (7t)",
        "artifact_route" to "ARTEFAKT-ROUTE (AR 45)",
        "ready_farm" to "Bereit zum Farmen!",
        "route_finished" to "Route beendet",
        "endgame_stars" to "ENDGAME STERNE (AR 45)",
        "abyss" to "Gewundener Abgrund:",
        "theater" to "Theater der Realität:",

        // Screens: Crafting
        "crafting_title" to "🧪 Alchemie & Crafting Rechner",
        "crafting_passive" to "Crafting Passiv-Talent:",
        "none" to "Keines",
        "sucrose_passive" to "Saccharose (2x)",
        "mona_passive" to "Mona (Erstattung)",
        "tier1" to "🟢 Stufe 1 (Grün / 2★)",
        "tier2" to "🔵 Stufe 2 (Blau / 3★)",
        "tier3" to "🟣 Stufe 3 (Lila / 4★)",
        "crafting_summary" to "CRAFTING ÜBERSICHT",
        "total_blue" to "Gesamt Blaue Materialien (3★):",
        "max_purple" to "Max Lila Materialien (4★):",
        "est_cost" to "Geschätzte Kosten:",

        // Screens: Wishes
        "wish_title" to "🌠 Gebete & Pity Rechner",
        "current_pity" to "Aktuelles Pity (0-89)",
        "next_guaranteed" to "Nächster 5★ ist Garantiert",
        "primos_owned" to "Vorhandenes Urgestein",
        "fates_owned" to "Verwobenes Schicksal",
        "pity_summary" to "PITY & SPAR-ÜBERSICHT",
        "total_pulls" to "Gesamte verfügbare Züge:",
        "to_soft" to "Züge bis Soft Pity (75):",
        "to_hard" to "Züge bis Hard Pity (90):",
        "status_guar" to "✨ Status: 5★ GARANTIERT",
        "status_5050" to "🎲 Status: 50/50 Chance",

        // Screens: Resin Planner
        "resin_planner_title" to "⚡ Harz Überlauf & Planer",
        "calc_regen" to "REGENERATION BERECHNEN",
        "target_resin" to "Ziel Harz-Menge",
        "time_from_zero" to "Dauer von 0 bis",

        // Screens: Boss Tracker
        "boss_title" to "🐲 Wöchentliche Boss-Rabatte",
        "discounts_avail" to "50% HARZ RABATTE",
        "discount_slot" to "Rabatt-Slot",
        "resin_saved" to "Gespartes Harz:",
        "defeated_bosses" to "BESIEGTE BOSSE DIESE WOCHE:",

        // Screens: Team Goals
        "goals_title" to "🎯 Team-Aufbau & Farm-Ziele",
        "team_char" to "TEAM CHARAKTER",
        "talent_goal" to "TALENTBUCH ZIEL",
        "schedule_title" to "WÖCHENTLICHER SPHÄREN-PLAN",
        "mon_thu" to "Mo / Do:",
        "tue_fri" to "Di / Fr:",
        "wed_sat" to "Mi / Sa:",
        "sun_all" to "Sonntag: Alle Talent-Sphären offen!"
    )

    fun tr(key: String, lang: String): String {
        val map = if (lang == "Deutsch") de else en
        return map[key] ?: key
    }
}