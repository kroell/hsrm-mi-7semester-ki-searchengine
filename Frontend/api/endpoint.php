<?php 

header('Content-Type: application/json');


$test = json_encode($_POST);

 
// Ta-da, using $_POST as normal; PHP is able to
// unserialize the AngularJS request no problem
echo $test;

?>