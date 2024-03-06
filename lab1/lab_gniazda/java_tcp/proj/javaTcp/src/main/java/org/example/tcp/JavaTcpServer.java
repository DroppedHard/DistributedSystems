package org.example.tcp;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class JavaTcpServer {

    public static void main(String[] args) throws IOException {

        System.out.println("JAVA TCP SERVER");
        int portNumber = 12345;
        ServerSocket serverSocket = null;

        try {
            // create socket
            serverSocket = new ServerSocket(portNumber);

            while(true){

                // accept client
                Socket clientSocket = serverSocket.accept();
                System.out.println("client connected");

                // inSocket & outSocket streams
                PrintWriter outSocket = new PrintWriter(clientSocket.getOutputStream(), true);
                BufferedReader inSocket = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));

                // read msg, send response
                String msg = inSocket.readLine();
                System.out.println("received msg: " + msg);
                outSocket.println("Pong Java Tcp");

            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        finally{
            if (serverSocket != null){
                serverSocket.close();
            }
        }
    }

}

