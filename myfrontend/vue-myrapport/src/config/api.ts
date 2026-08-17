// Configuration centralisée des APIs externes
const API_CONFIG = {
  EXTERNAL: {
    HOST: import.meta.env.VITE_EXTERNAL_API_HOST || '192.168.1.254',
    PORT: import.meta.env.VITE_EXTERNAL_API_PORT || '8001',
    get BASE_URL() {
      return `http://${this.HOST}:${this.PORT}`
    }
  },
  LOCAL: {
    BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://192.168.1.204'
  }
}

export default API_CONFIG