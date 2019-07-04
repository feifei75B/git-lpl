<?php
require_once("Face.class.php");
if (!empty($_FILES['photo1']['tmp_name'])) {
    $photo1_tmp = $_FILES['photo1']['tmp_name'];
    $photo2_tmp = $_FILES['photo2']['tmp_name'];
    $fp = fopen($photo1_tmp, 'rb');
    $photo1 = fread($fp, filesize($photo1_tmp));
    fclose($fp); 
    $fp = fopen($photo2_tmp, 'rb');
    $photo2 = fread($fp, filesize($photo2_tmp));
    fclose($fp);
    $face1 = new Face($photo1);
    $face2 = new Face($photo2);
    echo $face1->face_token;
    echo '<br>';
    echo $face2->face_token;
    echo '<br>';
    $result = Face::compareFace($photo1, $photo2);
    echo $result;
}
?>
