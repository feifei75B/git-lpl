<?php
require_once(dirname(__FILE__) . "/api_key.php");
require_once(dirname(__FILE__) . "/Face.class.php");

class FaceSet
{
    private $outer_id;

    public function __construct($outer_id)
    {
        $this->outer_id = $outer_id;
    }

    public function __set($name, $value)
    {
        $this->$name = $value;
    }

    public function __get($name)
    {
        return $this->$name;
    }

    public function createFaceSet()
    {
        $curl_create = curl_init();
        curl_setopt_array($curl_create, array(
            CURLOPT_URL => "https://api-cn.faceplusplus.com/facepp/v3/faceset/create",
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
                'outer_id' => $this->outer_id
            )
        ));
        $response_create = curl_exec($curl_create);
        $err_create = curl_error($curl_create);
        curl_close($curl_create);
        if ($err_create) {
            return "REQUEST_ERROR";
        } else {
            $res_create = json_decode($response_create, true);
            if (isset($res_create['error_message'])) {
                return $res_create['error_message'];
            } else {
                return true;
            }
        }
    }

    public function addFace(Face $face_obj)
    {
        $curl_add = curl_init();
        curl_setopt_array($curl_add, array(
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
                'outer_id' => $this->outer_id,
                'face_tokens' => $face_obj->face_token
            )
        ));
        $response_add = curl_exec($curl_add);
        $err_add = curl_error($curl_add);
        curl_close($curl_add);
        if($err_add) {
            return "REQUEST_ERROR";
        } else {
            $res_add = json_decode($response_add, true);
            if (isset($res_add['error_message'])) {
                return $res_add['error_message'];
            } else {
                if ($res_add['face_added'] != 1) {
                    return "NO_FACE_ADDED";
                } else {
                    return true;
                }
            }
        }
    }

    public function removeFace($face_token)
    {
        $curl_remove = curl_init();
        curl_setopt_array($curl_remove, array(
            CURLOPT_URL => "https://api-cn.faceplusplus.com/facepp/v3/faceset/removeface",
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
                'outer_id' => $this->outer_id,
                'face_tokens' => $face_token
            )
        ));
        $response_remove = curl_exec($curl_remove);
        $err_remove = curl_error($curl_remove);
        curl_close($curl_remove);
        if ($err_remove) {
            return "REQUEST_ERROR";
        } else {
            $res_remove = json_decode($response_remove, true);
            if (isset($res_remove['error_message'])) {
                return $res_remove['error_message'];
            } else {
                if ($res_remove['face_removed'] != 1) {
                    return $res_remove['failure_detail'][0]['reason'];
                } else {
                    return true;
                }
            }
        }
    }

    public function removeAllFace()
    {
        $curl_remove_all = curl_init();
        curl_setopt_array($curl_remove_all, array(
            CURLOPT_URL => "https://api-cn.faceplusplus.com/facepp/v3/faceset/removeface",
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
                'outer_id' => $this->outer_id,
                'face_tokens' => "RemoveAllFaceTokens"
            )
        ));
        $response_remove_all = curl_exec($curl_remove_all);
        $err_remove_all = curl_error($curl_remove_all);
        curl_close($curl_remove_all);
        if ($err_remove_all) {
            return "REQUEST_ERROR";
        } else {
            $res_remove_all = json_decode($response_remove_all, true);
            if (isset($res_remove_all['error_message'])) {
                return $res_remove_all['error_message'];
            } else {
                if ($res_remove_all['face_count'] != 0) {
                    return "FACES_EXISTING";
                } else {
                    return true;
                }
            }
        }
    }

    public function deleteFaceSet()
    {
        $curl_delete = curl_init();
        curl_setopt_array($curl_delete, array(
            CURLOPT_URL => "https://api-cn.faceplusplus.com/facepp/v3/faceset/delete",
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
                'outer_id' => $this->outer_id
            )
        ));
        $response_delete = curl_exec($curl_delete);
        $err_delete = curl_error($curl_delete);
        curl_close($curl_delete);
        if ($err_delete) {
            return "REQUEST_ERROR";
        } else {
            $res_delete = json_decode($response_delete, true);
            if (isset($res_delete['error_message'])) {
                return $res_delete['error_message'];
            } else {
                return true;
            }
        }
    }

    public function updateFaceSet($new_outer_id)
    {
        $curl_update = curl_init();
        curl_setopt_array($curl_update, array(
            CURLOPT_URL => "https://api-cn.faceplusplus.com/facepp/v3/faceset/update",
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
                'outer_id' => $this->outer_id,
                'new_outer_id' => $new_outer_id
            )
        ));
        $response_update = curl_exec($curl_update);
        $err_update = curl_error($curl_update);
        curl_close($curl_update);
        if ($err_update) {
            return "REQUEST_ERROR";
        } else {
            $res_update = json_decode($response_update, true);
            if (isset($res_update['error_message'])) {
                return $res_update['error_message'];
            } else {
                $this->outer_id = $new_outer_id;
                return true;
            }
        }
    }

    public function searchFace($image_file)
    {
        $curl_search = curl_init();
        curl_setopt_array($curl_search, array(
            CURLOPT_URL => "https://api-cn.faceplusplus.com/facepp/v3/search",
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
                'outer_id' => $this->outer_id,
                'image_file";filename="image' => $image_file
            )
        ));
        $response_search = curl_exec($curl_search);
        $err_search = curl_error($curl_search);
        curl_close($curl_search);
        if ($err_search) {
            return "REQUEST_ERROR";
        } else {
            $res_search = json_decode($response_search, true);
            if (isset($res_search['error_message'])) {
                return $res_search['error_message'];
            } else {
                if (empty($res_search['faces'])) {
                    return "NO_FACE_DETECTED";
                } else {
                    $thresholds = $res_search['thresholds'];
                    $face_token = $res_search['results'][0]['face_token'];
                    $confidence = $res_search['results'][0]['confidence'];
                    if ($confidence > $thresholds['1e-5']) {
                        return array('match_face_token' => $face_token);
                    } else {
                        return "NO_MATCHING_FACE";
                    }
                }
            }
        }
    }
}
