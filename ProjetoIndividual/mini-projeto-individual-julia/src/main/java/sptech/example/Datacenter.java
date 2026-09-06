package sptech.example;

public class Datacenter {
    Integer id;
    String nome;
    String coordenadas;

    Empresa empresa;

    Datacenter(Integer pId, String pNome, String pCoordenadas, Empresa pEmpresa) {
        id = pId;
        nome = pNome;
        coordenadas = pCoordenadas;
        empresa = pEmpresa;
    }
}
