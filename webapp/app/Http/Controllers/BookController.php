<?php

namespace App\Http\Controllers;

use App\Book;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Illuminate\Support\Facades\Validator;

class BookController extends Controller
{
    /**
      * Create a new BookController
      *
      * @return void
      */
    public function __construct()
    {
        $this->middleware('auth');
    }


    /**
     * Display a listing of the books.
     * If a valid format (XML or CSV) is specified in the request query, return
     * the data in that same format and redirect to this page without any format
     * option.
     *
     * @param  \Illuminate\Http\Request  $request
     *
     * @return \Illuminate\Http\Response
     */
    public function index(Request $request)
    {
        if (array_key_exists('format', $request->query()) == false) {
            $books = Book::orderBy('author')->get();
            return view('books', ['books' => $books]);
        } else {
            // export in CSV format
            if ($request->query()['format'] == 'csv') {
                //$books = Book::select($query)->get(); //TODO : check chunck Eloquent method
                $filename = "books.csv";
                $handle = fopen(storage_path("app/public/$filename"), 'w+');

                if ($request->query()['filter_out'] == 'author') {
                    $books = Book::select('title')->get();
                    fputcsv($handle, array('title'));
                    foreach ($books as $book) {
                        fputcsv($handle, array($book['title']));
                    }
                } elseif ($request->query()['filter_out'] == 'title') {
                    $books = Book::select('author')->get();
                    fputcsv($handle, array('author'));
                    foreach ($books as $book) {
                        fputcsv($handle, array($book['author']));
                    }
                } else {
                    $books = Book::select('title', 'author')->get();
                    fputcsv($handle, array('title', 'author'));
                    foreach ($books as $book) {
                        fputcsv($handle, array($book['title'], $book['author']));
                    }
                }

                fclose($handle);

                $headers = array(
                    'Content-Type' => 'text/csv',
                );

                return response()->download(storage_path("app/public/$filename"));

            // export in XML format
            } elseif ($request->query()['format'] == 'xml') {
                $books = Book::orderBy('author')->get();
                $filename = "books.xml";

                try {
                    $xml = new \XMLWriter();
                    $xml->openURI(storage_path("app/public/$filename"));
                    $xml->startDocument('1.0');
                    $xml->startElement('books');

                    if ($request->query()['filter_out'] == 'title') {
                        $books = Book::select('author')->get();
                        foreach ($books as $book) {
                            $xml->startElement('book');
                            $xml->writeElement('AUTHOR', $book['author']);
                            $xml->endElement();
                        }
                    } elseif ($request->query()['filter_out'] == 'author') {
                        $books = Book::select('title')->get();
                        foreach ($books as $book) {
                            $xml->startElement('book');
                            $xml->writeElement('TITLE', $book['title']);
                            $xml->endElement();
                        }
                    } else {
                        $books = Book::select('title', 'author')->get();
                        foreach ($books as $book) {
                            $xml->startElement('book');
                            $xml->writeElement('TITLE', $book['title']);
                            $xml->writeElement('AUTHOR', $book['author']);
                            $xml->endElement();
                        }
                    }

                    $xml->endElement();
                    $xml->endDocument();
                    $xml->flush();
                } catch (Exception $e) {
                    return redirect('books')->withErrors('failed preparing the XML export');
                }

                $headers = array(
                    'ContentType' => 'text/xml',
                );

                return response()->download(storage_path("app/public/$filename"));
            } else {
                return redirect('books')->withErrors('wrong format');
            }
        }
    }

    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'title' => 'required|max:255',
            'author' => 'required|max:255',
        ]);

        if ($validator->fails()) {
            return redirect('books')
                ->withInput()
                ->withErrors($validator);
        }

        $book = new Book;
        $book->title = $request->title;
        $book->author = $request->author;
        $book->save();

        return redirect('books');
    }

    /**
     * Display the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function show($id)
    {
        $book = Book::where('id', $id)->get();
        return view(
            'book',
            ['book' => $book]
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
        Book::findOrFail($id)->delete();
        return redirect('books');
    }
}
