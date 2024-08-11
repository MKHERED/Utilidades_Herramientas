<?php

$ruta = "uploads/";

$directorio = scandir($ruta);


foreach ($directorio as $key => $value) {
    if ($value != "." || $value != "..") {
        $ruta_relativa = $ruta.$value;
        $a_borrar = realpath($ruta_relativa);
        unlink($a_borrar);
    }
}



$ruta = $ruta.basename($_FILES["file"]["name"]);
move_uploaded_file($_FILES["file"]["tmp_name"], $ruta);
return
//var_dump ($_FILES['file']);
//return response()->json($_FILES);   
?>
