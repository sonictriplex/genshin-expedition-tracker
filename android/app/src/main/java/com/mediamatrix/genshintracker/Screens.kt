package com.mediamatrix.genshintracker

import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

// =========================================================
// Crafting Calculator Screen
// =========================================================
@Composable
fun CraftingCalculatorScreen(theme: RegionTheme) {
    var tier1 by remember { mutableStateOf("0") }
    var tier2 by remember { mutableStateOf("0") }
    var tier3 by remember { mutableStateOf("0") }
    var passiveMode by remember { mutableIntStateOf(0) }

    val t1Val = tier1.toIntOrNull() ?: 0
    val t2Val = tier2.toIntOrNull() ?: 0
    val t3Val = tier3.toIntOrNull() ?: 0

    val multiplier = when (passiveMode) {
        1 -> 1.10
        2 -> 1.0833
        else -> 1.0
    }

    val craftedT2 = Math.floor((t1Val / 3.0) * multiplier).toInt()
    val totalT2 = t2Val + craftedT2
    val craftedT3 = Math.floor((totalT2 / 3.0) * multiplier).toInt()
    val totalT3 = t3Val + craftedT3
    val totalSteps = (t1Val / 3) + (totalT2 / 3)
    val estimatedMora = totalSteps * 175

    val customFieldColors = OutlinedTextFieldDefaults.colors(
        focusedTextColor = Color.White,
        unfocusedTextColor = Color.White,
        focusedLabelColor = theme.cyan,
        unfocusedLabelColor = Color(0xFFCBD5E1),
        focusedBorderColor = theme.cyan,
        unfocusedBorderColor = Color(0xFF475569),
        cursorColor = theme.cyan
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState()),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text(
            text = "🧪 Alchemy & Crafting Calculator",
            color = Color.White,
            fontWeight = FontWeight.Bold,
            fontSize = 16.sp
        )

        Card(
            colors = CardDefaults.cardColors(containerColor = theme.cardBg),
            shape = RoundedCornerShape(12.dp),
            modifier = Modifier
                .fillMaxWidth()
                .border(1.dp, Color(0xFF333847), RoundedCornerShape(12.dp))
        ) {
            Column(
                modifier = Modifier.padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                Text(
                    text = "Crafting Passive:",
                    color = Color(0xFFE2E8F0),
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Bold
                )

                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    Button(
                        onClick = { passiveMode = 0 },
                        colors = ButtonDefaults.buttonColors(
                            containerColor = if (passiveMode == 0) theme.cyan else Color(0xFF2E323F)
                        )
                    ) {
                        Text("None", fontSize = 11.sp, color = if (passiveMode == 0) Color.Black else Color.White, fontWeight = FontWeight.Bold)
                    }
                    Button(
                        onClick = { passiveMode = 1 },
                        colors = ButtonDefaults.buttonColors(
                            containerColor = if (passiveMode == 1) theme.cyan else Color(0xFF2E323F)
                        )
                    ) {
                        Text("Sucrose (2x)", fontSize = 11.sp, color = if (passiveMode == 1) Color.Black else Color.White, fontWeight = FontWeight.Bold)
                    }
                    Button(
                        onClick = { passiveMode = 2 },
                        colors = ButtonDefaults.buttonColors(
                            containerColor = if (passiveMode == 2) theme.cyan else Color(0xFF2E323F)
                        )
                    ) {
                        Text("Mona (Refund)", fontSize = 11.sp, color = if (passiveMode == 2) Color.Black else Color.White, fontWeight = FontWeight.Bold)
                    }
                }

                Spacer(modifier = Modifier.height(4.dp))

                OutlinedTextField(
                    value = tier1,
                    onValueChange = { tier1 = it },
                    label = { Text("🟢 Tier 1 (Green / 2★)") },
                    colors = customFieldColors,
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = tier2,
                    onValueChange = { tier2 = it },
                    label = { Text("🔵 Tier 2 (Blue / 3★)") },
                    colors = customFieldColors,
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = tier3,
                    onValueChange = { tier3 = it },
                    label = { Text("🟣 Tier 3 (Purple / 4★)") },
                    colors = customFieldColors,
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
            }
        }

        Card(
            colors = CardDefaults.cardColors(containerColor = theme.cardBg),
            shape = RoundedCornerShape(12.dp),
            modifier = Modifier
                .fillMaxWidth()
                .border(1.dp, Color(0xFF333847), RoundedCornerShape(12.dp))
        ) {
            Column(
                modifier = Modifier.padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Text(
                    text = "CRAFTING SUMMARY",
                    color = theme.cyan,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold
                )
                Text(
                    text = "🔵 Total Blue Materials (3★): $totalT2 (+ $craftedT2 crafted)",
                    color = Color.White,
                    fontSize = 13.sp
                )
                Text(
                    text = "🟣 Max Purple Materials (4★): $totalT3 (+ $craftedT3 crafted)",
                    color = Color.White,
                    fontSize = 13.sp
                )
                Text(
                    text = "💰 Estimated Cost: $estimatedMora Mora",
                    color = theme.amber,
                    fontWeight = FontWeight.Bold,
                    fontSize = 13.sp
                )
            }
        }
    }
}

// =========================================================
// Wish & Pity Counter Screen (Mit weißem Checkbox-Rahmen)
// =========================================================
@Composable
fun WishCounterScreen(theme: RegionTheme) {
    var pityStr by remember { mutableStateOf("0") }
    var isGuaranteed by remember { mutableStateOf(false) }
    var primosStr by remember { mutableStateOf("0") }
    var fatesStr by remember { mutableStateOf("0") }

    val pity = pityStr.toIntOrNull() ?: 0
    val primos = primosStr.toIntOrNull() ?: 0
    val fates = fatesStr.toIntOrNull() ?: 0

    val wishesFromPrimos = primos / 160
    val totalWishes = fates + wishesFromPrimos
    val toSoft = (75 - pity).coerceAtLeast(0)
    val toHard = (90 - pity).coerceAtLeast(0)

    val customFieldColors = OutlinedTextFieldDefaults.colors(
        focusedTextColor = Color.White,
        unfocusedTextColor = Color.White,
        focusedLabelColor = theme.cyan,
        unfocusedLabelColor = Color(0xFFCBD5E1),
        focusedBorderColor = theme.cyan,
        unfocusedBorderColor = Color(0xFF475569),
        cursorColor = theme.cyan
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState()),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text(
            text = "🌠 Wish & Pity Savings Counter",
            color = Color.White,
            fontWeight = FontWeight.Bold,
            fontSize = 16.sp
        )

        Card(
            colors = CardDefaults.cardColors(containerColor = theme.cardBg),
            shape = RoundedCornerShape(12.dp),
            modifier = Modifier
                .fillMaxWidth()
                .border(1.dp, Color(0xFF333847), RoundedCornerShape(12.dp))
        ) {
            Column(
                modifier = Modifier.padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                OutlinedTextField(
                    value = pityStr,
                    onValueChange = { pityStr = it },
                    label = { Text("Current Pity (0-89)") },
                    colors = customFieldColors,
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Checkbox(
                        checked = isGuaranteed,
                        onCheckedChange = { isGuaranteed = it },
                        colors = CheckboxDefaults.colors(
                            checkedColor = theme.cyan,
                            uncheckedColor = Color.White, // Weißer Rahmen!
                            checkmarkColor = Color.Black
                        )
                    )
                    Text("Next 5★ is Guaranteed", color = Color.White, fontSize = 13.sp)
                }
                OutlinedTextField(
                    value = primosStr,
                    onValueChange = { primosStr = it },
                    label = { Text("Primogems Owned") },
                    colors = customFieldColors,
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = fatesStr,
                    onValueChange = { fatesStr = it },
                    label = { Text("Intertwined Fates Owned") },
                    colors = customFieldColors,
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
            }
        }

        Card(
            colors = CardDefaults.cardColors(containerColor = theme.cardBg),
            shape = RoundedCornerShape(12.dp),
            modifier = Modifier
                .fillMaxWidth()
                .border(1.dp, Color(0xFF333847), RoundedCornerShape(12.dp))
        ) {
            Column(
                modifier = Modifier.padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                Text(
                    text = "PITY & SAVINGS SUMMARY",
                    color = theme.cyan,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold
                )
                Text("💫 Total Available Pulls: $totalWishes Wishes", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 13.sp)
                Text("🎯 Wishes to Soft Pity (75): $toSoft", color = Color.White, fontSize = 12.sp)
                Text("🛡️ Wishes to Hard Pity (90): $toHard", color = Color.White, fontSize = 12.sp)
                Text(
                    text = if (isGuaranteed) "✨ Status: GUARANTEED 5★" else "🎲 Status: 50/50 Chance",
                    color = if (isGuaranteed) Color(0xFF4ADE80) else theme.amber,
                    fontWeight = FontWeight.Bold,
                    fontSize = 12.sp
                )
            }
        }
    }
}

// =========================================================
// Weekly Boss Tracker Screen (Mit weißem Checkbox-Rahmen)
// =========================================================
@Composable
fun WeeklyBossScreen(theme: RegionTheme) {
    val bossList = listOf(
        "Stormterror Dvalin", "Wolf of the North", "Childe",
        "Azhdaha", "La Signora", "Narukami no Mikoto",
        "Scaramouche", "Apep's Oasis", "Narwhal", "Arlecchino"
    )

    var slot1 by remember { mutableStateOf(false) }
    var slot2 by remember { mutableStateOf(false) }
    var slot3 by remember { mutableStateOf(false) }
    val bossStates = remember { mutableStateMapOf<String, Boolean>() }

    val usedDiscounts = listOf(slot1, slot2, slot3).count { it }
    val remaining = 3 - usedDiscounts
    val savedResin = usedDiscounts * 30

    // Checkbox Colors mit weißem Rahmen im inaktiven Zustand
    val checkboxColors = CheckboxDefaults.colors(
        checkedColor = theme.cyan,
        uncheckedColor = Color.White, // Weißer Rahmen!
        checkmarkColor = Color.Black
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState()),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text(
            text = "🐲 Weekly Boss Discount Tracker",
            color = Color.White,
            fontWeight = FontWeight.Bold,
            fontSize = 16.sp
        )

        Card(
            colors = CardDefaults.cardColors(containerColor = theme.cardBg),
            shape = RoundedCornerShape(12.dp),
            modifier = Modifier
                .fillMaxWidth()
                .border(1.dp, Color(0xFF333847), RoundedCornerShape(12.dp))
        ) {
            Column(
                modifier = Modifier.padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(4.dp)
            ) {
                Text(
                    text = "50% RESIN DISCOUNTS ($remaining / 3 AVAILABLE)",
                    color = theme.cyan,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold
                )
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Checkbox(checked = slot1, onCheckedChange = { slot1 = it }, colors = checkboxColors)
                    Text("Discount Slot 1 (30 Resin)", color = Color.White, fontSize = 13.sp)
                }
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Checkbox(checked = slot2, onCheckedChange = { slot2 = it }, colors = checkboxColors)
                    Text("Discount Slot 2 (30 Resin)", color = Color.White, fontSize = 13.sp)
                }
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Checkbox(checked = slot3, onCheckedChange = { slot3 = it }, colors = checkboxColors)
                    Text("Discount Slot 3 (30 Resin)", color = Color.White, fontSize = 13.sp)
                }
                Spacer(modifier = Modifier.height(4.dp))
                Text("💰 Resin Saved: $savedResin Resin", color = theme.amber, fontWeight = FontWeight.Bold, fontSize = 13.sp)
            }
        }

        Card(
            colors = CardDefaults.cardColors(containerColor = theme.cardBg),
            shape = RoundedCornerShape(12.dp),
            modifier = Modifier
                .fillMaxWidth()
                .border(1.dp, Color(0xFF333847), RoundedCornerShape(12.dp))
        ) {
            Column(
                modifier = Modifier.padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(4.dp)
            ) {
                Text(
                    text = "DEFEATED BOSSES THIS WEEK:",
                    color = theme.cyan,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold
                )
                bossList.forEach { boss ->
                    val checked = bossStates[boss] ?: false
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Checkbox(checked = checked, onCheckedChange = { bossStates[boss] = it }, colors = checkboxColors)
                        Text(boss, color = Color.White, fontSize = 13.sp)
                    }
                }
            }
        }
    }
}