import org.apache.commons.math3.util.FastMath;

import java.lang.String;
import java.lang.Math;
import java.util.ArrayList;
import java.io.*;
import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveTask;


public class Main{

    public Graph createGraphs () throws IOException {
        String filePath = new File("").getAbsolutePath();
        final File folder = new File(filePath+"/dataset"); 
        Graph g = new Graph();
        int i = 0;
        Node node;
        for (final File fileEntry : folder.listFiles()) {
            File file = new File(filePath+"/dataset/"+fileEntry.getName()); 
            BufferedReader br = new BufferedReader(new FileReader(file)); 
            String st; 
            String[] line;
            while ((st = br.readLine()) != null) {
                if(i >= 1) {
                    double[] coords = new double[2];
                    line = st.split(","); 
                    coords[0] = Double.parseDouble(line[3]);
                    coords[1] = Double.parseDouble(line[4]);
                    node = new Node(line[0], coords, Long.parseLong(line[2]), line[1]);
                    g.add(node);
                }  
                i++; 
            }
        }
        return g;
    }

    public int calcDist(double[] point1, double[] point2) {
        double RRR = 6378.388;
        double x1 = convertToRadiant(point1[0]), x2 = convertToRadiant(point2[0]), y1 = convertToRadiant(point1[1]), y2 = convertToRadiant(point2[1]);
        double q1 = FastMath.cos(y1 - y2);
        double q2 = FastMath.cos(x1 - x2);
        double q3 = FastMath.cos(x1 + x2);
        return (int)(RRR * FastMath.acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0);
    } 

    public double convertToRadiant(double value) {
        int deg = (int)value;
        double min = value - deg;
        return FastMath.PI * (deg + 5.0 * min / 3.0) / 180.0;
    }


    public double calcDistrosion(ArrayList<Cluster> clusters) {
        double distorsion = 0.0;
        double error = 0.0;
        for(Cluster c: clusters) {
            error = 0.0;
            for(Node n: c.getNodes()) {
                error += n.getPopulation() * FastMath.pow(this.calcDist(n.getCoords(), c.getCentroid()), 2);
            }
            distorsion += error;
        }
        return distorsion;
    }

    public ArrayList<Cluster> makeClustering(ArrayList<Node> points, int[] cluster, ArrayList<double[]> centroids) {
        ArrayList<Cluster> toRet = new ArrayList<Cluster>();
        Cluster c;
        for(double[] centroid: centroids) {
            c = new Cluster();
            for(int i=0;i<cluster.length;i++) {
                if(cluster[i] == centroids.indexOf(centroid)) {
                    c.addNode(points.get(i));
                }
            }
            c.setCentroid(centroid);
            toRet.add(c);
        }
        return toRet;
    }

    public void questionOne(Graph graph) throws IOException{
        int pointsNumber;
        FileWriter csvWriter = new FileWriter("questionOne.csv");
        csvWriter.append("Grafo,serialTime,parallelTime\n");
        int[] subsets = { Integer.MIN_VALUE, 250, 2000, 5000, 15000, 50000, 100000 };
        for (int subset : subsets) {
            
            Graph g = new Graph();
            g.setNodes(graph.getNodesByPopulation(subset)); // build a graph made with the nodes that respect a minimum population
            pointsNumber = g.getDim();
            csvWriter.append(pointsNumber + ",");

            System.out.println("Dataset con città con almeno " + subset + " abitanti");
            long startTime = System.currentTimeMillis();
            SerialKMeans km = new SerialKMeans(g, 50, 100);
            long afterTime = System.currentTimeMillis();
            csvWriter.append(Float.toString((afterTime - startTime) / 1000F) + ",");
            System.out.println("Serial k-means execution time: " + ((afterTime - startTime) / 1000F) + " seconds");
            ArrayList<Cluster> clusters = km.getClustering();
            System.out.println("Serial k-means distorsion: " + this.calcDistrosion(clusters));
            startTime = System.currentTimeMillis();
            PKMeansClustering parallelClustering = new PKMeansClustering(30000, g, 50, 100);
            afterTime = System.currentTimeMillis();
            System.out.println("Parallel k-means execution time: " + ((afterTime - startTime) / 1000F) + " seconds");
            csvWriter.append(Float.toString(((afterTime - startTime) / 1000F)));
            csvWriter.append("\n");
            int[] cluster = parallelClustering.getClustering();
            ArrayList<double[]> centroids = parallelClustering.getCentroids();
            System.out.println("Parallel k-means distorsion: "
                    + this.calcDistrosion(this.makeClustering(g.getNodes(), cluster, centroids)));
            System.out.println("\n");
        }
        csvWriter.flush();  
        csvWriter.close(); 
    }

    public void questionTwo(Graph graph) throws IOException {
        FileWriter csvWriter = new FileWriter("questionTwo.csv");
        csvWriter.append("clusterNumber,serialTime,parallelTime\n");
        for(int k = 10; k<=100; k+=10) {
            csvWriter.append(k + ",");
            System.out.println("Numero di cluster: " + k);
            long startTime = System.currentTimeMillis();
            SerialKMeans km = new SerialKMeans(graph, k, 100);
            long afterTime = System.currentTimeMillis();
            System.out.println("Serial k-means execution time: " + ((afterTime -
            startTime) / 1000F) + " seconds");
            csvWriter.append(Float.toString((afterTime - startTime) / 1000F) + ",");
            ArrayList<Cluster> clusters = km.getClustering();
            System.out.println("Serial k-means distorsion: " +
            this.calcDistrosion(clusters));
            startTime = System.currentTimeMillis();
            PKMeansClustering parallelClustering = new PKMeansClustering(10000, graph, k, 100);
            afterTime = System.currentTimeMillis();
            System.out.println("Parallel k-means execution time: " + ((afterTime -
            startTime) / 1000F) + " seconds");
            csvWriter.append(Float.toString((afterTime - startTime) / 1000F));
            csvWriter.append("\n");
            int[] cluster = parallelClustering.getClustering();
            ArrayList<double[]> centroids = parallelClustering.getCentroids();
            System.out.println("Parallel k-means distorsion: "
            + this.calcDistrosion(this.makeClustering(graph.getNodes(), cluster, centroids)));
    
            System.out.println("\n");
        }
        csvWriter.flush();  
        csvWriter.close();
    }

    public void questionThree(Graph graph) throws IOException {
        FileWriter csvWriter = new FileWriter("questionThree.csv");
        csvWriter.append("iterationNumber,serialTime,parallelTime\n");
        for(int q = 10; q<=1010; q+=100) {
            if(q == 1010) {
                q = 1000;
            }
            csvWriter.append(q + ",");
            System.out.println("Numero di iterazioni: " + q);
            long startTime = System.currentTimeMillis();
            SerialKMeans km = new SerialKMeans(graph, 50, q);
            long afterTime = System.currentTimeMillis();
            System.out.println("Serial k-means execution time: " + ((afterTime -
            startTime) / 1000F) + " seconds");
            csvWriter.append(Float.toString((afterTime - startTime) / 1000F) + ",");
            ArrayList<Cluster> clusters = km.getClustering();
            System.out.println("Serial k-means distorsion: " +
            this.calcDistrosion(clusters));
            startTime = System.currentTimeMillis();
            PKMeansClustering parallelClustering = new PKMeansClustering(0, graph, 50, q);
            afterTime = System.currentTimeMillis();
            System.out.println("Parallel k-means execution time: " + ((afterTime -
            startTime) / 1000F) + " seconds");
            csvWriter.append(Float.toString((afterTime - startTime) / 1000F));
            csvWriter.append("\n");
            int[] cluster = parallelClustering.getClustering();
            ArrayList<double[]> centroids = parallelClustering.getCentroids();
            System.out.println("Parallel k-means distorsion: "
            + this.calcDistrosion(this.makeClustering(graph.getNodes(), cluster, centroids)));
    
            System.out.println("\n");
        }
        csvWriter.flush();  
        csvWriter.close();
    }

    public void questionFour(Graph graph) throws IOException {
        FileWriter csvWriter = new FileWriter("questionFour.csv");
        csvWriter.append("cutoff,time\n");
        for(int cutoff=0; cutoff<=1000; cutoff+=100) {
            csvWriter.append(cutoff + ",");
            long startTime = System.currentTimeMillis();
            PKMeansClustering parallelClustering = new PKMeansClustering(cutoff, graph, 50, 100);
            long afterTime = System.currentTimeMillis();
            System.out.println("Cutoff: " + cutoff);
            System.out.println("Parallel k-means execution time: " + ((afterTime - startTime) / 1000F) + " seconds");
            csvWriter.append(Float.toString((afterTime - startTime) / 1000F));
            csvWriter.append("\n");
            int[] cluster = parallelClustering.getClustering();
            ArrayList<double[]> centroids = parallelClustering.getCentroids();
            System.out.println("Parallel k-means distorsion: "
                    + this.calcDistrosion(this.makeClustering(graph.getNodes(), cluster, centroids)));

            System.out.println("\n");
        }
        csvWriter.flush();  
        csvWriter.close();
    }

    public static void main(String[] args) throws IOException {
        Main m = new Main();
        Graph graph = m.createGraphs();

        //m.questionOne(graph);
        m.questionTwo(graph);
        //m.questionThree(graph);
        //m.questionFour(graph);
    }
}