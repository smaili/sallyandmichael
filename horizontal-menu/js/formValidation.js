/* Contact Form validations start here  */
(function ($) {
	'use strict';
$( "#frm" ).submit(function( event ) {
	
  	event.preventDefault();
  	
  	var tempn = 0;
    var tempe = 0;
	var tempc = 0;
	var tempa = 0;
	var tempg = 0;

    var a =$("#Name").val();
    if(a==""){
			tempn=1;
	}
	else{
			tempn=0;
	}
	
	var a =$("#Emailaddress").val();
	var filter = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
    if(a==""){
        tempe=1;
	}
	else if (!filter.test(a)) {
	    tempe=1;
    }
	else{
		tempe=0;
	}
	
	var a =$("#Contactnumber").val();
    if(a==""){
        tempc=1;
	}
	else if (isNaN(a)) 
    {
	    tempc=1;
    }
	else{
		tempc=0;
	}
	
	var a =$("#attendiesDetails").val();
    if(a==""){
	    tempa=1;
	}
	else{
		tempa=0;
	}
	
	var a =$("#guestDetails").val();
    if(a==""){
			tempg=1;
	}
	else{
			tempg=0;
	}  	
  	
  	if(tempn == 0 && tempe == 0 && tempc == 0 && tempa == 0 && tempg == 0 ){
  	    $("#loding").css("display","inline-block");
  	    $.post( "mail_script.php", { 
		    Name:             $("#Name").val(),
			Emailaddress:     $("#Emailaddress").val(),
			Contactnumber:    $("#Contactnumber").val(),
			attendiesDetails: $("#attendiesDetails").val(),
			guestDetails:     $("#guestDetails").val(),
			message:          $("#message").val()
		})
        .done(function( data ) {
  		    if(data==1)	{
  			    $( "#loding").hide();
  			    $( "#Success").slideDown( "slow" );
        		setTimeout(function() {
                	$( "#Success").slideUp( "slow" );
            	}, 3000);
            	$("#frm")[0].reset();
			}
			else{
			    $( "#loding").hide();
				$( "#Error").slideDown( "slow" );
        		setTimeout(function() {
                	$( "#Error").slideUp( "slow" );
            	}, 3000);
			}
		});
  	}	
});
})(jQuery);
/* Contact Form validation ends here  */