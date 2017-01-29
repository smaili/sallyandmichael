<?php
	$Name             = addslashes($_POST['Name']);
	$Emailaddress     = addslashes($_POST['Emailaddress']);
	$Contactnumber    = addslashes($_POST['Contactnumber']);
	$attendiesDetails = addslashes($_POST['attendiesDetails']);
	$guestDetails     = addslashes($_POST['guestDetails']);
	$message          = addslashes($_POST['message']);
	$headers= "MIME-Version: 1.0\n";
	$headers.="Content-type: text/html; charset=iso-8859-1\n";
 	$headers.= "From: $Name < ".$Emailaddress." >"; //FROM Email Address & Name
	$subject = "Lovebird User "; // Email Subject Line
	$toemail = "YOUR EMAIL ADDRESS"; // to Email Address
	$mail2 = "<table width='600' border='0' cellpadding='3' cellspacing='3'>
			  			<tr>
							<td colspan='2' align='center'>
								<table width='600' cellpadding='3' cellspacing='3' border='0'>
									<tr>
					  					<td>
					  						<table width='100%' cellspacing='0' cellpadding='12' border='1' bordercolor='#919191'>
						  						<tr>
													<td width='32%' align='right'><font face='Arial, Helvetica, sans-serif' size='4'>Name :</font></td>
													<td width='68%' align='left'><font face='Arial, Helvetica, sans-serif' size='4'>$Name</font></td>
						  						</tr>
						  						<tr>
													<td align='right'><font face='Arial, Helvetica, sans-serif' size='4'>Email :</font></td>
													<td align='left'><font face='Arial, Helvetica, sans-serif' size='4'>$Emailaddress</font></td>
						  						</tr>
						  						<tr>
													<td align='right'><font face='Arial, Helvetica, sans-serif' size='4'>Contact :</font></td>
													<td align='left'><font face='Arial, Helvetica, sans-serif' size='4'>$Contactnumber</font></td>
						  						</tr>
						  						<tr>
													<td align='right'><font face='Arial, Helvetica, sans-serif' size='4'>Attending? :</font></td>
													<td align='left'><font face='Arial, Helvetica, sans-serif' size='4'>$attendiesDetails</font></td>
						  						</tr>
						  						<tr>
													<td align='right'><font face='Arial, Helvetica, sans-serif' size='4'>Guests :</font></td>
													<td align='left'><font face='Arial, Helvetica, sans-serif' size='4'>$guestDetails</font></td>
						  						</tr>
						  						<tr>
													<td align='right' valign='top'><font face='Arial, Helvetica, sans-serif' size='4'>Message :</font></td>
													<td align='left'><font face='Arial, Helvetica, sans-serif' size='4'>$message</font></td>
												</tr>
						  					</table>
						  				</td>
									</tr>
				  				</table>
				  			</td>
			  			</tr>
					</table>";
	$sendmail = mail($toemail,$subject,$mail2,$headers);
   	if(!$sendmail){ 
		echo "0";
   	}
   	else{	
	   	echo "1";
   	} 
?>