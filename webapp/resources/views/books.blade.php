@extends('layouts.app')

@section('content')

    <!-- Bootstrap Boilerplate... -->

    <div class="card border-light mb-3">
        <!-- export button -->
        <div class="dropdown">
            <form action="/books" method="GET">
                <fieldset class="form-group">
                    <div class="row">
                        <legend class="col-form-label col-sm-2 pt-0">Format</legend>
                        <div class="col-sm-10">

                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="format" id="exportCSV" value="csv" checked>
                                <label class="form-check-label" for="exportCSV">
                                    CSV format
                                </label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="format" id="exportXML" value="xml">
                                <label class="form-check-label" for="exportXML">
                                    XML format
                                </label>
                    
                            </div>
                        </div>    
                    </div>
                </fieldset>
                <fieldset class="form-group">
                    <div class="row">
                        <legend class="col-form-label col-sm-2 pt-0">Filter out:</legend>
                        <div class="col-sm-10">
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="filter_out" id="filterOutNone" value="" checked>
                                <label class="form-check-label" for="filterOutNone">
                                    none
                                </label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="filter_out" id="filterOutTitle" value="title">
                                <label class="form-check-label" for="filterOutTitle">
                                    title
                                </label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="filter_out" id="filterOutAuthor" value="author">
                                <label class="form-check-label" for="filterOutAuthor">
                                    author
                                </label>
                            </div>
                        </div>    
                    </div>
                </fieldset>
                <div class="form-group row">
                    <div class="col-sm-10">
                        <button type="submit" class="btn btn-primary">Export</button>
                    </div>
                </div>
            </form>
        </div>

    <div class="card bg-light mb-3">
        <div class="card-body bg-light">
            <!-- New book Form -->
            <form action="/books" method="POST">
                
                {{ csrf_field() }}

                <!-- book Name -->
                <div class="form-group row">
                    <label for="book-title" class="col-sm-2 col-form-label">Title</label>
                    <div class="col-auto">
                        <input type="text" name="title" id="book-title" class="form-control" required>
                    </div>
                </div>
                <div class="form-group row">
                    <label for="book-author" class="col-sm-2 col-form-label">Author</label>
                    <div class="col-auto">
                        <input type="text" name="author" id="book-author" class="form-control" required>
                    </div>
                </div>

                <hr class="mb-4">
                <div class="form-group row">
                    <div class="col-auto">
                        <button type="submit" class="btn btn-primary">
                            Add book
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>

    <!-- current books -->
    <div class="card border-light mb-3">
            

        <!-- book list -->
        <div class="table-responsive">
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th scope="col" style="width: 60%">Title</th>
                        <th scope="col" style="width: 35%">Author</th>
                        <th scope="col" style="width: 5%">Delete</th>
                    </tr>
                </thead>
                <!-- Table Body -->
                <tbody>
                    @foreach ($books as $book)
                    <tr>
                        <td><a href="/book/{{ $book->id }}">{{ $book->title}}</a></td>
                        <td>{{ $book->author}}</td>
                        <!-- Delete Button -->
                        <td>
                            <form action="/book/{{ $book->id }}" method="POST">
                                {{ csrf_field() }}
                                @method('DELETE')
                        
                                <button class="btn btn-primary"><i class="fa fa-trash"></i></button>
                            </form>
                        </td>
                    </tr>
                    @endforeach
                </tbody>
            </table>
        </div>
    </div>

    <!-- Display Validation Errors -->
    @include('common.errors')

    </div>

@endsection

