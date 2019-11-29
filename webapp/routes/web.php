<?php

use App\Book;
use Illuminate\Http\Request;

// display all books
Route::get('/', function () {
    $books = Book::orderBy('author')->get();

    return view('books', ['books' => $books]);
});


// add new book
Route::post('/book', function (Request $request) {
    $validator = Validator::make($request->all(), [
        'title' => 'required|max:255',
        'author' => 'required|max:255',
    ]);

    if ($validator->fails()) {
        return redirect('/')
            ->withInput()
            ->withErrors($validator);
    }

    $book = new Book;
    $book->title = $request->title;
    $book->author = $request->author;
    $book->save();

    return redirect('/');
});

// delete a book
Route::delete('/book/{id}', function ($id) {
    Book::findOrFail($id)->delete();

    return redirect('/');
});
