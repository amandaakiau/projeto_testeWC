<!-- arquivo responsável por buscar os registros no banco de dados -->

<?php
include_once "conexao.php";


//Consulta no banco de dados
$result_usuario = "SELECT id, dt_criacao, cd_placa, ds_cor, hr_entrada, hr_saida, hr_total, vl_pago FROM usuario";
$resultado_usuario = mysqli_query($conn, $result_usuario);

$dados = "";

//Verifica se encontrou resultado na tabela "veiculos"

while($row_usuario = mysqli_fetch_assoc($resultado_usuario)){
    extract($row_usuario);
        $dados .=   "<tr>
                        <td>$id</td><td>$dt_criacao</td><td>$cd_placa</td><td>$ds_cor</td><td>$hr_entrada</td><td>$hr_saida</td>
                        <td>$hr_total</td><td>$vl_pago</td>
                    </tr>";
}

echo $dados;





