package com.mediamatrix.genshintracker

import android.Manifest
import android.content.Context
import android.content.pm.ActivityInfo
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.BlendMode
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.ColorFilter
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.workDataOf
import com.mediamatrix.genshintracker.ui.theme.GenshinExpeditionTrackerTheme
import kotlinx.coroutines.delay
import org.json.JSONArray
import org.json.JSONObject
import java.util.Calendar
import java.util.Locale
import java.util.concurrent.TimeUnit

// --- Regionales Theme-System für Teyvat ---
data class RegionTheme(
    val name: String,
    val cyan: Color,
    val amber: Color,
    val bgDark: Color,
    val cardBg: Color,
    val boxDark: Color = Color(0xFF12141C)
)

val REGION_THEMES = mapOf(
    "Mondstadt (Anemo)" to RegionTheme("Mondstadt (Anemo)", Color(0xFF38E3E3), Color(0xFFFFAA00), Color(0xFF1A1C24), Color(0xFF252833)),
    "Liyue (Geo)" to RegionTheme("Liyue (Geo)", Color(0xFFE6A000), Color(0xFFFFD266), Color(0xFF221D14), Color(0xFF30291D)),
    "Inazuma (Electro)" to RegionTheme("Inazuma (Electro)", Color(0xFFA855F7), Color(0xFFF0ABFC), Color(0xFF1A1325), Color(0xFF251B36)),
    "Sumeru (Dendro)" to RegionTheme("Sumeru (Dendro)", Color(0xFF22C55E), Color(0xFFFACC15), Color(0xFF122017), Color(0xFF1A2E21)),
    "Fontaine (Hydro)" to RegionTheme("Fontaine (Hydro)", Color(0xFF38BDF8), Color(0xFFF472B6), Color(0xFF111C28), Color(0xFF182838)),
    "Natlan (Pyro)" to RegionTheme("Natlan (Pyro)", Color(0xFFEF4444), Color(0xFFFBBF24), Color(0xFF241313), Color(0xFF331C1C)),
    "Snezhnaya (Cryo)" to RegionTheme("Snezhnaya (Cryo)", Color(0xFF99F6E4), Color(0xFFA5F3FC), Color(0xFF121D24), Color(0xFF1A2933))
)

// --- MEHRSPRACHIGKEIT / TRANSLATION DICTIONARY ---
object AppTranslations {
    private val en = mapOf(
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
        "settings" to "Settings",
        "language" to "Language / Sprache:",
        "in" to "in",
        "full" to "FULL!",
        "full_in" to "Full in"
    )

    private val de = mapOf(
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
        "claim_all" to "Alle Bereits Einsammeln",
        "start_new" to "+ Neue Expedition starten",
        "limit_reached" to "Limit erreicht",
        "ready" to "BEREIT!",
        "running" to "Läuft",
        "claim_reward" to "Belohnung holen",
        "settings" to "Einstellungen",
        "language" to "Sprache / Language:",
        "in" to "in",
        "full" to "VOLL!",
        "full_in" to "Voll in"
    )

    fun tr(key: String, lang: String): String {
        val map = if (lang == "Deutsch") de else en
        return map[key] ?: key
    }
}

// --- Bonus-Zuordnung: Charakter zu Heimatregion (-25% Zeitersparnis) ---
val TIME_REDUCTION_BONUS = mapOf(
    "Bennett" to "Mondstadt",
    "Fischl" to "Mondstadt",
    "Chongyun" to "Liyue",
    "Keqing" to "Liyue",
    "Shenhe" to "Liyue",
    "Yelan" to "Liyue",
    "Kujou Sara" to "Inazuma"
)

val DURATIONS_STANDARD = listOf(
    "4 Hours" to 4,
    "8 Hours" to 8,
    "12 Hours" to 12,
    "20 Hours (Standard)" to 20
)

val DURATIONS_BONUS = listOf(
    "3 Hours (Bonus 4h)" to 3,
    "6 Hours (Bonus 8h)" to 6,
    "9 Hours (Bonus 12h)" to 9,
    "15 Hours (Bonus 20h)" to 15
)

class MainActivity : ComponentActivity() {

    private val requestPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { _ -> }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val isTablet = resources.configuration.smallestScreenWidthDp >= 600
        if (!isTablet) {
            requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_PORTRAIT
        }

        NotificationHelper.createNotificationChannel(this)
        checkAndRequestNotificationPermission()

        setContent {
            GenshinExpeditionTrackerTheme {
                MainScreen()
            }
        }
    }

    private fun checkAndRequestNotificationPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(
                    this,
                    Manifest.permission.POST_NOTIFICATIONS
                ) != PackageManager.PERMISSION_GRANTED
            ) {
                requestPermissionLauncher.launch(Manifest.permission.POST_NOTIFICATIONS)
            }
        }
    }
}

@Composable
fun MainScreen() {
    val context = LocalContext.current

    var activeExpeditions by remember { mutableStateOf<List<Expedition>>(loadExpeditions(context)) }
    var currentResin by remember { mutableIntStateOf(loadResin(context)) }
    var lastResinUpdate by remember { mutableLongStateOf(loadLastResinUpdate(context)) }

    var currentThemeName by remember { mutableStateOf(loadTheme(context)) }
    var currentLanguage by remember { mutableStateOf(loadLanguage(context)) }
    val currentTheme = REGION_THEMES[currentThemeName] ?: REGION_THEMES["Mondstadt (Anemo)"]!!

    var showAddDialog by remember { mutableStateOf(false) }
    var showResinDialog by remember { mutableStateOf(false) }
    var showSettingsDialog by remember { mutableStateOf(false) }
    var themeExpanded by remember { mutableStateOf(false) }
    var selectedTab by remember { mutableIntStateOf(0) }
    val maxResin = 200

    LaunchedEffect(activeExpeditions) {
        saveExpeditions(context, activeExpeditions)
    }

    LaunchedEffect(currentResin, lastResinUpdate) {
        saveResinData(context, currentResin, lastResinUpdate)
    }

    LaunchedEffect(currentThemeName) {
        saveTheme(context, currentThemeName)
    }

    LaunchedEffect(currentLanguage) {
        saveLanguage(context, currentLanguage)
    }

    LaunchedEffect(Unit) {
        while (true) {
            delay(1000)
            val now = System.currentTimeMillis() / 1000
            val elapsed = now - lastResinUpdate
            val gained = (elapsed / 480).toInt()
            if (gained > 0 && currentResin < maxResin) {
                currentResin = (currentResin + gained).coerceAtMost(maxResin)
                lastResinUpdate += gained * 480
            }
        }
    }

    Surface(
        modifier = Modifier.fillMaxSize(),
        color = currentTheme.bgDark
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .statusBarsPadding()
                .navigationBarsPadding()
                .padding(16.dp)
        ) {
            // Header mit App-Titel, Settings-Icon & Theme-Dropdown
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    IconButton(
                        onClick = { showSettingsDialog = true },
                        modifier = Modifier.size(32.dp)
                    ) {
                        Text("⚙️", fontSize = 16.sp)
                    }
                    Spacer(modifier = Modifier.width(4.dp))
                    Text(
                        text = AppTranslations.tr("app_name", currentLanguage),
                        color = Color.White,
                        fontSize = 18.sp,
                        fontWeight = FontWeight.Bold
                    )
                }

                Box {
                    OutlinedButton(
                        onClick = { themeExpanded = true },
                        shape = RoundedCornerShape(8.dp),
                        contentPadding = PaddingValues(horizontal = 8.dp, vertical = 4.dp),
                        border = androidx.compose.foundation.BorderStroke(1.dp, currentTheme.cyan)
                    ) {
                        Text(
                            text = currentThemeName,
                            color = currentTheme.cyan,
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                    DropdownMenu(
                        expanded = themeExpanded,
                        onDismissRequest = { themeExpanded = false }
                    ) {
                        REGION_THEMES.keys.forEach { tName ->
                            DropdownMenuItem(
                                text = { Text(tName) },
                                onClick = {
                                    currentThemeName = tName
                                    themeExpanded = false
                                }
                            )
                        }
                    }
                }
            }

            Spacer(modifier = Modifier.height(12.dp))

            // Hauptinhalt
            Box(modifier = Modifier.weight(1f)) {
                when (selectedTab) {
                    0 -> ExpeditionMainContent(
                        activeExpeditions = activeExpeditions,
                        currentResin = currentResin,
                        maxResin = maxResin,
                        lastResinUpdate = lastResinUpdate,
                        theme = currentTheme,
                        language = currentLanguage,
                        context = context,
                        onEditResin = { showResinDialog = true },
                        onClaimAll = {
                            val now = System.currentTimeMillis() / 1000
                            activeExpeditions = activeExpeditions.filter { it.endTimestampEpochSec > now }
                        },
                        onDeleteExpedition = { target ->
                            WorkManager.getInstance(context).cancelAllWorkByTag(target.id)
                            activeExpeditions = activeExpeditions.filter { it.id != target.id }
                        },
                        onStartExpedition = { if (activeExpeditions.size < 5) showAddDialog = true },
                        limitReached = activeExpeditions.size >= 5
                    )
                    1 -> TeyvatJournalScreen(theme = currentTheme)
                    2 -> CraftingCalculatorScreen(theme = currentTheme)
                    3 -> WishCounterScreen(theme = currentTheme)
                    4 -> ResinPlannerScreen(theme = currentTheme)
                    5 -> WeeklyBossScreen(theme = currentTheme)
                    6 -> TeamGoalsScreen(theme = currentTheme)
                }
            }

            Spacer(modifier = Modifier.height(8.dp))

            // Untere Navigationsleiste
            Surface(
                color = currentTheme.cardBg,
                shape = RoundedCornerShape(12.dp),
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(12.dp))
                    .border(1.dp, Color(0xFF333847), RoundedCornerShape(12.dp))
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .horizontalScroll(rememberScrollState()),
                    horizontalArrangement = Arrangement.Start,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    val itemColors = NavigationBarItemDefaults.colors(
                        selectedIconColor = Color.Black,
                        selectedTextColor = currentTheme.cyan,
                        indicatorColor = currentTheme.cyan,
                        unselectedIconColor = Color.White,
                        unselectedTextColor = Color(0xFFE2E8F0)
                    )

                    val navItems = listOf(
                        Triple(0, "⏳", AppTranslations.tr("nav_tracker", currentLanguage)),
                        Triple(1, "📖", AppTranslations.tr("nav_journal", currentLanguage)),
                        Triple(2, "🧪", AppTranslations.tr("nav_crafting", currentLanguage)),
                        Triple(3, "🌠", AppTranslations.tr("nav_wishes", currentLanguage)),
                        Triple(4, "⚡", AppTranslations.tr("nav_resin", currentLanguage)),
                        Triple(5, "🐲", AppTranslations.tr("nav_bosses", currentLanguage)),
                        Triple(6, "🎯", AppTranslations.tr("nav_goals", currentLanguage))
                    )

                    navItems.forEach { item ->
                        val tabIndex = item.first
                        val iconStr = item.second
                        val titleStr = item.third
                        val isSelected = selectedTab == tabIndex

                        NavigationBarItem(
                            selected = isSelected,
                            onClick = { selectedTab = tabIndex },
                            icon = { Text(iconStr, fontSize = 16.sp) },
                            label = {
                                Text(
                                    text = titleStr,
                                    fontSize = 10.sp,
                                    fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Medium
                                )
                            },
                            colors = itemColors
                        )
                    }
                }
            }
        }

        // Settings-Dialog (Sprachauswahl)
        if (showSettingsDialog) {
            AlertDialog(
                onDismissRequest = { showSettingsDialog = false },
                title = { Text(AppTranslations.tr("settings", currentLanguage), color = currentTheme.cyan) },
                text = {
                    Column {
                        Text(AppTranslations.tr("language", currentLanguage), color = Color.White, fontSize = 14.sp)
                        Spacer(modifier = Modifier.height(8.dp))

                        var langExpanded by remember { mutableStateOf(false) }
                        Box {
                            OutlinedButton(
                                onClick = { langExpanded = true },
                                modifier = Modifier.fillMaxWidth(),
                                border = androidx.compose.foundation.BorderStroke(1.dp, currentTheme.cyan)
                            ) {
                                Text(currentLanguage, color = currentTheme.cyan, fontWeight = FontWeight.Bold)
                            }
                            DropdownMenu(
                                expanded = langExpanded,
                                onDismissRequest = { langExpanded = false }
                            ) {
                                listOf("Deutsch", "English").forEach { lang ->
                                    DropdownMenuItem(
                                        text = { Text(lang) },
                                        onClick = {
                                            currentLanguage = lang
                                            langExpanded = false
                                        }
                                    )
                                }
                            }
                        }
                    }
                },
                confirmButton = {
                    Button(
                        onClick = { showSettingsDialog = false },
                        colors = ButtonDefaults.buttonColors(containerColor = currentTheme.cyan)
                    ) {
                        Text("OK", color = Color.Black)
                    }
                },
                containerColor = currentTheme.cardBg
            )
        }

        if (showAddDialog) {
            AddExpeditionDialog(
                theme = currentTheme,
                onDismiss = { showAddDialog = false },
                onSubmit = { charName, location, hours ->
                    val now = System.currentTimeMillis() / 1000
                    val totalSec = hours * 3600L
                    val newExp = Expedition(
                        charName = charName,
                        location = location,
                        totalSeconds = totalSec,
                        endTimestampEpochSec = now + totalSec
                    )
                    activeExpeditions = activeExpeditions + newExp

                    scheduleExpeditionNotification(
                        context = context,
                        expeditionId = newExp.id,
                        charName = charName,
                        location = location,
                        delaySeconds = totalSec
                    )

                    showAddDialog = false
                }
            )
        }

        if (showResinDialog) {
            AdjustResinDialog(
                currentResin = currentResin,
                maxResin = maxResin,
                theme = currentTheme,
                onDismiss = { showResinDialog = false },
                onConfirm = { newVal ->
                    currentResin = newVal
                    lastResinUpdate = System.currentTimeMillis() / 1000
                    showResinDialog = false
                }
            )
        }
    }
}

@Composable
fun ExpeditionMainContent(
    activeExpeditions: List<Expedition>,
    currentResin: Int,
    maxResin: Int,
    lastResinUpdate: Long,
    theme: RegionTheme,
    language: String,
    context: Context,
    onEditResin: () -> Unit,
    onClaimAll: () -> Unit,
    onDeleteExpedition: (Expedition) -> Unit,
    onStartExpedition: () -> Unit,
    limitReached: Boolean
) {
    LazyVerticalGrid(
        columns = GridCells.Fixed(1),
        verticalArrangement = Arrangement.spacedBy(12.dp),
        horizontalArrangement = Arrangement.spacedBy(12.dp),
        modifier = Modifier.fillMaxSize()
    ) {
        item {
            OperationsHQCard(
                expeditions = activeExpeditions,
                currentResin = currentResin,
                maxResin = maxResin,
                lastResinUpdate = lastResinUpdate,
                theme = theme,
                language = language,
                onEditResin = onEditResin,
                onClaimAll = onClaimAll
            )
        }

        items(activeExpeditions, key = { it.id }) { expedition ->
            ExpeditionCard(
                expedition = expedition,
                theme = theme,
                language = language,
                onDelete = onDeleteExpedition
            )
        }

        item {
            Spacer(modifier = Modifier.height(4.dp))
            Button(
                onClick = onStartExpedition,
                enabled = !limitReached,
                colors = ButtonDefaults.buttonColors(
                    containerColor = if (limitReached) Color(0xFF1E2029) else theme.cardBg,
                    disabledContainerColor = Color(0xFF1E2029)
                ),
                shape = RoundedCornerShape(8.dp),
                modifier = Modifier
                    .fillMaxWidth()
                    .border(
                        width = 1.dp,
                        color = if (limitReached) Color(0xFF333745) else theme.cyan,
                        shape = RoundedCornerShape(8.dp)
                    )
            ) {
                Text(
                    text = if (limitReached) "${AppTranslations.tr("limit_reached", language)} (${activeExpeditions.size}/5)"
                    else "${AppTranslations.tr("start_new", language)} (${activeExpeditions.size}/5)",
                    color = if (limitReached) Color(0xFF555866) else theme.cyan,
                    fontWeight = FontWeight.Bold
                )
            }
        }
    }
}

@Composable
fun OperationsHQCard(
    expeditions: List<Expedition>,
    currentResin: Int,
    maxResin: Int,
    lastResinUpdate: Long,
    theme: RegionTheme,
    language: String,
    onEditResin: () -> Unit,
    onClaimAll: () -> Unit
) {
    var currentTime by remember { mutableLongStateOf(System.currentTimeMillis() / 1000) }

    LaunchedEffect(Unit) {
        while (true) {
            delay(1000)
            currentTime = System.currentTimeMillis() / 1000
        }
    }

    Card(
        colors = CardDefaults.cardColors(containerColor = theme.cardBg),
        shape = RoundedCornerShape(12.dp),
        modifier = Modifier
            .fillMaxWidth()
            .border(1.dp, Color(0xFF333847), RoundedCornerShape(12.dp))
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = AppTranslations.tr("hq_title", language),
                color = theme.cyan,
                fontWeight = FontWeight.Bold,
                fontSize = 13.sp
            )

            Spacer(modifier = Modifier.height(8.dp))

            val readyCards = expeditions.filter { it.endTimestampEpochSec <= currentTime }
            val nextCard = expeditions.filter { it.endTimestampEpochSec > currentTime }
                .minByOrNull { it.endTimestampEpochSec }

            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(theme.boxDark, RoundedCornerShape(6.dp))
                    .padding(8.dp)
            ) {
                Column {
                    Text(AppTranslations.tr("next_arrival", language), color = Color.Gray, fontSize = 9.sp, fontWeight = FontWeight.Bold)
                    if (readyCards.isNotEmpty()) {
                        Text("${readyCards.size} ${AppTranslations.tr("ready_claim", language)}", color = theme.amber, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                    } else if (nextCard != null) {
                        val rem = nextCard.endTimestampEpochSec - currentTime
                        val h = rem / 3600
                        val m = (rem % 3600) / 60
                        val s = rem % 60
                        Text("${nextCard.charName} ${AppTranslations.tr("in", language)} ${String.format(Locale.getDefault(), "%02d:%02d:%02d", h, m, s)}", color = theme.cyan, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                    } else {
                        Text(AppTranslations.tr("no_expeditions", language), color = Color.Gray, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                    }
                }
            }

            Spacer(modifier = Modifier.height(6.dp))

            val cal = Calendar.getInstance().apply {
                if (get(Calendar.HOUR_OF_DAY) >= 4) add(Calendar.DAY_OF_YEAR, 1)
                set(Calendar.HOUR_OF_DAY, 4)
                set(Calendar.MINUTE, 0)
                set(Calendar.SECOND, 0)
            }
            val secondsToReset = ((cal.timeInMillis / 1000) - currentTime).coerceAtLeast(0)
            val resH = secondsToReset / 3600
            val resM = (secondsToReset % 3600) / 60

            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(theme.boxDark, RoundedCornerShape(6.dp))
                    .padding(8.dp)
            ) {
                Column {
                    Text(AppTranslations.tr("daily_reset", language), color = Color.Gray, fontSize = 9.sp, fontWeight = FontWeight.Bold)
                    Text("${AppTranslations.tr("in", language)} ${resH}h ${resM}m", color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                }
            }

            Spacer(modifier = Modifier.height(6.dp))

            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(theme.boxDark, RoundedCornerShape(6.dp))
                    .padding(8.dp)
            ) {
                Column {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(AppTranslations.tr("resin_counter", language), color = Color.Gray, fontSize = 9.sp, fontWeight = FontWeight.Bold)
                        IconButton(onClick = onEditResin, modifier = Modifier.size(18.dp)) {
                            Text("⚙", color = theme.cyan, fontSize = 10.sp)
                        }
                    }
                    if (currentResin >= maxResin) {
                        Text("$maxResin / $maxResin (${AppTranslations.tr("full", language)})", color = theme.amber, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                    } else {
                        val needed = maxResin - currentResin
                        val secLeft = (needed * 480) - ((currentTime - lastResinUpdate) % 480)
                        val h = secLeft / 3600
                        val m = (secLeft % 3600) / 60
                        Text("$currentResin / $maxResin (${AppTranslations.tr("full_in", language)} ${h}h ${m}m)", color = Color.White, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                    }
                }
            }

            Spacer(modifier = Modifier.height(10.dp))

            Button(
                onClick = onClaimAll,
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2E323F)),
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(AppTranslations.tr("claim_all", language), color = theme.cyan)
            }
        }
    }
}

@Composable
fun ExpeditionCard(expedition: Expedition, theme: RegionTheme, language: String, onDelete: (Expedition) -> Unit) {
    var currentTime by remember { mutableLongStateOf(System.currentTimeMillis() / 1000) }

    LaunchedEffect(Unit) {
        while (true) {
            delay(1000)
            currentTime = System.currentTimeMillis() / 1000
        }
    }

    val rem = (expedition.endTimestampEpochSec - currentTime).coerceAtLeast(0)
    val isComplete = rem <= 0
    val activeColor = if (isComplete) theme.amber else theme.cyan
    val imageResId = getDrawableIdForChar(expedition.charName)

    Card(
        colors = CardDefaults.cardColors(containerColor = theme.cardBg),
        shape = RoundedCornerShape(12.dp),
        modifier = Modifier
            .fillMaxWidth()
            .border(1.dp, Color(0xFF333847), RoundedCornerShape(12.dp))
    ) {
        Box(modifier = Modifier.fillMaxWidth()) {
            if (imageResId != 0) {
                Image(
                    painter = painterResource(id = imageResId),
                    contentDescription = expedition.charName,
                    contentScale = ContentScale.Crop,
                    colorFilter = ColorFilter.tint(
                        Color.Black.copy(alpha = 0.55f),
                        BlendMode.Darken
                    ),
                    modifier = Modifier.matchParentSize()
                )
            }

            Column(modifier = Modifier.padding(12.dp)) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = expedition.charName,
                        color = Color.White,
                        fontWeight = FontWeight.Bold,
                        fontSize = 14.sp
                    )
                    IconButton(onClick = { onDelete(expedition) }, modifier = Modifier.size(24.dp)) {
                        Text("✕", color = Color.Gray, fontSize = 12.sp)
                    }
                }

                Spacer(modifier = Modifier.height(8.dp))

                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(8.dp),
                    contentAlignment = Alignment.Center
                ) {
                    if (isComplete) {
                        Text(AppTranslations.tr("ready", language), color = theme.amber, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                    } else {
                        val h = rem / 3600
                        val m = (rem % 3600) / 60
                        val s = rem % 60
                        Text(
                            text = String.format(Locale.getDefault(), "%02d:%02d:%02d", h, m, s),
                            color = theme.cyan,
                            fontWeight = FontWeight.Bold,
                            fontSize = 16.sp
                        )
                    }
                }

                Spacer(modifier = Modifier.height(8.dp))

                Text(
                    text = "📍 ${expedition.location}",
                    color = theme.cyan,
                    fontSize = 11.sp,
                    modifier = Modifier
                        .background(theme.boxDark.copy(alpha = 0.85f), RoundedCornerShape(6.dp))
                        .padding(horizontal = 8.dp, vertical = 4.dp)
                        .align(Alignment.CenterHorizontally)
                )

                Spacer(modifier = Modifier.height(8.dp))

                Button(
                    onClick = { if (isComplete) onDelete(expedition) },
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2E323F).copy(alpha = 0.9f)),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text(if (isComplete) AppTranslations.tr("claim_reward", language) else AppTranslations.tr("running", language), color = activeColor)
                }
            }
        }
    }
}

// =========================================================
// Dialoge & Helfer
// =========================================================
@Composable
fun AddExpeditionDialog(
    theme: RegionTheme,
    onDismiss: () -> Unit,
    onSubmit: (String, String, Int) -> Unit
) {
    val charList = CHARACTERS.keys.toList().sorted()
    var selectedChar by remember { mutableStateOf(charList.firstOrNull() ?: "Bennett") }
    var selectedRegion by remember { mutableStateOf(REGIONS.first()) }
    var selectedResource by remember { mutableStateOf(RESOURCES.first()) }

    val hasBonus = TIME_REDUCTION_BONUS[selectedChar] == selectedRegion
    val durationOptions = if (hasBonus) DURATIONS_BONUS else DURATIONS_STANDARD

    var selectedIndex by remember { mutableIntStateOf(3) }

    LaunchedEffect(hasBonus) {
        if (selectedIndex >= durationOptions.size) {
            selectedIndex = durationOptions.size - 1
        }
    }

    val selectedDuration = durationOptions[selectedIndex.coerceIn(durationOptions.indices)]

    var charExpanded by remember { mutableStateOf(false) }
    var regionExpanded by remember { mutableStateOf(false) }
    var resourceExpanded by remember { mutableStateOf(false) }
    var durationExpanded by remember { mutableStateOf(false) }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("New Expedition", color = theme.cyan) },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("Character:", color = Color.White, fontSize = 12.sp)
                Box {
                    OutlinedButton(
                        onClick = { charExpanded = true },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(selectedChar, color = theme.cyan, fontWeight = FontWeight.Bold)
                    }
                    DropdownMenu(
                        expanded = charExpanded,
                        onDismissRequest = { charExpanded = false }
                    ) {
                        charList.forEach { charName ->
                            DropdownMenuItem(
                                text = { Text(charName) },
                                onClick = {
                                    selectedChar = charName
                                    charExpanded = false
                                }
                            )
                        }
                    }
                }

                Text("Region:", color = Color.White, fontSize = 12.sp)
                Box {
                    OutlinedButton(
                        onClick = { regionExpanded = true },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(selectedRegion, color = Color.White)
                    }
                    DropdownMenu(
                        expanded = regionExpanded,
                        onDismissRequest = { regionExpanded = false }
                    ) {
                        REGIONS.forEach { region ->
                            DropdownMenuItem(
                                text = { Text(region) },
                                onClick = {
                                    selectedRegion = region
                                    regionExpanded = false
                                }
                            )
                        }
                    }
                }

                Text("Resource:", color = Color.White, fontSize = 12.sp)
                Box {
                    OutlinedButton(
                        onClick = { resourceExpanded = true },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(selectedResource, color = Color.White)
                    }
                    DropdownMenu(
                        expanded = resourceExpanded,
                        onDismissRequest = { resourceExpanded = false }
                    ) {
                        RESOURCES.forEach { resource ->
                            DropdownMenuItem(
                                text = { Text(resource) },
                                onClick = {
                                    selectedResource = resource
                                    resourceExpanded = false
                                }
                            )
                        }
                    }
                }

                Text("Duration:", color = Color.White, fontSize = 12.sp)
                Box {
                    OutlinedButton(
                        onClick = { durationExpanded = true },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(
                            text = selectedDuration.first,
                            color = if (hasBonus) theme.amber else theme.cyan,
                            fontWeight = FontWeight.Bold
                        )
                    }
                    DropdownMenu(
                        expanded = durationExpanded,
                        onDismissRequest = { durationExpanded = false }
                    ) {
                        durationOptions.forEachIndexed { index, option ->
                            DropdownMenuItem(
                                text = { Text(option.first) },
                                onClick = {
                                    selectedIndex = index
                                    durationExpanded = false
                                }
                            )
                        }
                    }
                }
            }
        },
        confirmButton = {
            Button(
                onClick = {
                    val loc = "$selectedRegion ($selectedResource)"
                    onSubmit(selectedChar, loc, selectedDuration.second)
                },
                colors = ButtonDefaults.buttonColors(containerColor = theme.cyan)
            ) {
                Text("Start", color = Color.Black)
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) { Text("Cancel", color = Color.Gray) }
        },
        containerColor = theme.cardBg
    )
}

@Composable
fun AdjustResinDialog(
    currentResin: Int,
    maxResin: Int,
    theme: RegionTheme,
    onDismiss: () -> Unit,
    onConfirm: (Int) -> Unit
) {
    var textVal by remember { mutableStateOf(currentResin.toString()) }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Adjust Resin", color = theme.cyan) },
        text = {
            Column {
                Text("Current Resin (0-$maxResin):", color = Color.White)
                Spacer(modifier = Modifier.height(8.dp))
                OutlinedTextField(
                    value = textVal,
                    onValueChange = { textVal = it },
                    singleLine = true,
                    textStyle = androidx.compose.ui.text.TextStyle(
                        color = Color.White,
                        fontSize = 16.sp,
                        fontWeight = FontWeight.Bold
                    ),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = theme.cyan,
                        unfocusedBorderColor = Color.Gray,
                        focusedTextColor = Color.White,
                        unfocusedTextColor = Color.White,
                        cursorColor = theme.cyan
                    ),
                    modifier = Modifier.fillMaxWidth()
                )
            }
        },
        confirmButton = {
            Button(
                onClick = {
                    val parsed = textVal.toIntOrNull() ?: currentResin
                    onConfirm(parsed.coerceIn(0, maxResin))
                },
                colors = ButtonDefaults.buttonColors(containerColor = theme.cyan)
            ) {
                Text("OK", color = Color.Black)
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) { Text("Cancel", color = Color.Gray) }
        },
        containerColor = theme.cardBg
    )
}

fun scheduleExpeditionNotification(
    context: Context,
    expeditionId: String,
    charName: String,
    location: String,
    delaySeconds: Long
) {
    val inputData = workDataOf(
        "char_name" to charName,
        "location" to location
    )

    val workRequest = OneTimeWorkRequestBuilder<ExpeditionWorker>()
        .setInitialDelay(delaySeconds, TimeUnit.SECONDS)
        .setInputData(inputData)
        .addTag(expeditionId)
        .build()

    WorkManager.getInstance(context).enqueue(workRequest)
}

@Composable
fun getDrawableIdForChar(charName: String): Int {
    val context = LocalContext.current
    val imageName = charName.lowercase().replace(" ", "_")
    return context.resources.getIdentifier(imageName, "drawable", context.packageName)
}

// --- Speicher-Logik ---
private const val PREFS_NAME = "GenshinTrackerPrefs"
private const val KEY_EXPEDITIONS = "key_expeditions"
private const val KEY_RESIN = "key_resin"
private const val KEY_LAST_RESIN_UPDATE = "key_last_resin_update"
private const val KEY_THEME = "key_theme"
private const val KEY_LANGUAGE = "key_language"

fun saveTheme(context: Context, themeName: String) {
    val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    prefs.edit().putString(KEY_THEME, themeName).apply()
}

fun loadTheme(context: Context): String {
    val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    return prefs.getString(KEY_THEME, "Mondstadt (Anemo)") ?: "Mondstadt (Anemo)"
}

fun saveLanguage(context: Context, language: String) {
    val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    prefs.edit().putString(KEY_LANGUAGE, language).apply()
}

fun loadLanguage(context: Context): String {
    val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    return prefs.getString(KEY_LANGUAGE, "Deutsch") ?: "Deutsch"
}

fun saveExpeditions(context: Context, expeditions: List<Expedition>) {
    val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    val jsonArray = JSONArray()

    expeditions.forEach { exp ->
        val obj = JSONObject().apply {
            put("id", exp.id)
            put("charName", exp.charName)
            put("location", exp.location)
            put("totalSeconds", exp.totalSeconds)
            put("endTimestampEpochSec", exp.endTimestampEpochSec)
        }
        jsonArray.put(obj)
    }

    prefs.edit().putString(KEY_EXPEDITIONS, jsonArray.toString()).apply()
}

fun loadExpeditions(context: Context): List<Expedition> {
    val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    val jsonStr = prefs.getString(KEY_EXPEDITIONS, null) ?: return emptyList()
    val list = mutableListOf<Expedition>()

    try {
        val jsonArray = JSONArray(jsonStr)
        for (i in 0 until jsonArray.length()) {
            val obj = jsonArray.getJSONObject(i)
            list.add(
                Expedition(
                    id = obj.getString("id"),
                    charName = obj.getString("charName"),
                    location = obj.getString("location"),
                    totalSeconds = obj.getLong("totalSeconds"),
                    endTimestampEpochSec = obj.getLong("endTimestampEpochSec")
                )
            )
        }
    } catch (e: Exception) {
        e.printStackTrace()
    }
    return list
}

fun saveResinData(context: Context, resin: Int, lastUpdateSec: Long) {
    val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    prefs.edit()
        .putInt(KEY_RESIN, resin)
        .putLong(KEY_LAST_RESIN_UPDATE, lastUpdateSec)
        .apply()
}

fun loadResin(context: Context): Int {
    val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    return prefs.getInt(KEY_RESIN, 120)
}

fun loadLastResinUpdate(context: Context): Long {
    val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    return prefs.getLong(KEY_LAST_RESIN_UPDATE, System.currentTimeMillis() / 1000)
}