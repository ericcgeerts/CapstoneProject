const { app, BrowserWindow, ipcMain, dialog } = require('electron/main')
const path = require('node:path')
const fs = require('fs')
//reference algorithim script
const pythonProcess = spawn('python', ['final_capstone_algorithm.py'])

//generic electron boilerplate code
function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,

    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  })

  win.loadFile('index.html')
}
//handle closing and opening of application
app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})


//Grab values from Text input and pass to a CSV so that when we call python, it can read them
ipcMain.on('text-input', (event, inputValue, inputValue1, inputValue2, inputValue3) => {

  //console.log(`Received input: ${inputValue}`);
  // console.log(`Received input: ${inputValue1}`);
  //console.log(`Received input: ${inputValue2}`);
  //console.log(`Received input: ${inputValue3}`); 

  const array = [];
  array.push(inputValue, inputValue1, inputValue2, inputValue3);
  //console.log(`Received input: ${array}`)

  const result = array.join(',');

  fs.writeFile('Weights.csv', result, (err) => {
    if (err) {
      console.error('Error writing to CSV file', err);
    }
  });
})
//Handle Student Data Upload
ipcMain.handle('select-file', async () => {
  const result = await dialog.showOpenDialog({
    properties: ['openFile'], // Allow file selection
  })

  if (result.canceled) {
    return null; // User canceled the dialog
  }

  // Return the file path and save in a .txt so that it can be passed to python algorithim
  fs.writeFile('FilePath.txt', result, (err) => {
    if (err) {
      console.error('Error writing to txt file', err);
    }
  })
})

//On Submit, call the python algorithim after saving the student data file path that was uploaded
// No need to pass data as it is saved locally in a CSV
ipcMain.on('results-input', (event, inputValue) => {
  // console.log(`Received input: ${inputValue}`);
  const dataPython = ''
  pythonProcess.stdout.on('data', (dataPython) => {
    //console.log(`Output: ${dataPython}`);
  });
})
