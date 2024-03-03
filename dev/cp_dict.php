<?php
$file = 'php_dict.txt';
$f = get_defined_functions();
sort( $f['internal'] );
$dict = implode( "\n", $f['internal'] );
file_put_contents($file, $dict);
?>
