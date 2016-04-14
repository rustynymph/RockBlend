<?php 

$pitch = $_GET['pitch'];
$mode = $_GET['mode'];
$commandString = 'sudo -u akelly python ../scripts/notes.py 0 ' . $pitch . ' ' . $mode;
echo exec($commandString);

?>