import { app, BrowserWindow, ipcMain, dialog } from 'electron'
import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
import path from 'node:path'
import { exec } from 'node:child_process';  // ✅ Importar exec con ES modules

// Simula __dirname y __filename en módulos ES
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const isDev = !app.isPackaged

let win

async function createWindow () {
  win = new BrowserWindow({
    fullscreen: true,
    backgroundColor: '#0b0c0f',
    titleBarStyle: 'hiddenInset',
    vibrancy: 'under-window',
    webPreferences: {
      preload: path.join(process.cwd(), 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      spellcheck: false,
    }
  })

  await win.loadFile(path.join(__dirname, 'src', 'index.html'))
}

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow()
})

// Confirmación de salida (para el modal "¿Seguro que querés salir?")
ipcMain.handle('app:confirm-exit', async () => {
  app.quit()
})

// Matar procesos hijos (backend, python, node, etc.)
app.on('before-quit', () => {
  exec('taskkill /IM node.exe /F');
  exec('taskkill /IM python.exe /F');
  exec('taskkill /IM cmd.exe /F');
});