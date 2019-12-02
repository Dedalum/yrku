<?php

use App\Book;
use Illuminate\Http\Request;

Route::any('/', function () {
    return View::make('home');
});
Route::resource('books', 'BookController');
Route::get('/book/{id}', 'BookController@show');
Route::delete('/book/{id}', 'BookController@destroy');
Route::get('/recommend/{id}', 'NLPApiController@show');

Auth::routes();

Route::get('/home', 'HomeController@index')->name('home');
