<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body>
    <form action="" method="post">
        Name: <input type="text" name="name"><br>

        E-mail: <input type="text" name="email"><br>

        Website: <input type="text" name="website"><br>

        Comment: <textarea name="comment" rows="5" cols="40"></textarea><br>

        Gender:
        <input type="radio" name="gender" value="female">Female
        <input type="radio" name="gender" value="male">Male
        <input type="radio" name="gender" value="other">Other
        <br>
            <legend>What is Your Favorite Pet?</legend>
            <input type="checkbox" name="favorite_pet[]" value="Cats">Cats<br>
            <input type="checkbox" name="favorite_pet[]" value="Dogs">Dogs<br>
            <input type="checkbox" name="favorite_pet[]" value="Birds">Birds<br>
        <br>
        <input type="submit" value="Submit">
    </form>

    <br><br><br>
    <button id="elem">
        test of jquery
    </button>

    <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha256-pasqAKBDmFT4eHoN2ndd6lN370kFiGUFyTiUHWhU7k8=" crossorigin="anonymous"></script>
    <script>
        $("#elem").click(() => {
            console.log("test in jquery");
        })
        console.log("this is my js file");
    </script>
</body>

</html>

<?php

if (!empty($_POST)) {
    echo "<pre>";
    print_r($_POST);
    echo "</pre>";


    // $name = $_POST["name"];
    // $email = $_POST["email"];
    // $website = $_POST["website"];
    // $comment = $_POST["comment"];
    // $gender = $_POST["gender"];

    // echo "<br>";
    // echo "<br>";
    // echo $name;
    // echo "<br>";
    // echo $email;
    // echo "<br>";
    // echo $website;
    // echo "<br>";
    // echo $comment;
    // echo "<br>";
    // echo $gender;
}

?>