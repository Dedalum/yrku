<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class NLPData extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array
     */
    public function toArray($request)
    {
        $res = [
            'title' => $this->resource->title,
            'author' => $this->resource->author // TODO: if author==null ?
        ];
        return $res;
    }
}
