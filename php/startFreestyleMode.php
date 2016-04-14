<?php 

$commandString = 'export DISPLAY=:0.0; sudo -u akelly python ../scripts/notes.py 0';
//$commandString = 'sudo -u akelly ../scripts/rockblend.sh 0';
echo shell_exec($commandString);

?>