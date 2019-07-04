<?php
require_once(dirname(__FILE__) . "/api_key.php");

class Face
{
    private $image_file;
    private $face_token;

    public function __construct($image_file)
    {
        $this->image_file = $image_file;
        $this->detectFace($this->image_file);
    }

    public function __set($name, $value)
    {
        if ($name == 'image_file') {
            $this->$name = $value;
        }
    }

    public function __get($name)
    {
        if ($name == 'face_token') {
            return $this->$name;
        } else {
            return null;
        }
    }

    public function detectFace()
    {
        $curl_detect = curl_init();
        curl_setopt_array($curl_detect, array(
            CURLOPT_URL => "https://api-cn.faceplusplus.com/facepp/v3/detect",
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_ENCODING => "",
            CURLOPT_MAXREDIRS => 10,
            CURLOPT_TIMEOUT => 30,
            CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
            CURLOPT_CUSTOMREQUEST => "POST",
            CURLOPT_HTTPHEADER => array("cache-control: no-cache"),
            CURLOPT_POSTFIELDS => array(
                'api_key' => API_KEY,
                'api_secret' => API_SECRET,
                'image_file";filename="image' => $this->image_file
            )
        ));
        $response_detect = curl_exec($curl_detect);
        $err_detect = curl_error($curl_detect);
        curl_close($curl_detect);
        if($err_detect) {
            return "REQUEST_ERROR";
        } else {
            $res_detect = json_decode($response_detect, true);
            if (isset($res_detect['error_message'])) {
                return $res_detect['error_message'];
            } else {
                if (empty($res_detect['faces'])) {
                    return "NO_FACE_DETECTED";
                } else {
                    $this->face_token = $res_detect['faces'][0]['face_token'];
                    return true;
                }
            }
        }
    }

    public function uploadFace($outer_id)
    {
        $curl_upload = curl_init();
        curl_setopt_array($curl_upload, array(
            CURLOPT_URL => "https://api-cn.faceplusplus.com/facepp/v3/faceset/addface",
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_ENCODING => "",
            CURLOPT_MAXREDIRS => 10,
            CURLOPT_TIMEOUT => 30,
            CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
            CURLOPT_CUSTOMREQUEST => "POST",
            CURLOPT_HTTPHEADER => array("cache-control: no-cache"),
            CURLOPT_POSTFIELDS => array(
                'api_key' => API_KEY,
                'api_secret' => API_SECRET,
                'outer_id' => $outer_id,
                'face_tokens' => $this->face_token
            )
        ));
        $response_upload = curl_exec($curl_upload);
        $err_upload = curl_error($curl_upload);
        curl_close($curl_upload);
        if($err_upload) {
            return "REQUEST_ERROR";
        } else {
            $res_upload = json_decode($response_upload, true);
            if (isset($res_upload['error_message'])) {
                return $res_upload['error_message'];
            } else {
                if ($res_upload['face_added'] != 1) {
                    return "NO_FACE_UPLOADED";
                } else {
                    return true;
                }
            }
        }
    }

    public static function compareFace($image_file1, $image_file2)
    {
        $curl_compare = curl_init();
        curl_setopt_array($curl_compare, array(
            CURLOPT_URL => "https://api-cn.faceplusplus.com/facepp/v3/compare",
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_ENCODING => "",
            CURLOPT_MAXREDIRS => 10,
            CURLOPT_TIMEOUT => 30,
            CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
            CURLOPT_CUSTOMREQUEST => "POST",
            CURLOPT_HTTPHEADER => array("cache-control: no-cache"),
            CURLOPT_POSTFIELDS => array(
                'api_key' => API_KEY,
                'api_secret' => API_SECRET,
                'image_file1";filename="image' => $image_file1,
                'image_file2";filename="image' => $image_file2
            )
        ));
        $response_compare = curl_exec($curl_compare);
        $err_compare = curl_error($curl_compare);
        curl_close($curl_compare);
        if($err_compare) {
            return "REQUEST_ERROR";
        } else {
            $res_compare = json_decode($response_compare, true);
            if (isset($res_compare['error_message'])) {
                return $res_compare['error_message'];
            } else {
                if (empty($res_compare['faces1']) || empty($res_compare['faces2'])) {
                    return "NO_FACE_DETECTED";
                } else {
                    $thresholds = $res_compare['thresholds'];
                    $confidence = $res_compare['confidence'];
                    if ($confidence > $thresholds['1e-5']) {
                        return true;
                    } else {
                        return "MATCHING_FAIL";
                    }
                }
            }
        }
    }
}
