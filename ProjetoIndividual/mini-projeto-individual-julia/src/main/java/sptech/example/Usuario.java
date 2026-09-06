package sptech.example;

public class Usuario {
    Integer id;
    String nome;
    String email;
    String senha;
    String cargo;

    Empresa empresa;

    Usuario(Integer pId, String pNome, String pEmail, String pSenha, String pCargo, Empresa pEmpresa) {
        id = pId;
        nome = pNome;
        email = pEmail;
        senha = pSenha;
        cargo = pCargo;
        empresa = pEmpresa;
    }
}
