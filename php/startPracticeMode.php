<?php 

$pitch = $_GET['pitch'];
$mode = $_GET['mode'];
$commandString = 'python /home/akelly/RockBlend/notes.py 0 ' . $pitch . ' ' . $mode;
$command = escapeshellcmd($commandString);
$output = shell_exec($command);
echo $output;

?>