package com.mediamatrix.genshintracker

import java.util.UUID

// Information über einen Charakter und ob er den 25% Zeit-Bonus besitzt
data class CharacterInfo(
    val name: String,
    val hasBonus: Boolean = false
)

// Die globale Charakter-Liste mit allen Charakteren
val CHARACTERS = mapOf(
    "Albedo" to CharacterInfo("Albedo", false),
    "Alhaitham" to CharacterInfo("Alhaitham", false),
    "Aloy" to CharacterInfo("Aloy", false),
    "Amber" to CharacterInfo("Amber", false),
    "Arataki Itto" to CharacterInfo("Arataki Itto", false),
    "Arlecchino" to CharacterInfo("Arlecchino", false),
    "Barbara" to CharacterInfo("Barbara", false),
    "Beidou" to CharacterInfo("Beidou", false),
    "Bennett" to CharacterInfo("Bennett", true),
    "Candace" to CharacterInfo("Candace", false),
    "Charlotte" to CharacterInfo("Charlotte", false),
    "Chasca" to CharacterInfo("Chasca", false),
    "Chevreuse" to CharacterInfo("Chevreuse", false),
    "Chiori" to CharacterInfo("Chiori", false),
    "Chongyun" to CharacterInfo("Chongyun", true),
    "Citlali" to CharacterInfo("Citlali", false),
    "Clorinde" to CharacterInfo("Clorinde", false),
    "Collei" to CharacterInfo("Collei", false),
    "Cyno" to CharacterInfo("Cyno", false),
    "Dehya" to CharacterInfo("Dehya", false),
    "Diluc" to CharacterInfo("Diluc", false),
    "Diona" to CharacterInfo("Diona", false),
    "Dori" to CharacterInfo("Dori", false),
    "Emilie" to CharacterInfo("Emilie", false),
    "Eula" to CharacterInfo("Eula", false),
    "Faruzan" to CharacterInfo("Faruzan", false),
    "Fischl" to CharacterInfo("Fischl", true),
    "Freminet" to CharacterInfo("Freminet", false),
    "Furina" to CharacterInfo("Furina", false),
    "Gaming" to CharacterInfo("Gaming", false),
    "Ganyu" to CharacterInfo("Ganyu", false),
    "Gorou" to CharacterInfo("Gorou", false),
    "Hu Tao" to CharacterInfo("Hu Tao", false),
    "Iansan" to CharacterInfo("Iansan", false),
    "Jean" to CharacterInfo("Jean", false),
    "Kachina" to CharacterInfo("Kachina", false),
    "Kaedehara Kazuha" to CharacterInfo("Kaedehara Kazuha", false),
    "Kaeya" to CharacterInfo("Kaeya", false),
    "Kamisato Ayaka" to CharacterInfo("Kamisato Ayaka", false),
    "Kamisato Ayato" to CharacterInfo("Kamisato Ayato", false),
    "Kaveh" to CharacterInfo("Kaveh", false),
    "Keqing" to CharacterInfo("Keqing", true),
    "Kinich" to CharacterInfo("Kinich", false),
    "Kirara" to CharacterInfo("Kirara", false),
    "Klee" to CharacterInfo("Klee", false),
    "Kujou Sara" to CharacterInfo("Kujou Sara", false),
    "Kuki Shinobu" to CharacterInfo("Kuki Shinobu", false),
    "Lan Yan" to CharacterInfo("Lan Yan", false),
    "Lanyan" to CharacterInfo("Lanyan", false),
    "Layla" to CharacterInfo("Layla", false),
    "Lisa" to CharacterInfo("Lisa", false),
    "Lynette" to CharacterInfo("Lynette", false),
    "Lyney" to CharacterInfo("Lyney", false),
    "Mavuika" to CharacterInfo("Mavuika", false),
    "Mika" to CharacterInfo("Mika", false),
    "Mona" to CharacterInfo("Mona", false),
    "Mualani" to CharacterInfo("Mualani", false),
    "Nahida" to CharacterInfo("Nahida", false),
    "Navia" to CharacterInfo("Navia", false),
    "Neuvillette" to CharacterInfo("Neuvillette", false),
    "Nilou" to CharacterInfo("Nilou", false),
    "Ningguang" to CharacterInfo("Ningguang", false),
    "Noelle" to CharacterInfo("Noelle", false),
    "Ororon" to CharacterInfo("Ororon", false),
    "Qiqi" to CharacterInfo("Qiqi", false),
    "Raiden Shogun" to CharacterInfo("Raiden Shogun", false),
    "Razor" to CharacterInfo("Razor", false),
    "Rosaria" to CharacterInfo("Rosaria", false),
    "Sangonomiya Kokomi" to CharacterInfo("Sangonomiya Kokomi", false),
    "Sayu" to CharacterInfo("Sayu", false),
    "Sethos" to CharacterInfo("Sethos", false),
    "Shenhe" to CharacterInfo("Shenhe", true),
    "Shikanoin Heizou" to CharacterInfo("Shikanoin Heizou", false),
    "Sigewinne" to CharacterInfo("Sigewinne", false),
    "Sucrose" to CharacterInfo("Sucrose", false),
    "Thoma" to CharacterInfo("Thoma", false),
    "Tighnari" to CharacterInfo("Tighnari", false),
    "Traveller" to CharacterInfo("Traveller", false),
    "Venti" to CharacterInfo("Venti", false),
    "Wanderer" to CharacterInfo("Wanderer", false),
    "Wriothesley" to CharacterInfo("Wriothesley", false),
    "Xiangling" to CharacterInfo("Xiangling", false),
    "Xianyun" to CharacterInfo("Xianyun", false),
    "Xiao" to CharacterInfo("Xiao", false),
    "Xilonen" to CharacterInfo("Xilonen", false),
    "Xingqiu" to CharacterInfo("Xingqiu", false),
    "Xinyan" to CharacterInfo("Xinyan", false),
    "Yae Miko" to CharacterInfo("Yae Miko", false),
    "Yanfei" to CharacterInfo("Yanfei", false),
    "Yao Yao" to CharacterInfo("Yao Yao", false),
    "Yelan" to CharacterInfo("Yelan", true),
    "Yoimiya" to CharacterInfo("Yoimiya", false),
    "Yun Jin" to CharacterInfo("Yun Jin", false),
    "Zhongli" to CharacterInfo("Zhongli", false)
)

val REGIONS = listOf("Mondstadt", "Liyue", "Inazuma", "Sumeru", "Fontaine", "Natlan")

val RESOURCES = listOf(
    "Mora",
    "Ores (Iron & Crystal)",
    "Meat & Fowl",
    "Ingredients & Plants",
    "Fish"
)

// Repräsentiert eine laufende Expedition
data class Expedition(
    val id: String = UUID.randomUUID().toString(),
    val charName: String,
    val location: String,
    val totalSeconds: Long,
    val endTimestampEpochSec: Long
) {
    // Rechnet die verbleibenden Sekunden live aus
    fun remainingSeconds(): Long {
        val nowSec = System.currentTimeMillis() / 1000
        return (endTimestampEpochSec - nowSec).coerceAtLeast(0)
    }

    fun isComplete(): Boolean = remainingSeconds() <= 0
}