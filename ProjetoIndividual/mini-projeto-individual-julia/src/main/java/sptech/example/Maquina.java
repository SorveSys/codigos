package sptech.example;

public class Maquina {
    Integer id;
    String hostname;
    String macAddress;
    String sistemaOperacional;
    Datacenter datacenter;

    Maquina(Integer pId, String pHostname, String pMacAddress, String pSistemaOperacional, Datacenter pDatacenter) {
        id = pId;
        hostname = pHostname;
        macAddress = pMacAddress;
        sistemaOperacional = pSistemaOperacional;
        datacenter = pDatacenter;
    }
}
