function generatePracticePitchOptions(){
	var pitch = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#'];
	var htmlString = '<select class="practiceDropdown" id="pitch">';
	for (var i = 0; i < pitch.length; i++){
		htmlString = htmlString + '<option value="' + pitch[i] + '">' + pitch[i] + '</option>'
	}
	htmlString = htmlString + '</select>';
	return htmlString;
}

function generatePracticeModeOptions(){
	var mode = ['Major', 'Minor'];
	var htmlString = '<select class="practiceDropdown" id="mode">';
	htmlString = htmlString + '<option value="' + mode[0] + '">' + mode[0] + '</option>';
	htmlString = htmlString + '<option value="' + mode[1] + '">' +  mode[1] + '</option>';
	htmlString = htmlString + '</select>'
	return htmlString;
}

function showPracticeOptions(){
	var mainContainer = document.getElementById("mainContainer");
	var selectPitch = generatePracticePitchOptions();
	var selectMode = generatePracticeModeOptions();
	var buttons = '<br><br><button onclick="goBack()">BACK</button>&nbsp<button onclick="go()" id="practiceGoButton">GO</button>';
	mainContainer.innerHTML = selectPitch + selectMode + buttons;
}

function goBack(){
	var mainContainer = document.getElementById("mainContainer");
	mainContainer.innerHTML = '<center><input onclick="showPracticeOptions()" width="300px" id="practice" type="image" src="images/practicehover.png" alt="Submit" style="">&nbsp&nbsp&nbsp&nbsp' +
		'<input onclick="showFreestyle()" width="365px" id="freestyle" type="image" src="images/freestylehover.png" alt="Submit" style=""></center>';
	addButtonHovers();
}

function go(){
	var selectedPitch = document.getElementById("pitch").value;
	var selectedMode = document.getElementById("mode").value;
	mainContainer.innerHTML = 'You\'ve selected: ' + selectedPitch + ' ' + selectedMode + '!';	
	mainContainer.innerHTML = mainContainer.innerHTML + '<br><br><button onclick="showPracticeOptions()">BACK</button>';

	$.ajax({
	    data: 'pitch=' + selectedPitch + '&mode=' + selectedMode,
	    url: 'php/startPracticeMode.php',
	    error: function (xhr, status, error) {
	        if (xhr.status > 0) alert('got error: ' + status); // status 0 - when load is interrupted
	    },
	    success: function(data) {
	    	console.log(data);
	   	}
	});	
}
