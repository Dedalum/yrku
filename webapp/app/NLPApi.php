<?php

namespace App;

use App\Http\Resources\NLPDataCollection;
use App\Http\Resources\NLPData;
use Config;

class NLPApi
{
    /**
      * The URL of the API to query
      *
      * @var string
      */
    protected $url;

    /**
      * Create a new NLPApi instance
      *
      * @return void
      */
    public function __construct()
    {
        $this->url  =  config('nlp_api.host');
    }

    /**
      * Get a book recommendation from the API.
      *
      * @param string $title
      * @param string $author
      *
      * @return App\Http\Resources\NLPDataCollection
      */
    public function recommend($title, $author)
    {
        if (is_null($author)) {
            $books = collect($this->getJson($this->url . '/recommend/' . urlencode($title)));
        } else {
            $books = collect($this->getJson($this->url . '/recommend/' . urlencode("$title") . "?author=" . urlencode($author)));
        }
        return NLPDataCollection::make($books)->resolve();
    }

    /**
      * Protected method helper to query the API and decode the JSON response
      *
      * @param string $url
      *
      * @return string
      */
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
