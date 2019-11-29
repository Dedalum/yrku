@extends('layouts.app')

@section('content')

    <!-- Bootstrap Boilerplate... -->

<div class="card border-light mb-3">
    <div class="card bg-light mb-3">
        <div class="card-body bg-light">
            <!-- Display Validation Errors -->
            <!-- @include('common.errors') -->

            <!-- New book Form -->
            <form action="/book" method="POST">
                
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
            
        <!-- export button -->
        <div class="dropdown">
            <button class="btn btn-primary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                Export
            </button>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <a class="dropdown-item" href="/export?format=csv">CSV format</a>
                <a class="dropdown-item" href="/export?format=xml">XML format</a>
            </div>
        </div>


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
                        <td>{{ $book->title}}</td>
                        <td>{{ $book->author}}</td>
                        <!-- Delete Button -->
                        <td>
                            <form action="/book/{{ $book->id }}" method="POST">
                                {{ csrf_field() }}
                                {{ method_field('DELETE') }}
                        
                                <button class="btn btn-primary"><i class="fa fa-trash"></i></button>
                            </form>
                        </td>
                    </tr>
                    @endforeach
                </tbody>
            </table>
        </div>
    </div>
</div>

@endsection

