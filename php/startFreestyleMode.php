<?php 

$commandString = 'python /home/akelly/RockBlend/notes.py 0';
$command = escapeshellcmd($commandString);
$output = shell_exec($command);
echo $output;

?>