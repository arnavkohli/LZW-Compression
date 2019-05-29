const renderer = require('electron').ipcRenderer

function pushUp(){
	let heading = document.getElementById('heading');
	let buttons = document.getElementById('buttons');

	heading.style.animationName = 'up-anim-heading';
	buttons.style.animationName = 'up-anim-buttons';
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function pushDown() {

  let upld_info = document.getElementById('uploaded_data_info');
  let data_info = document.getElementById('data_info');
  upld_info.style.animationName = 'down-anim';

  console.log('Taking a break...');
  await sleep(2000);
  console.log('Two seconds later');

  upld_info.parentNode.insertBefore(data_info, upld_info);
  data_info.style.visibility = 'visible';
  data_info.style.animationName = 'data-anim'
}

// function pushDown(){
// 	let upld_info = document.getElementById('uploaded_data_info');
// 	let data_info = document.getElementById('data_info');
// 	upld_info.style.animationName = 'down-anim';


// 	demo();

// }

function backToHome(){
	renderer.send('back-home', 'Back To Home');
}


renderer.on('lzw_file_data', function(event , arg){
	// console.log(arg)
	let upld_info = document.getElementById('uploaded_data_info');
	let comp_info = document.getElementById('data_info');

	// upld_info.parentNode.insertBefore(comp_info, upld_info);

	// upld_info.style.animationName = 'left-anim';
	// upld_info.style.visibility = 'hidden';
	// comp_info.style.visibility = 'visible';
	// comp_info.style.animationName = 'data-anim';

	document.getElementById('new_file_size').innerHTML = arg.new_size
	document.getElementById('old_file_size').innerHTML = arg.old_size
	console.log(arg.comp_ratio)
	document.getElementById('comp_ratio').innerHTML = arg.comp_ratio

	let comp_btn = document.getElementById('compress_btn');
	let download_btn = document.getElementById('download_btn');
	comp_btn.parentNode.insertBefore(download_btn, comp_btn);

	comp_btn.style.visibility = 'hidden';
	download_btn.style.visibility = 'visible';
})

renderer.on('new_file_data', function(event, arg){
	let upld_info = document.getElementById('uploaded_data_info');
	let comp_info = document.getElementById('data_info');

	// upld_info.parentNode.insertBefore(comp_info, upld_info);

	// upld_info.style.visibility = 'hidden';
	// comp_info.style.visibility = 'visible';

	document.getElementById('new_file_size').innerHTML = arg.new_size
	document.getElementById('old_file_size').innerHTML = arg.old_size
	document.getElementById('comp_ratio').innerHTML = arg.comp_ratio

	let decomp_btn = document.getElementById('decompress_btn');
	let download_btn = document.getElementById('download_btn');
	decomp_btn.parentNode.insertBefore(download_btn, decomp_btn);

	decomp_btn.style.visibility = 'hidden';
	download_btn.style.visibility = 'visible';

})


renderer.on('file-details', function(event, arg){
	console.log('RECIEVED')

	document.getElementById('file_name').innerHTML = arg[0]
	document.getElementById('file_type').innerHTML = arg[1]
	let fileType = document.getElementById('file_type').innerHTML


	document.getElementById('last_accessed').innerHTML = arg[2]
	document.getElementById('last_modified').innerHTML = arg[3]
	document.getElementById('date_created').innerHTML = arg[4]
	document.getElementById('file_size').innerHTML = arg[5] + " bytes"



	let upld_btn = document.getElementById('file_path_btn');

	if (fileType == 'lzw'){
		let decomp_btn = document.getElementById('decompress_btn');
		upld_btn.parentNode.insertBefore(decomp_btn, upld_btn);

		upld_btn.style.visibility = 'hidden';
		decomp_btn.style.visibility = 'visible';
	}

	else{
		let comp_btn = document.getElementById('compress_btn');
		upld_btn.parentNode.insertBefore(comp_btn, upld_btn);

		upld_btn.style.visibility = 'hidden';
		comp_btn.style.visibility = 'visible';
	}


	let upld_info = document.getElementById('uploaded_data_info');

	upld_info.style.visibility = 'visible';


})