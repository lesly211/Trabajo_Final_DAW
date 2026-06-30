/**
 * Frontend Configuration
 * Centraliza todas las configuraciones de la aplicación
 * Se adapta automáticamente basado en las variables de entorno
 */

const isDevelopment = import.meta.env.MODE === 'development'
const isProduction = import.meta.env.MODE === 'production'

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || (
  isDevelopment ? 'http://localhost:5000' : window.location.origin
)

const API_ENDPOINTS = {
  HEALTH: '/api/health',
  STATS: '/api/stats',
  MODULES: '/api/modules'
}

// Feature Flags
const FEATURES = {
  ENABLE_LOGGING: isDevelopment,
  ENABLE_DEBUG_PANEL: isDevelopment,
  ENABLE_ANALYTICS: isProduction
}

// Timeouts (milliseconds)
const TIMEOUTS = {
  API_REQUEST: import.meta.env.VITE_API_TIMEOUT || 30000,
  RETRY_DELAY: import.meta.env.VITE_RETRY_DELAY || 2000
}

// Retry Configuration
const RETRY_CONFIG = {
  MAX_ATTEMPTS: import.meta.env.VITE_MAX_RETRY_ATTEMPTS || 3,
  BACKOFF_MULTIPLIER: 1.5
}

// App Configuration
const APP_CONFIG = {
  NAME: 'Sistema Académico',
  VERSION: '1.0.0',
  DESCRIPTION: 'Plataforma de Gestión Académica Integral'
}

// Utility Functions
export const getApiUrl = (endpoint) => `${API_BASE_URL}${endpoint}`

export const getConfig = (key) => {
  const configs = {
    ...API_ENDPOINTS,
    ...FEATURES,
    ...TIMEOUTS,
    ...APP_CONFIG
  }
  return configs[key]
}

// Logger utility
export const logger = {
  log: (message, data) => {
    if (FEATURES.ENABLE_LOGGING) {
      console.log(`[${APP_CONFIG.NAME}]`, message, data || '')
    }
  },
  error: (message, error) => {
    console.error(`[${APP_CONFIG.NAME}] ERROR:`, message, error)
  },
  warn: (message, data) => {
    if (FEATURES.ENABLE_LOGGING) {
      console.warn(`[${APP_CONFIG.NAME}] WARN:`, message, data || '')
    }
  }
}

export default {
  API_BASE_URL,
  API_ENDPOINTS,
  FEATURES,
  TIMEOUTS,
  RETRY_CONFIG,
  APP_CONFIG,
  getApiUrl,
  getConfig,
  logger
}
