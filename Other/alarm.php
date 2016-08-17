<?php
	$time = $_GET['time'];
	
	if($time){
		file_put_contents("alarm.txt", $time);
		echo $time;
	} else {
		echo file_get_contents("alarm.txt");
	}
?>