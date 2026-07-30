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

        NotificationHelper.showNotification(
            context = context,
            title = "Expedition complete! 🎉",
            message = "$charName has returned from the ($location) expedition.",
            notificationId = System.currentTimeMillis().toInt()
        )

        return Result.success()
    }
}
