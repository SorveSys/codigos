package sptech.example;

import java.util.Scanner;

//TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or
// click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.
public class Main {
    static void main() {

        Scanner leitor = new Scanner(System.in);

        Empresa empresaCadastrada = null;
        Usuario usuarioCadastrado = null;
        Usuario usuarioLogado = null;
        Datacenter datacenterCadastrado = null;
        Maquina maquinaCadastrada = null;
        Componente componenteCadastrado = null;

        Integer opcao = 0;

        while (!opcao.equals(3)) {
            System.out.println("\n SISTEMA DE MONITORAMENTO PARA EMPRESAS DE PEDÁGIO");
            System.out.println("1. Cadastrar empresa e usuário");
            System.out.println("2. Fazer login");
            System.out.println("3. Sair");

            System.out.println("Escolha uma opção: ");
            opcao = leitor.nextInt();
            leitor.nextLine();

            if (opcao.equals(1)) {
                System.out.println("\n CADASTRAR EMPRESA");
                System.out.println("Razão Social: ");
                String razao = leitor.nextLine();
                System.out.println("Nome Fantasia: ");
                String fantasia = leitor.nextLine();
                System.out.println("CNPJ: ");
                String cnpj = leitor.nextLine();
                System.out.println("E-mail: ");
                String emailEmpresa = leitor.nextLine();

                empresaCadastrada = new Empresa(1, razao, fantasia, cnpj, emailEmpresa);

                System.out.println("\n CADASTRO DE USUÁRIO DA EMPRESA");
                System.out.println("Nome do funcionário: ");
                String nomeFunc = leitor.nextLine();
                System.out.println("E-mail do funcionári: ");
                String emailFunc = leitor.nextLine();
                System.out.println("Senha: ");
                String senhaFunc = leitor.nextLine();
                System.out.println("Cargo: ");
                String cargo = leitor.nextLine();

                usuarioCadastrado = new Usuario(1, nomeFunc, emailFunc, senhaFunc, cargo, empresaCadastrada);
                System.out.println("Empresa e Usuário cadastrado com sucesso!");
            } else if (opcao.equals(2)) {
                if (usuarioCadastrado == null) {
                    System.out.println("Ainda não há um usuário cadastrado.");
                } else {
                    System.out.println("\n LOGIN");
                    System.out.println("E-mail: ");
                    String emailLogin = leitor.nextLine();
                    System.out.println("Senha: ");
                    String senhaLogin = leitor.nextLine();

                    if (emailLogin.equals(usuarioCadastrado.email) && senhaLogin.equals(usuarioCadastrado.senha)) {
                        usuarioLogado = usuarioCadastrado;
                        System.out.println("\n Login realizado com sucesso! Olá, " + usuarioLogado.nome);
                        System.out.println("Empresa vinculada: " + usuarioLogado.empresa.nomeFantasia);

                        Integer opcaoMenuLogado = 0;
                        while (!opcaoMenuLogado.equals(5)) {
                            System.out.println("\n CONFIGURAÇÃO DO SISTEMA");
                            System.out.println("1. Cadastrar Datacenter");
                            System.out.println("2. Cadastrar Máquina");
                            System.out.println("3. Cadastrar Componente e Limite de Alerta");
                            System.out.println("4. Exibir Resumo");
                            System.out.println("5. Deslogar");
                            System.out.println("Digite uma opção: ");
                            opcaoMenuLogado = leitor.nextInt();
                            leitor.nextLine();

                            if (opcaoMenuLogado.equals(1)) {
                                System.out.println("Nome do Datacenter: ");
                                String nomeDatacenter = leitor.nextLine();
                                System.out.println("Coordenadas: ");
                                String coord = leitor.nextLine();

                                datacenterCadastrado = new Datacenter(1, nomeDatacenter, coord, usuarioLogado.empresa);
                                System.out.println("Datacenter cadastrado!");
                            } else if (opcaoMenuLogado.equals(2)) {
                                if (datacenterCadastrado == null) {
                                    System.out.println("Cadastre um datacenter!");
                                } else {
                                    System.out.println("Hostname da Máquina: ");
                                    String hostMaq = leitor.nextLine();
                                    System.out.println("Mac Address: ");
                                    String macMaq = leitor.nextLine();
                                    System.out.println("Sistema Operacional: ");
                                    String so = leitor.nextLine();

                                    maquinaCadastrada = new Maquina(1, hostMaq, macMaq, so, datacenterCadastrado);
                                    System.out.println("Máquina cadastrada!");
                                }
                            } else if (opcaoMenuLogado.equals(3)) {
                                System.out.println("Tipo do componente");
                                String comp = leitor.nextLine();
                                System.out.println("Valor máximo (para alerta)");
                                Double maxComp = leitor.nextDouble();
                                leitor.nextLine();

                                componenteCadastrado = new Componente(1, comp, maxComp);
                                System.out.println("Componente cadastrado!");
                            } else if (opcaoMenuLogado.equals(4)) {
                                System.out.println("\n RESUMO");
                                System.out.println("Empresa: " + usuarioLogado.empresa.nomeFantasia);

                                String nomeDatacenter = "Nulo";
                                if (datacenterCadastrado != null) {
                                    nomeDatacenter = datacenterCadastrado.nome;
                                }
                                System.out.println("Datacenter: " + nomeDatacenter);

                                String nomeMaq = "Nulo";
                                if (maquinaCadastrada != null) {
                                    nomeMaq = maquinaCadastrada.hostname;
                                }
                                System.out.println("Máquina: " + nomeMaq);

                                String infoComponente = "Nulo";
                                if (componenteCadastrado != null) {
                                    infoComponente = componenteCadastrado.tipo + " (Limite: " + componenteCadastrado.valorMaximo + ")";
                                }
                                System.out.println("Componente: " + infoComponente);
                            }
                        }
                    } else {
                        System.out.println("E-mail ou senha inválidos!");
                    }
                }
            } else if (opcao.equals(3)) {
                System.out.println("Sistema encerrado.");
            } else {
                System.out.println("Opção inválida!");
            }
        }
    }
}