<!-- arquivo responsável pela conexão com o banco de dados  -->

<?php
$servidor = "localhost";
$usuario = "root";
$senha = "";
$dbname = "estacionamento";

// Criar a conexão 
$conn = mysqli_connect($servidor, $usuario, $senha, $dbname);


