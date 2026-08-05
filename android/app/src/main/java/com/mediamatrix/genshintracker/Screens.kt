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
// 1. Teyvat Journal Screen
// =========================================================
@Composable
fun TeyvatJournalScreen(theme: RegionTheme, language: String) {
    var arLevel by remember { mutableIntStateOf(60) }

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
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = AppTranslations.tr("journal_title", language),
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

        // 1. Daily Commissions
        Card(
            colors = CardDefaults.cardColors(containerColor = theme.cardBg),
            shape = RoundedCornerShape(12.dp),
            modifier = Modifier
                .fillMaxWidth()
                .border(1.dp, Color(0xFF333847), RoundedCornerShape(12.dp))
        ) {
            Column(modifier = Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                Text(AppTranslations.tr("daily_comm", language), color = theme.cyan, fontSize = 11.sp, fontWeight = FontWeight.Bold)
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
                    Text(AppTranslations.tr("katheryne_bonus", language), color = theme.amber, fontWeight = FontWeight.Bold, fontSize = 12.sp)
                }
            }
        }

        // 2. Weekly Bosses
        Card(
            colors = CardDefaults.cardColors(containerColor = theme.cardBg),
            shape = RoundedCornerShape(12.dp),
            modifier = Modifier
                .fillMaxWidth()
                .border(1.dp, Color(0xFF333847), RoundedCornerShape(12.dp))
        ) {
            Column(modifier = Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                Text(AppTranslations.tr("weekly_bosses", language), color = theme.cyan, fontSize = 11.sp, fontWeight = FontWeight.Bold)
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
                Text(AppTranslations.tr("sunday_talent", language), color = theme.amber, fontSize = 11.sp, fontWeight = FontWeight.Bold)
            }
        }

        // 3. Serenitea Pot
        if (arLevel >= 28) {
            Card(
                colors = CardDefaults.cardColors(containerColor = theme.cardBg),
                shape = RoundedCornerShape(12.dp),
                modifier = Modifier
                    .fillMaxWidth()
                    .border(1.dp, Color(0xFF333847), RoundedCornerShape(12.dp))
            ) {
                Column(modifier = Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    Text(AppTranslations.tr("teapot", language), color = theme.cyan, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Checkbox(checked = resinClaimed, onCheckedChange = { resinClaimed = it }, colors = checkboxColors)
                        Text(AppTranslations.tr("transient_resin", language), color = Color.White, fontSize = 12.sp)
                        Spacer(modifier = Modifier.width(6.dp))
                        Checkbox(checked = xpClaimed, onCheckedChange = { xpClaimed = it }, colors = checkboxColors)
                        Text(AppTranslations.tr("heros_wit", language), color = Color.White, fontSize = 12.sp)
                    }
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Checkbox(checked = coinsClaimed, onCheckedChange = { coinsClaimed = it }, colors = checkboxColors)
                        Text(AppTranslations.tr("artifact_exp", language), color = Color.White, fontSize = 12.sp)
                    }
                }
            }
        }

        // 4. Parametric Transformer
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
                        Text(AppTranslations.tr("parametric", language), color = theme.cyan, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                        Text(AppTranslations.tr("ready_claim", language), color = Color(0xFF4ADE80), fontWeight = FontWeight.Bold, fontSize = 13.sp)
                    }
                    Button(
                        onClick = { },
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2E323F)),
                        shape = RoundedCornerShape(6.dp),
                        border = androidx.compose.foundation.BorderStroke(1.dp, theme.cyan)
                    ) {
                        Text(AppTranslations.tr("use_now", language), color = theme.cyan, fontSize = 11.sp)
                    }
                }
            }
        }

        // 5. Artifact Route
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
                        Text(AppTranslations.tr("artifact_route", language), color = theme.cyan, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                        Text(AppTranslations.tr("ready_farm", language), color = Color(0xFF4ADE80), fontWeight = FontWeight.Bold, fontSize = 13.sp)
                    }
                    Button(
                        onClick = { },
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2E323F)),
                        shape = RoundedCornerShape(6.dp),
                        border = androidx.compose.foundation.BorderStroke(1.dp, theme.cyan)
                    ) {
                        Text(AppTranslations.tr("route_finished", language), color = theme.cyan, fontSize = 11.sp)
                    }
                }
            }
        }

        // 6. Endgame Stars
        if (arLevel >= 45) {
            Card(
                colors = CardDefaults.cardColors(containerColor = theme.cardBg),
                shape = RoundedCornerShape(12.dp),
                modifier = Modifier
                    .fillMaxWidth()
                    .border(1.dp, Color(0xFF333847), RoundedCornerShape(12.dp))
            ) {
                Column(modifier = Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text(AppTranslations.tr("endgame_stars", language), color = theme.cyan, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text("${AppTranslations.tr("abyss", language)} ", color = Color.White, fontSize = 12.sp)
                            IconButton(onClick = { if (abyssStars > 0) abyssStars-- }, modifier = Modifier.size(24.dp)) {
                                Text("-", color = theme.cyan, fontSize = 14.sp)
                            }
                            Text("$abyssStars / 36", color = theme.amber, fontWeight = FontWeight.Bold, fontSize = 12.sp)
                            IconButton(onClick = { if (abyssStars < 36) abyssStars++ }, modifier = Modifier.size(24.dp)) {
                                Text("+", color = theme.cyan, fontSize = 14.sp)
                            }
                        }

                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text("${AppTranslations.tr("theater", language)} ", color = Color.White, fontSize = 12.sp)
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
fun CraftingCalculatorScreen(theme: RegionTheme, language: String) {
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
            text = AppTranslations.tr("crafting_title", language),
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
                    text = AppTranslations.tr("crafting_passive", language),
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
                        Text(AppTranslations.tr("none", language), fontSize = 11.sp, color = if (passiveMode == 0) Color.Black else Color.White, fontWeight = FontWeight.Bold)
                    }
                    Button(
                        onClick = { passiveMode = 1 },
                        colors = ButtonDefaults.buttonColors(
                            containerColor = if (passiveMode == 1) theme.cyan else Color(0xFF2E323F)
                        )
                    ) {
                        Text(AppTranslations.tr("sucrose_passive", language), fontSize = 11.sp, color = if (passiveMode == 1) Color.Black else Color.White, fontWeight = FontWeight.Bold)
                    }
                    Button(
                        onClick = { passiveMode = 2 },
                        colors = ButtonDefaults.buttonColors(
                            containerColor = if (passiveMode == 2) theme.cyan else Color(0xFF2E323F)
                        )
                    ) {
                        Text(AppTranslations.tr("mona_passive", language), fontSize = 11.sp, color = if (passiveMode == 2) Color.Black else Color.White, fontWeight = FontWeight.Bold)
                    }
                }

                Spacer(modifier = Modifier.height(4.dp))

                OutlinedTextField(
                    value = tier1,
                    onValueChange = { tier1 = it },
                    label = { Text(AppTranslations.tr("tier1", language)) },
                    colors = customFieldColors,
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = tier2,
                    onValueChange = { tier2 = it },
                    label = { Text(AppTranslations.tr("tier2", language)) },
                    colors = customFieldColors,
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = tier3,
                    onValueChange = { tier3 = it },
                    label = { Text(AppTranslations.tr("tier3", language)) },
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
                    text = AppTranslations.tr("crafting_summary", language),
                    color = theme.cyan,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold
                )
                Text(
                    text = "${AppTranslations.tr("total_blue", language)} $totalT2 (+ $craftedT2)",
                    color = Color.White,
                    fontSize = 13.sp
                )
                Text(
                    text = "${AppTranslations.tr("max_purple", language)} $totalT3 (+ $craftedT3)",
                    color = Color.White,
                    fontSize = 13.sp
                )
                Text(
                    text = "${AppTranslations.tr("est_cost", language)} $estimatedMora Mora",
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
fun WishCounterScreen(theme: RegionTheme, language: String) {
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
            text = AppTranslations.tr("wish_title", language),
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
                    label = { Text(AppTranslations.tr("current_pity", language)) },
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
                    Text(AppTranslations.tr("next_guaranteed", language), color = Color.White, fontSize = 13.sp)
                }
                OutlinedTextField(
                    value = primosStr,
                    onValueChange = { primosStr = it },
                    label = { Text(AppTranslations.tr("primos_owned", language)) },
                    colors = customFieldColors,
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = fatesStr,
                    onValueChange = { fatesStr = it },
                    label = { Text(AppTranslations.tr("fates_owned", language)) },
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
                    text = AppTranslations.tr("pity_summary", language),
                    color = theme.cyan,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold
                )
                Text("💫 ${AppTranslations.tr("total_pulls", language)} $totalWishes", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 13.sp)
                Text("🎯 ${AppTranslations.tr("to_soft", language)} $toSoft", color = Color.White, fontSize = 12.sp)
                Text("🛡️ ${AppTranslations.tr("to_hard", language)} $toHard", color = Color.White, fontSize = 12.sp)
                Text(
                    text = if (isGuaranteed) AppTranslations.tr("status_guar", language) else AppTranslations.tr("status_5050", language),
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
fun ResinPlannerScreen(theme: RegionTheme, language: String) {
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
            text = AppTranslations.tr("resin_planner_title", language),
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
                    text = AppTranslations.tr("calc_regen", language),
                    color = theme.cyan,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold
                )
                OutlinedTextField(
                    value = targetResinStr,
                    onValueChange = { targetResinStr = it },
                    label = { Text(AppTranslations.tr("target_resin", language)) },
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
                    text = "⏱️ ${AppTranslations.tr("time_from_zero", language)} $targetResin: ${hoursNeeded}h ${remMinutes}m",
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
fun WeeklyBossScreen(theme: RegionTheme, language: String) {
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
            text = AppTranslations.tr("boss_title", language),
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
                    text = "${AppTranslations.tr("discounts_avail", language)} ($remaining / 3)",
                    color = theme.cyan,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold
                )
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Checkbox(checked = slot1, onCheckedChange = { slot1 = it }, colors = checkboxColors)
                    Text("${AppTranslations.tr("discount_slot", language)} 1 (30 Resin)", color = Color.White, fontSize = 13.sp)
                }
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Checkbox(checked = slot2, onCheckedChange = { slot2 = it }, colors = checkboxColors)
                    Text("${AppTranslations.tr("discount_slot", language)} 2 (30 Resin)", color = Color.White, fontSize = 13.sp)
                }
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Checkbox(checked = slot3, onCheckedChange = { slot3 = it }, colors = checkboxColors)
                    Text("${AppTranslations.tr("discount_slot", language)} 3 (30 Resin)", color = Color.White, fontSize = 13.sp)
                }
                Spacer(modifier = Modifier.height(4.dp))
                Text("💰 ${AppTranslations.tr("resin_saved", language)} $savedResin Resin", color = theme.amber, fontWeight = FontWeight.Bold, fontSize = 13.sp)
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
                    text = AppTranslations.tr("defeated_bosses", language),
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
// 6. Team Building & Material Farming Goals Screen
// =========================================================

val CHARACTER_BOOKS = mapOf(
    // Mondstadt
    "Amber" to "Freedom (Mon/Thu/Sun)",
    "Barbara" to "Freedom (Mon/Thu/Sun)",
    "Bennett" to "Resistance (Tue/Fri/Sun)",
    "Diluc" to "Resistance (Tue/Fri/Sun)",
    "Diona" to "Freedom (Mon/Thu/Sun)",
    "Eula" to "Resistance (Tue/Fri/Sun)",
    "Fischl" to "Resistance (Tue/Fri/Sun)",
    "Jean" to "Resistance (Tue/Fri/Sun)",
    "Kaeya" to "Ballad (Wed/Sat/Sun)",
    "Klee" to "Freedom (Mon/Thu/Sun)",
    "Lisa" to "Ballad (Wed/Sat/Sun)",
    "Mona" to "Resistance (Tue/Fri/Sun)",
    "Mika" to "Ballad (Wed/Sat/Sun)",
    "Noelle" to "Resistance (Tue/Fri/Sun)",
    "Razor" to "Resistance (Tue/Fri/Sun)",
    "Rosaria" to "Ballad (Wed/Sat/Sun)",
    "Sucrose" to "Freedom (Mon/Thu/Sun)",
    "Traveler (Anemo)" to "Freedom (Mon/Thu/Sun)",
    "Traveler (Geo)" to "Prosperity (Mon/Thu/Sun)",
    "Venti" to "Ballad (Wed/Sat/Sun)",

    // Liyue
    "Beidou" to "Gold (Wed/Sat/Sun)",
    "Chongyun" to "Diligence (Tue/Fri/Sun)",
    "Ganyu" to "Diligence (Tue/Fri/Sun)",
    "Gaming" to "Prosperity (Mon/Thu/Sun)",
    "Hu Tao" to "Diligence (Tue/Fri/Sun)",
    "Keqing" to "Prosperity (Mon/Thu/Sun)",
    "Ningguang" to "Prosperity (Mon/Thu/Sun)",
    "Qiqi" to "Prosperity (Mon/Thu/Sun)",
    "Shenhe" to "Prosperity (Mon/Thu/Sun)",
    "Xiangling" to "Gold (Wed/Sat/Sun)",
    "Xianyun" to "Gold (Wed/Sat/Sun)",
    "Xingqiu" to "Gold (Wed/Sat/Sun)",
    "Xinyan" to "Gold (Wed/Sat/Sun)",
    "Yanfei" to "Gold (Wed/Sat/Sun)",
    "Yelan" to "Prosperity (Mon/Thu/Sun)",
    "Yao Yao" to "Diligence (Tue/Fri/Sun)",
    "Yun Jin" to "Diligence (Tue/Fri/Sun)",
    "Zhongli" to "Gold (Wed/Sat/Sun)",

    // Inazuma
    "Arataki Itto" to "Elegance (Tue/Fri/Sun)",
    "Gorou" to "Light (Wed/Sat/Sun)",
    "Kaedehara Kazuha" to "Diligence (Tue/Fri/Sun)",
    "Kamisato Ayaka" to "Elegance (Tue/Fri/Sun)",
    "Kamisato Ayato" to "Elegance (Tue/Fri/Sun)",
    "Kirara" to "Transience (Mon/Thu/Sun)",
    "Kujou Sara" to "Elegance (Tue/Fri/Sun)",
    "Kuki Shinobu" to "Elegance (Tue/Fri/Sun)",
    "Raiden Shogun" to "Light (Wed/Sat/Sun)",
    "Sangonomiya Kokomi" to "Transience (Mon/Thu/Sun)",
    "Sayu" to "Light (Wed/Sat/Sun)",
    "Shikanoin Heizou" to "Transience (Mon/Thu/Sun)",
    "Thoma" to "Transience (Mon/Thu/Sun)",
    "Yae Miko" to "Light (Wed/Sat/Sun)",
    "Yoimiya" to "Transience (Mon/Thu/Sun)",

    // Sumeru
    "Alhaitham" to "Ingenuity (Tue/Fri/Sun)",
    "Candace" to "Admonition (Mon/Thu/Sun)",
    "Collei" to "Praxis (Wed/Sat/Sun)",
    "Cyno" to "Admonition (Mon/Thu/Sun)",
    "Dehya" to "Praxis (Wed/Sat/Sun)",
    "Faruzan" to "Admonition (Mon/Thu/Sun)",
    "Kaveh" to "Ingenuity (Tue/Fri/Sun)",
    "Layla" to "Ingenuity (Tue/Fri/Sun)",
    "Nahida" to "Ingenuity (Tue/Fri/Sun)",
    "Nilou" to "Praxis (Wed/Sat/Sun)",
    "Tighnari" to "Admonition (Mon/Thu/Sun)",
    "Wanderer" to "Praxis (Wed/Sat/Sun)",

    // Fontaine
    "Arlecchino" to "Order (Wed/Sat/Sun)",
    "Clorinde" to "Justice (Tue/Fri/Sun)",
    "Charlotte" to "Justice (Tue/Fri/Sun)",
    "Chevreuse" to "Order (Wed/Sat/Sun)",
    "Freminet" to "Justice (Tue/Fri/Sun)",
    "Furina" to "Justice (Tue/Fri/Sun)",
    "Lynette" to "Freedom (Mon/Thu/Sun)",
    "Lyney" to "Equity (Mon/Thu/Sun)",
    "Navia" to "Equity (Mon/Thu/Sun)",
    "Neuvillette" to "Equity (Mon/Thu/Sun)",
    "Wriothesley" to "Justice (Tue/Fri/Sun)",

    // Natlan
    "Kachina" to "Conflict (Wed/Sat/Sun)",
    "Kinich" to "Kindling (Tue/Fri/Sun)",
    "Mualani" to "Contention (Mon/Thu/Sun)",
    "Xilonen" to "Kindling (Tue/Fri/Sun)"
)

val TALENT_BOOK_OPTIONS = listOf(
    "Freedom (Mon/Thu/Sun)", "Resistance (Tue/Fri/Sun)", "Ballad (Wed/Sat/Sun)",
    "Prosperity (Mon/Thu/Sun)", "Diligence (Tue/Fri/Sun)", "Gold (Wed/Sat/Sun)",
    "Transience (Mon/Thu/Sun)", "Elegance (Tue/Fri/Sun)", "Light (Wed/Sat/Sun)",
    "Admonition (Mon/Thu/Sun)", "Ingenuity (Tue/Fri/Sun)", "Praxis (Wed/Sat/Sun)",
    "Equity (Mon/Thu/Sun)", "Justice (Tue/Fri/Sun)", "Order (Wed/Sat/Sun)",
    "Contention (Mon/Thu/Sun)", "Kindling (Tue/Fri/Sun)", "Conflict (Wed/Sat/Sun)"
)

data class TeamSlotData(
    val character: String,
    val book: String
)

@Composable
fun TeamGoalsScreen(theme: RegionTheme, language: String) {
    val charList = remember { CHARACTER_BOOKS.keys.toList().sorted() }

    var slots by remember {
        mutableStateOf(
            listOf(
                TeamSlotData("Kaeya", CHARACTER_BOOKS["Kaeya"] ?: TALENT_BOOK_OPTIONS[2]),
                TeamSlotData("Fischl", CHARACTER_BOOKS["Fischl"] ?: TALENT_BOOK_OPTIONS[1]),
                TeamSlotData("Xiangling", CHARACTER_BOOKS["Xiangling"] ?: TALENT_BOOK_OPTIONS[5]),
                TeamSlotData("Barbara", CHARACTER_BOOKS["Barbara"] ?: TALENT_BOOK_OPTIONS[0])
            )
        )
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState()),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text(
            text = AppTranslations.tr("goals_title", language),
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
                    Text(AppTranslations.tr("team_char", language), color = Color.Gray, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                    Text(AppTranslations.tr("talent_goal", language), color = Color.Gray, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                }

                slots.forEachIndexed { index, slot ->
                    TeamSlotRow(
                        slotData = slot,
                        charList = charList,
                        bookOptions = TALENT_BOOK_OPTIONS,
                        theme = theme,
                        onSlotChange = { updatedSlot ->
                            val updatedList = slots.toMutableList()
                            updatedList[index] = updatedSlot
                            slots = updatedList
                        }
                    )
                }
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
                    text = AppTranslations.tr("schedule_title", language),
                    color = theme.cyan,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold
                )

                val monThu = mutableListOf<String>()
                val tueFri = mutableListOf<String>()
                val wedSat = mutableListOf<String>()

                slots.forEach { s ->
                    if (s.character.isNotBlank()) {
                        val bookName = s.book.split(" ")[0]
                        val entry = "${s.character} ($bookName)"
                        when {
                            "Mon/Thu" in s.book -> monThu.add(entry)
                            "Tue/Fri" in s.book -> tueFri.add(entry)
                            "Wed/Sat" in s.book -> wedSat.add(entry)
                        }
                    }
                }

                val monText = if (monThu.isNotEmpty()) monThu.joinToString(", ") else "None"
                val tueText = if (tueFri.isNotEmpty()) tueFri.joinToString(", ") else "None"
                val wedText = if (wedSat.isNotEmpty()) wedSat.joinToString(", ") else "None"

                Text("📅 ${AppTranslations.tr("mon_thu", language)} $monText", color = Color.White, fontSize = 12.sp)
                Text("📅 ${AppTranslations.tr("tue_fri", language)} $tueText", color = Color.White, fontSize = 12.sp)
                Text("📅 ${AppTranslations.tr("wed_sat", language)} $wedText", color = Color.White, fontSize = 12.sp)
                Text("📅 ${AppTranslations.tr("sun_all", language)}", color = theme.amber, fontWeight = FontWeight.Bold, fontSize = 12.sp)
            }
        }
    }
}

@Composable
fun TeamSlotRow(
    slotData: TeamSlotData,
    charList: List<String>,
    bookOptions: List<String>,
    theme: RegionTheme,
    onSlotChange: (TeamSlotData) -> Unit
) {
    var charExpanded by remember { mutableStateOf(false) }
    var bookExpanded by remember { mutableStateOf(false) }

    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(modifier = Modifier.weight(1f)) {
            OutlinedButton(
                onClick = { charExpanded = true },
                shape = RoundedCornerShape(4.dp),
                contentPadding = PaddingValues(horizontal = 8.dp, vertical = 4.dp),
                border = androidx.compose.foundation.BorderStroke(1.dp, theme.cyan),
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(
                    text = slotData.character,
                    color = Color.White,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    maxLines = 1
                )
            }
            DropdownMenu(
                expanded = charExpanded,
                onDismissRequest = { charExpanded = false }
            ) {
                charList.forEach { cName ->
                    DropdownMenuItem(
                        text = { Text(cName, fontSize = 12.sp) },
                        onClick = {
                            val autoBook = CHARACTER_BOOKS[cName] ?: slotData.book
                            onSlotChange(TeamSlotData(character = cName, book = autoBook))
                            charExpanded = false
                        }
                    )
                }
            }
        }

        Box(modifier = Modifier.weight(1.2f)) {
            OutlinedButton(
                onClick = { bookExpanded = true },
                shape = RoundedCornerShape(4.dp),
                contentPadding = PaddingValues(horizontal = 8.dp, vertical = 4.dp),
                border = androidx.compose.foundation.BorderStroke(1.dp, theme.cyan),
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(
                    text = slotData.book,
                    color = theme.cyan,
                    fontSize = 10.sp,
                    fontWeight = FontWeight.Bold,
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
                            onSlotChange(slotData.copy(book = opt))
                            bookExpanded = false
                        }
                    )
                }
            }
        }
    }
}