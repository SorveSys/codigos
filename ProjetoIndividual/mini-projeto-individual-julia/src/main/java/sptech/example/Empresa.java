package sptech.example;

public class Empresa {
    Integer id;
    String razaoSocial;
    String nomeFantasia;
    String cnpj;
    String email;

    Empresa(Integer pId, String pRazaoSocial, String pNomeFantasia, String pCnpj, String pEmail) {
        id = pId;
        razaoSocial = pRazaoSocial;
        nomeFantasia = pNomeFantasia;
        cnpj = pCnpj;
        email = pEmail;
    }
}
