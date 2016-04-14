function showFreestyle(){
	var mainContainer = document.getElementById("mainContainer");
	mainContainer.innerHTML = "FREESTYLE!!!";
	var buttons = '<br><br><button onclick="goBack()" id="practiceBackButton">BACK</button>'
	mainContainer.innerHTML = mainContainer.innerHTML + buttons;

	$.ajax({
	    url: 'php/startFreestyleMode.php',
	    error: function (xhr, status, error) {
	        if (xhr.status > 0) alert('got error: ' + status); // status 0 - when load is interrupted
	    },
	    success: function(data){
	    	console.log(data);
	    }
	});		
}