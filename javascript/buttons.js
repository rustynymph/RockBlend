function addButtonHovers(){
	var freestyleButton = document.getElementById("freestyle");
	freestyleButton.onmouseover = function(){
	    this.setAttribute('src', 'images/freestyle.png');
	    };
	freestyleButton.onmouseout = function(){
	    this.setAttribute('src', 'images/freestylehover.png');
	};    

	var practiceButton = document.getElementById("practice");
	practiceButton.onmouseover = function(){
	    this.setAttribute('src', 'images/practice.png');
	    };
	practiceButton.onmouseout = function(){ 
	    this.setAttribute('src', 'images/practicehover.png');
	}; 	
}

addButtonHovers();