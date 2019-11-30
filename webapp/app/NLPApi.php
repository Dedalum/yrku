<?php

namespace App;

use App\Http\Resources\NLPDataCollection;
use App\Http\Resources\NLPData;

class NLPApi
{
    protected $url = 'http://localhost:5000';

    public function recommend($title, $author=null)
    {
        $books = collect($this->getJson($this->url . '/recommend/' . $title));
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
