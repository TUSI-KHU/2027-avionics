/**
 * @file main.c
 * @brief NURA Flight Computer Main Entry Point
 * @target Espressif ESP32-S3-WROOM-1-N16R8
 * @framework ESP-IDF with FreeRTOS
 */

#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "esp_system.h"

static const char *TAG = "NURA_MAIN";

void app_main(void)
{
    ESP_LOGI(TAG, "========================================");
    ESP_LOGI(TAG, "  NURA 2027 Avionics Flight Computer    ");
    ESP_LOGI(TAG, "  Target: ESP32-S3-WROOM-1-N16R8        ");
    ESP_LOGI(TAG, "========================================");

    // TODO: FreeRTOS Core 0 태스크 (센서 수집 및 EKF 자세 추정)
    // TODO: FreeRTOS Core 1 태스크 (통신, 데이터 로깅 및 사출 FSM)
}
