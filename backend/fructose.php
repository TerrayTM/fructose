<?php

$password = "*******************";

if ($_SERVER['REQUEST_METHOD'] === "POST") {
    if (isset($_POST['password']) && hash_equals($password, $_POST['password'])) {
        header("Content-Type: application/json");
        http_response_code(200);

        if ($_POST['action'] === "ping") {
            die(json_encode([
                "success" => "true"
            ]));
        } else if ($_POST['action'] === "sync") {
            $data = json_decode($_POST['data']);

            foreach ($data->subdirectories as $folder) {
                $path = __DIR__ . "/" . $folder;

                if (file_exists($path)) { 
                    $iterator = new RecursiveDirectoryIterator($path, RecursiveDirectoryIterator::SKIP_DOTS);
                    $files = new RecursiveIteratorIterator($iterator, RecursiveIteratorIterator::CHILD_FIRST);

                    foreach($files as $file) {
                        if ($file->isDir()){
                            rmdir($file->getRealPath());
                        } else {
                            unlink($file->getRealPath());
                        }
                    }
                } else {
                    mkdir($path);
                }
            }

            foreach ($_FILES as $path => $data) {
                if ($data['tmp_name'] !== "") {
                    $new_path = __DIR__ . "/" . $path;
                
                    move_uploaded_file($data['tmp_name'], $new_path);
                }
            }

            die(json_encode([
                "success" => "true"
            ]));
        }
    }
}

http_response_code(404);
die();

?>