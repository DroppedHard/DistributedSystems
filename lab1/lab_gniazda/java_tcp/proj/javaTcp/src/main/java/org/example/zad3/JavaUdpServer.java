package org.example.zad3;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.ByteBuffer;
import java.util.Arrays;

public class JavaUdpServer {

    public static void main(String args[])
    {
        System.out.println("JAVA UDP SERVER");
        DatagramSocket socket = null;
        int portNumber = 9008;
        int pongPort = 9009;

        try{
            socket = new DatagramSocket(portNumber);
            byte[] receiveBuffer = new byte[1024];

            while(true) {
                Arrays.fill(receiveBuffer, (byte)0);
                DatagramPacket receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
                socket.receive(receivePacket);
//                String msg = new String(receivePacket.getData(), "Cp1250");
                int nb = ByteBuffer.wrap(receivePacket.getData()).getInt();

                System.out.println("received msg: " + nb);


                InetAddress senderAddress = receivePacket.getAddress();
                socket = new DatagramSocket();

                byte[] responseBuffer = ByteBuffer.allocate(4).putInt(nb+1).array();
                DatagramPacket responsePacket = new DatagramPacket(responseBuffer, responseBuffer.length, senderAddress, pongPort);
                socket.send(responsePacket);
            }
        }
        catch(Exception e){
            e.printStackTrace();
        }
        finally {
            if (socket != null) {
                socket.close();
            }
        }
    }
}
