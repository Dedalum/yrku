<?php

namespace App\Http\Controllers;

use App\NLPApi;
use App\Book;
use Illuminate\Http\Request;

class NLPApiController extends Controller
{
    public function __construct()
    {
        $this->nlp_api = new NLPApi;
        $this->middleware('auth');
    }

    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        //
    }

    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
        //
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        //
    }

    /**
     * Display the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function show($id, Request $request)
    {
        $book = Book::where('id', $id)->get();
        if (array_key_exists('use_author', $request->query())) {
            if ($request->query()['use_author'] === "1") {
                $recommended_books = $this->nlp_api->recommend($book[0]->title, $book[0]->author);
                return view(
                    'book',
                    ['book' => $book],
                    ['recommended_books' => $recommended_books]
                );
            }
        }

        $recommended_books = $this->nlp_api->recommend($book[0]->title, null);
       
        return view(
            'book',
            ['book' => $book],
            ['recommended_books' => $recommended_books]
        );
    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function edit($id)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, $id)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function destroy($id)
    {
        //
    }
}
