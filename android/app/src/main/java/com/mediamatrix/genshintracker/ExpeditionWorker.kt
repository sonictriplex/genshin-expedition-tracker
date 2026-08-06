package com.mediamatrix.genshintracker

import android.content.Context
import androidx.work.Worker
import androidx.work.WorkerParameters

class ExpeditionWorker(
    private val context: Context,
    workerParams: WorkerParameters
) : Worker(context, workerParams) {

    override fun doWork(): Result {
        val charName = inputData.getString("char_name") ?: "Character"
        val location = inputData.getString("location") ?: "Expedition"
        val language = inputData.getString("language") ?: "Deutsch"

        val title = AppTranslations.tr("notif_title", language)
        val msgTemplate = AppTranslations.tr("notif_msg", language)
        val message = String.format(msgTemplate, charName, location)

        NotificationHelper.showNotification(
            context = context,
            title = title,
            message = message,
            notificationId = System.currentTimeMillis().toInt()
        )

        return Result.success()
    }
}
