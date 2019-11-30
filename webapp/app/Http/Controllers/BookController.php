<?php

namespace App\Http\Controllers;

use App\Book;
use App\NLPApi;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class BookController extends Controller
{
    protected $nlp_api;
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */

    public function __construct()
    {
        $this->nlp_api = new NLPApi;
    }

    public function index()
    {
        $books = Book::orderBy('author')->get();
        return view('books', ['books' => $books]);
    }

    public function export(Request $request)
    {
        // export in CSV format
        if ($request->query()['format'] == 'csv') {
            //$books = Book::select($query)->get(); //TODO : check chunck Eloquent method
            $filename = "books.csv";
            $handle = fopen($filename, 'w+');

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
   
                // TODO : select only what we need (all, title or just author)
                foreach ($books as $book) {
                    fputcsv($handle, array($book['title'], $book['author']));
                }
            }

            fclose($handle);

            $headers = array(
                'Content-Type' => 'text/csv',
            );

            return Response::download($filename, 'books.csv', $headers);

        // export in XML format
        } elseif ($request->query()['format'] == 'xml') {
            $books = Book::orderBy('author')->get();
            $filename = "books.xml";

            // ($request->query()['fields'] == 'all') {
            try {
                $xml = new XMLWriter();
                $xml->openURI($filename);
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
                return redirect('books')
            ->withErrors('wrong format');
            }

            $headers = array(
                'ContentType' => 'text/xml',
            );

            return Response::download($filename, 'books.xml', $headers);
        } else {
            return redirect('books')
            ->withErrors('wrong format');
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
        $recommended_books = $this->nlp_api->recommend($book[0]->title);
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
        Book::findOrFail($id)->delete();
        return redirect('books');
    }
}
