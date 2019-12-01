@extends('layouts.app')

@section('content')
<div class="card border-light mb3">
    <div class="card-body bg-light">
        <h3><i>{{ $book[0]->title }}</i> by {{ $book[0]->author }}</h3>
        <form action="/recommend/{{ $book[0]->id }}" method="GET">
            <button class="btn btn-primary">Recommend books</button>
            <div class="form-check">
                <input class="form-check-input" type="checkbox" name="use_author" id="useAuthor" value="1">
                <label class="form-check-label" for="useAuthor">
                    Include author for recommendation 
                </label>
            </div>

        </form>
        <hr class="mb-4">

        @isset($recommended_books)
        <ul class="list-group list-group-flush">
            <li class="list-group-item active">Recommended books:</li>
            @foreach ($recommended_books ?? '' as $recommended_book)
            <li class="list-group-item">
                <i>{{ $recommended_book['title'] }}</i> by {{ $recommended_book['author'] }}
            </li>
        </ul>
        

        @endforeach
        @endisset
    </div>


    @include('common.errors')
</div>
@endsection
