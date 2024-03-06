package org.example.udp;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class JavaUdpClient {

    public static void main(String args[]) throws Exception
    {
        System.out.println("JAVA UDP CLIENT");
        DatagramSocket socket = null;
        DatagramSocket resSocket = null;
        int portNumber = 9008;
        int pongPort = 9009;

        byte[] receiveBuffer = new byte[1024];

        try {
            socket = new DatagramSocket();
            InetAddress address = InetAddress.getByName("localhost");
            byte[] sendBuffer = "Ping Java Udp".getBytes();

            DatagramPacket sendPacket = new DatagramPacket(sendBuffer, sendBuffer.length, address, portNumber);
            socket.send(sendPacket);

            resSocket = new DatagramSocket(pongPort);
            DatagramPacket serverResponse = new DatagramPacket(receiveBuffer, receiveBuffer.length);
            resSocket.receive(serverResponse);
            String responseMsg = new String(serverResponse.getData());
            System.out.println("Received server response: " + responseMsg);

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
