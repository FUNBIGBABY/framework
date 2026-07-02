export const APP_NAME =
  import.meta.env.VITE_APP_NAME || 'Personal AI Framework Studio'

export const APP_INITIAL = (APP_NAME.trim()[0] || 'A').toUpperCase()
