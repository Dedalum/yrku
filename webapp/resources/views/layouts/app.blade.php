<!DOCTYPE html>
<html lang="en">
    <head>
        <title>@yield('title')</title>

        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">


        
        <!-- CSS And JavaScript -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <link href="css/app.css" rel="stylesheet" type="text/css">
        <script type="text/javascript" src="js/app.js"></script>

    </head>

    <body>
        @include('common.header')

        <div class="container">
            @yield('content')
        </div>

    </body>
</html>
