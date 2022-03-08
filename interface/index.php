<!DOCTYPE HTML>
<html lang="pt-br">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="bootstrap/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
        <title>Estacionamento</title>
        <script src="jQUERY/jquery.min.js"></script>
    </head>
    <body>
        <div class="container">
            <div class="row mt-4">
                <div class="col-lg-12">
                    <div>
                        <h4><span id="conteudo"></span></h4>
                    </div>
                </div>
            </div>
            <hr>
            <div class="row">
                <div class="col-lg-12">
                    <div class="table-responsive">
                        <table class="table table-dark table-striped table-bordered">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Data de Entrada</th>
                                    <th>Placa</th>
                                    <th>Cor</th>
                                    <th>Hora de Entrada</th>
                                    <th>Hora de Saída</th>
                                    <th>Hora Total</th>
                                    <th>Valor Pago</th>
                                </tr>  
                            </thead>
                            <tbody> 
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

    <script src="bootstrap/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
    <script src="js/custom.js"></script>
    <script>
        $(document).ready(function () {
            $.post('contagem.php', function(retorna){
                $("#conteudo").html(retorna);
            });
        });
    </script>
    </body>

</html>