<?php
include_once "conexao.php";


$sql = "SELECT COUNT(*) as quantidade FROM usuario WHERE vl_pago = 0";
$sql = $conn->query($sql);;
$row = $sql->fetch_assoc();
$soma = $row['quantidade'];


echo 'Quantidade de Veículos: '.$soma;