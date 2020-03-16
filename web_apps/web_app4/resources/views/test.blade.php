<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title>Laravel</title>
    </head>
    <body>
        <h2>test</h2>
        <form action="test" method="post">
            {{ csrf_field() }}
            <input type="text" name="username"><br>
            <input type="password" name="password"><br>
            <button type="submit">Submit</button>
        </form>
    </body>        
</html>
