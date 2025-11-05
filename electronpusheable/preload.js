// Use CommonJS in preload to avoid ESM import errors in sandboxed context
const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('atlas', {
  confirmExit: async () => {
    return await ipcRenderer.invoke('app:confirm-exit')
  }
})
