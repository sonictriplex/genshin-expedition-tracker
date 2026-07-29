package com.mediamatrix.genshintracker

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
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

// --- Farbschema ---
val CoreCyan = Color(0xFF38E3E3)
val CoreAmber = Color(0xFFFFAA00)
val BgDark = Color(0xFF1A1C24)
val CardBg = Color(0xFF252833)
val BoxDark = Color(0xFF12141C)

class MainActivity : ComponentActivity() {

    // Launcher zur Abfrage der Benachrichtigungs-Berechtigung (Android 13+)
    private val requestPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { isGranted: Boolean ->
        // Berechtigung erteilt/abgelehnt
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // 1. Notification-Channel für Benachrichtigungen anlegen
        NotificationHelper.createNotificationChannel(this)

        // 2. Rechte abfragen (Android 13+)
        checkAndRequestNotificationPermission()

        setContent {
            GenshinExpeditionTrackerTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = BgDark
                ) {
                    MainScreen()
                }
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

    // Zustand beim Start aus SharedPreferences laden
    var activeExpeditions by remember { mutableStateOf(loadExpeditions(context)) }
    var currentResin by remember { mutableIntStateOf(loadResin(context)) }
    var lastResinUpdate by remember { mutableLongStateOf(loadLastResinUpdate(context)) }

    var showAddDialog by remember { mutableStateOf(false) }
    var showResinDialog by remember { mutableStateOf(false) }
    val maxResin = 200

    // Automatisch Speichern, sobald sich Expeditionen ändern
    LaunchedEffect(activeExpeditions) {
        saveExpeditions(context, activeExpeditions)
    }

    // Automatisch Speichern, sobald sich Harz ändert
    LaunchedEffect(currentResin, lastResinUpdate) {
        saveResinData(context, currentResin, lastResinUpdate)
    }

    // 1-Sekunden Ticker für Timer-Updates & Harz-Regeneration
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

    Column(
        modifier = Modifier
            .fillMaxSize()
            .statusBarsPadding()
            .padding(16.dp)
    ) {
        // --- Header Text ---
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = "Genshin Expedition Tracker",
                color = Color.White,
                fontSize = 20.sp,
                fontWeight = FontWeight.Bold
            )
        }

        Spacer(modifier = Modifier.height(12.dp))

        // --- Start New Expedition Button ---
        val limitReached = activeExpeditions.size >= 5
        Button(
            onClick = { if (!limitReached) showAddDialog = true },
            enabled = !limitReached,
            colors = ButtonDefaults.buttonColors(
                containerColor = if (limitReached) Color(0xFF1E2029) else CardBg,
                disabledContainerColor = Color(0xFF1E2029)
            ),
            shape = RoundedCornerShape(8.dp),
            modifier = Modifier
                .fillMaxWidth()
                .border(
                    width = 1.dp,
                    color = if (limitReached) Color(0xFF333745) else CoreCyan,
                    shape = RoundedCornerShape(8.dp)
                )
        ) {
            Text(
                text = if (limitReached) "Limit Reached (${activeExpeditions.size}/5)"
                else "+ Start New Expedition (${activeExpeditions.size}/5)",
                color = if (limitReached) Color(0xFF555866) else CoreCyan,
                fontWeight = FontWeight.Bold
            )
        }

        Spacer(modifier = Modifier.height(16.dp))

        // --- Grid Layout (Kacheln) ---
        LazyVerticalGrid(
            columns = GridCells.Fixed(1),
            verticalArrangement = Arrangement.spacedBy(12.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            modifier = Modifier.weight(1f)
        ) {
            item {
                OperationsHQCard(
                    expeditions = activeExpeditions,
                    currentResin = currentResin,
                    maxResin = maxResin,
                    lastResinUpdate = lastResinUpdate,
                    onEditResin = { showResinDialog = true },
                    onClaimAll = {
                        val now = System.currentTimeMillis() / 1000
                        activeExpeditions = activeExpeditions.filter { it.endTimestampEpochSec > now }
                    }
                )
            }

            items(activeExpeditions, key = { it.id }) { expedition ->
                ExpeditionCard(
                    expedition = expedition,
                    onDelete = { target ->
                        activeExpeditions = activeExpeditions.filter { it.id != target.id }
                    }
                )
            }
        }
    }

    // --- Overlay Dialog: Neue Expedition ---
    if (showAddDialog) {
        AddExpeditionDialog(
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

                // WorkManager Benachrichtigung für diesen Timer einplanen
                scheduleExpeditionNotification(
                    context = context,
                    charName = charName,
                    location = location,
                    durationInHours = hours.toLong()
                )

                showAddDialog = false
            }
        )
    }

    // --- Overlay Dialog: Resin anpassen ---
    if (showResinDialog) {
        AdjustResinDialog(
            currentResin = currentResin,
            maxResin = maxResin,
            onDismiss = { showResinDialog = false },
            onConfirm = { newVal ->
                currentResin = newVal
                lastResinUpdate = System.currentTimeMillis() / 1000
                showResinDialog = false
            }
        )
    }
}

// =========================================================
// UI Komponente: Operations HQ
// =========================================================
@Composable
fun OperationsHQCard(
    expeditions: List<Expedition>,
    currentResin: Int,
    maxResin: Int,
    lastResinUpdate: Long,
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
        colors = CardDefaults.cardColors(containerColor = CardBg),
        shape = RoundedCornerShape(12.dp),
        modifier = Modifier
            .fillMaxWidth()
            .border(1.dp, Color(0xFF333847), RoundedCornerShape(12.dp))
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "OPERATIONS HQ",
                color = CoreCyan,
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
                    .background(BoxDark, RoundedCornerShape(6.dp))
                    .padding(8.dp)
            ) {
                Column {
                    Text("NEXT ARRIVAL", color = Color.Gray, fontSize = 9.sp, fontWeight = FontWeight.Bold)
                    if (readyCards.isNotEmpty()) {
                        Text("${readyCards.size} Ready to claim!", color = CoreAmber, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                    } else if (nextCard != null) {
                        val rem = nextCard.endTimestampEpochSec - currentTime
                        val h = rem / 3600
                        val m = (rem % 3600) / 60
                        val s = rem % 60
                        Text("${nextCard.charName} in ${String.format(Locale.getDefault(), "%02d:%02d:%02d", h, m, s)}", color = CoreCyan, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                    } else {
                        Text("No active expeditions", color = Color.Gray, fontSize = 12.sp, fontWeight = FontWeight.Bold)
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
                    .background(BoxDark, RoundedCornerShape(6.dp))
                    .padding(8.dp)
            ) {
                Column {
                    Text("DAILY RESET (04:00)", color = Color.Gray, fontSize = 9.sp, fontWeight = FontWeight.Bold)
                    Text("In ${resH}h ${resM}m", color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                }
            }

            Spacer(modifier = Modifier.height(6.dp))

            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(BoxDark, RoundedCornerShape(6.dp))
                    .padding(8.dp)
            ) {
                Column {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text("RESIN COUNTER", color = Color.Gray, fontSize = 9.sp, fontWeight = FontWeight.Bold)
                        IconButton(onClick = onEditResin, modifier = Modifier.size(18.dp)) {
                            Text("⚙", color = Color.Gray, fontSize = 10.sp)
                        }
                    }
                    if (currentResin >= maxResin) {
                        Text("$maxResin / $maxResin (FULL!)", color = CoreAmber, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                    } else {
                        val needed = maxResin - currentResin
                        val secLeft = (needed * 480) - ((currentTime - lastResinUpdate) % 480)
                        val h = secLeft / 3600
                        val m = (secLeft % 3600) / 60
                        Text("$currentResin / $maxResin (Full in ${h}h ${m}m)", color = Color.White, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                    }
                }
            }

            Spacer(modifier = Modifier.height(10.dp))

            Button(
                onClick = onClaimAll,
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2E323F)),
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Claim All Ready", color = CoreCyan)
            }
        }
    }
}

// =========================================================
// UI Komponente: Expeditions-Karte (GEFIXT)
// =========================================================
@Composable
fun ExpeditionCard(expedition: Expedition, onDelete: (Expedition) -> Unit) {
    var currentTime by remember { mutableLongStateOf(System.currentTimeMillis() / 1000) }

    // Sekündlicher Ticker
    LaunchedEffect(Unit) {
        while (true) {
            delay(1000)
            currentTime = System.currentTimeMillis() / 1000
        }
    }

    // FIX: Restzeit direkt über 'currentTime' berechnen, damit Compose neu rendert!
    val rem = (expedition.endTimestampEpochSec - currentTime).coerceAtLeast(0)
    val isComplete = rem <= 0
    val activeColor = if (isComplete) CoreAmber else CoreCyan
    val imageResId = getDrawableIdForChar(expedition.charName)

    Card(
        colors = CardDefaults.cardColors(containerColor = CardBg),
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
                        Text("READY!", color = CoreAmber, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                    } else {
                        val h = rem / 3600
                        val m = (rem % 3600) / 60
                        val s = rem % 60
                        Text(
                            text = String.format(Locale.getDefault(), "%02d:%02d:%02d", h, m, s),
                            color = CoreCyan,
                            fontWeight = FontWeight.Bold,
                            fontSize = 16.sp
                        )
                    }
                }

                Spacer(modifier = Modifier.height(8.dp))

                Text(
                    text = "📍 ${expedition.location}",
                    color = CoreCyan,
                    fontSize = 11.sp,
                    modifier = Modifier
                        .background(BoxDark.copy(alpha = 0.85f), RoundedCornerShape(6.dp))
                        .padding(horizontal = 8.dp, vertical = 4.dp)
                        .align(Alignment.CenterHorizontally)
                )

                Spacer(modifier = Modifier.height(8.dp))

                Button(
                    onClick = { if (isComplete) onDelete(expedition) },
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2E323F).copy(alpha = 0.9f)),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text(if (isComplete) "Claim Reward" else "Running", color = activeColor)
                }
            }
        }
    }
}

// =========================================================
// Dialog: Neue Expedition hinzufügen
// =========================================================
@Composable
fun AddExpeditionDialog(onDismiss: () -> Unit, onSubmit: (String, String, Int) -> Unit) {
    val charList = CHARACTERS.keys.toList().sorted()
    var selectedChar by remember { mutableStateOf(charList.firstOrNull() ?: "Bennett") }
    var selectedRegion by remember { mutableStateOf(REGIONS.first()) }
    var selectedResource by remember { mutableStateOf(RESOURCES.first()) }

    val durationOptions = listOf(
        "4 Hours" to 4,
        "8 Hours" to 8,
        "12 Hours" to 12,
        "16 Hours (Bonus)" to 16,
        "20 Hours (Standard)" to 20
    )

    var selectedDuration by remember { mutableStateOf(durationOptions.last()) }

    var charExpanded by remember { mutableStateOf(false) }
    var regionExpanded by remember { mutableStateOf(false) }
    var resourceExpanded by remember { mutableStateOf(false) }
    var durationExpanded by remember { mutableStateOf(false) }

    LaunchedEffect(selectedChar) {
        val info = CHARACTERS[selectedChar]
        val targetHours = if (info?.hasBonus == true) 16 else 20
        selectedDuration = durationOptions.firstOrNull { it.second == targetHours } ?: durationOptions.last()
    }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("New Expedition", color = CoreCyan) },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("Character:", color = Color.White, fontSize = 12.sp)
                Box {
                    OutlinedButton(
                        onClick = { charExpanded = true },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(selectedChar, color = CoreCyan, fontWeight = FontWeight.Bold)
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
                        Text(selectedDuration.first, color = CoreAmber, fontWeight = FontWeight.Bold)
                    }
                    DropdownMenu(
                        expanded = durationExpanded,
                        onDismissRequest = { durationExpanded = false }
                    ) {
                        durationOptions.forEach { option ->
                            DropdownMenuItem(
                                text = { Text(option.first) },
                                onClick = {
                                    selectedDuration = option
                                    durationExpanded = false
                                }
                            )
                        }
                    }
                }
            }
        },
        confirmButton = {
            Button(onClick = {
                val loc = "$selectedRegion ($selectedResource)"
                onSubmit(selectedChar, loc, selectedDuration.second)
            }) {
                Text("Start")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) { Text("Cancel", color = Color.Gray) }
        },
        containerColor = CardBg
    )
}

// =========================================================
// Dialog: Harz bearbeiten (mit lesbarer Schrift)
// =========================================================
@Composable
fun AdjustResinDialog(currentResin: Int, maxResin: Int, onDismiss: () -> Unit, onConfirm: (Int) -> Unit) {
    var textVal by remember { mutableStateOf(currentResin.toString()) }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Adjust Resin", color = CoreCyan) },
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
                        focusedBorderColor = CoreCyan,
                        unfocusedBorderColor = Color.Gray,
                        focusedTextColor = Color.White,
                        unfocusedTextColor = Color.White,
                        cursorColor = CoreCyan
                    ),
                    modifier = Modifier.fillMaxWidth()
                )
            }
        },
        confirmButton = {
            Button(onClick = {
                val parsed = textVal.toIntOrNull() ?: currentResin
                onConfirm(parsed.coerceIn(0, maxResin))
            }) {
                Text("OK")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) { Text("Cancel", color = Color.Gray) }
        },
        containerColor = CardBg
    )
}

// =========================================================
// Helper: WorkManager Task einplanen
// =========================================================
fun scheduleExpeditionNotification(
    context: Context,
    charName: String,
    location: String,
    durationInHours: Long
) {
    val inputData = workDataOf(
        "char_name" to charName,
        "location" to location
    )

    val workRequest = OneTimeWorkRequestBuilder<ExpeditionWorker>()
        .setInitialDelay(durationInHours, TimeUnit.HOURS)
        .setInputData(inputData)
        .build()

    WorkManager.getInstance(context).enqueue(workRequest)
}

// =========================================================
// Helper: Dynamische Resource-ID Auflösung für Bilder
// =========================================================
@Composable
fun getDrawableIdForChar(charName: String): Int {
    val context = LocalContext.current
    val imageName = charName.lowercase().replace(" ", "_")
    return context.resources.getIdentifier(imageName, "drawable", context.packageName)
}

// =========================================================
// Speicher-Logik mit SharedPreferences & JSON
// =========================================================
private const val PREFS_NAME = "GenshinTrackerPrefs"
private const val KEY_EXPEDITIONS = "key_expeditions"
private const val KEY_RESIN = "key_resin"
private const val KEY_LAST_RESIN_UPDATE = "key_last_resin_update"

private fun saveExpeditions(context: Context, expeditions: List<Expedition>) {
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

private fun loadExpeditions(context: Context): List<Expedition> {
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

private fun saveResinData(context: Context, resin: Int, lastUpdateSec: Long) {
    val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    prefs.edit()
        .putInt(KEY_RESIN, resin)
        .putLong(KEY_LAST_RESIN_UPDATE, lastUpdateSec)
        .apply()
}

private fun loadResin(context: Context): Int {
    val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    return prefs.getInt(KEY_RESIN, 120)
}

private fun loadLastResinUpdate(context: Context): Long {
    val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    return prefs.getLong(KEY_LAST_RESIN_UPDATE, System.currentTimeMillis() / 1000)
}