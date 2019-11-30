@extends('layouts.app')

@section('content')
<div class="card border-light mb3">
    <div class="card-body bg-light">
        <h3>Book : <i>{{ $book[0]->title }}</i>, from {{ $book[0]->author }}</h3>
        <hr class="mb-4">
        <ul class="list-group list-group-flush">
            <li class="list-group-item active">Recommended books:</li>
            @foreach ($recommended_books as $recommended_book)
            <li class="list-group-item">
                <i>{{ $recommended_book['title'] }}</i>, from {{ $recommended_book['author'] }}
            </li>
        </ul>
        

        @endforeach
    </div>


    @include('common.errors')
</div>
@endsection
