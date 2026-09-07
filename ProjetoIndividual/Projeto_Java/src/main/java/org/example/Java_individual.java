package org.example;

import java.util.Locale;
import java.util.Scanner;

public class Java_individual {

    public static void main(String[] args){



        Scanner projeto= new Scanner(System.in);

        while(true) {

            System.out.print("Deseja usar o serviço? (S/N) : ");
            String resposta = projeto.nextLine().toUpperCase();

            if (resposta.equalsIgnoreCase("N")) {
                break;
            }


            String statuscpu;
            String statusram;
            String statustemp;
            String statusdisc;


            System.out.println("==========CENTRAL DE DIAGNÓSTICO==========");

            System.out.print("Nome da Praça:");
            String praca = projeto.nextLine();

            if (praca==""){
                System.out.println("Erro na escrita da praça");
                break;
            }

            System.out.print("ID do servidor:");
            String servidor = projeto.nextLine();

            if (servidor==""){
                System.out.println("Erro na escrita no servidor");
                break;
            }

            System.out.print("Uso de CPU (%):");
            double CPU = projeto.nextDouble();

            if (CPU<0){
                System.out.println("Erro na escrita da CPU");
                break;
            }

            projeto.nextLine();

            System.out.print("Uso de RAM (%):");
            double RAM = projeto.nextDouble();

            if (RAM<0){
                System.out.println("Erro na escrita na RAM");
                break;
            }

            projeto.nextLine();

            System.out.print("Temperatura (ºC):");
            double temp = projeto.nextDouble();

            projeto.nextLine();

            System.out.print("Uso de Disco (%):");
            double disco = projeto.nextDouble();

            if (disco<0){
                System.out.println("Erro na escrita no disco");
                break;
            }

            projeto.nextLine();


            System.out.println("==========RELATÓRIO DO SERVIDOR===========");

            System.out.println("Nome da praça:" + praca);

            System.out.println("Servidor:" + servidor);


            //CPU
            if (CPU < 70) {
                statuscpu = "Normal";
            } else if (CPU >= 70 && CPU <= 89) {
                statuscpu = "Atenção";
            } else {
                statuscpu = "Critíco";
            }
            //RAM
            if (RAM < 80) {
                statusram = "Normal";
            } else if (RAM >= 80 && RAM <= 89) {
                statusram = "Atenção";
            } else {
                statusram = "Critíco";
            }

            //TEMPERATURA

            if (temp < 70) {
                statustemp = "Normal";
            } else if (temp >= 70 && temp <= 79) {
                statustemp = "Atenção";
            } else {
                statustemp = "Critíco";
            }

            //DISCO

            if (disco <= 69) {
                statusdisc = "Normal";
            } else if (disco >= 70 && disco <= 89) {
                statusdisc = "Atenção";
            } else {
                statusdisc = "Critíco";
            }

            System.out.println("CPU:" + CPU + "------- STATUS:" + statuscpu);

            System.out.println("RAM:" + RAM + "------- STATUS:" + statusram);

            System.out.println("TEMPERATURA:" + temp + "------- STATUS:" + statustemp);

            System.out.println("DISCO:" + disco + "------- STATUS:" + statusdisc);


            System.out.print("Deseja realizar a leitura novamente?  (S/N): ");
            String novamente = projeto.nextLine().toUpperCase();

            if (novamente.equalsIgnoreCase("N")) {
                break;
            }
        }



        System.out.println("Programa Encerrado!");
    }

}

