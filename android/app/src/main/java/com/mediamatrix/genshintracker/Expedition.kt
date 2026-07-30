package com.mediamatrix.genshintracker

import java.util.UUID

// Information über einen Charakter
data class CharacterInfo(
    val name: String
)

// Die globale Charakter-Liste mit allen Charakteren (ohne Duplikate)
val CHARACTERS = mapOf(
    "Albedo" to CharacterInfo("Albedo"),
    "Alhaitham" to CharacterInfo("Alhaitham"),
    "Aloy" to CharacterInfo("Aloy"),
    "Amber" to CharacterInfo("Amber"),
    "Arataki Itto" to CharacterInfo("Arataki Itto"),
    "Arlecchino" to CharacterInfo("Arlecchino"),
    "Barbara" to CharacterInfo("Barbara"),
    "Beidou" to CharacterInfo("Beidou"),
    "Bennett" to CharacterInfo("Bennett"),
    "Candace" to CharacterInfo("Candace"),
    "Charlotte" to CharacterInfo("Charlotte"),
    "Chasca" to CharacterInfo("Chasca"),
    "Chevreuse" to CharacterInfo("Chevreuse"),
    "Chiori" to CharacterInfo("Chiori"),
    "Chongyun" to CharacterInfo("Chongyun"),
    "Citlali" to CharacterInfo("Citlali"),
    "Clorinde" to CharacterInfo("Clorinde"),
    "Collei" to CharacterInfo("Collei"),
    "Cyno" to CharacterInfo("Cyno"),
    "Dehya" to CharacterInfo("Dehya"),
    "Diluc" to CharacterInfo("Diluc"),
    "Diona" to CharacterInfo("Diona"),
    "Dori" to CharacterInfo("Dori"),
    "Emilie" to CharacterInfo("Emilie"),
    "Eula" to CharacterInfo("Eula"),
    "Faruzan" to CharacterInfo("Faruzan"),
    "Fischl" to CharacterInfo("Fischl"),
    "Freminet" to CharacterInfo("Freminet"),
    "Furina" to CharacterInfo("Furina"),
    "Gaming" to CharacterInfo("Gaming"),
    "Ganyu" to CharacterInfo("Ganyu"),
    "Gorou" to CharacterInfo("Gorou"),
    "Hu Tao" to CharacterInfo("Hu Tao"),
    "Iansan" to CharacterInfo("Iansan"),
    "Jean" to CharacterInfo("Jean"),
    "Kachina" to CharacterInfo("Kachina"),
    "Kaedehara Kazuha" to CharacterInfo("Kaedehara Kazuha"),
    "Kaeya" to CharacterInfo("Kaeya"),
    "Kamisato Ayaka" to CharacterInfo("Kamisato Ayaka"),
    "Kamisato Ayato" to CharacterInfo("Kamisato Ayato"),
    "Kaveh" to CharacterInfo("Kaveh"),
    "Keqing" to CharacterInfo("Keqing"),
    "Kinich" to CharacterInfo("Kinich"),
    "Kirara" to CharacterInfo("Kirara"),
    "Klee" to CharacterInfo("Klee"),
    "Kujou Sara" to CharacterInfo("Kujou Sara"),
    "Kuki Shinobu" to CharacterInfo("Kuki Shinobu"),
    "Lan Yan" to CharacterInfo("Lan Yan"),
    "Layla" to CharacterInfo("Layla"),
    "Lisa" to CharacterInfo("Lisa"),
    "Lynette" to CharacterInfo("Lynette"),
    "Lyney" to CharacterInfo("Lyney"),
    "Mavuika" to CharacterInfo("Mavuika"),
    "Mika" to CharacterInfo("Mika"),
    "Mona" to CharacterInfo("Mona"),
    "Mualani" to CharacterInfo("Mualani"),
    "Nahida" to CharacterInfo("Nahida"),
    "Navia" to CharacterInfo("Navia"),
    "Neuvillette" to CharacterInfo("Neuvillette"),
    "Nilou" to CharacterInfo("Nilou"),
    "Ningguang" to CharacterInfo("Ningguang"),
    "Noelle" to CharacterInfo("Noelle"),
    "Ororon" to CharacterInfo("Ororon"),
    "Qiqi" to CharacterInfo("Qiqi"),
    "Raiden Shogun" to CharacterInfo("Raiden Shogun"),
    "Razor" to CharacterInfo("Razor"),
    "Rosaria" to CharacterInfo("Rosaria"),
    "Sangonomiya Kokomi" to CharacterInfo("Sangonomiya Kokomi"),
    "Sayu" to CharacterInfo("Sayu"),
    "Sethos" to CharacterInfo("Sethos"),
    "Shenhe" to CharacterInfo("Shenhe"),
    "Shikanoin Heizou" to CharacterInfo("Shikanoin Heizou"),
    "Sigewinne" to CharacterInfo("Sigewinne"),
    "Sucrose" to CharacterInfo("Sucrose"),
    "Thoma" to CharacterInfo("Thoma"),
    "Tighnari" to CharacterInfo("Tighnari"),
    "Traveller" to CharacterInfo("Traveller"),
    "Venti" to CharacterInfo("Venti"),
    "Wanderer" to CharacterInfo("Wanderer"),
    "Wriothesley" to CharacterInfo("Wriothesley"),
    "Xiangling" to CharacterInfo("Xiangling"),
    "Xianyun" to CharacterInfo("Xianyun"),
    "Xiao" to CharacterInfo("Xiao"),
    "Xilonen" to CharacterInfo("Xilonen"),
    "Xingqiu" to CharacterInfo("Xingqiu"),
    "Xinyan" to CharacterInfo("Xinyan"),
    "Yae Miko" to CharacterInfo("Yae Miko"),
    "Yanfei" to CharacterInfo("Yanfei"),
    "Yao Yao" to CharacterInfo("Yao Yao"),
    "Yelan" to CharacterInfo("Yelan"),
    "Yoimiya" to CharacterInfo("Yoimiya"),
    "Yun Jin" to CharacterInfo("Yun Jin"),
    "Zhongli" to CharacterInfo("Zhongli")
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
