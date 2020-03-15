<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <form action="" method="post">
        Name: <input type="text" name="name" ><br>

        E-mail: <input type="text" name="email" ><br>

        Website: <input type="text" name="website" ><br>

        Comment: <textarea name="comment" rows="5" cols="40"></textarea><br>

        Gender:
        <input type="radio" name="gender"  value="female">Female
        <input type="radio" name="gender" value="male">Male
        <input type="radio" name="gender" value="other">Other
        <br>
        <input type="submit" value="Submit">
    </form>
</body>
</html>

<?php

if(!empty($_POST)) {
    $name = $_POST["name"];
    $email = $_POST["email"];
    $website = $_POST["website"];
    $comment = $_POST["comment"];
    $gender = $_POST["gender"];

    echo "<br>";
    echo "<br>";
    echo $name;
    echo "<br>";
    echo $email;
    echo "<br>";
    echo $website;
    echo "<br>";
    echo $comment;
    echo "<br>";
    echo $gender;
}

?>