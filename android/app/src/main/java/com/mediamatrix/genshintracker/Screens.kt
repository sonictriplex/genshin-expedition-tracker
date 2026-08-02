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
// 1. Teyvat Journal Screen (English Dashboard)
// =========================================================
@Composable
fun TeyvatJournalScreen(theme: RegionTheme) {
    var arLevel by remember { mutableIntStateOf(60) }

    // Checkbox States
    var daily1 by remember { mutableStateOf(false) }
    var daily2 by remember { mutableStateOf(false) }
    var daily3 by remember { mutableStateOf(false) }
    var daily4 by remember { mutableStateOf(false) }
    var katheryne by remember { mutableStateOf(false) }

    var boss1 by remember { mutableStateOf(false) }
    var boss2 by remember { mutableStateOf(false) }
    var boss3 by remember { mutableStateOf(false) }

    var resinClaimed by remember { mutableStateOf(false) }
    var xpClaimed by remember { mutableStateOf(false) }
    var coinsClaimed by remember { mutableStateOf(false) }

    var abyssStars by remember { mutableIntStateOf(0) }
    var theaterStars by remember { mutableIntStateOf(0) }

    val checkboxColors = CheckboxDefaults.colors(
        checkedColor = theme.cyan,
        uncheckedColor = Color.White,
        checkmarkColor = Color.Black
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState()),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        // Top Bar: Title & Adventure Rank
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = "📖 Teyvat Journal & Checklists",
                color = Color.White,
                fontWeight = FontWeight.Bold,
                fontSize = 16.sp
            )

            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("AR: ", color = Color.Gray, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                IconButton(onClick = { if (arLevel > 1) arLevel-- }, modifier = Modifier.size(24.dp)) {
                    Text("-", color = theme.cyan, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                }
                Text("$arLevel", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 13.sp)
                IconButton(onClick = { if (arLevel < 60) arLevel++ }, modifier = Modifier.size(24.dp)) {
                    Text("+", color = theme.cyan, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                }
            }
        }

        // 1. DAILY COMMISSIONS
        Card(
            colors = CardDefaults.cardColors(containerColor = theme.cardBg),
            shape = RoundedCornerShape(12.dp),
            modifier = Modifier
                .fillMaxWidth()
                .border(1.dp, Color(0xFF333847), RoundedCornerShape(12.dp))
        ) {
            Column(modifier = Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                Text("DAILY COMMISSIONS", color = theme.cyan, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Checkbox(checked = daily1, onCheckedChange = { daily1 = it }, colors = checkboxColors)
                        Text("#1", color = Color.White, fontSize = 12.sp)
                        Checkbox(checked = daily2, onCheckedChange = { daily2 = it }, colors = checkboxColors)
                        Text("#2", color = Color.White, fontSize = 12.sp)
                        Checkbox(checked = daily3, onCheckedChange = { daily3 = it }, colors = checkboxColors)
                        Text("#3", color = Color.White, fontSize = 12.sp)
                        Checkbox(checked = daily4, onCheckedChange = { daily4 = it }, colors = checkboxColors)
                        Text("#4", color = Color.White, fontSize = 12.sp)
                    }
                }
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Checkbox(checked = katheryne, onCheckedChange = { katheryne = it }, colors = checkboxColors)
                    Text("🎁 Katheryne Bonus Reward", color = theme.amber, fontWeight = FontWeight.Bold, fontSize = 12.sp)
                }
            }
        }

        // 2. WEEKLY BOSSES & ROTATION
        Card(
            colors = CardDefaults.cardColors(containerColor = theme.cardBg),
            shape = RoundedCornerShape(12.dp),
            modifier = Modifier
                .fillMaxWidth()
                .border(1.dp, Color(0xFF333847), RoundedCornerShape(12.dp))
        ) {
            Column(modifier = Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                Text("WEEKLY BOSSES & ROTATION", color = theme.cyan, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Checkbox(checked = boss1, onCheckedChange = { boss1 = it }, colors = checkboxColors)
                    Text("Boss #1", color = Color.White, fontSize = 12.sp)
                    Spacer(modifier = Modifier.width(8.dp))
                    Checkbox(checked = boss2, onCheckedChange = { boss2 = it }, colors = checkboxColors)
                    Text("Boss #2", color = Color.White, fontSize = 12.sp)
                    Spacer(modifier = Modifier.width(8.dp))
                    Checkbox(checked = boss3, onCheckedChange = { boss3 = it }, colors = checkboxColors)
                    Text("Boss #3", color = Color.White, fontSize = 12.sp)
                }
                Text("🌟 Sunday: All Talent Domains Open!", color = theme.amber, fontSize = 11.sp, fontWeight = FontWeight.Bold)
            }
        }

        // 3. SERENITEA POT (UNLOCKS AT AR 28)
        if (arLevel >= 28) {
            Card(
                colors = CardDefaults.cardColors(containerColor = theme.cardBg),
                shape = RoundedCornerShape(12.dp),
                modifier = Modifier
                    .fillMaxWidth()
                    .border(1.dp, Color(0xFF333847), RoundedCornerShape(12.dp))
            ) {
                Column(modifier = Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    Text("SERENITEA POT (UNLOCKED AT AR 28)", color = theme.cyan, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Checkbox(checked = resinClaimed, onCheckedChange = { resinClaimed = it }, colors = checkboxColors)
                        Text("Transient Resin", color = Color.White, fontSize = 12.sp)
                        Spacer(modifier = Modifier.width(6.dp))
                        Checkbox(checked = xpClaimed, onCheckedChange = { xpClaimed = it }, colors = checkboxColors)
                        Text("Hero's Wit/Books", color = Color.White, fontSize = 12.sp)
                    }
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Checkbox(checked = coinsClaimed, onCheckedChange = { coinsClaimed = it }, colors = checkboxColors)
                        Text("Artifact Unction/Exp", color = Color.White, fontSize = 12.sp)
                    }
                }
            }
        }

        // 4. PARAMETRIC TRANSFORMER (UNLOCKS AT AR 31)
        if (arLevel >= 31) {
            Card(
                colors = CardDefaults.cardColors(containerColor = theme.cardBg),
                shape = RoundedCornerShape(12.dp),
                modifier = Modifier
                    .fillMaxWidth()
                    .border(1.dp, Color(0xFF333847), RoundedCornerShape(12.dp))
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(14.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column {
                        Text("PARAMETRIC TRANSFORMER (AR 31)", color = theme.cyan, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                        Text("Ready!", color = Color(0xFF4ADE80), fontWeight = FontWeight.Bold, fontSize = 13.sp)
                    }
                    Button(
                        onClick = { /* Reset Timer */ },
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2E323F)),
                        shape = RoundedCornerShape(6.dp),
                        border = androidx.compose.foundation.BorderStroke(1.dp, theme.cyan)
                    ) {
                        Text("Use Now (7d)", color = theme.cyan, fontSize = 11.sp)
                    }
                }
            }
        }

        // 5. ARTIFACT ROUTE (UNLOCKS AT AR 45)
        if (arLevel >= 45) {
            Card(
                colors = CardDefaults.cardColors(containerColor = theme.cardBg),
                shape = RoundedCornerShape(12.dp),
                modifier = Modifier
                    .fillMaxWidth()
                    .border(1.dp, Color(0xFF333847), RoundedCornerShape(12.dp))
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(14.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column {
                        Text("ARTIFACT ROUTE (AR 45)", color = theme.cyan, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                        Text("Ready to Farm!", color = Color(0xFF4ADE80), fontWeight = FontWeight.Bold, fontSize = 13.sp)
                    }
                    Button(
                        onClick = { /* Set Cooldown */ },
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2E323F)),
                        shape = RoundedCornerShape(6.dp),
                        border = androidx.compose.foundation.BorderStroke(1.dp, theme.cyan)
                    ) {
                        Text("Route Finished", color = theme.cyan, fontSize = 11.sp)
                    }
                }
            }
        }

        // 6. ENDGAME STARS (UNLOCKS AT AR 45)
        if (arLevel >= 45) {
            Card(
                colors = CardDefaults.cardColors(containerColor = theme.cardBg),
                shape = RoundedCornerShape(12.dp),
                modifier = Modifier
                    .fillMaxWidth()
                    .border(1.dp, Color(0xFF333847), RoundedCornerShape(12.dp))
            ) {
                Column(modifier = Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("ENDGAME STARS (AR 45)", color = theme.cyan, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text("Abyss: ", color = Color.White, fontSize = 12.sp)
                            IconButton(onClick = { if (abyssStars > 0) abyssStars-- }, modifier = Modifier.size(24.dp)) {
                                Text("-", color = theme.cyan, fontSize = 14.sp)
                            }
                            Text("$abyssStars / 36", color = theme.amber, fontWeight = FontWeight.Bold, fontSize = 12.sp)
                            IconButton(onClick = { if (abyssStars < 36) abyssStars++ }, modifier = Modifier.size(24.dp)) {
                                Text("+", color = theme.cyan, fontSize = 14.sp)
                            }
                        }

                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text("Theater: ", color = Color.White, fontSize = 12.sp)
                            IconButton(onClick = { if (theaterStars > 0) theaterStars-- }, modifier = Modifier.size(24.dp)) {
                                Text("-", color = theme.cyan, fontSize = 14.sp)
                            }
                            Text("$theaterStars / 10", color = theme.amber, fontWeight = FontWeight.Bold, fontSize = 12.sp)
                            IconButton(onClick = { if (theaterStars < 10) theaterStars++ }, modifier = Modifier.size(24.dp)) {
                                Text("+", color = theme.cyan, fontSize = 14.sp)
                            }
                        }
                    }
                }
            }
        }
    }
}

// =========================================================
// 2. Crafting Calculator Screen
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
// 3. Wish & Pity Counter Screen
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
                            uncheckedColor = Color.White,
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
// 4. Resin Overflow Planner Screen
// =========================================================
@Composable
fun ResinPlannerScreen(theme: RegionTheme) {
    var targetResinStr by remember { mutableStateOf("160") }
    val targetResin = targetResinStr.toIntOrNull() ?: 160
    val minutesNeeded = (targetResin * 8)
    val hoursNeeded = minutesNeeded / 60
    val remMinutes = minutesNeeded % 60

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState()),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text(
            text = "⚡ Resin Overflow & Cap Planner",
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
                Text(
                    text = "CALCULATE REGEN TIME",
                    color = theme.cyan,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold
                )
                OutlinedTextField(
                    value = targetResinStr,
                    onValueChange = { targetResinStr = it },
                    label = { Text("Target Resin Amount") },
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedTextColor = Color.White,
                        unfocusedTextColor = Color.White,
                        focusedLabelColor = theme.cyan,
                        unfocusedLabelColor = Color(0xFFCBD5E1),
                        focusedBorderColor = theme.cyan,
                        unfocusedBorderColor = Color(0xFF475569)
                    ),
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )

                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = "⏱️ Time from 0 to $targetResin Resin: ${hoursNeeded}h ${remMinutes}m",
                    color = Color.White,
                    fontWeight = FontWeight.Bold,
                    fontSize = 13.sp
                )
            }
        }
    }
}

// =========================================================
// 5. Weekly Boss Tracker Screen
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

    val checkboxColors = CheckboxDefaults.colors(
        checkedColor = theme.cyan,
        uncheckedColor = Color.White,
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

// =========================================================
// 6. Team Building & Farming Goals Screen (Mobil-Dashboard)
// =========================================================
@Composable
fun TeamGoalsScreen(theme: RegionTheme) {
    // 4 Team slots (Default: Kaeya, Fischl, Noelle, Traveler)
    var char1 by remember { mutableStateOf("Kaeya") }
    var book1 by remember { mutableStateOf("Ballad (Wed/Sat/Sun)") }

    var char2 by remember { mutableStateOf("Fischl") }
    var book2 by remember { mutableStateOf("Resistance (Tue/Fri/Sun)") }

    var char3 by remember { mutableStateOf("Noelle") }
    var book3 by remember { mutableStateOf("Resistance (Tue/Fri/Sun)") }

    var char4 by remember { mutableStateOf("Traveler (Anemo)") }
    var book4 by remember { mutableStateOf("Freedom (Mon/Thu/Sun)") }

    val talentBookOptions = listOf(
        "Freedom (Mon/Thu/Sun)",
        "Resistance (Tue/Fri/Sun)",
        "Ballad (Wed/Sat/Sun)",
        "Prosperity (Mon/Thu/Sun)",
        "Diligence (Tue/Fri/Sun)",
        "Gold (Wed/Sat/Sun)",
        "Transience (Mon/Thu/Sun)",
        "Elegance (Tue/Fri/Sun)",
        "Light (Wed/Sat/Sun)",
        "Admonition (Mon/Thu/Sun)",
        "Ingenuity (Tue/Fri/Sun)",
        "Praxis (Wed/Sat/Sun)",
        "Equity (Mon/Thu/Sun)",
        "Justice (Tue/Fri/Sun)",
        "Order (Wed/Sat/Sun)",
        "Contention (Mon/Thu/Sun)",
        "Kindling (Tue/Fri/Sun)",
        "Conflict (Wed/Sat/Sun)"
    )

    // Automatische Gruppierung nach Wochentagen für den Schedule
    fun getScheduleForDays(daysKeyword: String): String {
        val chars = mutableListOf<String>()
        val slots = listOf(
            Triple(char1, book1, "Freedom"),
            Triple(char2, book2, "Resistance"),
            Triple(char3, book3, "Ballad"),
            Triple(char4, book4, "Freedom")
        )

        // Helper zum Zuordnen
        if (book1.contains(daysKeyword)) chars.add("$char1 (${book1.substringBefore(" ")})")
        if (book2.contains(daysKeyword)) chars.add("$char2 (${book2.substringBefore(" ")})")
        if (book3.contains(daysKeyword)) chars.add("$char3 (${book3.substringBefore(" ")})")
        if (book4.contains(daysKeyword)) chars.add("$char4 (${book4.substringBefore(" ")})")

        return if (chars.isNotEmpty()) chars.joinToString(", ") else "None"
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState()),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text(
            text = "🎯 Team Building & Material Farming Goals",
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
                modifier = Modifier.padding(14.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text("TEAM CHARACTER", color = Color.Gray, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                    Text("TALENT BOOK GOAL", color = Color.Gray, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                }

                // Slot 1
                TeamSlotRow(
                    charName = char1,
                    onCharChange = { char1 = it },
                    bookName = book1,
                    onBookChange = { book1 = it },
                    bookOptions = talentBookOptions,
                    theme = theme
                )

                // Slot 2
                TeamSlotRow(
                    charName = char2,
                    onCharChange = { char2 = it },
                    bookName = book2,
                    onBookChange = { book2 = it },
                    bookOptions = talentBookOptions,
                    theme = theme
                )

                // Slot 3
                TeamSlotRow(
                    charName = char3,
                    onCharChange = { char3 = it },
                    bookName = book3,
                    onBookChange = { book3 = it },
                    bookOptions = talentBookOptions,
                    theme = theme
                )

                // Slot 4
                TeamSlotRow(
                    charName = char4,
                    onCharChange = { char4 = it },
                    bookName = book4,
                    onBookChange = { book4 = it },
                    bookOptions = talentBookOptions,
                    theme = theme
                )
            }
        }

        // Schedule Card
        Card(
            colors = CardDefaults.cardColors(containerColor = theme.cardBg),
            shape = RoundedCornerShape(12.dp),
            modifier = Modifier
                .fillMaxWidth()
                .border(1.dp, Color(0xFF333847), RoundedCornerShape(12.dp))
        ) {
            Column(
                modifier = Modifier.padding(14.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Text(
                    text = "WEEKLY DOMAIN FARMING SCHEDULE",
                    color = theme.cyan,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold
                )

                Text(
                    text = "📅 Mon / Thu: ${getScheduleForDays("Mon")}",
                    color = Color.White,
                    fontSize = 12.sp
                )
                Text(
                    text = "📅 Tue / Fri: ${getScheduleForDays("Tue")}",
                    color = Color.White,
                    fontSize = 12.sp
                )
                Text(
                    text = "📅 Wed / Sat: ${getScheduleForDays("Wed")}",
                    color = Color.White,
                    fontSize = 12.sp
                )
                Text(
                    text = "📅 Sunday: All Talent Domains Open!",
                    color = theme.amber,
                    fontWeight = FontWeight.Bold,
                    fontSize = 12.sp
                )
            }
        }
    }
}

// Helper für die einzelnen Zeilen in Android
@Composable
fun TeamSlotRow(
    charName: String,
    onCharChange: (String) -> Unit,
    bookName: String,
    onBookChange: (String) -> Unit,
    bookOptions: List<String>,
    theme: RegionTheme
) {
    var bookExpanded by remember { mutableStateOf(false) }

    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Charakter Name
            OutlinedTextField(
                value = charName,
                onValueChange = onCharChange,
                singleLine = true,
                textStyle = androidx.compose.ui.text.TextStyle(color = Color.White, fontSize = 12.sp),
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = theme.cyan,
                    unfocusedBorderColor = Color(0xFF475569)
                ),
                modifier = Modifier.weight(1f)
            )

            // Talent Buch Dropdown
            Box(modifier = Modifier.weight(1.2f)) {
                OutlinedButton(
                    onClick = { bookExpanded = true },
                    shape = RoundedCornerShape(4.dp),
                    contentPadding = PaddingValues(horizontal = 8.dp, vertical = 0.dp),
                    border = androidx.compose.foundation.BorderStroke(1.dp, theme.cyan),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text(
                        text = bookName,
                        color = theme.cyan,
                        fontSize = 10.sp,
                        maxLines = 1
                    )
                }
                DropdownMenu(
                    expanded = bookExpanded,
                    onDismissRequest = { bookExpanded = false }
                ) {
                    bookOptions.forEach { opt ->
                        DropdownMenuItem(
                            text = { Text(opt, fontSize = 11.sp) },
                            onClick = {
                                onBookChange(opt)
                                bookExpanded = false
                            }
                        )
                    }
                }
            }
        }
    }
}
