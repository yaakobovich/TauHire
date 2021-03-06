var newNum = 0; //always the numeric ID of the new input field being added
var elems = 1; //number of course elements on page, starts as 1

//get list of courses
var courses = $("#courses option").map(function () {
    return this.value;
}).get();

//function to delete a course element from the page
function b() {
  var num = this.id.substring(9);
  elems--;

  $('#cloneme' + num).remove(); // remove the correct element

  //if only one element remains, disable the "remove" button
  if (elems == 1) {
	    var inputs = document.getElementsByClassName("buttondel");
	for (var i = 0; i < inputs.length; i++) {
        inputs[i].disabled = true;
	}
  }
}



//upon clicking on add button, add another set of fields for course to pages html
$('#buttonadd').click(function ab() {
  elems++;
  newNum = new Number(newNum + 1); // the numeric ID of the new input field being added
  // create the new element via clone(), and manipulate it's ID using newNum value
  //var newElem = $('#cloneme' + (newNum - 1)).clone().attr('id', 'cloneme' + newNum);
  var newElem = $('.cloneme:first').clone().attr('id', 'cloneme' + newNum).attr('class', 'cloneme');
  // manipulate the name/id values of the input inside the new element
  newElem.children().eq(0).val('');
  newElem.children().eq(1).val('');
  newElem.children().eq(2).attr('id', 'buttondel' + newNum).attr('class', 'buttondel');
 
  newElem.children().eq(2)[ 0 ].onclick= b;
 
  // insert the new element after the last "duplicatable" input field
  //$('#cloneme' + (newNum-1)).after(newElem);
  $(newElem).insertBefore('#avgEntry');
  // enable the "remove" button
  //$('.buttondel').attr('disabled', '');
  var inputs = document.getElementsByClassName("buttondel");
	for (var i = 0; i < inputs.length; i++) {
        inputs[i].disabled = false;
	}


});

//validate form input before submission, if not stop and alert with error message
function validateForm() {
	var git=document.getElementById("git").value;
	
	var allCourseNamesValid = $(".feedback-input").filter(function (key, element) {
        var value = $(element).val();   
        return value === "" || courses.indexOf(value) < 0;
    }).length === 0;


 	var allGradesValid = $(".feedback-input2").filter(function (key, element) {
        var value = $(element).val();
        return value === "";
    }).length === 0; 
	
	var avgValid = $(".average").filter(function (key, element) {
        var value = $(element).val();
        return value === "";
    }).length === 0; 
	
	var file = document.getElementsByName('cv')[0];
	var iscvvalid=true;
	if (file.value!==""){
		if (file.value.match(/\.([^.]+)$/)==null) {
			iscvvalid=false;
		}
		else{
			var ext =  file.value.match(/\.([^.]+)$/)[1];
			switch(ext){
				case 'pdf':
					break;
				default:
					iscvvalid=false;
			}
		}
	}

    if ( !allCourseNamesValid) {
		alert("please enter a valid course name");
		return false }
		
    if (!allGradesValid) {
		alert("please enter a grade between 60 and 100");
		return false }
		
	if (!avgValid) {
		alert("please enter a grade average between 60 and 100");
		return false }
	
	
	if (git!="" && git.substring(0,"github.com/".length) !== "github.com/"){
		alert("please enter github.com/(YOUR ACCOUNT) or leave the field empty");
		return false;
	}
	
	if (!iscvvalid){
		alert('Error: Chosen file type is not allowed, please insert a pdf file');
		return false
	}	
	
	
	return true;
}


//deleting is disabled until add is clicked
$('.buttondel')[ 0 ].onclick= b;
$('.buttondel').attr('disabled', 'disabled');


$(document).ready(function() {
// JS code for tooltip to appear and tooltip message
var msg="!פרטיותך חשובה לנו<br/>.SSL האתר מאובטח על ידי<br/>.רק חברות שאושרו על ידי צוות האתר יוכלו לצפות בנתוניך, ורק באופן אנונימי"
$('#masterTooltip').hover(function(){
        // Hover over code
        var title = $(this).attr('title');
        $(this).data('tipText', title).removeAttr('title');
        $('<p class="tooltip"></p>')
        .html(msg)
        .appendTo('body')
        .fadeIn('slow');
}, function() {
        // Hover out code
        $(this).attr('title', $(this).data('tipText'));
        $('.tooltip').remove();
}).mousemove(function(e) {
        var mousex = e.pageX - 509; //Get X coordinates
        var mousey = e.pageY - 90; //Get Y coordinates
        $('.tooltip')
        .css({ top: mousey, left: mousex })
});
});



