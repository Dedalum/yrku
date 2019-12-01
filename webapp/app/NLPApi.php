<?php

namespace App;

use App\Http\Resources\NLPDataCollection;
use App\Http\Resources\NLPData;
use Config;

class NLPApi
{
    protected $url;

    public function __construct()
    {
        $this->url  =  config('nlp_api.host');
    }

    public function recommend($title, $author)
    {
        if (is_null($author)) {
            $books = collect($this->getJson($this->url . '/recommend/' . urlencode($title)));
        } else {
            $books = collect($this->getJson($this->url . '/recommend/' . urlencode("$title") . "?author=" . urlencode($author)));
        }
        return NLPDataCollection::make($books)->resolve();
    }

    protected function getJson($url)
    {
        $curlSession = curl_init();
        curl_setopt($curlSession, CURLOPT_URL, $url);
        curl_setopt($curlSession, CURLOPT_BINARYTRANSFER, true);
        curl_setopt($curlSession, CURLOPT_RETURNTRANSFER, true);
        $json_response = curl_exec($curlSession);
        curl_close($curlSession);
        return json_decode($json_response);
    }
}
