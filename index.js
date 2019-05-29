const electron = require('electron')
const {app, BrowserWindow, dialog} = require('electron')

const main = require('electron').ipcMain


let currentWindow;
let filePath = '';

let eleCountMain = 0


app.on('ready', () => {
	let win = new BrowserWindow({width:600, height:400, title:'The Pied Piper Project'})
	win.setResizable(false)
	currentWindow = win

	win.loadURL(`file://${__dirname}/index.html`)

	/* Prompt the user to upload a file which
		extracts the path of the selected file */

	main.on('back-home', function(event, arg){
		win.loadURL(`file://${__dirname}/index.html`)
	})

	main.on('get-file-path', function (event, arg) {
		filePath = dialog.showOpenDialog(currentWindow)

		let {PythonShell} = require('python-shell')
		let options = {
			args:[filePath]
		}

		PythonShell.run('getFileInfo.py', options, function  (err, results)  {
			if  (err)  throw err;
			console.log('getFileInfo.py finished running!');

			event.sender.send('file-details', results)
			// event.sender.send('update-ele-cnt', eleCountMain)
			})

	})

	main.on('download-file', function(event, arg){

		let {PythonShell} = require('python-shell')
		let options = {
			args:[filePath]
		}

		PythonShell.run('download.py', options, function  (err, results)  {
			if  (err)  throw err;
			console.log('download.py finished running!');
		
			})

	})

	main.on('decompress-file', function(event, arg){

		let {PythonShell} = require('python-shell')
		let options = {
			args:[filePath]
		}

		PythonShell.run('main.py', options, function  (err, results)  {
			if  (err)  throw err;
			console.log('decompressor.py finished running!');

			filePath = results[6]

			let new_file_data = {
				path: results[6],
				old_size: results[7] / 1000000 + " mB",
				new_size: results[8] / 1000000 + " mB",
				comp_ratio: results[7] / results[8]
			}

			event.sender.send('new_file_data', new_file_data)
			// event.sender.send('update-ele-cnt', eleCountMain)
			})
		
	})

	main.on('compress-file', function(event, arg) {

		let {PythonShell} = require('python-shell')
		let options = {
			args:[filePath]
		}

		PythonShell.run('main.py', options, function  (err, results)  {
			if  (err)  throw err;
			console.log('compressor.py finished running!');
			console.log(results)

			filePath = results[6]

			let lzw_file_data = {
				path: results[6],
				old_size: results[7] / 1000000 + " mB",
				new_size: results[8] / 1000000 + " mB",
				comp_ratio: results[7] / results[8]
			}

			event.sender.send('lzw_file_data', lzw_file_data)
			// event.sender.send('update-ele-cnt', eleCountMain)
			})

	})
	
})

